from rule_kit import *

def process(count, maxConsecutiveCount, seq, nearGapStat, gapStat, prob_cand_arr, pred, avg_window, data_len, good_count, strategy_name, range_stat):
    big_tmp = pattern_sort(prob_cand_arr, pred, seq['big'], False, 0)
    big_gap_tmp = [prob_cand_arr[v] - pred for v in big_tmp]
    small_tmp = pattern_sort(prob_cand_arr, pred, seq['small'], False, 0)
    small_gap_tmp = [prob_cand_arr[v] - pred for v in small_tmp]
    big_near_tmp = pattern_sort(prob_cand_arr, pred, seq['bigNear'], False, 0)
    big_near_gap_tmp = [prob_cand_arr[v] - pred for v in big_near_tmp]
    small_near_tmp = pattern_sort(prob_cand_arr, pred, seq['smallNear'], False, 0)
    small_near_gap_tmp = [prob_cand_arr[v] - pred for v in small_near_tmp]
    arr = set()
    #大部分大
    if count['big'] >= 7:
        print('大的全都要')
    #参差不齐接近
    elif count['near'] >= 5 and maxConsecutiveCount['near'] < 4:
        if len(seq['small']) + len(seq['smallNear']) >= 7:
            print('参差不齐接近时小的偏多' + extraSmall(seq))
        elif len(seq['big']) + len(seq['bigNear']) >= 7:
            print('参差不齐接近时大的偏多' + extraBig(seq))
        elif len(seq['small']) + len(seq['smallNear']) > len(seq['big']) + len(seq['bigNear']):
            print('参差不齐接近时小的比大的多一些' + extraSmall(seq))
        elif len(seq['small']) + len(seq['smallNear']) < len(seq['big']) + len(seq['bigNear']):
            print('参差不齐接近时大的比小的多一些' + extraBig(seq))
        else:
            print('参差不齐接近时大小一样')
    #连续接近
    elif count['near'] >= 5 and maxConsecutiveCount['near'] >= 4:
        if len(seq['small']) + len(seq['smallNear']) >= 7:
            print('连续接近时小的偏多' + extraSmall(seq))
        elif len(seq['big']) + len(seq['bigNear']) >= 7:
            print('连续接近时大的偏多' + extraBig(seq))
        elif len(seq['small']) + len(seq['smallNear']) > len(seq['big']) + len(seq['bigNear']):
            print('连续接近时小的比大的多一些' + extraSmall(seq))
        elif len(seq['small']) + len(seq['smallNear']) < len(seq['big']) + len(seq['bigNear']):
            print('连续接近时大的比小的多一些' + extraBig(seq))
        else:
            print('连续接近时大小一样')
    elif count['small'] >= 5 and maxConsecutiveCount['small'] < 4:
        print('参差不齐小' + restExcSmall(seq))
    #不是大的就是接近的(大的偏多)
    elif count['big'] >= 5 and count['near'] >= 2:
        flag = ':参差' if maxConsecutiveCount['big'] < 4 else ':连续'
        print('不是大的就是接近的(大的偏多)' + flag + restExcBig(seq))
    #不是大的就是小的(大的偏多)
    elif count['big'] >= 5 and count['small'] >= 2:
        flag = ':参差' if maxConsecutiveCount['big'] < 4 else ':连续'
        print('不是大的就是小的(大的偏多)' + flag + restExcBig(seq))
    #大:接近:小很均衡
    elif count['big'] <= 4 and count['near'] <= 4 and count['small'] <= 4:
        if len(seq['small']) + len(seq['smallNear']) > len(seq['big']) + len(seq['bigNear']):
            print('很均衡时小的偏多' + extraSmall(seq))
        elif len(seq['small']) + len(seq['smallNear']) < len(seq['big']) + len(seq['bigNear']):
            print('很均衡时大的偏多' + extraBig(seq))
        else:
            print('非常均衡')
    elif count['small'] >= 7:
        print('大部分小')
    elif count['small'] >= 5 and maxConsecutiveCount['small'] >= 4:
        print('连续小' + restExcSmall(seq))
    else:
        print('不对呀', data_len)
    print(data_len, good_count, arr)
    del(seq['near'])
    show(gapStat, avg_window, data_len, range_stat, prob_cand_arr, pred, seq)
    return arr
