import pickle, sys
import numpy as np
from datetime import datetime, timedelta
from colorama import init, Fore, Style
#from imblearn.over_sampling import *


def category_distribution(label_arr):
    label_arr_final = None
    if isinstance(label_arr, np.ndarray):
        label_arr_final = [v[0] if isinstance(v, list) else v for v in label_arr.tolist()]
    else:
        label_arr_final = [v[0] if isinstance(v, list) else v for v in label_arr]
    rst = {label : 0.0 for label in set(label_arr_final)}
    for label in label_arr_final:
        rst[label] += 1.0 / len(label_arr_final)
    rst = {k : '{:.2f}'.format(rst[k]) for k in rst}
    return rst

def category_label_by_comparison(truth, pred):
    # if abs(truth - pred) <= 0.015:
    #     return 1
    # elif truth < pred:
    #     return 0
    # else:
    #     return 2
    #return 0 if truth < pred or truth - pred < 0.01 else 1
    return 1 if truth >= pred else 0

def my_corr(a, b):
    return np.corrcoef(a, b)[0][1]

 
def days_between_dates(start, end):
    date1 = datetime.strptime(start, "%Y-%m-%d")
    date2 = datetime.strptime(end, "%Y-%m-%d")
    return (date2 - date1).days

def add_days(date_str, days):
    date = datetime.strptime(date_str, "%Y-%m-%d")
    new_date = date + timedelta(days=days)
    return new_date.strftime("%Y-%m-%d")

def get_weekday(date_str):
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    weekday = date_obj.weekday()
    weekday_str = [1, 2, 3, 4, 5, 6, 7]
    return weekday_str[weekday]

def build_sin():
    # 参数
    length = 1200  # 序列长度
    sample_rate = 44100  # 采样率
    frequency = 440  # 频率（A4音符）
    # 时间向量
    t = np.arange(length) / sample_rate
    # 生成正弦序列
    sine_wave = np.sin(2 * np.pi * frequency * t) * 100
    # 输出序列
    return sine_wave


def avg(arr):
    length = len(arr[0])
    result = []
    for i in range(length):
        result.append(sum([v[i] for v in arr]) / len(arr))
    return result

def sort_arr(arr):
    arr = [(i + 1, arr[i]) for i in range(len(arr))]
    return sorted(arr, key=lambda k : k[1], reverse=True)


def special_show(cand, true_y, label_dim):
    mp = [{} for i in range(7)]
    day = 0
    for i in range(len(cand) - 1, -1, -1):
        v = cand[i]
        for j in range(len(v)):
            if v[j] not in mp[j]:
                mp[j][v[j]] = [1, [len(cand) - i]]
            else:
                mp[j][v[j]][0] += 1
                mp[j][v[j]][1].append(len(cand) - i)
    tmp = []
    for v in mp:
        tmp.append(sorted(v.items(), key = lambda x:x[1][0]))
    hit = 0.0
    yes = False
    for pair in tmp[label_dim]:
        hit += 1.0
        if pair[0] == true_y[0]:
            yes = True
            break;
    return tmp, hit if yes else -1

def fill_hole(currentRawX, y_pos, time_window, mode, true_y, label_dim, name='ssq'):
    time_window_cand = currentRawX[y_pos - time_window : y_pos]
    recent_cand = currentRawX[y_pos - 30 : y_pos]
    if mode == 'REPEAT':
        currentRawX[y_pos] = currentRawX[y_pos - 1]
    elif mode == 'AVG':
        currentRawX[y_pos] = avg(time_window_cand)
    elif mode == 'KEEP':
        pass
    elif mode == 'RND':
        currentRawX[y_pos] = time_window_cand[random.randint(0,len(time_window_cand) - 1)]
    elif mode == 'SPECIAL':
        mp = [{} for i in range(len(currentRawX[0]))]
        dim_time_window_mp = {dim_pos : [] for dim_pos in range(get_dim_limit(label_dim, name))}
        for i in range(len(time_window_cand) - 1, -1, -1):
            num = time_window_cand[i][label_dim]
            dim_time_window_mp[num - 1].append(len(time_window_cand) - i)
        for num in dim_time_window_mp:
            dim_time_window_mp[num] = gen_detail_feature(dim_time_window_mp[num])
        dim_recent_mp = {dim_pos : [] for dim_pos in range(get_dim_limit(label_dim, name))}
        for i in range(len(recent_cand) - 1, -1, -1):
            num = recent_cand[i][label_dim]
            dim_recent_mp[num - 1].append(len(recent_cand) - i)
        for num in dim_recent_mp:
            dim_recent_mp[num] = gen_detail_feature(dim_recent_mp[num])
        detail = [{} for i in range(len(currentRawX[0]))]
        for j in range(len(currentRawX[0])):
            for v in time_window_cand:
                if v[j] not in mp[j]:
                    mp[j][v[j]] = 1
                else:
                    mp[j][v[j]] += 1
        for v in detail:
            for num in v:
                day_arr = v[num]
        rst = []
        middle = []
        for v in mp:
            middle.append(sorted(v.items(), key = lambda x:x[1]))
        for i in range(len(middle)):
            current = middle[i][-5:]
            if i == 0 or i == 6:
                rst.append(current[random.randint(0, len(current) - 1)][0])
            else:
                previous = middle[i-1][-5:]
                hit = -1
                for j in range(len(current) - 1, -1, -1):
                    for k in range(len(previous) - 1, -1, -1):
                        if previous[k][0] <= current[j][0] - 1 and previous[k][0] >= current[j][0] - 3:
                            hit = current[j][0]
                            break
                    if hit > 0:
                        break
                if hit > 0:
                    rst.append(hit)
                else:
                    for v in middle[i][:5]:
                        if v[0] < 30:
                            hit = v[0]
                            break
                    rst.append(hit)
        currentRawX[y_pos] = rst
        # if debug:
        #     current_hit = 0.0
        #     for pair in tmp[label_dim]:
        #         current_hit += 1.0
        #         if pair[0] == true_y[0]:
        #             break;
        #     recent_tmp, current_recent_hit = special_show(recent_cand, true_y, label_dim)
        #     tmp[label_dim] = [(v[0], v[1], dim_time_window_mp[v[0] - 1]['min_day_dis'], dim_time_window_mp[v[0] - 1]['max_day_dis'], dim_time_window_mp[v[0] - 1]['avg_range_len'], dim_time_window_mp[v[0] - 1]['max_range_len'], dim_time_window_mp[v[0] - 1]['min_range_len'], dim_time_window_mp[v[0] - 1]['std_range_len'], dim_time_window_mp[v[0] - 1]['pacf_range_len']) for v in tmp[label_dim]]
        #     recent_tmp[label_dim] = [(v[0], v[1], ) for v in recent_tmp[label_dim]]
        #     print('prob dist:', tmp[label_dim], "      ", true_y, "      ", recent_tmp[label_dim], '      ', current_recent_hit / len(recent_tmp[label_dim]) if current_recent_hit > -1 else -1)
        #     print([v[label_dim] for v in time_window_cand[-10:]])
        #     print(current_hit / (len(tmp[label_dim]) * 1.0))
        #     print('previous:', tmp[label_dim - 1], "      ", recent_tmp[label_dim - 1])
        #     print('\n\n')

def prepare_hole_data(label_dim=3, time_window=400, time_window_num=4, mode='SPECIAL', debug=False, cv_model='SCROLL', name='ssq'):
    lookback = time_window * time_window_num + time_window_num
    if lookback % 2 != 0:
        print('smooth_back must be even number!')
        exit()
    eX = {
        'x' : [None for i in range(lookback)],
        "extract_feature" : [None for i in range(lookback)]
    }
    dX = {
        'x' : [None for i in range(lookback)],
        "extract_feature" : [None for i in range(lookback)]
    }
    Y = [None for i in range(lookback)] # smooth or origin
    if debug:
        rawX = [[i,i,i] for i in range(1000)]
        rawY = [[i] for i in range(1000)]
        extractFeatures = [[i] for i in range(1000)]
    else:
        rawX, rawY, extractFeatures = raw_data(name, label_dim)
    rawX = rawX[-(lookback * 2):]
    rawY = rawY[-(lookback * 2):]
    length = len(rawX)
    for pos in range(time_window + 1):
        currentRawX = []
        currentRawY = []
        for i in range(length - pos - 1, length - pos - lookback - 1, -1):
            currentRawX.insert(0, rawX[i])
            currentRawY.insert(0, rawY[i])
        #[[1,4,3,5,6],[2,3,4,5,6],[3,4,5,6,7],[3,2,3,4,5]]
        #[[2],[3],[1],[6]]
        # 1 1 1 1 x 1 1 1 1 x 1 1 1 1 x 1 1 1 1 x
        for i in range(time_window_num):
            y_pos = -1 - i * (time_window + 1)
            fill_hole(currentRawX, y_pos, time_window, mode, currentRawY[y_pos], label_dim, name)
        currentRawX = smooth(currentRawX, label_dim, 'ORIGIN' if debug else 'VMD')
        for i in range(time_window_num):
            y_pos = -1 - i * (time_window + 1)
            x_cand = currentRawX[y_pos - time_window : y_pos]
            #extract_feature_cand = extractFeatures[y_pos - time_window - pos : y_pos - pos]
            eX['x'][y_pos - pos] = x_cand
            eX['extract_feature'][y_pos - pos] = extract_feature_cand
            dX['x'][y_pos - pos] = x_cand[-int(len(x_cand) / 2) : ]
            dX['extract_feature'][y_pos - pos] = extract_feature_cand[-int(len(extract_feature_cand) / 2) : ]
            Y[y_pos - pos] = currentRawY[y_pos]
    return generate_train_test_pred_data(eX, dX, Y, cv_model)




def day_range(split, total, fact):
    # if total % split != 0:
    #     print('split mast be interger times larger than split!')
    #     exit()
    length = total / split
    for i in range(split):
        if fact >= length * i and fact <= ((length * i + length) if i < split - 1 else (length * i + length + 0.1)):
            return i
    print('oh no!', fact)
    for i in range(split):
        print('区间', length * i, length * i + length)
    exit()



def ap(m):
    rst = []
    for k in m:
        if isinstance(m[k], list):
            rst += m[k]
        else:
            rst += [m[k]]
    return rst





# 0 : [7, 6, 8],
# 1 : [5, 4],
# 2 : [10, 9],
# 3 : [1,2,3],
# 4 : [11,12],
# 5 : [13,14,15,16,17,18,19,20,21,22,23,24]



# golden

# 0 : [21, 6],
# 1 : [5, 4],
# 2 : [10, 8, 15],
# 3 : [1,2,3],
# 4 : [9, 22, 16, 11, 24, 20, 23],
# 5 : [14, 17, 7, 12, 13]




# 0 : [10, 31, 14]
# 1 : [21, 8]
# 2 : [32, 30, 11]
# 3 : [7, 29, 9]
# 4 : [28, 27, 23, 26, 25, 24, 15, 20, 17, 18, 19, 22, 16, 13, 12]
label_discret_bck = {}

label_discret = {
    'ssq' : {
        0 : {
            0 : [21, 6],
            1 : [5, 4],
            2 : [10, 8, 15],
            3 : [1,2,3],
            4 : [9, 22, 16, 11, 24, 20, 23],
            5 : [14, 17, 7, 12, 13, 18, 19]
        },
        1 : {
            0 : [7, 23, 2],
            1 : [5, 25],
            2 : [3, 26, 4],
            3 : [11, 28, 24],
            4 : [17, 13, 21, 14, 8, 12, 6, 19, 15, 20, 10, 9, 16, 18, 22]
        },
        2 : {
            0 : [29, 8, 6],
            1 : [9, 7],
            2 : [11, 28, 4],
            3 : [14, 5, 3],
            4 : [20, 25, 24, 17, 23, 10, 26, 15, 13, 16, 21, 12, 19, 22, 18, 27, 30]
        },
        3 : {
            0 : [0],
            1 : [1]
            # 0 : [30, 28, 23],
            # 1 : [24, 31],
            # 2 : [25, 29, 18],
            # 3 : [21, 26, 27],
            # 4 : [22, 20, 16, 8, 12, 10, 19, 15, 11, 13, 17, 6, 14, 5, 7, 9, 4]
        },
        4 : {
            0 : [11, 9, 25],
            1 : [32, 27],
            2 : [31, 29, 10],
            3 : [30, 7, 8],
            4 : [28, 23, 26, 14, 24, 15, 20, 17, 18, 21, 19, 22, 16, 13, 12]
        },
        5 : {
            0 : [30, 16],
            1 : [31, 10, 18],
            2 : [14, 22, 27],
            3 : [11, 19, 15, 26],
            4 : [28, 29, 32, 20, 33, 21, 25, 24, 23, 17]
        },
        6 : {
            0 : [13, 4],
            1 : [9, 2],
            2 : [1, 10, 16],
            3 : [14, 5, 12],
            4 : [15, 7, 3, 11, 6, 8]
        }
    },
    'dlt' : {},
    'qxc' : {
        0 : {
            0 : [0,1,2],
            1 : [3,4],
            2 : [5,6],
            3 : [7,8,9]
        },
        1 : {
            0 : [0,1,2,3],
            1 : [4,5,6],
            2 : [7,8,9]
        },
        2 : {
            0 : [0,1,2,3],
            1 : [4,5,6],
            2 : [7,8,9]
        },
        3 : {
            0 : [0],
            1 : [1]
        },
        4 : {
            0 : [9, 0, 8, 6, 1],
            1 : [5, 4, 2, 3, 7]
        },
        5 : {
            0 : [0,1,2,3],
            1 : [4,5,6],
            2 : [7,8,9]
        },
        6 : {
            0 : [0,1,2,3],
            1 : [4,5,6,7],
            2 : [8,9,10,11],
            3 : [12,13,14,15]
        }
    },
    'rnd' : {}
}




def get_dim_limit(label_dim, name, discrete=False):
    global label_discret
    if discrete:
        return len(label_discret[name][label_dim])
    if 'ssq' in name:
        return 33 if label_dim < 6 else 16
    elif 'dlt' in name:
        return 35 if label_dim < 5 else 12
    elif 'qxc' in name:
        return 10 if label_dim < 6 else 15
    elif 'seq' in name:
        return 7

def gen_label_pos(label_dim, label_val, name='ssq', discrete=False):
    global label_discret
    if not discrete:
        #return label_val if name == 'qxc' else (label_val - 1)
        return label_val
    for label in label_discret[name][label_dim]:
        if label_val in label_discret[name][label_dim][label]:
            return label
        

def d_2_n(arr):
    arr_true = arr#v for v in (np.array(arr) - 0.5 / len(arr)) / (1-0.5)]
    if isinstance(arr_true, list) or isinstance(arr_true, np.ndarray):
        for i in range(len(arr_true)):
            if arr_true[i] == 1:
                return i
    else:
        return arr

def n_2_d(num, size):
    arr = [0 for i in range(size)]
    arr[num] = 1
    return arr


def multiply(arr):
    v = arr[0]
    for i in range(1, len(arr)):
        v *= arr[i]
    return v

def flatten(arr):
    arr = np.reshape(arr, multiply(np.array(arr).shape))
    return [v for v in arr]


def sort_pos_confirm(sorted, unsorted):
    val = []
    for v in sorted:
        val.append(unsorted.index(v))
    return val


def depend_on_rnd_simple(origin_arr):
    while True:
        a = np.array([v for v in np.random.choice(np.array([0,1,2,3,4,5,6,7,8,9]), 6, True)] + [np.random.randint(0,15)])
        b = origin_arr
        corr = my_corr(a, b)
        if corr > 0.99:
            return a
def build_rnd(origin_arr_arr):
    result = []
    for origin_arr in origin_arr_arr:
        new_arr = depend_on_rnd_simple(origin_arr)
        result.append(new_arr)
    return result

# build_rnd([np.array([v for v in np.random.choice(np.array([0,1,2,3,4,5,6,7,8,9]), 6, True)] + [np.random.randint(0,15)]) for k in range(20)])

def raw_data(name, label_dim, time_window, cat=True):
    extra = []
    ssq_raw = load_obj('ssq_raw')
    # ssq_raw.append({'sorted': '1 7 12 17 22 27 16', 'unsorted': '1 7 12 17 22 27 16', 'date': '2024-12-26', '1st_cnt': '0'})
    rawDLT = [ {'sorted' : [float(crt) for crt in v['sorted'].split(' ')], 'unsorted' : [float(crt) for crt in v['sorted'].split(' ')], 'date' : v['date']} for v in [w for w in load_obj('dlt_raw') if get_weekday(w['date']) > -1] ]
    rawSSQ = [ {'sorted' : [float(crt) for crt in v['sorted'].split(' ')], 'unsorted' : [float(crt) for crt in v['unsorted'].split(' ')], 'date' : v['date']} for v in [w for w in ssq_raw if get_weekday(w['date']) > -1] ]
    rawQXC = [ {'sorted' : [float(crt) for crt in v['sorted'].split(' ')], 'unsorted' : [float(crt) for crt in v['sorted'].split(' ')], 'date' : v['date']} for v in [w for w in load_obj('qxc_raw') if get_weekday(w['date']) > -1] ]
    raw3D = [ [float(crt) for crt in v['sorted'].split(' ')] for v in [w for w in load_obj('3d_raw') if get_weekday(w['date']) > -1] ]
    rawPLS = [ [float(crt) for crt in v['sorted'].split(' ')] for v in [w for w in load_obj('pls_raw') if get_weekday(w['date']) > -1] ]
    rawPLW = [ [float(crt) for crt in v['sorted'].split(' ')] for v in [w for w in load_obj('plw_raw') if get_weekday(w['date']) > -1] ]
    if 'ssq' in name:
        rawRND = [ sorted(random.sample([(i+1) for i in range(33)], 6)) +  random.sample([(i+1) for i in range(16)], 1) for i in range(3200)]
    elif 'qxc' in name:
        rawRND = [random.choices([i for i in range(10)], k=6) + random.choices([i for i in range(14)], k=1) for n in range(6000)]
    rawSIN = [[v,v,v,v,v,v,v] for v in build_sin()]
    if name == 'qxc':
        raw = [{'x' : v['sorted'], 'y' : [v['sorted'][label_dim]], 'sort_pos' : sort_pos_confirm(v['sorted'], v['unsorted']), 'date' : v['date'], 'dt' : datetime.datetime.strptime(v['date'], "%Y-%m-%d")} for v in rawQXC]
    elif name == 'ssq':
        raw = [{'x' : v['sorted'], 'y' : [v['sorted'][label_dim]], 'sort_pos' : sort_pos_confirm(v['sorted'], v['unsorted']), 'date' : v['date'], 'dt' : datetime.datetime.strptime(v['date'], "%Y-%m-%d")} for v in rawSSQ]
    elif name == 'dlt':
        raw = [{'x' : v['sorted'], 'y' : [v['sorted'][label_dim]], 'sort_pos' : sort_pos_confirm(v['sorted'], v['unsorted']), 'date' : v['date'], 'dt' : datetime.datetime.strptime(v['date'], "%Y-%m-%d")} for v in rawDLT]
    elif name == 'seq':
        raw = [{'x' : [i,i,i,i,i,i,i], 'y' : [i]} for i in range(len(rawSSQ))]
    elif 'rnd' in name:
        if 'qxc' in name:
            raw = []
            origin_arr_arr = [np.array(v['sorted']) for v in rawQXC]
            new_arr_arr = build_rnd(origin_arr_arr)
            for i in range(len(rawQXC)):
                raw.append({'x' : new_arr_arr[i].tolist(), 'y' : [new_arr_arr[i][label_dim]], 'dt' : datetime.datetime.strptime(rawQXC[i]['date'], "%Y-%m-%d"), 'date' : rawQXC[i]['date']})
        else:
            raw = [{'x' : v, 'y' : [v[label_dim]], 'date' : str(random.randint(0, len(rawRND) - 1))} for v in rawRND]
    stat = [v['x'][label_dim] for v in raw]
    dim_limit = get_dim_limit(label_dim, name)
    current_all = []
    for i in range(len(stat) - 1, len(stat) - time_window - 1, -1):
        current = [0 for d in range(dim_limit)]
        for v in stat[i - time_window : i]:
            current[int(v if 'qxc' in name else v - 1)] += 1
        current_all += current
    current_all = sorted(current_all)
    print(np.mean(current_all), max(current_all), min(current_all), current_all[int(len(current_all) / 2)], current_all[int(len(current_all) * 2 / 3)])
    min_segment = 18#int(np.mean(current_all))
    # future_raw = load_obj(name + '_' + str(time_window) + '_rnd_' + str(label_dim))
    # final_raw = []
    # for date in future_raw:
    #     body = future_raw[date]
    #     for i in range(len(raw)):
    #         v = raw[i]
    #         if date == v['date']:
    #             stat = {}
    #             a = [v['x'][label_dim] for v in raw[i - time_window : i]]
    #             for ck in body:
    #                 yv = (0 if abs(v['x'][label_dim] - body[ck][-1]) < 3 else 1) if cat else v['x'][label_dim] - body[ck][-1]
    #                 final_raw.append({'date' : date,'origin' : a, 'generate' : body[ck][:-1], 'y' : [yv]})
    #                 if yv in stat:
    #                     stat[yv] += 1
    #                 else:
    #                     stat[yv] = 1
    #             # print({k: v for k, v in sorted(stat.items(), key=lambda item: item[1], reverse=True)})
    #             break
    return raw, min_segment


def change_label_dict(y_stats, name, label_dim):
    global label_discret
    if name not in label_discret:
        label_discret[name] = {}
    if label_dim not in label_discret[name]:
        label_discret[name][label_dim] = {}
    retry_cnt = 0
    while True:
        pos_array = [l for l in y_stats]
        valid = True
        cnt = 0
        for n in [5]:
            sampled_arr = random.sample(pos_array, n)
            label_discret[name][label_dim][cnt] = [int(v) for v in sampled_arr]
            pos_array = [v for v in pos_array if v not in sampled_arr]
            current_sum = sum([y_stats[l] for l in sampled_arr])
            valid = valid and current_sum > 150
            cnt += 1
        current_sum = sum([y_stats[l] for l in pos_array])
        label_discret[name][label_dim][cnt] = [int(v) for v in pos_array]
        valid = valid and current_sum > 150
        if label_dim < 6:
            valid = valid and np.std(label_discret[name][label_dim][cnt]) < 4
        retry_cnt += 1
        if valid:
            break
    print('\nlabel with retry:' + str(retry_cnt))


def to_numpy(data):
    for k in data:
        if k == 'ref':
            return
        if data[k] and isinstance(data[k], list):
            data[k] = np.array(data[k])


def gen_aggr_shit(arr):
    result = []
    result.append(np.std(arr))
    result.append(np.mean(arr))
    result.append(np.max(arr))
    result.append(np.min(arr))
    _adf = adf_check(arr)
    result.append(_adf[0])
    result.append(_adf[1])
    result.append(_adf[4]['1%'])
    result.append(_adf[4]['5%'])
    result.append(_adf[4]['10%'])
    result.append(_adf[5])
    # _lb = lb_check(arr, 10)
    # result.append(_lb[0][0])
    # result.append(_lb[1][0])
    # result.append(_lb[2][0])
    # result.append(_lb[5][0])
    # result.append(_lb[7][0])
    # result.append(_lb[0][1])
    # result.append(_lb[1][1])
    # result.append(_lb[2][1])
    # result.append(_lb[5][1])
    # result.append(_lb[7][1])
    _acf = acf_check(arr, 10)
    result.append(_acf[1])
    result.append(_acf[2])
    result.append(_acf[4])
    result.append(_acf[5])
    result.append(_acf[7])
    _pacf = pacf_check(arr, 10)
    result.append(_pacf[1])
    result.append(_pacf[2])
    result.append(_pacf[4])
    result.append(_pacf[5])
    result.append(_pacf[7])
    return result




sms = {
    'origin' : {'VMD' : 6}
}

def diff_fill(pos, i, min_segment, currentResult):
    if len(currentResult[pos][i]) < min_segment:
        mi = currentResult[pos][i][0] if len(currentResult[pos][i]) > 0 else 0
        currentResult[pos][i] = [mi for k in range(min_segment - len(currentResult[pos][i]))] + currentResult[pos][i]

def gen_feature_future(current):
    currentResult = [[],[]]
    a = np.array(current['origin'])
    b = np.array(current['generate'])
    currentResult[0] = [v for v in a - b]
    currentResult[1] = [math.sqrt(v * v) for v in a - b]
    return currentResult

def gen_feature_current(date, name, label_dim, raw, y_pos, time_window, dim_limit, min_segment, dim_seq=0, smooth_methods=None, external=None, discrete=False, persist=False, pred_y=None, current_days_all=None):
    if False:
        current_days = current_days_all[date]
    else:
        current_days = [[] for j in range(dim_limit)]
        last_day = raw[ : y_pos][-1]['dt']
        for twv in raw[ : y_pos]:
            v = int(gen_label_pos(label_dim, twv['x'][label_dim], name, discrete))
            current_days[v].append((last_day - twv['dt']).days)
        current_days_all[date] = current_days
    smooth_method_num = 0
    if smooth_methods is not None:
        for out_key in smooth_methods:
            for in_key in smooth_methods[out_key]:
                smooth_method_num += smooth_methods[out_key][in_key]
    out_pos = 0
    if dim_seq == 0:
        dvs = [2,8,16,32,64,128]
        time_window_shift = [time_window, 128, 64, 32, 18]
        currentResult = [[[0 for c in range(min_segment)] for b in range(dim_limit)] for a in range(1 + len(dvs) + len(time_window_shift) + smooth_method_num)]
        for c_t_w in time_window_shift:
            day_pos = 0
            c_t_w_v = raw[y_pos - c_t_w : y_pos]
            if len(c_t_w_v) > 0:
                last_day = c_t_w_v[-1]['dt']
                first_day = c_t_w_v[0]['dt']
                for v in c_t_w_v:
                    currentResult[out_pos][int(gen_label_pos(label_dim, v['x'][label_dim], name, discrete))][day_range(min_segment, (last_day - first_day).days, (last_day - v['dt']).days)] += 1.0
            out_pos += 1
        for i in range(dim_limit):
            in_pos = out_pos
            currentResult[in_pos][i] = [v for v in np.diff(current_days[i])][-min_segment:]
            diff_fill(in_pos, i, min_segment, currentResult)
            dio = 0
            for k in range(len(current_days[i]) - 1, -1, -1):
                di = 0
                for dv in dvs:
                    if k - dv > -1:
                        currentResult[in_pos + 1 + di][i].insert(0, (current_days[i][k] - current_days[i][k - dv]))
                    # if k > -1 and dio % dv == 0:
                    #     currentResult[in_pos + 1 + dio][i].insert(0, current_days[i][k])
                    di += 1
                dio += 1
            for di in range(len(dvs)):
                # currentResult[in_pos + 1 + di][i] = [abs(v) for v in np.diff(currentResult[in_pos + 1 + di][i])][-min_segment:]
                currentResult[in_pos + 1 + di][i] = currentResult[in_pos + 1 + di][i][-min_segment:]
            for di in range(len(dvs)):
                diff_fill(in_pos + 1 + di, i, min_segment, currentResult)
            in_pos += len(dvs)
            if smooth_methods is not None:
                sm = {key : {} for key in smooth_methods}
                for smooth_method in smooth_methods['origin'].keys():
                    sm['origin'][smooth_method] = smooth(currentResult[in_pos][i], _type=smooth_method, param={'alpha' : 0.8, 'wavelet' : 'bior1.1', 'level' : 5, 'period' : 10, 'vmd_cut' : False})
                if date not in external:
                    external[date] = [None for n in range(dim_limit)]
                if  external[date][i] is None:
                    external[date][i] = sm
                else:
                    for out_key in sm:
                        if out_key not in external[date][i]:
                            external[date][i][out_key] = sm[out_key]
                        else:
                            for in_key in sm[out_key]:
                                external[date][i][out_key][in_key] = sm[out_key][in_key]
            if date in external and (smooth_methods is not None):
                sm = external[date][i]
                in_pos += 1
                for key in smooth_methods:
                    for smooth_method in smooth_methods[key]:
                        vvv = sm[key][smooth_method]
                        if smooth_method in ['EMD', 'EEMD', 'LMD', 'CEEMDAN', 'SGMD']:
                            vvv = vvv[:4]
                            # vvv = vvv[-3:]
                        elif smooth_method == 'FFT':
                            # vvv[0] = abs(vvv[0]) / (time_window * 2)
                            # vvv[2] = abs(vvv[2])
                            vvv[0] = vvv[0].real / (time_window * 2)
                            vvv[2] = vvv[2].real
                            vvv = [vvv[0]]
                        for row in vvv:
                            currentResult[in_pos][i] = row
                            in_pos += 1
    return currentResult




def gen_full_ts_feature_current(date, name, label_dim, raw, y_pos, time_window, dim_limit, min_segment, dim_seq=0, smooth_methods=sms, external=None, discrete=False, persist=False, pred_y=None):
    x = [v['x'][label_dim] for v in raw]
    smooth_method_num = 0
    if smooth_methods is not None:
        for out_key in smooth_methods:
            for in_key in smooth_methods[out_key]:
                smooth_method_num += smooth_methods[out_key][in_key]
    origin = x[y_pos - time_window : y_pos]
    if pred_y is None:
        origin = origin[1:]
    elif date in pred_y:
        origin.append(pred_y[date])
    else:
        origin.append(origin[-1])
        print('应该只有一个吧', date)
    diff = [v for v in np.diff(x[y_pos - time_window : y_pos])]
    currentResult = [[0 for c in range(time_window)] for b in range(smooth_method_num)]
    if persist and (smooth_methods is not None):
        sm = {key : {} for key in smooth_methods}
        for smooth_method in smooth_methods['origin'].keys():
            # sm['diff'][smooth_method] = smooth(currentResult[0], _type=smooth_method, param={'alpha' : 0.5, 'wavelet' : 'bior6.8', 'level' : 7})
            sm['origin'][smooth_method] = smooth(origin, _type=smooth_method, param={'alpha' : 0.5, 'wavelet' : 'bior6.8', 'level' : 7, 'period' : 8, 'vmd_cut' : pred_y is not None})
        external[date] = sm
    if external is not None and date in external:
        sm = external[date]
    out_pos = 0
    if smooth_methods is not None:
        for key in smooth_methods:
            for smooth_method in smooth_methods[key]:
                vvv = sm[key][smooth_method]
                if smooth_method in ['EMD', 'EEMD', 'LMD', 'CEEMDAN', 'SGMD']:
                    vvv = vvv[:5]
                    #vvv = vvv[-4:]
                elif smooth_method == 'FFT':
                    # vvv[0] = abs(vvv[0])
                    # vvv[2] = abs(vvv[2])
                    vvv[0] = vvv[0].real
                    vvv[2] = vvv[2].real
                    # vvv = [vvv[0],vvv[0],vvv[0],vvv[0]]
                for row in vvv:
                    currentResult[out_pos] = row
                    out_pos += 1
    return currentResult





def cat_label_gen(origin_label, name, label_dim):
    global label_discret
    hit = False
    yy = [0 for i in range(len(label_discret[name][label_dim]))]
    for label in label_discret[name][label_dim]:
        if origin_label in label_discret[name][label_dim][label]:
            yy[label] = 1
            hit = True
            break
    if not hit:
        print('不中', origin_label)
    return yy


base_path = '/Users/zhiljiang/proj/work/85000000'

def direct_feature(label_dim=1, time_window=10, name='seq', norm='MIN-MAX', dim_seq=0, discrete=False, feature_mode='FULL', label_mode='CAT', external=None, persist=False, pred_y=None, rnd_data_enhance=False):
    if feature_mode not in ['FULL', 'COMMON']:
        print('feature_mode must be FULL or COMMON')
        exit()
    if label_mode not in ['CAT', 'REG']:
        print('label_mode must be CAT or REG')
        exit()
    # raw
    # [{'x' : [3,7,10,15,24,31,12], 'y' : [15], 'sort_pos' : [2,3,4,5,0,1,6], 'date' : '20240201'}]
    X_M = []
    Y_M = []
    REF_M = []
    X = []
    Y = []
    REF = []
    raw, min_segment = raw_data(name, label_dim, time_window)
    raw_label_stats = {}
    # for i in range(len(raw)):
    #     y = raw[i]['y']
    #     if y[0] in raw_label_stats:
    #         raw_label_stats[y[0]] += 1
    #     else:
    #         raw_label_stats[y[0]] = 1
    # print('原始SKIP分布', sorted(raw_label_stats.items(), key = lambda x : x[1]))
    if label_mode == 'CAT':
        if len(label_discret) == 0:
            change_label_dict(raw_label_stats, name, label_dim)
        for k in label_discret[name][label_dim]:
            print(k, ':', label_discret[name][label_dim][k])
    if external is None:
        external = {}
    dim_limit = get_dim_limit(label_dim, name, discrete)
    current_days_all = {}
    # current_day_exist = False
    # if os.path.exists(base_path + '/current_day_' + str(len(raw)) + '_' + name + '_' + str(time_window) + '_' + str(discrete) + '.pkl'):
    #     current_days_all = load_obj('current_day_' + str(len(raw)) + '_' + name + '_' + str(time_window) + '_' + str(discrete))
    #     current_day_exist = True
    for i in range(len(raw) - 1, time_window - 1, -1):
        time_window_value = raw[i - time_window : i]
        y = raw[i]['y'][0]
        date = raw[i]['date']
        ref = None#{'x_back' : [v['x'][label_dim] for v in raw[i - 10 : i]], 'y' : y, 'date' : date}
        if feature_mode=='COMMON':
            #x = gen_feature_future(raw[i])
            x = gen_feature_current(date, name, label_dim, raw, i, time_window, dim_limit, min_segment, dim_seq, external=external, discrete=discrete, persist=persist, pred_y=pred_y, current_days_all=current_days_all)
        else:
            x = gen_full_ts_feature_current(date, name, label_dim, raw, i, time_window, dim_limit, min_segment, dim_seq, external=external, discrete=discrete, persist=persist, pred_y=pred_y)
        if len(Y) in [int((len(raw) - time_window) / 10), int((len(raw) - time_window) / 10) * 2, int((len(raw) - time_window) / 10) * 3, int((len(raw) - time_window) / 10) * 4, int((len(raw) - time_window) / 10) * 5, int((len(raw) - time_window) / 10) * 6, int((len(raw) - time_window) / 10) * 7, int((len(raw) - time_window) / 10) * 8, int((len(raw) - time_window) / 10) * 9, int(len(raw) - time_window)]:
            print('进度:', str(int(len(Y) / (len(raw) - time_window) * 100)) + '%', len(Y), len(raw) - time_window)
        X.insert(0, x)
        Y.insert(0, y)
        REF.insert(0, ref)
    # if not current_day_exist:
    #     persist_obj(current_days_all, 'current_day_' + str(len(raw)) + '_' + name + '_' + str(time_window) + '_' + str(discrete))
    if rnd_data_enhance:
        # montecarlo
        print('START MONTECARLO!!!!')
        raw_m, min_segment_m = raw_data('rnd_' + name, label_dim, time_window)
        for i in range(len(raw_m) - 1, time_window - 1, -1):
            time_window_value = raw_m[i - time_window : i]
            y = raw_m[i]['y'][0]
            date = raw_m[i]['date']
            ref = {'x_back' : [v['x'][label_dim] for v in raw_m[i - 10 : i]], 'y' : y, 'date' : date}
            if feature_mode=='COMMON':
                x = gen_feature_current(date, name, label_dim, raw_m, i, time_window, dim_limit, min_segment, dim_seq, external=external, discrete=discrete, persist=persist, pred_y=pred_y, current_days_all=current_days_all)
            else:
                x = gen_full_ts_feature_current(date, name, label_dim, raw_m, i, time_window, dim_limit, min_segment, dim_seq, external=external, discrete=discrete, persist=persist, pred_y=pred_y)
            if len(Y_M) in [int((len(raw_m) - time_window) / 10), int((len(raw_m) - time_window) / 10) * 2, int((len(raw_m) - time_window) / 10) * 3, int((len(raw_m) - time_window) / 10) * 4, int((len(raw_m) - time_window) / 10) * 5, int((len(raw_m) - time_window) / 10) * 6, int((len(raw_m) - time_window) / 10) * 7, int((len(raw_m) - time_window) / 10) * 8, int((len(raw_m) - time_window) / 10) * 9, int(len(raw_m) - time_window)]:
                print('进度:', str(int(len(Y_M) / (len(raw_m) - time_window) * 100)) + '%', len(Y_M), len(raw_m) - time_window)
            X_M.insert(0, x)
            Y_M.insert(0, y)
            REF_M.insert(0, ref)
        m_name = 'rnd_' + name
        if os.path.exists(base_path + '/' + m_name + '.pkl'):
            os.remove(base_path + '/' + m_name + '.pkl')
            print('清理 ' + m_name + ' 成功!')
        persist_obj(raw_m, m_name)
    if persist:
        external_name = 'external_' + name + '_' + str(label_dim) + '_' + feature_mode + '_' + str(time_window)
        if os.path.exists(base_path + '/' + external_name + '.pkl'):
            os.remove(base_path + '/' + external_name + '.pkl')
            print('清理 ' + external_name + ' 成功!')
        persist_obj(external, external_name)
        print('persist ' + external_name + ' 成功!')
    # split data set start
    y_stat = {}
    ##
    crt_pos = len(Y) - 1
    skip_pos = []
    while crt_pos > -1:
        skip_pos.append(crt_pos)
        crt_pos = crt_pos - 1
    pred_pos = skip_pos[0]
    for pos in skip_pos[1:]:
        y_for_stat = gen_label_pos(label_dim, Y[pos], name, discrete)
        if y_for_stat not in y_stat:
            y_stat[y_for_stat] = [pos]
        else:
            y_stat[y_for_stat].append(pos)
    y_stats_num = {k : len(y_stat[k]) for k in y_stat}
    print('\nSKIP后分布(去掉timewindow长度)', sorted(y_stats_num.items(), key = lambda x : x[1]), len(X))
    if label_mode == 'CAT':
        for i in range(len(Y)):
            Y[i] = cat_label_gen(Y[i], name, label_dim)
        for i in range(len(Y_M)):
            Y_M[i] = cat_label_gen(Y_M[i], name, label_dim)
    sample_stat = {i : [] for i in y_stat.keys()}
    result = []
    test_sum_check = []
    for sample_cnt in range(8):
        train_pos = []
        test_pos = []
        for l in y_stat:
            l_all_pos = y_stat[l]
            if len(l_all_pos) - len(sample_stat[l]) < int(len(l_all_pos) * 0.2) or sample_cnt == 8:
                l_test_pos = [v for v in l_all_pos if v not in sample_stat[l]]
                sample_stat[l] += l_test_pos
            else:
                l_test_pos = random.sample([v for v in l_all_pos if v not in sample_stat[l]], int(len(l_all_pos) * 0.2))
                # al = int(len(l_all_pos) * 0.12)
                # l_test_pos = l_all_pos[sample_cnt * al : (sample_cnt + 1) * al]
                sample_stat[l] += l_test_pos
            l_train_pos = [v for v in l_all_pos if v not in l_test_pos]
            train_pos += l_train_pos
            test_pos += l_test_pos
            print('sample之前:第' + str(sample_cnt) + '轮', 'ty:', l, 'tt:', len(l_test_pos))
        for vvv in test_pos:
            if vvv in train_pos:
                print('大事不妙啦', vvv)
                exit()
        test_sum_check += test_pos
        test = {
            'x' : [X[i] for i in test_pos],
            'y' : [Y[i] for i in test_pos],
            'ref' : [REF[i] for i in test_pos]
        }
        pred = {
            'x' : [X[pred_pos]],
            'y' : None,
            'ref' : [REF[pred_pos]]
        }
        train = {
            'x' : [X[i] for i in train_pos],
            'y' : [Y[i] for i in train_pos],
            'ref' : [REF[i] for i in train_pos]
        }
        if rnd_data_enhance:
            train['x'] += [X_M[i] for i in train_pos]
            train['y'] += [Y_M[i] for i in train_pos]
            train['ref'] += [REF_M[i] for i in train_pos]
        #over_sample(None, test, name, label_dim, 'ENRICH', {i : 2 for i in range(dim_limit)}, label_mode=='CAT')
        stat_after = {}
        for yv in test['y']:
            yvv = d_2_n(yv) if label_mode=='CAT' else yv
            if yvv not in stat_after:
                stat_after[yvv] = 1
            else:
                stat_after[yvv] += 1
        for sv in stat_after:
            print('sample之后:第' + str(sample_cnt) + '轮', 'ty:', sv, 'tt:', stat_after[sv])
        #over_sample(train, None, name, label_dim, 'BorderlineSMOTE', {'times' : 8}, label_mode=='CAT')
        #over_sample(train, None, name, label_dim, 'ENRICH', {i : 10 for i in range(dim_limit)}, label_mode=='CAT')
        if norm == 'MIN-MAX':
            norm_min_max([train['x'], test['x'], pred['x']])
        elif norm == 'Z-SCORE':
            norm_z_score([train['x'], test['x'], pred['x']])
        # if flat:
        #     for pos in range(len(train['x'])):
        #         train['x'][pos] = flatten(train['x'][pos])
        #         train['y'][pos] = d_2_n(train['y'][pos]) - 1
        to_numpy(train)
        # if flat:
        #     for pos in range(len(test['x'])):
        #         test['x'][pos] = flatten(test['x'][pos])
        #         test['y'][pos] = d_2_n(test['y'][pos]) - 1
        #     for pos in range(len(pred['x'])):
        #         pred['x'][pos] = flatten(pred['x'][pos])
        to_numpy(test)
        to_numpy(pred)
        # test['x'] = test['x'].reshape(test['x'].shape[0], test['x'].shape[1], test['x'].shape[3], test['x'].shape[2])
        # train['x'] = train['x'].reshape(train['x'].shape[0], train['x'].shape[1], train['x'].shape[3], train['x'].shape[2])
        result.append({'train' : train,  'test' : test, 'pred' : pred})
    return result



def raw_enrich(data, limit):
    exp = []
    for v in data:
        for n in range(random.randint(1, limit)):
            exp.append(v)
    return exp

def enrich(data, limit, cat=True):
    exp = {k : [] for k in data}
    for i in range(len(data['y'])):
        y_l = d_2_n(data['y'][i]) if cat else data['y'][i]
        for n in range(limit[y_l]):
            for k in exp:
                exp[k].append(data[k][i])
    for k in exp:
        data[k] = exp[k]


'''
    x =[
        [
            [1,2,3,3],
            [2,5,4,4],
            [7,6,5,5]
        ],
        [
            [2,2,2,2],
            [3,3,2,1],
            [1,2,2,2]
        ],
        [
            [4,5,3,3],
            [1,1,2,2],
            [6,6,5,5]
        ],
        [
            [2,3,2,3],
            [6,6,1,1],
            [1,6,7,7]
        ],
        [
            [6,1,2,2],
            [9,8,7,7],
            [6,3,2,2]
        ]
    ]
    shape = np.array(x[0]).shape
    for i in range(len(x)):
        x[i] = np.reshape(x[i], multiply(np.array(x[i]).shape))
        x[i] = [v for v in x[i]]

    print(x)
    for i in range(len(x)):
        x[i] = np.reshape(x[i], shape).tolist()
    print(x)
'''
def over_sample(train_x, train_y, mode='SMOTE'):
    shape = np.array(train_x[0]).shape
    for i in range(len(train_x)):
        train_x[i] = np.reshape(train_x[i], multiply(np.array(train_x[i]).shape))
        train_x[i] = [v for v in train_x[i]]
    if mode == 'BorderlineSMOTE':
        x_r, y_r = BorderlineSMOTE().fit_resample(train_x, train_y)
    elif mode == 'ADASYN':
        x_r, y_r = ADASYN().fit_resample(train_x, train_y)
    elif mode == 'SMOTE':
        x_r, y_r = SMOTE().fit_resample(train_x, train_y)
    elif mode == 'KMeansSMOTE':
        x_r, y_r = KMeansSMOTE().fit_resample(train_x, train_y)
    elif mode == 'SMOTENC':
        x_r, y_r = SMOTENC(categorical_features=[i for i in range(sum(shape))]).fit_resample(train_x, train_y)
    elif mode == 'SMOTEN':
        x_r, y_r = SMOTEN().fit_resample(train_x, train_y)
    elif mode == 'SVMSMOTE':
        x_r, y_r = SVMSMOTE().fit_resample(train_x, train_y)
    else:
        print('OVER SAMPLE MODE INVALID!')
        exit(0)
    for i in range(len(x_r)):
        x_r[i] = np.reshape(x_r[i], shape).tolist()
    for i in range(len(y_r)):
        y_r[i] = [y_r[i]]
    return x_r, y_r


def repeat(data):
    exp = {'y' : [], 'x' : []}
    for i in range(len(data['y'])):
        for l in ext_dict:
            if l > -1:
                if d_2_n(data['y'][i]) == l:
                    if ext_dict[l] == 0.5:
                        if random.randint(0, 1) == 0:
                            exp['x'].append(data['x'][i])
                            exp['y'].append(data['y'][i])
                    else:
                        for n in range(ext_dict[l]):
                            exp['x'].append(data['x'][i])
                            exp['y'].append(data['y'][i])
    data['x'] += exp['x']
    data['y'] += exp['y']


def merge(a, b):
    r = 0.5#random.randint(0,10) / 10.0
    s = 1.0 - r
    return (np.array(a) * r + np.array(b) * s).tolist()





def sample(name):
    with open(name + ".txt", "a") as f:
        for i in range(1200):
            arr = [random.random() for v in range(10)]
            f.write(str(arr).replace(' ', '').replace('[', '').replace(']', '') + ':' + str(arr[3]) + "\n")



SSQ_HISTORY="https://data.17500.cn/ssq_asc.txt"
URL_SSQ_BASE = "http://www.cwl.gov.cn";
URL_SSQ = "http://www.cwl.gov.cn/cwl_admin/front/cwlkj/search/kjxx/findDrawNotice?name=ssq&issueCount=&issueStart=&issueEnd=&dayStart=&dayEnd=&pageNo=1&pageSize=30&week=&systemType=PC";
URL_DLT = "https://webapi.sporttery.cn/gateway/lottery/getHistoryPageListV1.qry?gameNo=85&provinceId=0&pageSize=30&isVerify=1&pageNo=1";
URL_QXC = "https://webapi.sporttery.cn/gateway/lottery/getHistoryPageListV1.qry?gameNo=04&provinceId=0&pageSize=30&isVerify=1&pageNo=1";

seq = [[1,5,2,1,6],
       [2,4,3,3,1],
       [5,1,2,3,4],
       [6,7,4,2,2], # ==> 3
       [6,1,2,3,4], # ==> 5
       [8,1,2,1,9], # ==> 8
       [7,1,2,2,2], # ==> 2
       [9,5,3,2,1], # ==> 4
       [6,7,8,9,0], # ==> 6
       [2,3,1,1,1]] # ==> 8

result = [3,5,8,2,4,6,8]

step=4
dim=5


def g_mean(data):
    prod = np.prod(data)
    n = len(data) * 1.0
    return prod ** (1/n)


# print('\n怎么样', trainEX['origin'].shape, trainEX['fft'].shape, trainEX['avg'].shape, trainEX['exp'].shape, trainEX['extract_feature'].shape, trainEX['previous_freq'].shape, trainEX['previous_day'].shape, trainY['origin'].shape, JIEXIAN)



def persist_obj(obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f)

def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

def stat_gap(arr):
    result = {0:0,1:0,2:0,3:0}
    for v in arr:
        if abs(v) < 0.01:
            result[0] += 1
        elif abs(v) < 0.02:
            result[1] += 1
        elif abs(v) < 0.03:
            result[2] += 1
        else:
            result[3] += 1
    return result

def stat_gap_norm(arr):
    result = [0.0,0.0,0.0,0.0]
    for v in arr:
        if abs(v) < 0.01:
            result[0] += 1.0
        elif abs(v) < 0.02:
            result[1] += 1.0
        elif abs(v) < 0.03:
            result[2] += 1.0
        else:
            result[3] += 1.0
    return [v / float(len(arr)) for v in result]



def generateProbRawByDate(start, combine, name, label_pos, date, label_list):
    lookbacks = combine
    label = []
    for line in label_list:
        if line[0] < date:
            label.append(int(line[label_pos+1]))
        else:
            break
    #print('最后', line, label_pos, line[label_pos+1])
    x_raw = [[] for i in range(len(lookbacks))]
    y_raw = [[] for i in range(len(lookbacks))]
    for lookback_pos in range(len(lookbacks)):
        lookback = lookbacks[lookback_pos]
        for i in range(start, len(label) + 1):
            stat = [0.0 for l in (range(10) if label_pos < 6 else range(15))]
            current = label[i] if i < len(label) else -1
            for v in label[i - lookback : i]:
                stat[v] += 1.0
            mx = max(stat)
            mi = min(stat)
            if mx == mi:
                print(stat, label[i - lookback : i], lookback, i)
            for k in range(len(stat)):
                stat[k] = (stat[k] - mi) / (mx - mi)
            x_raw[lookback_pos].append([stat[s] for s in range(len(stat))])
            y_raw[lookback_pos].append(stat[current] if current > -1 else current)
    return x_raw, y_raw


def loadProbCand(name, label_pos, start, combine, avg_window, date, label_list):
    y_on_prob_raw = [[] for i in range(len(combine))]
    x_raw, y_raw = generateProbRawByDate(start, combine, name, label_pos, date, label_list)
    v_len = len(y_raw[0])
    h_len = len(y_raw)
    all_label_prob = []
    all_label_prob_accum = []
    for i in range(v_len):
        if y_raw[0][i] == -1:
            for al in range(len(x_raw[0][0])):
                all_label_prob.append([x_raw[j][i][al] for j in range(h_len)])
        #prepare time series on prob
        if i >= avg_window - 1:
            if y_raw[0][i] != -1:
                pass
            else:
                for al in range(len(x_raw[0][0])):
                    all_label_prob_accum.append([np.mean(y_raw[j][i - avg_window + 1: i] + [x_raw[j][i][al]]) for j in range(h_len)])
    direct = []
    accum = []
    for k in range(len(all_label_prob)):
        direct.append(all_label_prob[k][0])
        accum.append(all_label_prob_accum[k][0])
    return direct, accum


def get_best_item(name, label_dim, acc=False,metric_folder=None,date_list=None,label_list=None,debug=False):
    check_label_len = 10 if label_dim < 6 else 15
    data = load_obj(name + '/' + metric_folder + '/detail_' + str(label_dim))
    for i in range(len(data)):
        validate_html = data[i]['validate_html'].split('<br\\>')
        v = data[i]
        prob_cand_arr = []
        prob_cand_direct_arr = []
        prob_cand_gap_arr = []
        previous_truth_arr = []
        previous_pred_arr = []
        previous_truth_arr.append(float(validate_html[-3].split('----')[1].split(' ')[1].replace('[', '').replace(']', '').replace("'", '')))
        previous_truth_arr.append(float(validate_html[-4].split('----')[1].split(' ')[1].replace('[', '').replace(']', '').replace("'", '')))
        previous_truth_arr.append(float(validate_html[-5].split('----')[1].split(' ')[1].replace('[', '').replace(']', '').replace("'", '')))
        previous_truth_arr.append(float(validate_html[-6].split('----')[1].split(' ')[1].replace('[', '').replace(']', '').replace("'", '')))
        previous_truth_arr.append(float(validate_html[-7].split('----')[1].split(' ')[1].replace('[', '').replace(']', '').replace("'", '')))
        previous_truth_arr.append(float(validate_html[-8].split('----')[1].split(' ')[1].replace('[', '').replace(']', '').replace("'", '')))
        previous_truth_arr.append(float(validate_html[-9].split('----')[1].split(' ')[1].replace('[', '').replace(']', '').replace("'", '')))
        previous_truth_gap_arr = []
        previous_pred_arr.append(float(validate_html[-3].split('----')[0].split(' ')[1].replace('[', '').replace(']', '').replace("'", '')))
        previous_pred_arr.append(float(validate_html[-4].split('----')[0].split(' ')[1].replace('[', '').replace(']', '').replace("'", '')))
        previous_pred_arr.append(float(validate_html[-5].split('----')[0].split(' ')[1].replace('[', '').replace(']', '').replace("'", '')))
        previous_pred_arr.append(float(validate_html[-6].split('----')[0].split(' ')[1].replace('[', '').replace(']', '').replace("'", '')))
        previous_pred_arr.append(float(validate_html[-7].split('----')[0].split(' ')[1].replace('[', '').replace(']', '').replace("'", '')))
        previous_pred_arr.append(float(validate_html[-8].split('----')[0].split(' ')[1].replace('[', '').replace(']', '').replace("'", '')))
        previous_pred_arr.append(float(validate_html[-9].split('----')[0].split(' ')[1].replace('[', '').replace(']', '').replace("'", '')))
        for pi in range(len(previous_truth_arr)):
            previous_truth_gap_arr.append(previous_truth_arr[pi] - previous_pred_arr[pi])
        for item in v['prob_cand_html'].split('<br\\>'):
            if len(item) > 5:
                prob_cand_arr.append(float(item.split(', ')[2].replace('[', '').replace(']', '').replace("'", '')))
                prob_cand_direct_arr.append(float(item.split(', ')[1].replace('[', '').replace(']', '').replace("'", '')))
        if len(prob_cand_arr) != check_label_len:
            raise Exception('label len check invalid!', len(prob_cand_arr))
        data[i]['pred'] = float(validate_html[-2].replace('[', '').replace(']', '').replace("'", ''))
        data[i]['previous_prob_cand_arr'] = []
        data[i]['previous_prob_cand_arr_direct'] = []
        data[i]['previous_date'] = []
        data[i]['previous_truth_arr'] = previous_truth_arr
        data[i]['previous_pred_arr'] = previous_pred_arr
        data[i]['previous_truth_gap_arr'] = previous_truth_gap_arr
        data[i]['prob_cand_gap_arr'] = prob_cand_gap_arr
        for v in prob_cand_arr:
            prob_cand_gap_arr.append(v - data[i]['pred'])
        ### backtrace previous pred ###
        if date_list is not None:
            idx = date_list.index(metric_folder)
            for dt in date_list[:idx-1][::-1][::2][:7]:
                direct, accum = loadProbCand(name, label_dim, int(data[i]['data_len']), [int(data[i]['data_len'])], int(data[i]['avg_window']), dt, label_list)
                data[i]['previous_prob_cand_arr'].append(accum)
                data[i]['previous_prob_cand_arr_direct'].append(direct)
                data[i]['previous_date'].append(dt)
            if debug:
                print(metric_folder, label_dim, int(data[i]['data_len']), int(data[i]['avg_window']))
                for j in range(7):
                    print(data[i]['previous_truth_arr'][j], data[i]['previous_date'][j], data[i]['previous_prob_cand_arr'][j])
                exit(0)
        ### backtrace previous pred ###
        data[i]['std'] = np.std(prob_cand_arr)
        data[i]['prob_cand_arr'] = prob_cand_arr
        data[i]['prob_cand_direct_arr'] = prob_cand_direct_arr
        data[i]['best'] = data[i]['left_01'] + data[i]['right_01'] + data[i]['left_02'] + data[i]['right_02']
        data[i]['prod_cand_gap_stat'] = stat_gap(prob_cand_gap_arr)
        data[i]['prob_cand_gap_stat_norm'] = stat_gap_norm(prob_cand_gap_arr)
        data[i]['previous_truth_gap_stat'] = stat_gap(previous_truth_gap_arr)
    if not acc:
        data = sorted(data, key=lambda k : k['std'], reverse=True)
    else:
        data = sorted(data, key=lambda k : k['best'], reverse=True)
    return ','.join([str(v['data_len']) for v in data[:10]]), data


def minmax(arr):
    mx = max(arr)
    mi = min(arr)
    result = []
    for v in arr:
        result.append((v - mi) / (mx - mi))
    return result

def get_cand(data):
    return float(data.split(', ')[2].replace('[', '').replace(']', '').replace('"', '').replace("'", ''))

def get_history_prob(data):
    return float(data.split(', ')[1].replace('[', '').replace(']', '').replace('"', '').replace("'", ''))

def get_history_count(fn, range_arr, dt, label_dim):
    stat = {i : {data_len : 0.0 for data_len in range_arr} for i in range(15)}
    arr = []
    with open(fn, 'r') as f:
        for line in f:
            raw = line.replace('\n', '').split(' ')
            if raw[0].replace('-', '') < dt or dt is None or dt == 'latest':
                arr.append([int(v) for v in raw[1:]])
    arr = arr[0::2] if len(arr) % 2 == 0 else arr[1::2]
    for data_len in range_arr:
        for label in arr[-data_len:]:
            stat[label[label_dim]][data_len] += 1.0
    for data_len in range_arr:
        current = []
        for i in range(10 if label_dim < 6 else 15):
            current.append(stat[i][data_len] / float(data_len))
        current = minmax(current)
        for i in range(10 if label_dim < 6 else 15):
            stat[i][data_len] = current[i]
    return stat

def get_corr_diff(arr):
    result = []
    for i in range(1, len(arr)):
        result.append(abs(np.corrcoef(arr[i - 1], arr[i])[0][1]))
    return result

def color_format(label, after, hit_label):
    s = label + ":" + after
    return "\033[31m" + s + "\033[0m" if label == hit_label else s

def investigate(name, label_dim, hold, metric_folder):
    l_len = 10 if label_dim < 6 else 15
    hit_label = None
    with open(name + '_raw_txt', 'r') as f:
        for line in f:
            if len(line) > 5:
                line = line.replace('\n', '').split(' ')
                if metric_folder == line[0].replace('-', ''):
                    hit_label = line[label_dim + 1]
                    break
    data = load_obj(name + '/' + metric_folder + '/detail_' + str(label_dim))
    see = [{'diff_arr' : [], 'label' : i, 'acc' : 0, 'his_prob' : [], 'std' : 0.0, 'q' : 0.0, 'mean' : 0.0} for i in range(10)] if label_dim < 6 else [{'diff_arr' : [], 'label' : i, 'acc' : 0, 'his_prob' : [], 'std' : 0.0, 'q' : 0.0, 'mean' : 0.0} for i in range(15)]
    data_len_arr = []
    cand_corr_diff = []
    q = 0.0
    stat = get_history_count(name + '_raw_txt', [v['data_len'] for v in data], metric_folder, label_dim)
    for v in data:
        if v['data_len'] < 100000:
            q += (v['left_01'] + v['right_01'] + v['left_02'] + v['right_02'])
            cand_corr_diff.append([float(w.split('----')[1].split(' ')[0].replace('[', '').replace(']', '').replace("'", '').replace('"', '')) for w in v['validate_html'].split('<br\\>')[-17:-3]])
            data_len_arr.append(v['data_len'])
            cand = [get_cand(vv) for vv in v['prob_cand_html'].split('<br\\>')[:-1]]
            his_prob = [get_history_prob(vv) for vv in v['prob_cand_html'].split('<br\\>')[:-1]]
            #his_prob = [stat[i][v['data_len']] for i in range(l_len)]
            prob = float(v['validate_html'].split('<br\\>')[-2].replace('[', '').replace(']', '').replace('"', '').replace("'", ''))
            last = float(v['validate_html'].split('<br\\>')[-3].split(' ')[-1].replace('[', '').replace(']', '').replace('"', '').replace("'", ''))
            for l in range(l_len):
                if abs(cand[l] - prob) <= 0.015:
                    see[l]['acc'] += 1
                see[l]['diff_arr'].append(abs(cand[l] - last))
                see[l]['his_prob'].append(his_prob[l])
    cand_corr_diff = get_corr_diff(cand_corr_diff)
    for v in see:
        #v['his_prob_corr'] = abs(np.corrcoef(v['his_prob'], data_len_arr)[0][1]) if len(data_len_arr) > 1 else 0
        #v['prob_aggr'] = v['prob_aggr'] / (float(len(data_len_arr)) if len(data_len_arr) > 0 else 1.0)
        #v['prob_aggr'] = np.median(v['his_prob']) if len(v['his_prob']) > 0 else 0.0
        #v['prob_aggr'] = (min(v['his_prob']) + max(v['his_prob'])) / 2 if len(v['his_prob']) > 0 else 0.0
        v['std'] = np.std(v['his_prob']) if len(v['his_prob']) > 0 else 0.0
        v['mean'] = np.mean(v['his_prob']) if len(v['his_prob']) > 0 else 0.0
        #v['diff_corr'] = abs(np.corrcoef(minmax(v['diff_arr']), minmax(data_len_arr))[0][1]) if len(data_len_arr) > 1 else 0
        #v['cand_corr_diff'] = abs(np.corrcoef([abs(w) for w in np.diff(v['diff_arr'])], cand_corr_diff)[0][1])
    result = ''
    for v in sorted(see, key=lambda x : -x['acc']):
        result += color_format(str(v['label']), str(v['std'])[:4] + "," + str(v['mean'])[:4], hit_label) + '  '
    print(result)


