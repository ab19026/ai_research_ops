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
        if midJudge(big_tmp, gapStat, 0.05, False):
            pos = len(big_tmp) - gapStat[0.05]
            gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos, left=False)
        if midJudge(big_tmp, gapStat, 0.02, True):
            pos = len(big_tmp) - gapStat[0.02] - 1
            gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos, left=True)
            if big_gap_tmp[pos] > 0.0185:
                if pos - 1 > -1:
                    arr.add(big_tmp[pos - 1])
            findTurn(arr, big_tmp, big_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=False, choose_single=True)
            findTurn(arr, big_tmp, big_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=True, choose_single=False)
        if len(big_near_tmp) >= len(small_tmp) and len(big_near_tmp) >= len(small_near_tmp):
            if len(big_near_tmp) == 1:
                arr.add(big_near_tmp[0])
        print('大的全都要')
    #参差不齐接近
    elif count['near'] >= 5 and maxConsecutiveCount['near'] < 4:
        if len(seq['small']) + len(seq['smallNear']) >= 7:
            if len(small_near_tmp) >= len(big_near_tmp) and len(small_near_tmp) >= len(big_tmp):
                if midJudge(small_near_tmp, nearGapStat, -0.01, False):
                    if small_near_gap_tmp[-1] > -0.0009:
                        arr.add(small_near_tmp[-1])
            if len(small_tmp) >= len(big_tmp) and len(small_tmp) >= len(big_near_tmp):
                if midJudge(small_tmp, gapStat, -0.03, True):
                    pos = gapStat[-0.03]
                    gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos, left=False)
            if len(big_near_tmp) - len(small_near_tmp) >= -1 or len(big_near_tmp) - len(small_tmp) >= -1:
                if len(big_near_tmp) == 2:
                    if nearGapStat[0.01] == 0:
                        if big_near_gap_tmp[0] < 0.0023 and big_near_gap_tmp[1] > 0.0039:
                            arr.add(big_near_tmp[1])
                        if big_near_gap_tmp[0] < 0.0031 and big_near_gap_tmp[1] > 0.0055:
                            arr.add(big_near_tmp[0])
            print('参差不齐接近时小的偏多')
        elif len(seq['big']) + len(seq['bigNear']) >= 7:
            if len(big_near_tmp) >= len(small_tmp) and len(big_near_tmp) >= len(small_near_tmp):
                if midJudge(big_near_tmp, nearGapStat, 0.01, True):
                    pos = len(big_near_tmp) - nearGapStat[0.01] - 1
                    gapAndConsecutive(arr, big_near_tmp, big_near_gap_tmp, pos, left=True)
                    findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=True, consecutive_at_left=True, choose_single=False)
            print('参差不齐接近时大的偏多')
        elif len(seq['small']) + len(seq['smallNear']) > len(seq['big']) + len(seq['bigNear']):
            if len(big_near_tmp) - len(small_near_tmp) >= -1 and len(big_near_tmp) - len(small_tmp) >= -1:
                if midJudge(big_near_tmp, nearGapStat, 0.01, False):
                    pos = len(big_near_tmp) - nearGapStat[0.01]
                    gapAndConsecutive(arr, big_near_tmp, big_near_gap_tmp, pos, left=False)
            if len(small_near_tmp) - len(big_tmp) >= -1 and len(small_near_tmp) - len(big_near_tmp) >= -1:
                if nearGapStat[-0.01] == 0:
                    findTurn(arr, small_near_tmp, small_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=True, choose_single=False)
                if len(small_near_tmp) == 2:
                    if nearGapStat[-0.01] == 1:
                        arr.add(small_near_tmp[1])
            if len(small_tmp) >= len(big_tmp) and len(small_tmp) >= len(big_near_tmp):
                if midJudge(small_tmp, gapStat, -0.03, False):
                    pos = gapStat[-0.03]
                    if small_gap_tmp[pos] < -0.029:
                        if pos + 1 < len(small_tmp):
                            arr.add(small_tmp[pos + 1])
                    findTurn(arr, small_tmp, small_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=True, consecutive_at_left=False, choose_single=False)
            print('参差不齐接近时小的比大的多一些')
        elif len(seq['small']) + len(seq['smallNear']) < len(seq['big']) + len(seq['bigNear']):
            if len(big_near_tmp) >= len(small_tmp) and len(big_near_tmp) >= len(small_near_tmp):
                if midJudge(big_near_tmp, nearGapStat, 0.01, False):
                    pos = len(big_near_tmp) - nearGapStat[0.01] - 1
                    if big_near_gap_tmp[pos] > 0.0081:
                        if pos - 1 > -1:
                            arr.add(big_near_tmp[pos - 1])
            print('参差不齐接近时大的多一些')
        else:
            if len(big_near_tmp) >= len(small_tmp) and len(big_near_tmp) >= len(small_near_tmp):
                if midJudge(big_near_tmp, nearGapStat, 0.01, False):
                    pos = len(big_near_tmp) - nearGapStat[0.01] - 1
                    if big_near_gap_tmp[pos] > 0.009:
                        if pos - 1 > -1:
                            arr.add(big_near_tmp[pos - 1])
                    gapAndConsecutive(arr, big_near_tmp, big_near_gap_tmp, pos + 1, left=False)
            print('参差不齐接近时大小一样')
    #连续接近
    elif count['near'] >= 5 and maxConsecutiveCount['near'] >= 4:
        if len(seq['small']) + len(seq['smallNear']) >= 7:
            print('连续接近时小的偏多')
        elif len(seq['big']) + len(seq['bigNear']) >= 7:
            if len(big_near_tmp) >= len(small_tmp) and len(big_near_tmp) >= len(small_near_tmp):
                if midJudge(big_near_tmp, nearGapStat, 0.01, True):
                    pos = len(big_near_tmp) - nearGapStat[0.01]
                    gapAndConsecutive(arr, big_near_tmp, big_near_gap_tmp, pos, left=False)
            print('连续接近时大的偏多')
        elif len(seq['small']) + len(seq['smallNear']) > len(seq['big']) + len(seq['bigNear']):
            print('连续接近时小的比大的多一些')
        elif len(seq['small']) + len(seq['smallNear']) < len(seq['big']) + len(seq['bigNear']):
            if len(small_near_tmp) >= len(big_tmp):
                if midJudge(small_near_tmp, nearGapStat, -0.01, True):
                    pos = nearGapStat[-0.01]
                    gapAndConsecutive(arr, small_near_tmp, small_near_gap_tmp, pos, left=False)
            print('连续接近时大的比小的多一些')
        else:
            print('连续接近时大小一样')
    #参差不齐小
    elif count['small'] >= 5 and maxConsecutiveCount['small'] < 4:
        if len(small_near_tmp) >= len(big_tmp):
            if len(small_near_tmp) == 1:
                arr.add(small_near_tmp[0])
        if len(big_near_tmp) >= len(small_near_tmp):
            if midJudge(big_near_tmp, nearGapStat, 0.01, False):
                pos = len(big_near_tmp) - nearGapStat[0.01]
                gapAndConsecutive(arr, big_near_tmp, big_near_gap_tmp, pos, left=False)
            if len(big_near_tmp) == 2:
                if big_near_gap_tmp[1] > 0.009:
                    arr.add(big_near_tmp[1])
        print('参差不齐小')
    #不是大的就是接近的(大的偏多)
    elif count['big'] >= 5 and count['near'] >= 2:
        if midJudge(big_tmp, gapStat, 0.03, True):
            pos = len(big_tmp) - gapStat[0.03]
            gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos, left=False)
        if midJudge(big_tmp, gapStat, 0.02, True):
            pos = len(big_tmp) - gapStat[0.02] - 1
            gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos, left=True)
            if big_gap_tmp[pos] > 0.0178:
                if pos - 1 > -1:
                    arr.add(big_tmp[pos - 1])
        if len(big_near_tmp) >= len(small_tmp) and len(big_near_tmp) >= len(small_near_tmp):
            if midJudge(big_near_tmp, nearGapStat, 0.01, True):
                pos = len(big_near_tmp) - nearGapStat[0.01]
                gapAndConsecutive(arr, big_near_tmp, big_near_gap_tmp, pos, left=False)
        print('不是大的就是接近的(大的偏多)')
    #不是大的就是小的(大的偏多)
    elif count['big'] >= 5 and count['small'] >= 2:
        print('不是大的就是小的(大的偏多)')
    #大:接近:小很均衡
    elif count['big'] <= 4 and count['near'] <= 4 and count['small'] <= 4:
        if len(seq['small']) + len(seq['smallNear']) > len(seq['big']) + len(seq['bigNear']):
            if len(small_near_tmp) - len(big_tmp) >= -1 and len(small_near_tmp) - len(big_near_tmp) >= -1:
                if small_near_gap_tmp[0] == small_near_gap_tmp[-1]:
                    for v in small_near_tmp:
                        arr.add(v)
                if len(small_near_tmp) == 2:
                    if nearGapStat[-0.01] == 1:
                        arr.add(small_near_tmp[1])
                    if small_near_gap_tmp[0] < -0.0039 and small_near_gap_tmp[1] > -0.0022:
                        arr.add(small_near_tmp[1])
            if len(big_tmp) >= len(small_near_tmp):
                if len(big_tmp) == 2:
                    if gapStat[0.02] == 1:
                        arr.add(big_tmp[0])
            print('很均衡时小的偏多')
        elif len(seq['small']) + len(seq['smallNear']) < len(seq['big']) + len(seq['bigNear']):
            if len(big_near_tmp) >= len(small_tmp) and len(big_near_tmp) >= len(small_near_tmp):
                if midJudge(big_near_tmp, nearGapStat, 0.01, False):
                    pos = len(big_near_tmp) - nearGapStat[0.01] - 1
                    gapAndConsecutive(arr, big_near_tmp, big_near_gap_tmp, pos, left=True)
                    gapAndConsecutive(arr, big_near_tmp, big_near_gap_tmp, pos + 1, left=False)
            if len(big_tmp) >= len(small_tmp) and len(big_tmp) >= len(small_near_tmp):
                if midJudge(big_tmp, gapStat, 0.04, False):
                    pos = len(big_tmp) - gapStat[0.04] - 1
                    gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos, left=True)
            print('很均衡时大的偏多')
        else:
            if len(big_near_tmp) - len(small_tmp) >= -2 and len(big_near_tmp) >= len(small_near_tmp) >= -1:
                if len(big_near_tmp) == 2:
                    if big_near_gap_tmp[0] < 0.0006:
                        arr.add(big_near_tmp[0])
                    if nearGapStat[0.01] == 1:
                        arr.add(big_near_tmp[0])
            if len(small_near_tmp) == len(big_near_tmp):
                if len(big_near_tmp) == 2:
                    if nearGapStat[0.01] == 1:
                        arr.add(big_near_tmp[0])
            if len(big_tmp) >= len(small_near_tmp):
                if len(big_tmp) == 2:
                    if gapStat[0.03] == 1:
                        arr.add(big_tmp[0])
            print('非常均衡')
    #大部分小
    elif count['small'] >= 7:
        print('大部分小')
    #连续小
    elif count['small'] >= 5 and maxConsecutiveCount['small'] >= 4:
        print('连续小')
    else:
        print('不对呀', data_len)
    print(data_len, good_count, arr)
    del(seq['near'])
    show(gapStat, avg_window, data_len, range_stat, prob_cand_arr, pred, seq)
    return arr
