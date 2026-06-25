from rule_kit import *


def stat_strategy(tmp, stat, true_label, tmp_name):
    if tmp_name not in stat:
        stat[tmp_name] = {}
    for pos in range(len(tmp)):
        if int(tmp[pos]) == int(true_label):
            val = round(float(pos + 1) / float(len(tmp)) * 10) / 10
            if val in stat[tmp_name]:
                stat[tmp_name][val] += 1
            else:
                stat[tmp_name][val] = 1
            break

def stat_strategy_process(big_tmp, small_tmp, big_near_tmp, small_near_tmp, stat, true_label, strategy, current_strategy):
    if strategy == current_strategy:
        stat_strategy(big_tmp, stat, true_label, 'big_tmp')
        stat_strategy(small_tmp, stat, true_label, 'small_tmp')
        stat_strategy(big_near_tmp, stat, true_label, 'big_near_tmp')
        stat_strategy(small_near_tmp, stat, true_label, 'small_near_tmp')

def add_arr(strategy_name, big_tmp, small_tmp, big_near_tmp, small_near_tmp, arr, sorted_stat):
    if sorted_stat:
        for tmp_name in sorted_stat[strategy_name]:
            current_tmp = eval(tmp_name)
            for pos in range(len(current_tmp)):
                val = float(pos + 1) / float(len(current_tmp))
                for cand in sorted_stat[strategy_name][tmp_name]:
                    if val >= cand[0] - 0.5 and val < cand[0] + 0.5:
                        arr.add(current_tmp[pos])

def process(count, maxConsecutiveCount, seq, gapStat, prob_cand_arr, pred, data_len, good_count, true_label, stat, strategy=None, sorted_stat=None):
    arr = set()
    big_tmp = pattern_sort(prob_cand_arr, pred, seq['big'], False, 0)
    small_tmp = pattern_sort(prob_cand_arr, pred, seq['small'], False, 0)
    big_near_tmp = pattern_sort(prob_cand_arr, pred, seq['bigNear'], False, 0)
    small_near_tmp = pattern_sort(prob_cand_arr, pred, seq['smallNear'], False, 0)
    #大部分大
    if count['big'] >= 7:
        stat_strategy_process(big_tmp, small_tmp, big_near_tmp, small_near_tmp, stat, true_label, strategy, '大的全都要')
        add_arr('大的全都要', big_tmp, small_tmp, big_near_tmp, small_near_tmp, arr, sorted_stat)
        if strategy is None:
            print('大的全都要')
    #参差不齐接近
    elif count['near'] >= 5 and maxConsecutiveCount['near'] < 4:
        if len(seq['small']) + len(seq['smallNear']) >= 7:
            stat_strategy_process(big_tmp, small_tmp, big_near_tmp, small_near_tmp, stat, true_label, strategy, '参差不齐接近时小的偏多')
            add_arr('参差不齐接近时小的偏多', big_tmp, small_tmp, big_near_tmp, small_near_tmp, arr, sorted_stat)
            if strategy is None:
                print('参差不齐接近时小的偏多')
        elif len(seq['big']) + len(seq['bigNear']) >= 7:
            stat_strategy_process(big_tmp, small_tmp, big_near_tmp, small_near_tmp, stat, true_label, strategy, '参差不齐接近时大的偏多')
            add_arr('参差不齐接近时大的偏多', big_tmp, small_tmp, big_near_tmp, small_near_tmp, arr, sorted_stat)
            if strategy is None:
                print('参差不齐接近时大的偏多')
        elif len(seq['small']) + len(seq['smallNear']) > len(seq['big']) + len(seq['bigNear']):
            stat_strategy_process(big_tmp, small_tmp, big_near_tmp, small_near_tmp, stat, true_label, strategy, '参差不齐接近时小的比大的多一些')
            add_arr('参差不齐接近时小的比大的多一些', big_tmp, small_tmp, big_near_tmp, small_near_tmp, arr, sorted_stat)
            if strategy is None:
                print('参差不齐接近时小的比大的多一些')
        elif len(seq['small']) + len(seq['smallNear']) < len(seq['big']) + len(seq['bigNear']):
            stat_strategy_process(big_tmp, small_tmp, big_near_tmp, small_near_tmp, stat, true_label, strategy, '参差不齐接近时大的多一些')
            add_arr('参差不齐接近时大的多一些', big_tmp, small_tmp, big_near_tmp, small_near_tmp, arr, sorted_stat)
            if strategy is None:
                print('参差不齐接近时大的多一些')
        else:
            stat_strategy_process(big_tmp, small_tmp, big_near_tmp, small_near_tmp, stat, true_label, strategy, '参差不齐接近时大小一样')
            add_arr('参差不齐接近时大小一样', big_tmp, small_tmp, big_near_tmp, small_near_tmp, arr, sorted_stat)
            if strategy is None:
                print('参差不齐接近时大小一样')
    #连续接近
    elif count['near'] >= 5 and maxConsecutiveCount['near'] >= 4:
        if len(seq['small']) + len(seq['smallNear']) >= 7:
            stat_strategy_process(big_tmp, small_tmp, big_near_tmp, small_near_tmp, stat, true_label, strategy, '连续接近时小的偏多')
            add_arr('连续接近时小的偏多', big_tmp, small_tmp, big_near_tmp, small_near_tmp, arr, sorted_stat)
            if strategy is None:
                print('连续接近时小的偏多')
        elif len(seq['big']) + len(seq['bigNear']) >= 7:
            stat_strategy_process(big_tmp, small_tmp, big_near_tmp, small_near_tmp, stat, true_label, strategy, '连续接近时大的偏多')
            add_arr('连续接近时大的偏多', big_tmp, small_tmp, big_near_tmp, small_near_tmp, arr, sorted_stat)
            if strategy is None:
                print('连续接近时大的偏多')
        elif len(seq['small']) + len(seq['smallNear']) > len(seq['big']) + len(seq['bigNear']):
            stat_strategy_process(big_tmp, small_tmp, big_near_tmp, small_near_tmp, stat, true_label, strategy, '连续接近时小的比大的多一些')
            add_arr('连续接近时小的比大的多一些', big_tmp, small_tmp, big_near_tmp, small_near_tmp, arr, sorted_stat)
            if strategy is None:
                print('连续接近时小的比大的多一些')
        elif len(seq['small']) + len(seq['smallNear']) < len(seq['big']) + len(seq['bigNear']):
            stat_strategy_process(big_tmp, small_tmp, big_near_tmp, small_near_tmp, stat, true_label, strategy, '连续接近时大的多一些')
            add_arr('连续接近时大的多一些', big_tmp, small_tmp, big_near_tmp, small_near_tmp, arr, sorted_stat)
            if strategy is None:
                print('连续接近时大的多一些')
        else:
            stat_strategy_process(big_tmp, small_tmp, big_near_tmp, small_near_tmp, stat, true_label, strategy, '连续接近时大小一样')
            add_arr('连续接近时大小一样', big_tmp, small_tmp, big_near_tmp, small_near_tmp, arr, sorted_stat)
            if strategy is None:
                print('连续接近时大小一样')
    #参差不齐小
    elif count['small'] >= 5 and maxConsecutiveCount['small'] < 4:
        stat_strategy_process(big_tmp, small_tmp, big_near_tmp, small_near_tmp, stat, true_label, strategy, '参差不齐小')
        add_arr('参差不齐小', big_tmp, small_tmp, big_near_tmp, small_near_tmp, arr, sorted_stat)
        if strategy is None:
            print('参差不齐小')
    #不是大的就是接近的(大的偏多)
    elif count['big'] >= 5 and count['near'] >= 2:
        stat_strategy_process(big_tmp, small_tmp, big_near_tmp, small_near_tmp, stat, true_label, strategy, '不是大的就是接近的(大的偏多)')
        add_arr('不是大的就是接近的(大的偏多)', big_tmp, small_tmp, big_near_tmp, small_near_tmp, arr, sorted_stat)
        if strategy is None:
            print('不是大的就是接近的(大的偏多)')
    #不是大的就是小的(大的偏多)
    elif count['big'] >= 5 and count['small'] >= 2:
        stat_strategy_process(big_tmp, small_tmp, big_near_tmp, small_near_tmp, stat, true_label, strategy, '不是大的就是小的(大的偏多)')
        add_arr('不是大的就是小的(大的偏多)', big_tmp, small_tmp, big_near_tmp, small_near_tmp, arr, sorted_stat)
        if strategy is None:
            print('不是大的就是小的(大的偏多)')
    #大:接近:小很均衡
    elif count['big'] <= 4 and count['near'] <= 4 and count['small'] <= 4:
        if len(seq['small']) + len(seq['smallNear']) > len(seq['big']) + len(seq['bigNear']):
            stat_strategy_process(big_tmp, small_tmp, big_near_tmp, small_near_tmp, stat, true_label, strategy, '很均衡时小的偏多')
            add_arr('很均衡时小的偏多', big_tmp, small_tmp, big_near_tmp, small_near_tmp, arr, sorted_stat)
            if strategy is None:
                print('很均衡时小的偏多')
        elif len(seq['small']) + len(seq['smallNear']) < len(seq['big']) + len(seq['bigNear']):
            stat_strategy_process(big_tmp, small_tmp, big_near_tmp, small_near_tmp, stat, true_label, strategy, '很均衡时大的偏多')
            add_arr('很均衡时大的偏多', big_tmp, small_tmp, big_near_tmp, small_near_tmp, arr, sorted_stat)
            if strategy is None:
                print('很均衡时大的偏多')
        else:
            stat_strategy_process(big_tmp, small_tmp, big_near_tmp, small_near_tmp, stat, true_label, strategy, '非常均衡')
            add_arr('非常均衡', big_tmp, small_tmp, big_near_tmp, small_near_tmp, arr, sorted_stat)
            if strategy is None:
                print('非常均衡')
    #大部分小
    elif count['small'] >= 7:
        stat_strategy_process(big_tmp, small_tmp, big_near_tmp, small_near_tmp, stat, true_label, strategy, '大部分小')
        add_arr('大部分小', big_tmp, small_tmp, big_near_tmp, small_near_tmp, arr, sorted_stat)
        if strategy is None:
            print('大部分小')
    #连续小
    elif count['small'] >= 5 and maxConsecutiveCount['small'] >= 4:
        stat_strategy_process(big_tmp, small_tmp, big_near_tmp, small_near_tmp, stat, true_label, strategy, '连续小')
        add_arr('连续小', big_tmp, small_tmp, big_near_tmp, small_near_tmp, arr, sorted_stat)
        if strategy is None:
            print('连续小')
    else:
        stat_strategy_process(big_tmp, small_tmp, big_near_tmp, small_near_tmp, stat, true_label, strategy, '不对呀')
        if strategy is None:
            print('不对呀', data_len)
    if strategy is None:
        print(arr, data_len)
        print(count, seq, gapStat, maxConsecutiveCount)
    return arr
