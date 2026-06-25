from base import *
from rule import *


def predict_full(name, target_label_dim, dt_cand, mode=None):
    true_label_map = {}
    with open(name.split('_')[0] + '_raw_txt', 'r') as f:
        for line in f:
            line = line.replace('\n', '').split(' ')
            true_label_map[line[0].replace('-', '')] = line[target_label_dim + 1]
    path = name + '_conf_' + str(target_label_dim) + '.json'
    config = {}
    if os.path.exists(path):
        with open(path, 'r',  encoding='utf-8') as f:
            config = json.load(f)
    config_copy = None
    if len(config) > 0:
        config_copy = copy.deepcopy(config)
    range_stat = {}
    update_config = False
    invalid = False
    for dt in dt_cand:
        s, data = get_best_item(name, target_label_dim, True, dt)
        result = set()
        result_copy = set()
        all_stat = {}
        all_stat_copy = {}
        first = False
        first_copy = False
        for v in data:
            arr, arr_copy, need_update = pattern_check(name, v['prob_cand_arr'], v['pred'], target_label_dim, v['avg_window'], v['data_len'], v['best'], true_label_map[dt] if dt in true_label_map else None, mode, range_stat, config, config_copy)
            if need_update:
                update_config = True
            if not first_copy:
                first_copy = True
                result_copy = arr_copy
            else:
                result_copy &= arr_copy
            if not first:
                result = arr
                first = True
            else:
                result &= arr
            for l in arr:
                if l in all_stat:
                    all_stat[l] += 1
                else:
                    all_stat[l] = 1
            for l in arr_copy:
                if l in all_stat_copy:
                    all_stat_copy[l] += 1
                else:
                    all_stat_copy[l] = 1
        if arr_copy is not None:
            print('预测结果', result_copy, sorted(all_stat_copy.items(), key=lambda x : x[1], reverse=True))
        print('真实下标', dt, true_label_map[dt] if dt in true_label_map else 'unknown', result, sorted(all_stat.items(), key=lambda x : x[1], reverse=True))
        for l in range_stat:
            print(l, range_stat[l])
        print('\n\n')
        if len(result) == 0:
            invalid = True
    if update_config and dt in true_label_map:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
    if invalid:
        exit(0)



def predict(name, target_label_dim, dt_cand, mode=None):
    true_label_map = {}
    with open(name.split('_')[0] + '_raw_txt', 'r') as f:
        for line in f:
            line = line.replace('\n', '').split(' ')
            true_label_map[line[0].replace('-', '')] = line[target_label_dim + 1]
    range_stat = {}
    for dt in dt_cand:
        s,data = get_best_item(name, target_label_dim, True, dt)
        result = set()
        acc_stat = {}
        first = False
        for v in data[:10]:
            arr, arr_copy, need_update = pattern_check(name, v['prob_cand_arr'], v['pred'], target_label_dim, v['avg_window'], v['data_len'], v['best'], true_label_map[dt] if dt in true_label_map else None, mode, range_stat)
            if not first:
                result = arr
                first = True
            else:
                result &= arr
            for l in arr:
                if l in acc_stat:
                    acc_stat[l] += 1
                else:
                    acc_stat[l] = 1
        print('真实下标', dt, true_label_map[dt] if dt in true_label_map else 'unknown', result, sorted(acc_stat.items(), key=lambda x : x[1], reverse=True))
        for l in range_stat:
            print(l, range_stat[l])
        print('\n\n')
    range_stat = {}
    for dt in dt_cand:
        s,data = get_best_item(name, target_label_dim, False, dt)
        result = set()
        std_stat = {}
        first = False
        for v in data[:10]:
            arr, arr_copy, need_update = pattern_check(name, v['prob_cand_arr'], v['pred'], target_label_dim, v['avg_window'], v['data_len'], v['best'], true_label_map[dt] if dt in true_label_map else None, mode, range_stat)
            if not first:
                result = arr
                first = True
            else:
                result &= arr
            for l in arr:
                if l in std_stat:
                    std_stat[l] += 1
                else:
                    std_stat[l] = 1
        print('真实下标', dt, true_label_map[dt] if dt in true_label_map else 'unknown', result, sorted(std_stat.items(), key=lambda x : x[1], reverse=True))
        for l in range_stat:
            print(l, range_stat[l])
    all_stat = {}
    for k in acc_stat:
        all_stat[k] = acc_stat[k]
    for k in std_stat:
        if k in all_stat:
            all_stat[k] += std_stat[k]
    final_sorted = sorted(all_stat.items(), key=lambda x : x[1], reverse=True)
    print('final:', final_sorted)
    print(sorted([v[0] for v in final_sorted[:7]]))
    print('\n\n')

if __name__ == '__main__':
    date_pattern = re.compile(r'^\d{4}\d{2}\d{2}$')
    target_label_dim = int(sys.argv[1])
    target_dt = sys.argv[2]
    mode = sys.argv[3]
    name=sys.argv[4]
    exclude = ['20251230', '20251228', '20060609']
    if target_dt == 'ALL':
        for folder_name in sorted(os.listdir(name)):
            if date_pattern.match(folder_name) and folder_name not in exclude:
                if 'AUTO' in mode:
                    predict_full(name, target_label_dim, [folder_name], mode)
                elif mode == 'MANUALLY_PREDICT':
                    predict(name, target_label_dim, [folder_name], mode)
    elif date_pattern.match(target_dt):
        exclude.append(target_dt)
        if 'AUTO' in mode:
            predict_full(name, target_label_dim, [target_dt], mode)
        elif mode == 'MANUALLY_PREDICT':
            predict(name, target_label_dim, [target_dt], mode)




#python strategy.py 0 20260602 MANUALLY_PREDICT qxc
#python strategy.py 1 ALL AUTO qxc



