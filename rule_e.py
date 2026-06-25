from rule_kit import *
import os

def process(count, maxConsecutiveCount, seq, nearGapStat, gapStat, prob_cand_arr, pred, avg_window, data_len, good_count, range_stat, name, label, label_dim, config, config_copy):
    big_tmp = pattern_sort(prob_cand_arr, pred, seq['big'], False, 0)
    big_gap_tmp = [prob_cand_arr[v] - pred for v in big_tmp]
    small_tmp = pattern_sort(prob_cand_arr, pred, seq['small'], False, 0)
    small_gap_tmp = [prob_cand_arr[v] - pred for v in small_tmp]
    big_near_tmp = pattern_sort(prob_cand_arr, pred, seq['bigNear'], False, 0)
    big_near_gap_tmp = [prob_cand_arr[v] - pred for v in big_near_tmp]
    small_near_tmp = pattern_sort(prob_cand_arr, pred, seq['smallNear'], False, 0)
    small_near_gap_tmp = [prob_cand_arr[v] - pred for v in small_near_tmp]
    arr = set()
    arr_copy = set()
    strategy_name = None
    strategy_print = None
    if count['big'] >= 7 * (1.0 if label_dim < 6 else 1.5):
        strategy_name = '大的全都要'
        strategy_print = strategy_name
        print('大的全都要')
    elif count['near'] >= 5 * (1.0 if label_dim < 6 else 1.5) and maxConsecutiveCount['near'] < 4 * (1.0 if label_dim < 6 else 1.5):
        if len(seq['small']) + len(seq['smallNear']) >= 7 * (1.0 if label_dim < 6 else 1.5):
            strategy_name = '参差不齐接近时小的偏多'
            strategy_print = strategy_name + extraSmall(seq, 1.0 if label_dim < 6 else 1.5)
        elif len(seq['big']) + len(seq['bigNear']) >= 7 * (1.0 if label_dim < 6 else 1.5):
            strategy_name = '参差不齐接近时大的偏多'
            strategy_print = strategy_name + extraBig(seq, 1.0 if label_dim < 6 else 1.5)
        elif len(seq['small']) + len(seq['smallNear']) > len(seq['big']) + len(seq['bigNear']):
            strategy_name = '参差不齐接近时小的比大的多一些'
            strategy_print = strategy_name + extraSmall(seq, 1.0 if label_dim < 6 else 1.5)
        elif len(seq['small']) + len(seq['smallNear']) < len(seq['big']) + len(seq['bigNear']):
            strategy_name = '参差不齐接近时大的比小的多一些'
            strategy_print = strategy_name + extraBig(seq, 1.0 if label_dim < 6 else 1.5)
        else:
            strategy_name = '参差不齐接近时大小一样'
            strategy_print = strategy_name
    elif count['near'] >= 5 * (1.0 if label_dim < 6 else 1.5) and maxConsecutiveCount['near'] >= 4 * (1.0 if label_dim < 6 else 1.5):
        if len(seq['small']) + len(seq['smallNear']) >= 7 * (1.0 if label_dim < 6 else 1.5):
            strategy_name = '连续接近时小的偏多'
            strategy_print = strategy_name + extraSmall(seq, 1.0 if label_dim < 6 else 1.5)
        elif len(seq['big']) + len(seq['bigNear']) >= 7 * (1.0 if label_dim < 6 else 1.5):
            strategy_name = '连续接近时大的偏多'
            strategy_print = strategy_name + extraBig(seq, 1.0 if label_dim < 6 else 1.5)
        elif len(seq['small']) + len(seq['smallNear']) > len(seq['big']) + len(seq['bigNear']):
            strategy_name = '连续接近时小的比大的多一些'
            strategy_print = strategy_name + extraSmall(seq, 1.0 if label_dim < 6 else 1.5)
        elif len(seq['small']) + len(seq['smallNear']) < len(seq['big']) + len(seq['bigNear']):
            strategy_name = '连续接近时大的比小的多一些'
            strategy_print = strategy_name + extraBig(seq, 1.0 if label_dim < 6 else 1.5)
        else:
            strategy_name = '连续接近时大小一样'
            strategy_print = strategy_name
    elif count['small'] >= 5 * (1.0 if label_dim < 6 else 1.5) and maxConsecutiveCount['small'] < 4 * (1.0 if label_dim < 6 else 1.5):
        strategy_name = '参差不齐小'
        strategy_print = strategy_name + restExcSmall(seq, 1.0 if label_dim < 6 else 1.5)
    elif count['big'] >= 5 * (1.0 if label_dim < 6 else 1.5) and count['near'] >= 2 * (1.0 if label_dim < 6 else 1.5):
        flag = ':参差' if maxConsecutiveCount['big'] < 4 else ':连续'
        strategy_name = '不是大的就是接近的(大的偏多)'
        strategy_print = strategy_name + flag + restExcBig(seq, 1.0 if label_dim < 6 else 1.5)
    elif count['big'] >= 5 * (1.0 if label_dim < 6 else 1.5) and count['small'] >= 2 * (1.0 if label_dim < 6 else 1.5):
        flag = ':参差' if maxConsecutiveCount['big'] < 4 * (1.0 if label_dim < 6 else 1.5) else ':连续'
        strategy_name = '不是大的就是小的(大的偏多)'
        strategy_print = strategy_name + flag + restExcBig(seq, 1.0 if label_dim < 6 else 1.5)
    elif count['big'] <= 4 * (1.0 if label_dim < 6 else 1.5) and count['near'] <= 4 * (1.0 if label_dim < 6 else 1.5) and count['small'] <= 4 * (1.0 if label_dim < 6 else 1.5):
        if len(seq['small']) + len(seq['smallNear']) > len(seq['big']) + len(seq['bigNear']):
            strategy_name = '很均衡时小的偏多'
            strategy_print = strategy_name + extraSmall(seq, 1.0 if label_dim < 6 else 1.5)
        elif len(seq['small']) + len(seq['smallNear']) < len(seq['big']) + len(seq['bigNear']):
            strategy_name = '很均衡时大的偏多'
            strategy_print = strategy_name + extraBig(seq, 1.0 if label_dim < 6 else 1.5)
        else:
            strategy_name = '非常均衡'
            strategy_print = strategy_name
    elif count['small'] >= 7 * (1.0 if label_dim < 6 else 1.5):
        strategy_name = '大部分小'
        strategy_print = strategy_name
    elif count['small'] >= 5 * (1.0 if label_dim < 6 else 1.5) and maxConsecutiveCount['small'] >= 4 * (1.0 if label_dim < 6 else 1.5):
        strategy_name = '连续小'
        strategy_print = strategy_name + restExcSmall(seq, 1.0 if label_dim < 6 else 1.5)
    else:
        strategy_name = '不对呀'
        strategy_print = strategy_name
    update = False
    if train_and_predict(config,
            config_copy,
            strategy_name, 
            big_tmp, 
            big_gap_tmp, 
            small_tmp, 
            small_gap_tmp, 
            big_near_tmp, 
            big_near_gap_tmp, 
            small_near_tmp, 
            small_near_gap_tmp,
            gapStat,
            nearGapStat,
            arr,
            arr_copy,
            name,
            label,
            label_dim):
        update = True
        print('需要更新')
    print(strategy_print)
    print(data_len, good_count, arr_copy, arr)
    del(seq['near'])
    show(gapStat, avg_window, data_len, range_stat, prob_cand_arr, pred, seq)
    print("\n")
    return arr, arr_copy, update