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
        if midJudge(big_tmp, gapStat, 0.02, True):
            pos = len(big_tmp) - gapStat[0.02]
            gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos, left=False)
            if big_gap_tmp[0] < 0.0155 and big_gap_tmp[1] > 0.0171:
                arr.add(big_tmp[0])
        if midJudge(big_tmp, gapStat, 0.08, False):
            pos = len(big_tmp) - gapStat[0.08] - 1
            gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos, left=True)
        if midJudge(big_tmp, gapStat, 0.03, True):
            pos = len(big_tmp) - gapStat[0.03]
            gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos, left=False)
        if midJudge(big_tmp, gapStat, 0.04, True):
            pos = len(big_tmp) - gapStat[0.04]
            gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos, left=False)
        if midJudge(big_tmp, gapStat, 0.05, False):
            pos = len(big_tmp) - gapStat[0.05] - 1
            gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos, left=True)
        print('大的全都要')
    #参差不齐接近
    elif count['near'] >= 5 and maxConsecutiveCount['near'] < 4:
        if len(seq['small']) + len(seq['smallNear']) >= 7:
            if len(small_near_tmp) >= len(big_near_tmp) and len(small_near_tmp) >= len(big_tmp):
                if nearGapStat[-0.01] == 0:
                    findTurn(arr, small_near_tmp, small_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=True, choose_single=False)
                if noConsecutiveGap(small_near_gap_tmp):
                    if small_near_gap_tmp[-1] > -0.0009:
                        arr.add(small_near_tmp[-1])
                if midJudge(small_near_tmp, nearGapStat, -0.01, False):
                    pos = nearGapStat[-0.01]
                    gapAndConsecutive(arr, small_near_tmp, small_near_gap_tmp, pos, left=False)
                    if small_near_gap_tmp[pos] < -0.0083 and pos + 1 < len(small_near_tmp):
                        arr.add(small_near_tmp[pos + 1])
                if midJudge(small_near_tmp, nearGapStat, -0.01, True):
                    findTurn(arr, small_near_tmp, small_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=True, choose_single=False)
            print('参差不齐接近时小的偏多')
        elif len(seq['big']) + len(seq['bigNear']) >= 7:
            if len(big_tmp) >= len(small_tmp) and len(big_tmp) >= len(small_near_tmp):
                if big_gap_tmp[0] < 0.0315:
                    arr.add(big_tmp[0])
                if midJudge(big_tmp, gapStat, 0.02, True):
                    pos = len(big_tmp) - gapStat[0.02] - 1
                    gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos, left=True)
                if midJudge(big_tmp, gapStat, 0.03, False):
                    findTurn(arr, big_tmp, big_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=True, choose_single=False)
                if midJudge(big_tmp, gapStat, 0.03, True):
                    pos = len(big_tmp) - gapStat[0.03] - 1
                    gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos, left=True)
                    gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos + 1, left=False)
                if midJudge(big_tmp, gapStat, 0.05, False):
                    pos = len(big_tmp) - gapStat[0.05] - 1
                    gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos, left=True)
                    gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos + 1, left=False)
            if len(big_near_tmp) >= len(small_tmp) and len(big_near_tmp) >= len(small_near_tmp):
                if midJudge(big_near_tmp, nearGapStat, 0.01, False):
                    pos = len(big_near_tmp) - nearGapStat[0.01]
                    gapAndConsecutive(arr, big_near_tmp, big_near_gap_tmp, pos, left=False)
                if midJudge(big_near_tmp, nearGapStat, 0.01, True):
                    pos = len(big_near_tmp) - nearGapStat[0.01]
                    gapAndConsecutive(arr, big_near_tmp, big_near_gap_tmp, pos, left=False)
            if len(small_near_tmp) - len(big_tmp) >= -1 and len(small_near_tmp) - len(big_near_tmp) >= -1:
                if midJudge(small_near_tmp, nearGapStat, -0.01, False):
                    pos = nearGapStat[-0.01]
                    gapAndConsecutive(arr, small_near_tmp, small_near_gap_tmp, pos, left=False)
            if len(big_near_tmp) >= len(small_tmp) and len(big_near_tmp) >= len(small_near_tmp):
                if nearGapStat[0.01] == 0:
                    findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=False, choose_single=False)
                if midJudge(big_near_tmp, nearGapStat, 0.01, False):
                    pos = len(big_near_tmp) - nearGapStat[0.01] - 1
                    gapAndConsecutive(arr, big_near_tmp, big_near_gap_tmp, pos, left=True)
                    if big_near_gap_tmp[pos] > 0.0081:
                        if pos - 1 > -1:
                            arr.add(big_near_tmp[pos - 1])
            print('参差不齐接近时大的偏多')
        elif len(seq['small']) + len(seq['smallNear']) > len(seq['big']) + len(seq['bigNear']):
            if len(small_near_tmp) - len(big_near_tmp) >= -1 and len(small_near_tmp) - len(big_tmp) >= -1:
                if nearGapStat[-0.01] == 0:
                    findTurn(arr, small_near_tmp, small_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=True, choose_single=False)
                if small_near_gap_tmp[0] == small_near_gap_tmp[-1]:
                    for v in small_near_tmp:
                        arr.add(v)
                if len(small_near_tmp) == 2:
                    if nearGapStat[-0.01] == 1:
                        arr.add(small_near_tmp[0])
                if midJudge(small_near_tmp, nearGapStat, -0.01, True):
                    pos = nearGapStat[-0.01] - 1
                    gapAndConsecutive(arr, small_near_tmp, small_near_gap_tmp, pos, left=True)
                    gapAndConsecutive(arr, small_near_tmp, small_near_gap_tmp, pos + 1, left=False)
                if midJudge(small_near_tmp, nearGapStat, -0.01, False):
                    pos = nearGapStat[-0.01]
                    gapAndConsecutive(arr, small_near_tmp, small_near_gap_tmp, pos, left=False)
                    findTurn(arr, small_near_tmp, small_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=True, consecutive_at_left=True, choose_single=True)
            if len(big_near_tmp) - len(small_near_tmp) >= -1 and len(big_near_gap_tmp) - len(small_tmp) >= -1:
                if len(big_near_tmp) == 2:
                    if nearGapStat[0.01] == 1:
                        arr.add(big_near_tmp[0])
            if len(big_tmp) >= len(small_tmp):
                if len(big_tmp) == 2:
                    if gapStat[0.03] == 1:
                        arr.add(big_tmp[0])
                        arr.add(big_tmp[1])
            if len(big_tmp) - len(small_tmp) >= -1 and len(big_tmp) - len(small_near_tmp):
                if len(big_tmp) == 2:
                    if gapStat[0.03] == 1:
                        arr.add(big_tmp[1])
            print('参差不齐接近时小的比大的多一些')
        elif len(seq['small']) + len(seq['smallNear']) < len(seq['big']) + len(seq['bigNear']):
            if len(big_near_tmp) >= len(small_tmp) and len(big_near_tmp) >= len(small_near_tmp):
                if midJudge(big_near_tmp, nearGapStat, 0.01, True):
                    pos = len(big_near_tmp) - nearGapStat[0.01]
                    gapAndConsecutive(arr, big_near_tmp, big_near_gap_tmp, pos, left=False)
                if midJudge(big_near_tmp, nearGapStat, 0.01, False):
                    pos = len(big_near_tmp) - nearGapStat[0.01] - 1
                    gapAndConsecutive(arr, big_near_tmp, big_near_gap_tmp, pos, left=True)
                    if big_near_gap_tmp[pos] > 0.0085:
                        arr.add(big_near_tmp[pos - 1])
                    findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=True, choose_single=False)
                if nearGapStat[0.01] == 0:
                    if noConsecutiveGap(big_near_gap_tmp):
                        for i in range(1, len(big_near_tmp) - 1):
                            if big_near_gap_tmp[i-1] < 0.0018 and big_near_gap_tmp[i+1] > 0.0072:
                                arr.add(big_near_tmp[i])
                                break
                    findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=True, choose_single=True)
            if len(small_near_tmp) >= len(big_tmp) and len(small_near_tmp) >= len(big_near_tmp):
                if midJudge(small_near_tmp, nearGapStat, -0.01, False):
                    pos = nearGapStat[-0.01]
                    gapAndConsecutive(arr, small_near_tmp, small_near_gap_tmp, pos, left=False)
                    findTurn(arr, small_near_tmp, small_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=False, choose_single=False)
            if len(big_tmp) - len(small_tmp) >= -1 and len(big_tmp) - len(small_near_tmp) >= -1:
                if midJudge(big_tmp, gapStat, 0.04, False):
                    pos = len(big_tmp) - gapStat[0.04]
                    gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos, left=False)
                if gapStat[0.05] == 0:
                    if big_gap_tmp[-1] > 0.049:
                        arr.add(big_tmp[-1])
            print('参差不齐接近时大的多一些')
        else:
            if len(big_near_tmp) - len(small_tmp) >= -1 and len(big_near_tmp) - len(small_near_tmp) >= -1:
                if midJudge(big_near_tmp, nearGapStat, 0.01, True):
                    pos = len(big_near_tmp) - nearGapStat[0.01]
                    gapAndConsecutive(arr, big_near_tmp, big_near_gap_tmp, pos, left=False)
                if midJudge(big_near_tmp, nearGapStat, 0.01, False):
                    pos = len(big_near_tmp) - nearGapStat[0.01] - 1
                    gapAndConsecutive(arr, big_near_tmp, big_near_gap_tmp, pos, left=True)
                if len(big_near_tmp) == 2:
                    if big_near_gap_tmp[1] > 0.0055:
                        arr.add(big_near_tmp[1])
            if len(big_near_tmp) >= len(small_tmp):
                if big_near_gap_tmp[0] == big_near_gap_tmp[-1]:
                    for v in big_near_tmp:
                        arr.add(v)
                if len(big_near_tmp) == 2:
                    if nearGapStat[0.01] == 1:
                        arr.add(big_near_tmp[1])
                    if nearGapStat[0.01] == 0:
                        if big_near_gap_tmp[0] < 0.0004:
                            arr.add(big_near_tmp[1])
                if midJudge(big_near_tmp, nearGapStat, 0.01, False):
                    if noConsecutiveGap(big_near_gap_tmp):
                        pos = len(big_near_tmp) - nearGapStat[0.01] - 1
                        if big_near_gap_tmp[pos] > 0.0075 and big_near_gap_tmp[pos - 1] < 0.0048:
                            arr.add(big_near_tmp[pos - 1])
            if len(big_tmp) - len(small_tmp) >= -1 and len(big_tmp) - len(small_near_tmp) >= -1:
                if midJudge(big_tmp, gapStat, 0.02, False):
                    pos = len(big_tmp) - gapStat[0.02] - 1
                    gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos, left=True)
                if midJudge(big_tmp, gapStat, 0.04, False):
                    pos = len(big_tmp) - gapStat[0.04]
                    if big_gap_tmp[pos] < 0.0409:
                        if pos + 1 < len(big_tmp):
                            arr.add(big_tmp[pos + 1])
                if len(big_tmp) == 2:
                    if gapStat[0.04] == 1:
                        arr.add(big_tmp[0])
                        arr.add(big_tmp[1])
            if len(small_tmp) >= len(big_tmp) and len(small_tmp) >= len(big_near_tmp):
                if midJudge(small_tmp, gapStat, -0.03, False):
                    pos = gapStat[-0.03] - 1
                    if small_gap_tmp[pos] > -0.0311:
                        if pos - 1 > -1:
                            arr.add(small_tmp[pos - 1])
            if len(small_near_tmp) >= len(big_tmp) and len(small_near_tmp) >= len(big_near_tmp):
                if nearGapStat[-0.01] == 0:
                    findTurn(arr, small_near_tmp, small_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=False, choose_single=False)
            print('参差不齐接近时大小一样')
    #连续接近
    elif count['near'] >= 5 and maxConsecutiveCount['near'] >= 4:
        if len(seq['small']) + len(seq['smallNear']) >= 7:
            print('连续接近时小的偏多')
        elif len(seq['big']) + len(seq['bigNear']) >= 7:
            if len(big_near_tmp) >= len(small_near_tmp) and len(big_near_tmp) >= len(small_tmp):
                if midJudge(big_near_tmp, nearGapStat, 0.01, True):
                    pos = len(big_near_tmp) - nearGapStat[0.01]
                    gapAndConsecutive(arr, big_near_tmp, big_near_gap_tmp, pos, left=False)
            print('连续接近时大的偏多')
        elif len(seq['small']) + len(seq['smallNear']) > len(seq['big']) + len(seq['bigNear']):
            if len(small_near_tmp) >= len(big_tmp) and len(small_near_tmp) >= len(big_near_tmp):
                if midJudge(small_near_tmp, nearGapStat, -0.01, False):
                    pos = nearGapStat[-0.01] - 1
                    gapAndConsecutive(arr, small_near_tmp, small_near_gap_tmp, pos, left=True)
            print('连续接近时小的比大的多一些')
        elif len(seq['small']) + len(seq['smallNear']) < len(seq['big']) + len(seq['bigNear']):
            if len(big_near_tmp) - len(small_tmp) >= -1 and len(big_near_tmp) - len(small_near_tmp) >= -1:
                if midJudge(big_near_tmp, nearGapStat, 0.01, False):
                    pos = len(big_near_tmp) - nearGapStat[0.01] - 1
                    gapAndConsecutive(arr, big_near_tmp, big_near_gap_tmp, pos, left=True)
                    gapAndConsecutive(arr, big_near_tmp, big_near_gap_tmp, pos + 1, left=False)
            print('连续接近时大的比小的多一些')
        else:
            if len(big_near_tmp) >= len(small_tmp):
                if big_near_gap_tmp[0] == big_near_gap_tmp[-1]:
                    for v in big_near_tmp:
                        arr.add(v)
            if len(small_near_tmp) - len(big_tmp) >= -1 and len(small_near_tmp) - len(big_near_tmp) >= -1:
                if len(small_near_tmp) == 2:
                    if small_near_gap_tmp[0] < -0.008 and small_near_gap_tmp[1] > -0.0019:
                        arr.add(small_near_tmp[1])
            print('连续接近时大小一样')
    elif count['small'] >= 5 and maxConsecutiveCount['small'] < 4:
        if midJudge(small_tmp, gapStat, -0.03, False):
            pos = gapStat[-0.03]
            gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos, left=False)
            findTurn(arr, small_tmp, small_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=True, consecutive_at_left=False, choose_single=False)
        if midJudge(small_tmp, gapStat, -0.02, False):
            findTurn(arr, small_tmp, small_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=True, consecutive_at_left=False, choose_single=False)
        if midJudge(small_tmp, gapStat, -0.02, True):
            pos = gapStat[-0.02]
            gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos, left=True)
        if len(big_near_tmp) >= len(small_near_tmp):
            if nearGapStat[0.01] == 0:
                findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=False, choose_single=True)
            if len(big_near_tmp) == 2:
                if nearGapStat[0.01] == 1:
                    arr.add(big_near_tmp[0])
        if len(small_near_gap_tmp) - len(big_tmp) >= -2 and len(small_near_tmp) >= len(big_near_tmp):
            if midJudge(small_near_tmp, nearGapStat, -0.01, False):
                pos = nearGapStat[-0.01]
                gapAndConsecutive(arr, small_near_tmp, small_near_gap_tmp, pos, left=False)
            if small_near_gap_tmp[0] < -0.0098:
                if len(small_near_tmp) > 1:
                    arr.add(small_near_tmp[1])
            if len(small_near_tmp) == 2:
                if nearGapStat[-0.01] == 1:
                    arr.add(small_near_tmp[0])
                if nearGapStat[-0.01] == 0:
                    if small_near_gap_tmp[1] > -0.0009:
                        arr.add(small_near_tmp[0])
            if nearGapStat[-0.01] == 0:
                findTurn(arr, small_near_tmp, small_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=False, choose_single=False)
        if len(big_tmp) >= len(small_near_tmp):
            if len(big_tmp) == 2:
                if gapStat[0.03] == 1:
                    arr.add(big_tmp[1])
        print('参差不齐小')
    #不是大的就是接近的(大的偏多)
    elif count['big'] >= 5 and count['near'] >= 2:
        if midJudge(big_tmp, gapStat, 0.05, False):
            pos = len(big_tmp) - gapStat[0.05] - 1
            gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos, left=True)
        if midJudge(big_tmp, gapStat, 0.04, True):
            pos = len(big_tmp) - gapStat[0.04]
            gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos, left=False)
            gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos - 1, left=True)
        if midJudge(big_tmp, gapStat, 0.04, False):
            pos = len(big_tmp) - gapStat[0.04] - 1
            gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos, left=True)
            gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos + 1, left=False)
            if big_gap_tmp[pos + 1] < 0.0409:
                if pos + 2 < len(big_tmp):
                    arr.add(big_tmp[pos + 2])
        if midJudge(big_tmp, gapStat, 0.03, True):
            pos = len(big_tmp) - gapStat[0.03] - 1
            gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos, left=True)
            if big_gap_tmp[0] < 0.022 and big_gap_tmp[1] > 0.0288:
                arr.add(big_tmp[0])
        if midJudge(big_tmp, gapStat, 0.03, False):
            pos = len(big_tmp) - gapStat[0.03] - 1
            gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos, left=True)
            findTurn(arr, big_tmp, big_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=True, choose_single=False)
        if midJudge(big_tmp, gapStat, 0.02, True):
            pos = len(big_tmp) - gapStat[0.02] - 1
            gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos, left=True)
            gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos + 1, left=False)
        if len(small_near_tmp) - len(big_tmp) >= -2 and len(small_near_tmp) >= len(big_near_tmp):
            if midJudge(small_near_tmp, nearGapStat, -0.01, False):
                pos = nearGapStat[-0.01]
                gapAndConsecutive(arr, small_near_tmp, small_near_gap_tmp, pos, left=False)
        if len(small_near_tmp) >= len(big_near_tmp):
            if small_near_gap_tmp[0] == small_near_gap_tmp[-1]:
                for v in small_near_tmp:
                    arr.add(v)
            if len(small_near_tmp) == 2:
                if nearGapStat[-0.01] == 0:
                    if small_near_gap_tmp[1] > -0.002:
                        arr.add(small_near_tmp[1])
        if len(big_near_tmp) >= len(small_tmp) and len(big_near_tmp) >= len(small_near_tmp):
            if len(big_near_tmp) == 2:
                if big_near_gap_tmp[1] > 0.0059:
                    arr.add(big_near_tmp[1])
            if midJudge(big_near_tmp, nearGapStat, 0.01, False):
                pos = len(big_near_tmp) - nearGapStat[0.01]
                gapAndConsecutive(arr, big_near_tmp, big_near_gap_tmp, pos, left=False)
                gapAndConsecutive(arr, big_near_tmp, big_near_gap_tmp, pos - 1, left=True)
        if len(big_near_tmp) >= len(small_tmp):
            if len(big_near_tmp) == 1:
                arr.add(big_near_tmp[0])
        if len(small_tmp) >= len(big_near_tmp):
            if len(small_tmp) > 1:
                if small_gap_tmp[0] == small_gap_tmp[-1]:
                    for v in small_tmp:
                        arr.add(v)
        print('不是大的就是接近的(大的偏多)')
    #不是大的就是小的(大的偏多)
    elif count['big'] >= 5 and count['small'] >= 2:
        print('不是大的就是小的(大的偏多)')
    #大:接近:小很均衡
    elif count['big'] <= 4 and count['near'] <= 4 and count['small'] <= 4:
        if len(seq['small']) + len(seq['smallNear']) > len(seq['big']) + len(seq['bigNear']):
            if len(big_near_tmp) == 1:
                if nearGapStat[0.01] == 0:
                    arr.add(big_near_tmp[0])
            if len(big_near_tmp) >= len(small_near_tmp):
                if len(big_near_tmp) == 2:
                    if nearGapStat[0.01] == 0:
                        if big_near_gap_tmp[0] < 0.0006:
                            if big_near_gap_tmp[1] > 0.0043:
                                arr.add(big_near_tmp[1])
                            else:
                                arr.add(big_near_tmp[0])
            if len(big_tmp) >= len(small_tmp) and len(big_tmp) >= len(small_near_tmp):
                if midJudge(big_tmp, gapStat, 0.02, True):
                    pos = len(big_tmp) - gapStat[0.02] - 1
                    if big_gap_tmp[pos] > 0.018:
                        if pos - 1 > -1:
                            arr.add(big_tmp[pos - 1])
            elif len(big_tmp) >= len(small_near_tmp):
                if len(big_tmp) == 2:
                    if gapStat[0.03] == 1:
                        arr.add(big_tmp[0])
                        arr.add(big_tmp[1])
            if len(small_near_tmp) >= len(big_tmp) and len(small_near_tmp) >= len(big_near_tmp):
                if midJudge(small_near_tmp, nearGapStat, -0.01, True):
                    pos = nearGapStat[-0.01] - 1
                    gapAndConsecutive(arr, small_near_tmp, small_near_gap_tmp, pos, left=True)
            if len(small_tmp) >= len(big_tmp) and len(small_tmp) >= len(big_near_tmp):
                if midJudge(small_tmp, gapStat, -0.03, False):
                    pos = gapStat[-0.03] - 1
                    gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos, left=True)
                if len(small_near_tmp) == 2:
                    if nearGapStat[-0.01] == 1:
                        arr.add(small_near_tmp[1])
            print('很均衡时小的偏多')
        elif len(seq['small']) + len(seq['smallNear']) < len(seq['big']) + len(seq['bigNear']):
            if len(big_tmp) >= len(small_tmp) and len(big_tmp) >= len(small_near_tmp):
                if midJudge(big_tmp, gapStat, 0.04, False):
                    findTurn(arr, big_tmp, big_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=False, choose_single=True)
                if midJudge(big_tmp, gapStat, 0.02, True):
                    pos = len(big_tmp) - gapStat[0.02] - 1
                    gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos, left=True)
                    gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos + 1, left=False)
            if len(big_near_tmp) >= len(small_tmp) and len(big_near_tmp) >= len(small_near_tmp):
                if nearGapStat[0.01] == 0:
                    findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=False, choose_single=False)
                    findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=True, consecutive_at_left=True, choose_single=True)
                if midJudge(big_near_tmp, nearGapStat, 0.01, False):
                    pos = len(big_near_tmp) - nearGapStat[0.01]
                    gapAndConsecutive(arr, big_near_tmp, big_near_gap_tmp, pos, left=False)
            if len(small_tmp) >= len(big_tmp) and len(small_tmp) >= len(big_near_tmp):
                if midJudge(small_tmp, gapStat, -0.03, False):
                    pos = gapStat[-0.03]
                    gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos, left=False)
            if len(small_tmp) - len(big_near_tmp) >= -1:
                if small_gap_tmp[0] == small_gap_tmp[-1]:
                    for v in small_tmp:
                        arr.add(v)
            print('很均衡时大的偏多')
        else:
            if len(big_tmp) - len(small_tmp) >= -1 and len(big_tmp) >= len(small_near_tmp):
                if midJudge(big_tmp, gapStat, 0.02, True):
                    pos = len(big_tmp) - gapStat[0.02] - 1
                    gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos, left=True)
                    gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos + 1, left=False)
                if midJudge(big_tmp, gapStat, 0.03, False):
                    pos = len(big_tmp) - gapStat[0.03] - 1
                    gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos, left=True)
                    if big_gap_tmp[0] < 0.0216:
                        arr.add(big_tmp[0])
            elif len(big_tmp) >= len(small_near_tmp):
                if len(big_tmp) == 2:
                    if big_gap_tmp[1] > 0.0385:
                        arr.add(big_tmp[1])
            if len(big_near_tmp) - len(small_tmp) >= -1 and len(big_near_tmp) - len(small_near_tmp) >= -1:
                if midJudge(big_near_tmp, nearGapStat, 0.01, False):
                    pos = len(big_near_tmp) - nearGapStat[0.01]
                    gapAndConsecutive(arr, big_near_tmp, big_near_gap_tmp, pos, left=False)
                if nearGapStat[0.01] == 0:
                    findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=True, choose_single=True)
                if len(big_near_tmp) == 2:
                    if nearGapStat[0.01] == 1:
                        arr.add(big_near_tmp[0])
                    if nearGapStat[0.01] == 0:
                        if big_near_gap_tmp[1] > 0.0075:
                            arr.add(big_near_tmp[1])
            if len(small_near_tmp) - len(big_tmp) >= -1 and len(small_near_tmp) - len(big_near_tmp) >= -1:
                if small_near_gap_tmp[0] == small_near_gap_tmp[-1]:
                    for v in small_near_tmp:
                        arr.add(v)
            if len(small_tmp) >= len(big_near_tmp) and len(small_tmp) >= len(big_tmp):
                if midJudge(small_tmp, gapStat, -0.03, False):
                    pos = gapStat[-0.03] - 1
                    gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos, left=True)
            elif len(small_tmp) >= len(big_near_tmp):
                if len(small_tmp) == 2:
                    if gapStat[-0.02] == 1:
                        arr.add(small_tmp[1])
            if len(small_near_tmp) >= len(big_near_tmp):
                if len(small_near_tmp) == 1:
                    if small_near_gap_tmp[0] >= -0.012:
                        arr.add(small_near_tmp[0])
                if len(small_near_tmp) == 2:
                    if nearGapStat[-0.01] == 2:
                        if small_near_gap_tmp[1] > -0.011:
                            arr.add(small_near_tmp[1])
                    if nearGapStat[-0.01] == 0:
                        if small_near_gap_tmp[0] < -0.0091:
                            arr.add(small_near_tmp[1])
                if midJudge(small_near_tmp, nearGapStat, -0.01, False):
                    pos = nearGapStat[-0.01]
                    if small_near_gap_tmp[pos] < -0.0093:
                        if pos + 1 < len(small_near_tmp):
                            arr.add(small_near_tmp[pos + 1])
                if small_near_gap_tmp[0] == small_near_gap_tmp[-1]:
                    for v in small_near_tmp:
                        arr.add(v)
            print('非常均衡')
    #大部分小
    elif count['small'] >= 7:
        if midJudge(small_tmp, gapStat, -0.02, True):
            pos = gapStat[-0.02]
            gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos, left=False)
        if midJudge(small_tmp, gapStat, -0.03, True):
            pos = gapStat[-0.03]
            gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos, left=False)
        findTurn(arr, small_tmp, small_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=True, consecutive_at_left=False, choose_single=False)
        if small_gap_tmp[-1] > -0.0206:
            arr.add(small_tmp[-2])
        if small_gap_tmp[-1] > -0.0254 and small_gap_tmp[-2] < -0.0281:
            arr.add(small_tmp[-1])
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
