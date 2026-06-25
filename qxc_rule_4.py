from rule_kit import *


def process(count, maxConsecutiveCount, seq, nearGapStat, gapStat, prob_cand_arr, pred, avg_window, data_len, good_count, range_stat, name, label, label_dim):
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
        if len(big_tmp) == gapStat[0.03]:
            if big_gap_tmp[0] < 0.0312:
                arr.add(big_tmp[0])
        if midJudge(big_tmp, gapStat, 0.07, False):
            pos = len(big_tmp) - gapStat[0.07]
            gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos, left=False)
            gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos - 1, left=True)
        if midJudge(big_tmp, gapStat, 0.06, True):
            pos = len(big_tmp) - gapStat[0.06] - 1
            gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos, left=True)
        if midJudge(big_tmp, gapStat, 0.06, False):
            if big_gap_tmp[-1] > 0.065:
                arr.add(big_tmp[-1])
            pos = len(big_tmp) - gapStat[0.06] - 1
            gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos, left=True)
            gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos + 1, left=False)
        if midJudge(big_tmp, gapStat, 0.05, True):
            pos = len(big_tmp) - gapStat[0.05] - 1
            arr.add(big_tmp[pos])
        if midJudge(big_tmp, gapStat, 0.05, False):
            if gapStat[0.06] == 0 and big_gap_tmp[-1] > 0.057:
                arr.add(big_tmp[-1])
            pos = len(big_tmp) - gapStat[0.05] - 1
            if big_gap_tmp[pos] < 0.0495:
                arr.add(big_tmp[pos])
                arr.add(big_tmp[pos + 1])
            elif pos - 1 > -1 and big_gap_tmp[pos - 1] < 0.048:
                arr.add(big_tmp[pos - 1])
            if big_gap_tmp[pos + 1] < 0.053:
                arr.add(big_tmp[pos + 1])
        if midJudge(big_tmp, gapStat, 0.04, True):
            pos = len(big_tmp) - gapStat[0.04] - 1
            gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos, left=True)
            gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos + 1, left=False)
        if midJudge(big_tmp, gapStat, 0.04, False):
            pos = len(big_tmp) - gapStat[0.04] - 1
            gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos, left=True)
            gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos + 1, left=False)
        if midJudge(big_tmp, gapStat, 0.03, True):
            pos = len(big_tmp) - gapStat[0.03]
            if big_gap_tmp[pos] > 0.0314:
                arr.add(big_tmp[pos])
            else:
                arr.add(big_tmp[pos])
                if big_gap_tmp[pos + 1] > 0.032:
                    arr.add(big_tmp[pos + 1])
            arr.add(big_tmp[pos - 1])
            if big_gap_tmp[0] > 0.024 and big_gap_tmp[0] < 0.026:
                arr.add(big_tmp[0])
            findTurn(arr, big_tmp, big_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=True, choose_single=False)
            if big_gap_tmp[pos] < 0.0323:
                arr.add(big_tmp[pos + 1])
        if midJudge(big_tmp, gapStat, 0.03, False):
            pos = len(big_tmp) - gapStat[0.03] - 1
            if big_gap_tmp[pos] < 0.0295:
                arr.add(big_tmp[pos])
            else:
                if pos - 1 > -1 and big_gap_tmp[pos - 1] < 0.029:
                    arr.add(big_tmp[pos - 1])
        if len(big_tmp) == gapStat[0.02]:
            if big_gap_tmp[0] < 0.0213:
                arr.add(big_tmp[1])
            if big_gap_tmp[0] < 0.0207:
                arr.add(big_tmp[0])
            if midJudge(big_tmp, gapStat, 0.03, True):
                pos = len(big_tmp) - gapStat[0.03] - 1
                if big_gap_tmp[pos] > 0.0285:
                    if pos - 1 > -1:
                        arr.add(big_tmp[pos - 1])
                findTurn(arr, big_tmp, big_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=False, choose_single=True)
            for i in range(len(big_tmp) - 1):
                if big_gap_tmp[i] < 0.02 and big_gap_tmp[i] > 0.019 and big_gap_tmp[i+1] > 0.021:
                    arr.add(big_tmp[i+1])
                    for j in range(i+2, len(big_tmp)):
                        if big_gap_tmp[j] - big_gap_tmp[i+1] < 0.0001:
                            arr.add(big_tmp[j])
                    break
        if midJudge(big_tmp, gapStat, 0.02, True):
            pos = len(big_tmp) - gapStat[0.02]
            if big_gap_tmp[pos] > 0.0212:
                arr.add(big_tmp[pos])
                for i in range(pos + 1, len(big_tmp)):
                    if big_gap_tmp[i] - big_gap_tmp[pos] < 0.00001:
                        arr.add(big_tmp[i])
            else:
                arr.add(big_tmp[pos])
                arr.add(big_tmp[pos + 1])
                for i in range(pos + 2, len(big_tmp)):
                    if big_gap_tmp[i] - big_gap_tmp[pos + 1] < 0.0001:
                        arr.add(big_tmp[i])
            if big_gap_tmp[pos - 1] < 0.0192:
                arr.add(big_tmp[pos - 1])
            else:
                arr.add(big_tmp[pos - 1])
                if pos - 2 > -1:
                    arr.add(big_tmp[pos - 2])
            findTurn(arr, big_tmp, big_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=True, choose_single=False)
        if len(small_near_tmp) - len(big_near_tmp) >= -1:
            if len(small_near_tmp) == 1:
                if small_near_gap_tmp[0] > -0.012:
                    arr.add(small_near_tmp[0])
            if len(small_near_tmp) == 2:
                if nearGapStat[-0.01] == 1:
                    arr.add(small_near_tmp[0])
                if nearGapStat[-0.01] == 0:
                    arr.add(small_near_tmp[0])
                    if small_near_gap_tmp[1] - small_near_gap_tmp[0] < 0.0001:
                        arr.add(small_near_tmp[1])
        if len(big_near_tmp) - len(small_tmp) >= -1 and len(big_near_tmp) - len(small_near_tmp) >= -1:
            if len(big_near_tmp) == 1:
                arr.add(big_near_tmp[0])
            if len(big_near_tmp) == 2:
                if nearGapStat[0.01] == len(big_near_tmp):
                    if big_near_gap_tmp[1] - big_near_gap_tmp[0] < 0.0001:
                        arr.add(big_near_tmp[0])
                        arr.add(big_near_tmp[1])
                if big_near_gap_tmp[0] < 0.012:
                    arr.add(big_near_tmp[0])
                    arr.add(big_near_tmp[1])
        if len(small_tmp) >= len(big_near_tmp):
            if gapStat[-0.02] == 0:
                if len(small_tmp) > 0:
                    arr.add(small_tmp[0])
        print('大的全都要')
    elif count['near'] >= 5 and maxConsecutiveCount['near'] < 4:
        if len(seq['small']) + len(seq['smallNear']) >= 7:
            if len(big_tmp) - len(small_tmp) >= -1:
                if len(big_tmp) == 2:
                    if gapStat[0.02] == 1:
                        arr.add(big_tmp[1])
            if len(big_near_tmp) - len(small_tmp) >= -1 and len(big_near_tmp) >= len(small_near_tmp):
                if midJudge(big_near_tmp, nearGapStat, 0.01, True):
                    pos = len(big_near_tmp) - nearGapStat[0.01] - 1
                    arr.add(big_near_tmp[pos])
            elif len(big_near_tmp) - len(small_near_tmp) >= -1:
                if len(big_near_tmp) == 2:
                    if nearGapStat[0.01] == 0:
                        if big_near_gap_tmp[1] > 0.0075:
                            arr.add(big_near_tmp[0])
            if len(big_near_tmp) == 2:
                if nearGapStat[0.01] == 0:
                    if big_near_gap_tmp[0] < 0.001 and big_near_gap_tmp[1] > 0.003:
                        arr.add(big_near_tmp[0])
            if len(big_near_tmp) == 1:
                if nearGapStat[0.01] == 0:
                    arr.add(big_near_tmp[0])
            if len(small_near_tmp) >= len(big_tmp) and len(small_near_tmp) - len(big_near_tmp) >= -1:
                if midJudge(small_near_tmp, nearGapStat, -0.01, True):
                    pos = nearGapStat[-0.01] - 1
                    arr.add(small_near_tmp[pos])
                    arr.add(small_near_tmp[pos + 1])
                    for i in range(pos - 1, -1, -1):
                        if small_near_gap_tmp[pos] - small_near_gap_tmp[i] < 0.0001:
                            arr.add(small_near_tmp[i])
                if midJudge(small_near_tmp, nearGapStat, -0.01, False):
                    pos = nearGapStat[-0.01] - 1
                    arr.add(small_near_tmp[pos])
                    arr.add(small_near_tmp[pos + 1])
                    findTurn(arr, small_near_tmp, small_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=True, choose_single=False)
                    findTurn(arr, small_near_tmp, small_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=True, consecutive_at_left=True, choose_single=True)
                    if noConsecutiveGap(small_near_gap_tmp):
                        for i in range(len(small_near_tmp) - 1, -1, -1):
                            if small_near_gap_tmp[i] >= -0.004 and small_near_gap_tmp[i-1] > -0.01 and small_near_gap_tmp[i-1] < -0.005:
                                arr.add(small_near_tmp[i])
                                break
                if nearGapStat[-0.01] == 0:
                    for i in range(len(small_near_tmp) - 1, -1, -1):
                        if small_near_gap_tmp[i] > -0.0008:
                            if i - 1 > -1 and small_near_gap_tmp[i-1] < -0.002:
                                arr.add(small_near_tmp[i-1])
                                for j in range(i - 2, -1, -1):
                                    if small_near_gap_tmp[i-1] - small_near_gap_tmp[j] < 0.0001:
                                        arr.add(small_near_tmp[j])
                            break
                if len(small_near_tmp) == 2:
                    if nearGapStat[-0.01] == 1:
                        arr.add(small_near_tmp[1])
            if len(small_tmp) >= len(big_tmp) and len(small_tmp) >= len(big_near_tmp):
                if len(small_tmp) == 2:
                    if gapStat[-0.03] == 1:
                        arr.add(small_tmp[0])
                    if gapStat[-0.02] == 1:
                        arr.add(small_tmp[0])
                if len(small_tmp) == gapStat[-0.02]:
                    if midJudge(small_tmp, gapStat, -0.03, False):
                        if small_gap_tmp[-1] > -0.024:
                            arr.add(small_tmp[-1])
                if midJudge(small_tmp, gapStat, -0.03, False):
                    pos = gapStat[-0.03] - 1
                    if small_gap_tmp[pos] > -0.0302:
                        if pos - 1 > -1:
                            arr.add(small_tmp[pos - 1])
                    gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos, left=True)
                    gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos + 1, left=False)
                if midJudge(small_tmp, gapStat, -0.03, True):
                    pos = gapStat[-0.03]
                    gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos, left=False)
                if midJudge(small_tmp, gapStat, -0.02, False):
                    findTurn(arr, small_tmp, small_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=True, consecutive_at_left=False, choose_single=False)
                if midJudge(small_tmp, gapStat, -0.02, True):
                    pos = gapStat[-0.02]
                    gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos, left=False)
                if midJudge(small_tmp, gapStat, -0.05, False):
                    pos = gapStat[-0.05] - 1
                    gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos, left=True)
                if midJudge(small_tmp, gapStat, -0.04, False):
                    pos = gapStat[-0.04] - 1
                    gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos, left=True)
                    arr.add(small_tmp[pos + 1])
                    for i in range(pos + 2, len(small_tmp)):
                        if small_gap_tmp[i] - small_gap_tmp[pos + 1] < 0.0001:
                            arr.add(small_tmp[i])
            if len(big_tmp) == 1:
                if big_gap_tmp[0] < 0.0233:
                    arr.add(big_tmp[0])
            if len(big_near_tmp) == 1:
                arr.add(big_near_tmp[0])
            if len(small_near_tmp) >= len(big_tmp) and len(small_near_tmp) >= len(big_near_tmp):
                if midJudge(small_near_tmp, nearGapStat, -0.01, True):
                    pos = nearGapStat[-0.01] - 1
                    if small_near_gap_tmp[pos] > -0.011:
                        arr.add(small_near_tmp[pos - 1])
                if nearGapStat[-0.01] == 0:
                    if len(small_near_tmp) == 3:
                        if small_near_gap_tmp[0] == small_near_gap_tmp[1] and small_near_gap_tmp[1] == small_near_gap_tmp[2]:
                            arr.add(small_near_tmp[0])
                            arr.add(small_near_tmp[1])
                            arr.add(small_near_tmp[2])
            print('参差不齐接近时小的偏多' + extraSmall(seq))
        elif len(seq['big']) + len(seq['bigNear']) >= 7:
            if len(big_tmp) >= len(small_tmp) and len(big_tmp) >= len(small_near_tmp):
                if gapStat[0.02] == len(big_tmp):
                    if big_gap_tmp[0] < 0.021:
                        arr.add(big_tmp[0])
                    if midJudge(big_tmp, gapStat, 0.03, False):
                        for i in range(1, len(big_tmp)):
                            if big_gap_tmp[i] < 0.03 and big_gap_tmp[i] > 0.029 and big_gap_tmp[i-1] < 0.025:
                                arr.add(big_tmp[i - 1])
                                break
                if midJudge(big_tmp, gapStat, 0.04, False):
                    pos = len(big_tmp) - gapStat[0.04]
                    arr.add(big_tmp[pos])
                    for i in range(pos + 1, len(big_tmp)):
                        if big_gap_tmp[i] - big_gap_tmp[pos] < 0.0001:
                            arr.add(big_tmp[i])
                    arr.add(big_tmp[pos - 1])
                    for i in range(pos - 2, -1, -1):
                        if big_gap_tmp[pos - 1] - big_gap_tmp[i] < 0.0001:
                            arr.add(big_tmp[i])
                    if big_gap_tmp[pos - 1] > 0.0283:
                        if pos - 2 > -1:
                            arr.add(big_tmp[pos - 2])
                if midJudge(big_tmp, gapStat, 0.05, True):
                    pos = len(big_tmp) - gapStat[0.05]
                    gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos, left=False)
                if midJudge(big_tmp, gapStat, 0.05, False):
                    pos = len(big_tmp) - gapStat[0.05]
                    gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos, left=False)
                if midJudge(big_tmp, gapStat, 0.03, False):
                    pos = len(big_tmp) - gapStat[0.03] - 1
                    arr.add(big_tmp[pos])
                    gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos, left=True)
                    gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos + 1, left=False)
                if midJudge(big_tmp, gapStat, 0.03, True):
                    pos = len(big_tmp) - gapStat[0.03] - 1
                    gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos, left=True)
                    gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos + 1, left=False)
                if midJudge(big_tmp, gapStat, 0.02, True):
                    pos = len(big_tmp) - gapStat[0.02]
                    gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos, left=False)
                    gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos - 1, left=True)
                if len(big_tmp) == 2:
                    if gapStat[0.03] >= 1:
                        arr.add(big_tmp[1])
            if len(big_near_tmp) >= len(small_tmp) and len(big_near_tmp) - len(small_near_tmp) >= -1:
                if big_near_gap_tmp[0] == big_near_gap_tmp[-1]:
                    for v in big_near_tmp:
                        arr.add(v)
                if len(big_near_tmp) == 2:
                    if nearGapStat[0.01] == 0:
                        if big_near_gap_tmp[1] > 0.007 and big_near_gap_tmp[0] < 0.0009:
                            arr.add(big_near_tmp[1])
                if midJudge(big_near_tmp, nearGapStat, 0.01, False):
                    if big_near_gap_tmp[0] < 0.005:
                        arr.add(big_near_tmp[0])
                    pos = len(big_near_tmp) - nearGapStat[0.01]
                    gapAndConsecutive(arr, big_near_tmp, big_near_gap_tmp, pos - 1, left=True)
                    if pos - 1 > -1 and pos - 2 > -1:
                        if big_near_gap_tmp[pos - 1] > 0.007:
                            arr.add(big_near_tmp[pos - 2])
                    if big_near_gap_tmp[pos - 1] > 0.009 and big_near_gap_tmp[pos - 1] < 0.01 and pos - 2 > -1 and big_near_gap_tmp[pos - 2] < 0.008:
                        arr.add(big_near_tmp[pos - 2])
                    arr.add(big_near_tmp[pos])
                    if pos + 1 < len(big_near_tmp) and big_near_gap_tmp[pos + 1] > 0.012 and big_near_gap_tmp[pos] < 0.012:
                        arr.add(big_near_tmp[pos + 1])
                    findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=True, choose_single=True)
                    if noConsecutiveGap(big_near_gap_tmp):
                        if big_near_gap_tmp[0] < 0.0005:
                            arr.add(big_near_tmp[0])
                    findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=True, choose_single=False, remove_tiny=True)
                if midJudge(big_near_tmp, nearGapStat, 0.01, True):
                    pos = len(big_near_tmp) - nearGapStat[0.01]
                    arr.add(big_near_tmp[pos])
                    for i in range(pos + 1, len(big_near_tmp)):
                        if big_near_gap_tmp[i] - big_near_gap_tmp[pos] < 0.00001:
                            arr.add(big_near_tmp[i])
                    arr.add(big_near_tmp[pos - 1])
                if nearGapStat[0.01] == 0:
                    if big_near_gap_tmp[-1] > 0.009:
                        arr.add(big_near_tmp[-1])
                    findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=False, choose_single=False)
                    findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=True, choose_single=False)
            if len(small_near_tmp) == 2:
                if small_near_gap_tmp[0] == small_near_gap_tmp[1]:
                    arr.add(small_near_tmp[0])
                    arr.add(small_near_tmp[1])
                if nearGapStat[-0.01] == 0:
                    if noConsecutiveGap(small_near_gap_tmp):
                        arr.add(small_near_tmp[0])
                        arr.add(small_near_tmp[1])
                if nearGapStat[-0.01] == 1:
                    arr.add(small_near_tmp[0])
                    arr.add(small_near_tmp[1])
            if len(small_near_tmp) > len(big_near_tmp):
                if midJudge(small_near_tmp, nearGapStat, -0.01, True):
                    pos = nearGapStat[-0.01] - 1
                    gapAndConsecutive(arr, small_near_tmp, small_near_gap_tmp, pos, left=True)
                if midJudge(small_near_tmp, nearGapStat, -0.01, False):
                    pos = nearGapStat[-0.01]
                    arr.add(small_near_tmp[pos])
                    for i in range(pos + 1, len(small_near_tmp)):
                        if small_near_gap_tmp[i] - small_near_gap_tmp[pos] < 0.0001:
                            arr.add(small_near_tmp[i])
            if len(small_near_tmp) == 1:
                arr.add(small_near_tmp[0])
            if len(small_near_tmp) - len(big_tmp) >= -1 or len(small_near_tmp) >= len(big_near_tmp):
                if nearGapStat[-0.01] == 0:
                    findTurn(arr, small_near_tmp, small_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=False, choose_single=True)
                if len(small_near_tmp) == 2:
                    if nearGapStat[-0.01] == 0:
                        if noConsecutiveGap(small_near_gap_tmp):
                            if small_near_gap_tmp[1] > -0.001:
                                arr.add(small_near_tmp[1])
                if midJudge(small_near_tmp, nearGapStat, -0.01, False):
                    pos = nearGapStat[-0.01] - 1
                    gapAndConsecutive(arr, small_near_tmp, small_near_gap_tmp, pos, left=True)
                    gapAndConsecutive(arr, small_near_tmp, small_near_gap_tmp, pos + 1, left=False)
                if midJudge(small_near_tmp, nearGapStat, -0.01, True):
                    pos = nearGapStat[-0.01]
                    gapAndConsecutive(arr, small_near_tmp, small_near_gap_tmp, pos, left=False)
            if len(small_tmp) == 1:
                if gapStat[-0.03] == 0:
                    arr.add(small_tmp[0])
            print('参差不齐接近时大的偏多' + extraBig(seq))
        elif len(seq['small']) + len(seq['smallNear']) > len(seq['big']) + len(seq['bigNear']):
            if len(small_tmp) - len(big_tmp) >= -1 and len(small_tmp) >= len(big_near_tmp):
                if len(small_tmp) == 2:
                    if gapStat[-0.02] == 1:
                        arr.add(small_tmp[-1])
                    if gapStat[-0.03] == 1:
                        arr.add(small_tmp[0])
                if midJudge(small_tmp, gapStat, -0.02, True):
                    if small_gap_tmp[0] > -0.03 and small_gap_tmp[0] < -0.028:
                        arr.add(small_tmp[0])
                if midJudge(small_tmp, gapStat, -0.03, False):
                    pos = gapStat[-0.03]
                    gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos, left=False)
                    gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos - 1, left=True)
                if midJudge(small_tmp, gapStat, -0.04, False):
                    pos = gapStat[-0.04] - 1
                    gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos, left=True)
                    gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos + 1, left=False)
                if gapStat[-0.02] == len(small_tmp):
                    if gapStat[-0.03] == 0:
                        findTurn(arr, small_tmp, small_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=False, choose_single=True)
            if len(small_tmp) == 1:
                if gapStat[-0.04] == 0:
                    arr.add(small_tmp[0])
            if len(small_near_tmp) >= len(big_tmp) and len(small_near_tmp) - len(big_near_tmp) >= -1:
                if len(small_near_tmp) == 2:
                    if nearGapStat[-0.01] == 1:
                        arr.add(small_near_tmp[1])
                if midJudge(small_near_tmp, nearGapStat, -0.01, False):
                    if noConsecutiveGap(small_near_gap_tmp):
                        arr.add(small_near_tmp[-1])
                    if small_near_gap_tmp[0] <= -0.0139:
                        arr.add(small_near_tmp[0])
                    pos = nearGapStat[-0.01] - 1
                    arr.add(small_near_tmp[pos])
                    arr.add(small_near_tmp[pos + 1])
                    for i in range(pos + 2, len(small_near_tmp)):
                        if small_near_gap_tmp[i] - small_near_gap_tmp[pos + 1] < 0.0001:
                            arr.add(small_near_tmp[i])
                    findTurn(arr, small_near_tmp, small_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=True, consecutive_at_left=True, choose_single=False)
                    findTurn(arr, small_near_tmp, small_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=True, consecutive_at_left=False, choose_single=False)
                if midJudge(small_near_tmp, nearGapStat, -0.01, True):
                    if noConsecutiveGap(small_near_gap_tmp):
                        pos = nearGapStat[-0.01] - 1
                        if small_near_gap_tmp[pos] > -0.0113 and pos - 1 > -1:
                            arr.add(small_near_tmp[pos - 1])
                    pos = nearGapStat[-0.01]
                    arr.add(small_near_tmp[pos])
                if nearGapStat[-0.01] == 0:
                    if noConsecutiveGap(small_near_gap_tmp):
                        arr.add(small_near_tmp[0])
                        if small_near_gap_tmp[0] < -0.009:
                            arr.add(small_near_tmp[1])
                        if small_near_gap_tmp[-1] > -0.002:
                            arr.add(small_near_tmp[-2])
            if len(big_near_tmp) - len(small_tmp) >= -1 and len(big_near_tmp) - len(small_near_tmp) >= -2:
                if len(big_near_tmp) == 2:
                    if nearGapStat[0.01] == 1:
                        arr.add(big_near_tmp[1])
                if nearGapStat[0.01] == 0:
                    findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=True, choose_single=False)
                    if big_near_gap_tmp[0] < 0.0005:
                        arr.add(big_near_tmp[0])
                if len(big_near_tmp) == 2:
                    if nearGapStat[0.01] == 1:
                        arr.add(big_near_tmp[1])
                if midJudge(big_near_tmp, nearGapStat, 0.01, False):
                    for i in range(len(big_near_tmp) - 1):
                        if big_near_gap_tmp[i] < 0.0005 and big_near_gap_tmp[i+1] > 0.001:
                            arr.add(big_near_tmp[i])
                            break
                    pos = len(big_near_tmp) - nearGapStat[0.01] - 1
                    gapAndConsecutive(arr, big_near_tmp, big_near_gap_tmp, pos, left=True)
                if midJudge(big_near_tmp, nearGapStat, 0.01, True):
                    pos = len(big_near_tmp) - nearGapStat[0.01]
                    arr.add(big_near_tmp[pos])
                    for i in range(pos + 1, len(big_near_tmp)):
                        if big_near_gap_tmp[i] - big_near_gap_tmp[pos] < 0.0001:
                            arr.add(big_near_tmp[i])
                    arr.add(big_near_tmp[pos - 1])
            if len(big_tmp) - len(small_tmp) >= -1 and len(big_tmp) - len(small_near_tmp) >= -2:
                if len(big_tmp) == gapStat[0.02]:
                    if big_gap_tmp[1] > 0.029 and big_gap_tmp[1] < 0.03:
                        arr.add(big_tmp[0])
                if midJudge(big_tmp, gapStat, 0.05, False):
                    pos = len(big_tmp) - gapStat[0.05] - 1
                    gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos, left=True)
                if midJudge(big_tmp, gapStat, 0.04, True):
                    pos = len(big_tmp) - gapStat[0.04]
                    gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos, left=False)
                if midJudge(big_tmp, gapStat, 0.04, False):
                    pos = len(big_tmp) - gapStat[0.04]
                    if big_gap_tmp[pos] < 0.042:
                        arr.add(big_tmp[pos + 1])
                    gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos - 1, left=True)
                if midJudge(big_tmp, gapStat, 0.03, False):
                    pos = len(big_tmp) - gapStat[0.03]
                    arr.add(big_tmp[pos])
                if len(big_tmp) == 2:
                    if big_gap_tmp[0] < 0.021:
                        arr.add(big_tmp[0])
            elif len(big_tmp) - len(small_near_tmp) >= -1:
                if gapStat[0.03] == 0:
                    arr.add(big_tmp[0])
            print('参差不齐接近时小的比大的多一些' + extraSmall(seq))
        elif len(seq['small']) + len(seq['smallNear']) < len(seq['big']) + len(seq['bigNear']):
            if len(big_tmp) >= len(small_tmp) and len(big_tmp) >= len(small_near_tmp):
                if midJudge(big_tmp, gapStat, 0.02, True):
                    pos = len(big_tmp) - gapStat[0.02] - 1
                    gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos, left=True)
                    gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos + 1, left=False)
                if midJudge(big_tmp, gapStat, 0.03, False):
                    pos = len(big_tmp) - gapStat[0.03]
                    arr.add(big_tmp[pos])
                if midJudge(big_tmp, gapStat, 0.05, False):
                    pos = len(big_tmp) - gapStat[0.05] - 1
                    gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos, left=True)
                if midJudge(big_tmp, gapStat, 0.04, False):
                    pos = len(big_tmp) - gapStat[0.04]
                    arr.add(big_tmp[pos])
                    if pos + 1 < len(big_tmp) and big_gap_tmp[pos] < 0.043:
                        arr.add(big_tmp[pos + 1])
                if len(big_tmp) == gapStat[0.04]:
                    if midJudge(big_tmp, gapStat, 0.05, False):
                        findTurn(arr, big_tmp, big_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=True, choose_single=False)
                if len(big_tmp) == gapStat[0.02]:
                    if big_gap_tmp[0] < 0.021:
                        arr.add(big_tmp[0])
            if len(big_near_tmp) >= len(small_tmp) and len(big_near_tmp) - len(small_near_tmp) >= -1:
                if midJudge(big_near_tmp, nearGapStat, 0.01, False):
                    if noConsecutiveGap(big_near_gap_tmp):
                        if big_near_gap_tmp[0] < 0.005:
                            arr.add(big_near_tmp[0])
                    pos = len(big_near_tmp) - nearGapStat[0.01]
                    arr.add(big_near_tmp[pos])
                    if big_near_gap_tmp[pos - 1] > 0.008:
                        if pos - 2 > -1:
                            arr.add(big_near_tmp[pos - 2])
                    gapAndConsecutive(arr, big_near_tmp, big_near_gap_tmp, pos - 1, left=True)
                    findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=True, choose_single=False)
                    findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=False, choose_single=True)
                if midJudge(big_near_tmp, nearGapStat, 0.01, True):
                    pos = len(big_near_tmp) - nearGapStat[0.01]
                    arr.add(big_near_tmp[pos])
                    for i in range(len(big_near_tmp) - 2, -1, -1):
                        if i > -1 and big_near_gap_tmp[i] > 0.01 and big_near_gap_tmp[i] < 0.012 and big_near_gap_tmp[i+1] > 0.012:
                            arr.add(big_near_tmp[i+1])
                            break
                    gapAndConsecutive(arr, big_near_tmp, big_near_gap_tmp, pos - 1, left=True)
                if nearGapStat[0.01] == 0:
                    findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=True, consecutive_at_left=False, choose_single=False)
                    if noConsecutiveGap(big_near_gap_tmp):
                        arr.add(big_near_tmp[-2])
                    if len(big_near_tmp) > 2 and big_near_gap_tmp[1] - big_near_gap_tmp[0] == big_near_gap_tmp[2] - big_near_gap_tmp[1]:
                        arr.add(big_near_tmp[0])
                        for i in range(1, len(big_near_tmp)):
                            if big_near_gap_tmp[i] - big_near_gap_tmp[0] < 0.001:
                                arr.add(big_near_tmp[i])
                if len(big_near_tmp) == 2:
                    if nearGapStat[0.01] == 1:
                        arr.add(big_near_tmp[1])
            if len(big_tmp) == 2:
                if gapStat[0.03] == 2 and gapStat[0.04] == 1:
                    arr.add(big_tmp[1])
                if gapStat[0.03] == 2 and gapStat[0.04] == 0:
                    if big_gap_tmp[0] > 0.0301:
                        arr.add(big_tmp[0])
                        if big_gap_tmp[1] - big_gap_tmp[0] < 0.0001:
                            arr.add(big_tmp[1])
                    else:
                        arr.add(big_tmp[1])
                if gapStat[0.02] == 1:
                    arr.add(big_tmp[1])
            if len(small_tmp) >= len(big_tmp):
                if len(small_tmp) == 2:
                    if gapStat[-0.02] == 1:
                        arr.add(small_tmp[1])
                        if small_gap_tmp[0] < -0.029:
                            arr.add(small_tmp[0])
            if len(small_tmp) - len(big_near_tmp) >= -2 and len(small_tmp) - len(big_tmp) >= -1:
                if midJudge(small_tmp, gapStat, -0.03, False):
                    pos = gapStat[-0.03] - 1
                    gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos, left=True)
                if len(small_tmp) == 2:
                    if gapStat[-0.03] == 1:
                        arr.add(small_tmp[0])
                    if gapStat[-0.02] == 2:
                        if small_gap_tmp[0] < -0.0285:
                            arr.add(small_tmp[1])
            if len(small_tmp) == 1:
                if gapStat[-0.03] == 0:
                    arr.add(small_tmp[0])
            if len(small_near_tmp) == 2:
                if nearGapStat[-0.01] == 1:
                    arr.add(small_near_tmp[0])
                if nearGapStat[-0.01] == 0:
                    if noConsecutiveGap(small_near_gap_tmp):
                        arr.add(small_near_tmp[0])
            if len(small_near_tmp) - len(big_near_tmp) >= -1 and len(small_near_tmp) - len(big_tmp) >= -1:
                if small_near_gap_tmp[0] == small_near_gap_tmp[-1]:
                    for v in small_near_tmp:
                        arr.add(v)
                if nearGapStat[-0.01] == 0:
                    if small_near_gap_tmp[-1] > -0.0005:
                        arr.add(small_near_tmp[-1])
                    findTurn(arr, small_near_tmp, small_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=True, choose_single=False)
                    findTurn(arr, small_near_tmp, small_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=False, choose_single=True)
                    findTurn(arr, small_near_tmp, small_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=False, choose_single=False)
                    if noConsecutiveGap(small_near_gap_tmp):
                        if small_near_gap_tmp[-1] > -0.002:
                            arr.add(small_near_tmp[-2])
                        if small_near_gap_tmp[0] < -0.006:
                            arr.add(small_near_tmp[0])
                        for i in range(len(small_near_tmp) - 1, -1, -1):
                            if small_near_gap_tmp[i] > -0.0005 and i - 1 > -1 and small_near_gap_tmp[i-1] < -0.002:
                                arr.add(small_near_tmp[i-1])
                                break
                if midJudge(small_near_tmp, nearGapStat, -0.01, False):
                    if small_near_gap_tmp[-1] > -0.002:
                        arr.add(small_near_tmp[-2])
                    pos = nearGapStat[-0.01]
                    gapAndConsecutive(arr, small_near_tmp, small_near_gap_tmp, pos - 1, left=True)
                    gapAndConsecutive(arr, small_near_tmp, small_near_gap_tmp, pos, left=False)
                    findTurn(arr, small_near_tmp, small_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=True, consecutive_at_left=False, choose_single=False)
                if midJudge(small_near_tmp, nearGapStat, -0.01, True):
                    for i in range(1, len(small_near_tmp)):
                        if small_near_gap_tmp[i] < -0.01 and small_near_gap_tmp[i] > -0.0104:
                            if small_near_gap_tmp[i-1] < -0.012:
                                arr.add(small_near_tmp[i-1])
                                break
                    pos = nearGapStat[-0.01] - 1
                    arr.add(small_near_tmp[pos])
                    for i in range(pos - 1, -1, -1):
                        if small_near_gap_tmp[pos] - small_near_gap_tmp[i] < 0.0001:
                            arr.add(small_near_tmp[i])
                if nearGapStat[-0.01] == len(small_near_tmp):
                    findTurn(arr, small_near_tmp, small_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=False, choose_single=True)
                if len(small_near_tmp) == 2:
                    if small_near_gap_tmp[1] > -0.0007 and small_near_gap_tmp[0] < -0.006:
                        arr.add(small_near_tmp[1])
            print('参差不齐接近时大的比小的多一些' + extraBig(seq))
        else:
            if len(big_tmp) >= len(small_tmp) and len(big_tmp) - len(small_near_tmp) >= -1:
                if midJudge(big_tmp, gapStat, 0.02, True):
                    pos = len(big_tmp) - gapStat[0.02] - 1
                    arr.add(big_tmp[pos])
                if midJudge(big_tmp, gapStat, 0.03, False):
                    pos = len(big_tmp) - gapStat[0.03]
                    arr.add(big_tmp[pos])
                if midJudge(big_tmp, gapStat, 0.03, True):
                    pos = len(big_tmp) - gapStat[0.03]
                    if big_gap_tmp[pos] < 0.035 and pos + 1 < len(big_tmp) and big_gap_tmp[pos + 1] > 0.038:
                        arr.add(big_tmp[pos + 1])
                    else:
                        arr.add(big_tmp[pos])
                        for i in range(pos + 1, len(big_tmp)):
                            if big_gap_tmp[i] - big_gap_tmp[pos] < 0.0001:
                                arr.add(big_tmp[i])
                    arr.add(big_tmp[pos - 1])
                    for i in range(pos - 2, -1, -1):
                        if big_gap_tmp[pos - 1] - big_gap_tmp[i] < 0.0001:
                            arr.add(big_tmp[i])
                if midJudge(big_tmp, gapStat, 0.04, False):
                    pos = len(big_tmp) - gapStat[0.04] - 1
                    arr.add(big_tmp[pos])
                    for i in range(pos - 1, -1, -1):
                        if big_gap_tmp[pos] - big_gap_tmp[i] < 0.0001:
                            arr.add(big_tmp[i])
                    if big_gap_tmp[pos] > 0.0281:
                        if pos - 1 > -1:
                            arr.add(big_tmp[pos - 1])
                if midJudge(big_tmp, gapStat, 0.04, True):
                    pos = len(big_tmp) - gapStat[0.04]
                    arr.add(big_tmp[pos])
                    for i in range(pos + 1, len(big_tmp)):
                        if big_gap_tmp[i] - big_gap_tmp[pos] < 0.0001:
                            arr.add(big_tmp[i])
                if midJudge(big_tmp, gapStat, 0.06, True):
                    pos = len(big_tmp) - gapStat[0.06]
                    gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos, left=False)
                if midJudge(big_tmp, gapStat, 0.05, True):
                    pos = len(big_tmp) - gapStat[0.05] - 1
                    gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos, left=True)
                if len(big_tmp) == gapStat[0.02]:
                    if big_gap_tmp[0] < 0.022 and big_gap_tmp[1] < 0.03:
                        arr.add(big_tmp[0])
            if len(big_tmp) == 2:
                if gapStat[0.02] == 1:
                    arr.add(big_tmp[0])
                    if big_gap_tmp[-1] > 0.028:
                        arr.add(big_tmp[-1])
                if gapStat[0.02] == 2 and gapStat[0.03] <= 1:
                    if big_gap_tmp[0] < 0.022 and big_gap_tmp[1] > 0.025:
                        arr.add(big_tmp[0])
                    if big_gap_tmp[1] > 0.0295:
                        arr.add(big_tmp[1])
            if len(small_near_tmp) - len(big_tmp) >= -1 and len(small_near_tmp) - len(big_near_tmp) >= -1:
                if midJudge(small_near_tmp, nearGapStat, -0.01, False):
                    pos = nearGapStat[-0.01] - 1
                    if small_near_gap_tmp[pos + 1] < -0.009:
                        arr.add(small_near_tmp[pos + 2])
                    arr.add(small_near_tmp[pos])
                    arr.add(small_near_tmp[pos + 1])
                    for i in range(pos + 2, len(small_near_tmp)):
                        if small_near_gap_tmp[i] - small_near_gap_tmp[pos + 1] < 0.0001:
                            arr.add(small_near_tmp[i])
                    if small_near_gap_tmp[-1] > -0.0034 and small_near_gap_tmp[-2] < -0.0075:
                        arr.add(small_near_tmp[-1])
                if midJudge(small_near_tmp, nearGapStat, -0.01, True):
                    pos = nearGapStat[-0.01] - 1
                    gapAndConsecutive(arr, small_near_tmp, small_near_gap_tmp, pos, left=True)
                    if small_near_gap_tmp[pos] > -0.0117:
                        if pos - 1 > -1:
                            arr.add(small_near_tmp[pos - 1])
                    findTurn(arr, small_near_tmp, small_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=True, choose_single=False)
                if nearGapStat[-0.01] == 0:
                    findTurn(arr, small_near_tmp, small_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=True, choose_single=False)
                    if small_near_gap_tmp[0] < -0.009:
                        arr.add(small_near_tmp[1])
            if len(small_tmp) - len(big_tmp) >= -1 and len(small_tmp) - len(big_near_tmp) >= -1:
                if gapStat[-0.02] == 1:
                    arr.add(small_tmp[0])
                if midJudge(small_tmp, gapStat, -0.03, False):
                    pos = gapStat[-0.03] - 1
                    arr.add(small_tmp[pos])
                    for i in range(pos - 1, -1, -1):
                        if small_gap_tmp[pos] - small_gap_tmp[i] < 0.0001:
                            arr.add(small_tmp[i])
                    if gapStat[-0.02] == len(small_tmp):
                        findTurn(arr, small_tmp, small_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=True, choose_single=True)
                if len(big_near_tmp) == 2:
                    if nearGapStat[0.01] == 0:
                        if big_near_gap_tmp[0] > 0.009:
                            arr.add(big_near_tmp[1])
            if len(small_tmp) == len(big_tmp):
                if len(small_tmp) == 2:
                    if gapStat[-0.04] == 1:
                        arr.add(small_tmp[0])
                if gapStat[-0.02] == 1:
                    if small_gap_tmp[0] < -0.029:
                        arr.add(small_tmp[0])
                if midJudge(big_near_tmp, nearGapStat, 0.01, True):
                    arr.add(big_near_tmp[0])
            if len(big_near_tmp) - len(small_tmp) >= -1 and len(big_near_tmp) - len(big_tmp) >= -1:
                if nearGapStat[0.01] == 0:
                    if big_near_gap_tmp[0] < 0.003:
                        arr.add(big_near_tmp[0])
                    if noConsecutiveGap(big_near_gap_tmp):
                        if big_near_gap_tmp[-1] > 0.009:
                            arr.add(big_near_tmp[-2])
                    findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=True, choose_single=False)
                if midJudge(big_near_tmp, nearGapStat, 0.01, True):
                    for i in range(len(big_near_tmp) - 1, -1, -1):
                        if i + 1 < len(big_near_tmp) and big_near_gap_tmp[i] >= 0.01 and big_near_gap_tmp[i] < 0.011 and big_near_gap_tmp[i+1] > 0.011:
                            arr.add(big_near_tmp[i+1])
                            break
                if midJudge(big_near_tmp, nearGapStat, 0.01, False):
                    if noConsecutiveGap(big_near_gap_tmp):
                        if big_near_gap_tmp[0] < 0.0024 and big_near_gap_tmp[1] > 0.005:
                            arr.add(big_near_tmp[0])
                    pos = len(big_near_tmp) - nearGapStat[0.01]
                    arr.add(big_near_tmp[pos])
                    arr.add(big_near_tmp[pos - 1])
                    findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=False, choose_single=False)
                    findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=False, choose_single=True)
            if len(small_tmp) == 1:
                if gapStat[-0.04] == 0:
                    arr.add(small_tmp[0])
            if len(small_near_tmp) == 2 and len(small_near_tmp) > len(big_tmp):
                if nearGapStat[-0.01] == 1:
                    arr.add(small_near_tmp[0])
                if nearGapStat[-0.01] == 0:
                    arr.add(small_near_tmp[1])
            if len(small_tmp) - len(big_tmp) >= -1 and len(small_tmp) - len(big_near_tmp) >= -1:
                if small_gap_tmp[0] == small_gap_tmp[-1]:
                    for v in small_tmp:
                        arr.add(v)
                if midJudge(small_tmp, gapStat, -0.04, False):
                    pos = gapStat[-0.04]
                    if small_gap_tmp[pos - 1] > -0.041:
                        arr.add(small_tmp[pos])
                        for i in range(pos + 1, len(small_tmp)):
                            if small_gap_tmp[i] - small_gap_tmp[pos] < 0.0001:
                                arr.add(small_tmp[i])
                if midJudge(small_tmp, gapStat, -0.03, True):
                    pos = gapStat[-0.03]
                    arr.add(small_tmp[pos])
                if midJudge(small_tmp, gapStat, -0.02, True):
                    pos = gapStat[-0.02]
                    arr.add(small_tmp[pos])
                    for i in range(pos + 1, len(small_tmp)):
                        if small_gap_tmp[i] - small_gap_tmp[pos] < 0.0001:
                            arr.add(small_tmp[i])
                    arr.add(small_tmp[pos - 1])
                    for i in range(pos - 2, -1, -1):
                        if small_gap_tmp[pos - 1] - small_gap_tmp[i] < 0.0001:
                            arr.add(small_tmp[i])
                if len(small_tmp) == gapStat[-0.02]:
                    if noConsecutiveGap(small_gap_tmp):
                        if small_gap_tmp[-2] < -0.028:
                            arr.add(small_tmp[-1])
                    if gapStat[-0.03] == 0:
                        findTurn(arr, small_tmp, small_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=True, choose_single=False)
                        findTurn(arr, small_tmp, small_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=False, choose_single=False)
                        findTurn(arr, small_tmp, small_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=True, choose_single=True)
                if len(small_tmp) == 2:
                    if small_gap_tmp[1] > -0.0156 and small_gap_tmp[0] < -0.0168:
                        arr.add(small_tmp[1])
            print('参差不齐接近时大小一样')
    #连续接近
    elif count['near'] >= 5 and maxConsecutiveCount['near'] >= 4:
        if len(seq['small']) + len(seq['smallNear']) >= 7:
            if len(big_tmp) >= len(small_tmp) and len(big_tmp) == 1:
                if gapStat[0.03] == 0:
                    arr.add(big_tmp[0])
            print('连续接近时小的偏多' + extraSmall(seq))
        elif len(seq['big']) + len(seq['bigNear']) >= 7:
            print('连续接近时大的偏多' + extraBig(seq))
        elif len(seq['small']) + len(seq['smallNear']) > len(seq['big']) + len(seq['bigNear']):
            if len(small_near_tmp) >= len(big_near_tmp) and len(small_near_tmp) >= len(big_tmp):
                if midJudge(small_near_tmp, nearGapStat, -0.01, True):
                    if small_gap_tmp[0] < -0.014:
                        arr.add(small_near_tmp[0])
                if midJudge(small_near_tmp, nearGapStat, -0.01, False):
                    pos = nearGapStat[-0.01]
                    arr.add(small_near_tmp[pos])
            if len(big_near_tmp) - len(small_tmp) >= -1 and len(big_near_tmp) - len(small_near_tmp) >= -1:
                if len(big_near_tmp) == 2:
                    if nearGapStat[0.01] == 2:
                        if big_near_gap_tmp[0] < 0.0105 and big_near_gap_tmp[1] > 0.012:
                            arr.add(big_near_tmp[0])
            print('连续接近时小的比大的多一些' + extraSmall(seq))
        elif len(seq['small']) + len(seq['smallNear']) < len(seq['big']) + len(seq['bigNear']):
            print('连续接近时大的比小的多一些' + extraBig(seq))
        else:
            if len(big_near_tmp) >= len(small_tmp) and len(big_near_tmp) >= len(small_near_tmp):
                if midJudge(big_near_tmp, nearGapStat, 0.01, False):
                    if noConsecutiveGap(big_near_gap_tmp):
                        for i in range(0, len(big_near_tmp)):
                            if big_near_gap_tmp[i] < 0.001 and big_near_gap_tmp[i+1] > 0.002:
                                arr.add(big_near_tmp[i+1])
                                break
            print('连续接近时大小一样')
    elif count['small'] >= 5 and maxConsecutiveCount['small'] < 4:
        if gapStat[-0.02] == len(small_tmp):
            findTurn(arr, small_tmp, small_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=True, choose_single=False)
            findTurn(arr, small_tmp, small_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=True, consecutive_at_left=False, choose_single=False)
            findTurn(arr, small_tmp, small_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=True, consecutive_at_left=True, choose_single=True)
            for i in range(len(small_tmp) - 1, -1, -1):
                if small_gap_tmp[i] > -0.021 and small_gap_tmp[i-1] < -0.0215:
                    arr.add(small_tmp[i])
                    break
                if small_gap_tmp[i] > -0.03 and small_gap_tmp[i] < -0.029 and i + 1 < len(small_gap_tmp) and small_gap_tmp[i+1] > -0.028:
                    arr.add(small_tmp[i+1])
                    break
            if midJudge(small_tmp, gapStat, -0.03, True):
                findTurn(arr, small_tmp, small_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=True, consecutive_at_left=False, choose_single=False)
        if midJudge(small_tmp, gapStat, -0.02, True):
            for i in range(len(small_tmp) - 2, -1, -1):
                if small_gap_tmp[i] > -0.02 and small_gap_tmp[i] < -0.0195 and small_gap_tmp[i+1] > -0.019:
                    arr.add(small_tmp[i+1])
                    break
            pos = gapStat[-0.02]
            gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos, left=False)
            if small_gap_tmp[pos] < -0.018 and pos + 1 < len(small_tmp):
                arr.add(small_tmp[pos + 1])
            arr.add(small_tmp[pos - 1])
            findTurn(arr, small_tmp, small_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=True, consecutive_at_left=True, choose_single=True)
        if midJudge(small_tmp, gapStat, -0.03, True):
            pos = gapStat[-0.03]
            arr.add(small_tmp[pos])
            arr.add(small_tmp[pos - 1])
            if small_gap_tmp[pos - 1] > -0.0302:
                arr.add(small_tmp[pos - 2])
            gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos - 1, left=True)
        if midJudge(small_tmp, gapStat, -0.06, False):
            pos = gapStat[-0.06]
            arr.add(small_tmp[pos])
        if midJudge(small_tmp, gapStat, -0.05, False):
            pos = gapStat[-0.05] - 1
            arr.add(small_tmp[pos])
            arr.add(small_tmp[pos + 1])
            findTurn(arr, small_tmp, small_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=True, choose_single=False)
            if small_gap_tmp[0] < -0.058:
                arr.add(small_tmp[0])
        if midJudge(small_tmp, gapStat, -0.04, True):
            pos = gapStat[-0.04] - 1
            arr.add(small_tmp[pos])
            arr.add(small_tmp[pos + 1])
            for i in range(pos - 1, -1, -1):
                if small_gap_tmp[pos] - small_gap_tmp[i] < 0.0001:
                    arr.add(small_tmp[i])
            if small_gap_tmp[-2] < -0.038:
                arr.add(small_tmp[-1])
        if midJudge(small_tmp, gapStat, -0.04, False):
            if small_gap_tmp[0] < -0.049:
                arr.add(small_tmp[0])
            pos = gapStat[-0.04] - 1
            arr.add(small_tmp[pos])
            arr.add(small_tmp[pos + 1])
            gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos, left=True)
            gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos + 1, left=False)
            if small_gap_tmp[pos + 1] < -0.038 and pos + 2 < len(small_tmp) and small_gap_tmp[pos + 2] > -0.037:
                arr.add(small_tmp[pos + 2])
        if midJudge(small_tmp, gapStat, -0.03, False):
            if small_gap_tmp[0] > -0.04 and small_gap_tmp[0] < -0.0385:
                arr.add(small_tmp[0])
            pos = gapStat[-0.03]
            if small_gap_tmp[pos - 1] > -0.0312:
                if pos - 2 > -1:
                    arr.add(small_tmp[pos - 2])
            arr.add(small_tmp[pos])
            if small_gap_tmp[pos] < -0.028 and pos + 1 < len(small_tmp) and small_gap_tmp[pos + 1] > -0.028:
                arr.add(small_tmp[pos + 1])
            for i in range(pos + 1, len(small_tmp)):
                if small_gap_tmp[i] - small_gap_tmp[pos] < 0.00001:
                    arr.add(small_tmp[i])
            gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos - 1, left=True)
        if len(small_near_tmp) - len(big_near_tmp) >= -1 and len(small_near_tmp) >= len(big_tmp):
            if nearGapStat[-0.01] == 0:
                findTurn(arr, small_near_tmp, small_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=False, choose_single=True)
            if len(small_near_tmp) == 2:
                if nearGapStat[-0.01] == 1:
                    arr.add(small_near_tmp[0])
                    arr.add(small_near_tmp[-1])
                if nearGapStat[-0.01] == 0:
                    if small_near_gap_tmp[0] < -0.007 and small_near_gap_tmp[1] > -0.003:
                        arr.add(small_near_tmp[0])
                    if small_near_gap_tmp[0] < -0.006 and small_near_gap_tmp[1] > -0.005:
                        arr.add(small_near_tmp[1])
                    if small_near_gap_tmp[0] < -0.003 and small_near_gap_tmp[1] > -0.0015:
                        arr.add(small_near_tmp[1])
                        arr.add(small_near_tmp[0])
                    if small_near_gap_tmp[0] == small_near_gap_tmp[1]:
                        arr.add(small_near_tmp[0])
                        arr.add(small_near_tmp[1])
                if nearGapStat[-0.01] == 2:
                    if small_near_gap_tmp[0] == small_near_gap_tmp[1]:
                        arr.add(small_near_tmp[0])
                        arr.add(small_near_tmp[1])
            elif len(small_near_tmp) > 2:
                if midJudge(small_near_tmp, nearGapStat, -0.01, False):
                    pos = nearGapStat[-0.01] - 1
                    gapAndConsecutive(arr, small_near_tmp, small_near_gap_tmp, pos, left=True)
                    gapAndConsecutive(arr, small_near_tmp, small_near_gap_tmp, pos + 1, left=False)
                    if small_near_gap_tmp[-1] > -0.001 and small_near_gap_tmp[-2] < -0.007:
                        arr.add(small_near_tmp[-1])
                if midJudge(small_near_tmp, nearGapStat, -0.01, True):
                    pos = nearGapStat[-0.01]
                    gapAndConsecutive(arr, small_near_tmp, small_near_gap_tmp, pos, left=False)
                    if noConsecutiveGap(small_near_gap_tmp):
                        for i in range(1, len(small_near_tmp)):
                            if small_near_gap_tmp[i] < -0.01 and small_near_gap_tmp[i] > -0.0115 and small_near_gap_tmp[i-1] < -0.012:
                                arr.add(small_near_tmp[i])
                                break
                    else:
                        pos = nearGapStat[-0.01] - 1
                        arr.add(small_near_tmp[pos])
                        for i in range(pos - 1, -1, -1):
                            if small_near_gap_tmp[pos] - small_near_gap_tmp[i] < 0.0001:
                                arr.add(small_near_tmp[i])
                if nearGapStat[-0.01] == 0:
                    if small_near_gap_tmp[1] - small_near_gap_tmp[0] == small_near_gap_tmp[2] - small_near_gap_tmp[1]:
                        arr.add(small_near_tmp[0])
                        arr.add(small_near_tmp[1])
                        arr.add(small_near_tmp[2])
            elif len(small_near_tmp) == 1:
                arr.add(small_near_tmp[0])
        if len(small_near_tmp) >= len(big_tmp):
            if len(small_near_tmp) == 1:
                arr.add(small_near_tmp[0])
        if len(small_near_tmp) >= len(big_near_tmp):
            if len(small_near_tmp) == 1:
                arr.add(small_near_tmp[0])
        if len(big_tmp) == 1:
            if gapStat[0.03] == 0:
                arr.add(big_tmp[0])
        if len(big_tmp) >= len(small_near_tmp):
            if len(big_tmp) == 2:
                if big_gap_tmp[0] == big_gap_tmp[1]:
                    arr.add(big_tmp[0])
                    arr.add(big_tmp[1])
                if gapStat[0.03] == 0:
                    if big_gap_tmp[0] < 0.024 and big_gap_tmp[1] > 0.026:
                        arr.add(big_tmp[0])
                if gapStat[0.02] == 2 and gapStat[0.03] == 0:
                    if big_gap_tmp[0] < 0.0214:
                        arr.add(big_tmp[1])
                if gapStat[0.02] == 2 and gapStat[0.03] == 1:
                    arr.add(big_tmp[0])
            if midJudge(big_tmp, gapStat, 0.03, False):
                pos = len(big_tmp) - gapStat[0.03]
                gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos, left=False)
            if midJudge(big_tmp, gapStat, 0.02, False):
                pos = len(big_tmp) - gapStat[0.02] - 1
                gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos, left=True)
                if big_gap_tmp[pos] > 0.018:
                    arr.add(big_tmp[pos - 1])
            if midJudge(big_tmp, gapStat, 0.02, True):
                pos = len(big_tmp) - gapStat[0.02] - 1
                arr.add(big_tmp[pos])
                for i in range(pos - 1, -1, -1):
                    if big_gap_tmp[pos] - big_gap_tmp[i] < 0.0001:
                        arr.add(big_tmp[i])
                gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos + 1, left=False)
        if len(big_near_tmp) - len(small_near_tmp) >= -2:
            if nearGapStat[0.01] == len(big_near_tmp):
                findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=True, choose_single=False)
                findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=False, choose_single=True)
                findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=False, choose_single=False)
            if len(big_near_tmp) > 1 and big_near_gap_tmp[0] == big_near_gap_tmp[-1]:
                for v in big_near_tmp:
                    arr.add(v)
            if len(big_near_tmp) <= 2 and len(big_near_tmp) > 0:
                arr.add(big_near_tmp[0])
                if len(big_near_tmp) > 1 and big_near_gap_tmp[1] > 0.008:
                    arr.add(big_near_tmp[1])
            if len(big_near_tmp) == 2:
                if nearGapStat[0.01] == 1:
                    arr.add(big_near_tmp[1])
                if nearGapStat[0.01] == 0:
                    if big_near_gap_tmp[0] < 0.0025 and big_near_gap_tmp[1] > 0.0051:
                        arr.add(big_near_tmp[1])
            if len(big_near_tmp) == 1:
                if big_near_gap_tmp[0] > 0.01 and big_near_gap_tmp[0] < 0.011:
                    arr.add(big_near_tmp[0])
            if nearGapStat[0.01] == 0 and len(big_near_tmp) > 0:
                if noConsecutiveGap(big_near_gap_tmp):
                    if len(big_near_tmp) > 1:
                        if big_near_gap_tmp[0] < 0.0034 and big_near_gap_tmp[1] > 0.0055:
                            arr.add(big_near_tmp[1])
                        if big_near_gap_tmp[0] < 0.0005 and big_near_gap_tmp[1] > 0.0029:
                            arr.add(big_near_tmp[1]) 
                        if big_near_gap_tmp[0] < 0.0029 and big_near_gap_tmp[1] > 0.005: 
                            arr.add(big_near_tmp[0])
                        if len(big_near_tmp) > 1 and big_near_gap_tmp[0] < 0.0039 and big_near_gap_tmp[1] > 0.0065:
                            arr.add(big_near_tmp[0])
                        if big_near_gap_tmp[0] < 0.0015:
                            arr.add(big_near_tmp[0])
                else:
                    findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=True, choose_single=False)
            if midJudge(big_near_tmp, nearGapStat, 0.01, True):
                pos = len(big_near_tmp) - nearGapStat[0.01]
                gapAndConsecutive(arr, big_near_tmp, big_near_gap_tmp, pos, left=False)
            if midJudge(big_near_tmp, nearGapStat, 0.01, False):
                pos = len(big_near_tmp) - nearGapStat[0.01]
                gapAndConsecutive(arr, big_near_tmp, big_near_gap_tmp, pos, left=False)
            if midJudge(big_near_tmp, nearGapStat, 0.01, False) or nearGapStat[0.01] == 0:
                findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=True, choose_single=True)
        print('参差不齐小' + restExcSmall(seq))
    elif count['big'] >= 5 and count['near'] >= 2:
        if len(big_near_tmp) == 1:
            arr.add(big_near_tmp[0])
        if len(big_tmp) >= len(small_tmp) and len(big_tmp) >= len(small_near_tmp):
            if len(big_tmp) == gapStat[0.02]:
                if midJudge(big_tmp, gapStat, 0.03, True):
                    if big_gap_tmp[0] < 0.024 and big_gap_tmp[1] > 0.0255:
                        arr.add(big_tmp[0])
                findTurn(arr, big_tmp, big_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=False, choose_single=False)
            if len(big_tmp) == gapStat[0.03]:
                if big_gap_tmp[0] < 0.03:
                    arr.add(big_tmp[1])
                    for i in range(2, len(big_tmp)):
                        if big_gap_tmp[i] - big_gap_tmp[i] < 0.0001:
                            arr.add(big_tmp[i])
            if midJudge(big_tmp, gapStat, 0.02, False):
                findTurn(arr, big_tmp, big_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=False, choose_single=True)
            if midJudge(big_tmp, gapStat, 0.02, True):
                pos = len(big_tmp) - gapStat[0.02]
                gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos, left=False)
                gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos - 1, left=True)
            if midJudge(big_tmp, gapStat, 0.03, True):
                pos = len(big_tmp) - gapStat[0.03] - 1
                gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos, left=True)
                gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos + 1, left=True)
            if midJudge(big_tmp, gapStat, 0.04, True):
                pos = len(big_tmp) - gapStat[0.04]
                gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos, left=False)
            if midJudge(big_tmp, gapStat, 0.04, False):
                findTurn(arr, big_tmp, big_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=True, consecutive_at_left=True, choose_single=False)
                pos = len(big_tmp) - gapStat[0.04]
                if big_gap_tmp[pos] < 0.045 and pos + 1 < len(big_tmp) and big_gap_tmp[pos + 1] > 0.048:
                    arr.add(big_tmp[pos + 1])
                else:
                    arr.add(big_tmp[pos])
            if midJudge(big_tmp, gapStat, 0.05, False):
                pos = len(big_tmp) - gapStat[0.05]
                if big_gap_tmp[pos] < 0.051:
                    if pos + 1 < len(big_tmp):
                        arr.add(big_tmp[pos + 1])
                gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos - 1, left=True)
        if len(big_near_tmp) - len(small_near_tmp) >= -1 and len(big_near_tmp) - len(small_tmp) >= -1:
            if len(big_near_tmp) == 1:
                arr.add(big_near_tmp[0])
            if midJudge(big_near_tmp, nearGapStat, 0.01, False):
                pos = len(big_near_tmp) - nearGapStat[0.01]
                arr.add(big_near_tmp[pos])
                arr.add(big_near_tmp[pos - 1])
            if midJudge(big_near_tmp, nearGapStat, 0.01, True):
                pos = len(big_near_tmp) - nearGapStat[0.01] - 1
                gapAndConsecutive(arr, big_near_tmp, big_near_gap_tmp, pos, left=True)
                gapAndConsecutive(arr, big_near_tmp, big_near_gap_tmp, pos + 1, left=False)
            if len(big_near_tmp) == 3:
                if big_near_gap_tmp[0] < 0.0033 and big_near_gap_tmp[2] > 0.0083:
                    arr.add(big_near_tmp[1])
            if len(big_near_tmp) == 2:
                if nearGapStat[0.01] == 1:
                    arr.add(big_near_tmp[0])
                if nearGapStat[0.01] == 0:
                    arr.add(big_near_tmp[0])
                    if big_near_gap_tmp[1] - big_near_gap_tmp[0] < 0.0001:
                        arr.add(big_near_tmp[1])
                    if big_near_gap_tmp[0] < 0.0009:
                        arr.add(big_near_tmp[1])
                    if big_near_gap_tmp[1] > 0.0054 and big_near_gap_tmp[0] < 0.0035:
                        arr.add(big_near_tmp[1])
            if nearGapStat[0.01] == 0:
                if noConsecutiveGap(big_near_gap_tmp):
                    if big_near_gap_tmp[0] < 0.005 and big_near_gap_tmp[1] > 0.005:
                        arr.add(big_near_tmp[0])
                findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=False, choose_single=False)
        if len(small_tmp) == 1:
            if gapStat[-0.02] == 0:
                arr.add(small_tmp[0])
        if len(small_near_tmp) == 1:
            arr.add(small_near_tmp[0])
        if len(small_tmp) - len(big_near_tmp) >= -1:
            if len(small_tmp) == 2:
                if small_gap_tmp[0] < -0.028 and small_gap_tmp[1] > -0.022:
                    arr.add(small_tmp[0])
            if len(small_tmp) == 1:
                if gapStat[-0.03] == 0:
                    arr.add(small_tmp[0])
            if gapStat[-0.02] == 0 and len(small_tmp) > 0:
                arr.add(small_tmp[0])
                if len(small_tmp) > 1 and small_gap_tmp[1] - small_gap_tmp[0] < 0.0001:
                    arr.add(small_tmp[1])
            if gapStat[-0.02] == 1 and len(small_tmp) > 1:
                arr.add(small_tmp[1])
                if small_gap_tmp[1] - small_gap_tmp[0] < 0.0001:
                    arr.add(small_tmp[0])
            if midJudge(small_tmp, gapStat, -0.03, False):
                pos = gapStat[-0.03]
                gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos, left=False)
        if len(small_near_tmp) >= len(big_near_tmp):
            if small_near_gap_tmp[-1] > -0.0009:
                arr.add(small_near_tmp[-1])
            if midJudge(small_near_tmp, nearGapStat, -0.01, True):
                pos = nearGapStat[-0.01]
                gapAndConsecutive(arr, small_near_tmp, small_near_gap_tmp, pos, left=False)
            if midJudge(small_near_tmp, nearGapStat, -0.01, False):
                pos = nearGapStat[-0.01] - 1
                gapAndConsecutive(arr, small_near_tmp, small_near_gap_tmp, pos, left=True)
            if len(small_near_tmp) == 2:
                if nearGapStat[-0.01] == 1:
                    arr.add(small_near_tmp[1])
                if small_near_gap_tmp[0] < -0.009:
                    arr.add(small_near_tmp[0])
                if nearGapStat[-0.01] == 0:
                    if small_near_gap_tmp[1] - small_near_gap_tmp[0] < 0.0001:
                        arr.add(small_near_tmp[0])
                        arr.add(small_near_tmp[1])
                    if noConsecutiveGap(small_near_gap_tmp):
                        if small_near_gap_tmp[0] < -0.005 and small_near_gap_tmp[1] > -0.005:
                            arr.add(small_near_tmp[0])
            elif len(small_near_tmp) > 2:
                if nearGapStat[-0.01] == 0:
                    if small_near_gap_tmp[2] - small_near_gap_tmp[1] == small_near_gap_tmp[1] - small_near_gap_tmp[0]:
                        arr.add(small_near_tmp[0])
                        arr.add(small_near_tmp[1])
                        arr.add(small_near_tmp[2])
        flag = ':参差' if maxConsecutiveCount['big'] < 4 else ':连续'
        print('不是大的就是接近的(大的偏多)' + flag + restExcBig(seq))
    elif count['big'] >= 5 and count['small'] >= 2:
        if midJudge(big_tmp, gapStat, 0.03, True):
            pos = len(big_tmp) - gapStat[0.03]
            gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos, left=False)
        flag = ':参差' if maxConsecutiveCount['big'] < 4 else ':连续'
        print('不是大的就是小的(大的偏多)' + flag + restExcBig(seq))
    #大:接近:小很均衡
    elif count['big'] <= 4 and count['near'] <= 4 and count['small'] <= 4:
        if len(seq['small']) + len(seq['smallNear']) > len(seq['big']) + len(seq['bigNear']):
            if len(small_near_tmp) >= len(big_near_tmp) and len(small_near_tmp) >= len(big_tmp):
                if midJudge(small_near_tmp, nearGapStat, -0.01, False):
                    pos = nearGapStat[-0.01] - 1
                    gapAndConsecutive(arr, small_near_tmp, small_near_gap_tmp, pos, left=True)
                    gapAndConsecutive(arr, small_near_tmp, small_near_gap_tmp, pos + 1, left=False)
                if midJudge(small_near_tmp, nearGapStat, -0.01, True):
                    pos = nearGapStat[-0.01] - 1
                    arr.add(small_near_tmp[pos])
                    for i in range(pos - 1, -1, -1):
                        if small_near_gap_tmp[pos] - small_near_gap_tmp[i] < 0.0001:
                            arr.add(small_near_tmp[i])
                    gapAndConsecutive(arr, small_near_tmp, small_near_gap_tmp, pos + 1, left=False)
                if nearGapStat[-0.01] == 0:
                    findTurn(arr, small_near_tmp, small_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=False, choose_single=False)
            if len(small_near_tmp) > len(big_near_tmp):
                if len(small_near_tmp) == 2:
                    if nearGapStat[-0.01] == 1:
                        arr.add(small_near_tmp[1])
            if len(small_tmp) - len(big_tmp) >= -1 and len(small_tmp) >= len(big_near_tmp):
                if len(small_tmp) == gapStat[-0.02]:
                    if gapStat[-0.03] == 0:
                        if small_gap_tmp[0] < -0.029:
                            arr.add(small_tmp[0])
                        findTurn(arr, small_tmp, small_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=True, choose_single=False)
                        findTurn(arr, small_tmp, small_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=False, choose_single=True)
                    if noConsecutiveGap(small_gap_tmp):
                        if len(small_tmp) == 3:
                            if small_gap_tmp[1] < -0.025 and small_gap_tmp[2] >= -0.023:
                                arr.add(small_tmp[2])
                if midJudge(small_tmp, gapStat, -0.02, False):
                    pos = gapStat[-0.02]
                    gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos - 1, left=True)
                    if small_gap_tmp[pos] < -0.0185:
                        if pos + 1 < len(small_tmp):
                            arr.add(small_tmp[pos + 1])
                if midJudge(small_tmp, gapStat, -0.02, True):
                    if gapStat[-0.03] == 0:
                        findTurn(arr, small_tmp, small_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=True, choose_single=False)
                    pos = gapStat[-0.02]
                    gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos, left=False)
                    gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos - 1, left=True)
                if midJudge(small_tmp, gapStat, -0.03, True):
                    pos = gapStat[-0.03]
                    gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos, left=False)
                if midJudge(small_tmp, gapStat, -0.03, False):
                    pos = gapStat[-0.03]
                    arr.add(small_tmp[pos - 1])
                    arr.add(small_tmp[pos])
                    if small_gap_tmp[pos] < -0.028:
                        if pos + 1 < len(small_tmp):
                            arr.add(small_tmp[pos + 1])
                    for i in range(pos + 1, len(small_tmp)):
                        if small_gap_tmp[i] - small_gap_tmp[pos] < 0.0001:
                            arr.add(small_tmp[i])
                    if small_gap_tmp[-1] > -0.022:
                        arr.add(small_tmp[-1])
                if midJudge(small_tmp, gapStat, -0.04, False):
                    pos = gapStat[-0.04]
                    arr.add(small_tmp[pos])
                    arr.add(small_tmp[pos - 1])
                    for i in range(pos + 1, len(small_tmp)):
                        if small_gap_tmp[i] - small_gap_tmp[pos] < 0.0001:
                            arr.add(small_tmp[i])
            if len(big_near_tmp) == 1:
                arr.add(big_near_tmp[0])
            if len(big_tmp) == 2:
                if gapStat[0.02] == 2 and big_gap_tmp[1] > 0.028 and gapStat[0.03] == 0:
                    arr.add(big_tmp[0])
            if len(big_tmp) - len(small_tmp) >= -2 and len(big_tmp) - len(small_near_tmp) >= -1:
                if midJudge(big_tmp, gapStat, 0.03, False):
                    pos = len(big_tmp) - gapStat[0.03] - 1
                    arr.add(big_tmp[pos])
                if midJudge(big_tmp, gapStat, 0.05, False):
                    pos = len(big_tmp) - gapStat[0.05] - 1
                    gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos, left=True)
                if midJudge(big_tmp, gapStat, 0.04, False):
                    pos = len(big_tmp) - gapStat[0.04] - 1
                    gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos, left=True)
                if midJudge(big_tmp, gapStat, 0.04, True):
                    pos = len(big_tmp) - gapStat[0.04]
                    gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos, left=False)
                if midJudge(big_tmp, gapStat, 0.03, True):
                    pos = len(big_tmp) - gapStat[0.03]
                    arr.add(big_tmp[pos])
                    for i in range(pos + 1, len(big_tmp)):
                        if big_gap_tmp[i] - big_gap_tmp[pos] < 0.0001:
                            arr.add(big_tmp[i])
                if midJudge(big_tmp, gapStat, 0.02, True):
                    pos = len(big_tmp) - gapStat[0.02] - 1
                    arr.add(big_tmp[pos])
                if len(big_tmp) == 2:
                    if gapStat[0.03] == 1:
                        arr.add(big_tmp[0])
            print('很均衡时小的偏多' + extraSmall(seq))
        elif len(seq['small']) + len(seq['smallNear']) < len(seq['big']) + len(seq['bigNear']):
            if len(big_tmp) >= len(small_tmp) and len(big_tmp) >= len(big_near_tmp):
                if midJudge(big_tmp, gapStat, 0.04, False):
                    pos = len(big_tmp) - gapStat[0.04] - 1
                    gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos, left=True)
                if midJudge(big_tmp, gapStat, 0.05, False):
                    pos = len(big_tmp) - gapStat[0.05] - 1
                    arr.add(big_tmp[pos])
                    for i in range(pos - 1, -1, -1):
                        if big_gap_tmp[pos] - big_gap_tmp[i] < 0.00001:
                            arr.add(big_tmp[i])
                if midJudge(big_tmp, gapStat, 0.03, False):
                    pos = len(big_tmp) - gapStat[0.03]
                    arr.add(big_tmp[pos])
                if midJudge(big_tmp, gapStat, 0.02, False):
                    pos = len(big_tmp) - gapStat[0.02] - 1
                    gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos, left=True)
                if midJudge(big_tmp, gapStat, 0.02, True):
                    pos = len(big_tmp) - gapStat[0.02]
                    gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos, left=False)
                    arr.add(big_tmp[pos - 1])
            if len(big_near_tmp) >= len(small_tmp) and len(big_near_tmp) >= len(small_near_tmp):
                if midJudge(big_near_tmp, nearGapStat, 0.01, False):
                    pos = len(big_near_tmp) - nearGapStat[0.01] - 1
                    if big_near_gap_tmp[pos] > 0.0085:
                        arr.add(big_near_tmp[pos - 1])
                    arr.add(big_near_tmp[pos])
                    arr.add(big_near_tmp[pos + 1])
                    if noConsecutiveGap(big_near_gap_tmp):
                        if big_near_gap_tmp[0] < 0.005 and big_near_gap_tmp[1] > 0.005:
                            arr.add(big_near_tmp[0])
                if nearGapStat[0.01] == 0:
                    if len(big_near_tmp)  == 3:
                        if big_near_gap_tmp[0] == big_near_gap_tmp[1] and big_near_gap_tmp[1] == big_near_gap_tmp[2]:
                            arr.add(big_near_tmp[0])
                            arr.add(big_near_tmp[1])
                            arr.add(big_near_tmp[2])
                    if noConsecutiveGap(big_near_gap_tmp):
                        if big_near_gap_tmp[-1] > 0.0085:
                            arr.add(big_near_tmp[-1])
                    if big_near_gap_tmp[-1] > 0.008 and big_near_gap_tmp[-2] < 0.006:
                        arr.add(big_near_tmp[-2])
                    if big_near_gap_tmp[0] < 0.0005 and big_near_gap_tmp[1] > 0.001:
                        arr.add(big_near_tmp[0])
                    findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=False, choose_single=False)
                    findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=True, choose_single=True)
            if len(small_tmp) - len(big_tmp) >= -1 and len(small_tmp) - len(big_near_tmp) >= -1:
                if midJudge(small_tmp, gapStat, -0.02, True):
                    pos = gapStat[-0.02]
                    gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos, left=False)
                if midJudge(small_tmp, gapStat, -0.03, True):
                    pos = gapStat[-0.03] - 1
                    if small_gap_tmp[pos] > -0.0305:
                        if pos - 1 > -1:
                            arr.add(small_tmp[pos - 1])
                if midJudge(small_tmp, gapStat, -0.03, False):
                    pos = gapStat[-0.03]
                    gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos, left=False)
                    gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos - 1, left=True)
                if midJudge(small_tmp, gapStat, -0.02, False):
                    pos = gapStat[-0.02]
                    gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos, left=False)
                if len(small_tmp) == gapStat[-0.02]:
                    if gapStat[-0.03] == 0:
                        findTurn(arr, small_tmp, small_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=True, choose_single=False)
            elif len(small_tmp) >= len(big_near_tmp):
                if small_gap_tmp[0] == small_gap_tmp[-1]:
                    for v in small_tmp:
                        arr.add(v)
            if len(small_tmp) == 2:
                if gapStat[-0.02] == 1:
                    arr.add(small_tmp[1])
                if gapStat[-0.03] == 1:
                    arr.add(small_tmp[0])
            if len(small_near_tmp) == 1:
                if nearGapStat[-0.01] == 0:
                    arr.add(small_near_tmp[0])
            if len(small_near_tmp) >= len(big_near_tmp):
                if small_near_gap_tmp[0] == small_near_gap_tmp[-1]:
                    for v in small_near_tmp:
                        arr.add(v)
            print('很均衡时大的偏多' + extraBig(seq))
        else:
            if len(small_tmp) == 2:
                if gapStat[-0.02] == 2:
                    if small_gap_tmp[1] > -0.0205:
                        arr.add(small_tmp[1])
                if gapStat[-0.02] == 1:
                    arr.add(small_tmp[1])
                if gapStat[-0.03] == 1:
                    arr.add(small_tmp[0])
            if len(small_tmp) - len(big_tmp) >= -1 and len(small_tmp) >= len(big_near_tmp):
                if len(small_tmp) == gapStat[-0.02]:
                    if gapStat[-0.03] == 0:
                        findTurn(arr, small_tmp, small_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=True, consecutive_at_left=True, choose_single=False)
                if midJudge(small_tmp, gapStat, -0.04, False):
                    pos = gapStat[-0.04] - 1
                    gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos, left=True)
                if midJudge(small_tmp, gapStat, -0.03, False):
                    pos = gapStat[-0.03] - 1
                    arr.add(small_tmp[pos])
                    gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos, left=True)
                    gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos + 1, left=False)
                if midJudge(small_tmp, gapStat, -0.02, True):
                    pos = gapStat[-0.02] - 1
                    gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos + 1, left=False)
                    if small_gap_tmp[pos] > -0.0202:
                        arr.add(small_tmp[pos - 1])
                        for i in range(pos - 2, -1, -1):
                            if small_gap_tmp[pos - 1] - small_gap_tmp[i] < 0.0001:
                                arr.add(small_tmp[i])
                    elif small_gap_tmp[pos] < -0.021:
                        arr.add(small_tmp[pos])
                        for i in range(pos - 1, -1, -1):
                            if small_gap_tmp[pos] - small_gap_tmp[i] < 0.0001:
                                arr.add(small_tmp[i])
                    if gapStat[-0.03] == 0:
                        findTurn(arr, small_tmp, small_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=False, choose_single=True)
            if len(small_near_tmp) >= len(big_near_tmp):
                if len(small_near_tmp) == 2:
                    if nearGapStat[-0.01] == 1:
                        arr.add(small_near_tmp[1])
                    if nearGapStat[-0.01] == 0:
                        if small_near_gap_tmp[1] - small_near_gap_tmp[0] < 0.0001:
                            arr.add(small_near_tmp[0])
                            arr.add(small_near_tmp[1])
                    if small_near_gap_tmp[1] > -0.0004:
                        arr.add(small_near_tmp[1])
                elif len(small_near_tmp) > 2:
                    if midJudge(small_near_tmp, nearGapStat, -0.01, True):
                        pos = nearGapStat[-0.01] - 1
                        arr.add(small_near_tmp[pos])
                        for i in range(pos - 1, -1, -1):
                            if small_near_gap_tmp[i] - small_near_gap_tmp[pos] < 0.0001:
                                arr.add(small_near_tmp[i])
            if len(big_tmp) - len(small_tmp) >= -1 and len(big_tmp) >= len(small_near_tmp):
                if midJudge(big_tmp, gapStat, 0.04, True):
                    pos = len(big_tmp) - gapStat[0.04]
                    gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos, left=False)
                if midJudge(big_tmp, gapStat, 0.03, True):
                    pos = len(big_tmp) - gapStat[0.03]
                    gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos, left=False)
                    arr.add(big_tmp[pos - 1])
                    if big_gap_tmp[pos] < 0.0309:
                        arr.add(big_tmp[pos + 1])
                    if gapStat[0.04] == 0:
                        if big_gap_tmp[-1] > 0.039:
                            arr.add(big_tmp[-1])
                if midJudge(big_tmp, gapStat, 0.02, True):
                    pos = len(big_tmp) - gapStat[0.02]
                    arr.add(big_tmp[pos - 1])
            if len(big_near_tmp) - len(small_near_tmp) >= -1:
                if big_near_gap_tmp[-1] > 0.009:
                    arr.add(big_near_tmp[-1])
                if len(big_near_tmp) == 1:
                    arr.add(big_near_tmp[0])
                if nearGapStat[0.01] == 1:
                    if len(big_near_tmp) > 1:
                        arr.add(big_near_tmp[1])
                    arr.add(big_near_tmp[0])
                if nearGapStat[0.01] == 0:
                    if len(big_near_tmp) ==2 and big_near_gap_tmp[1] > 0.007:
                        arr.add(big_near_tmp[1])
                    if len(big_near_tmp) > 1 and big_near_gap_tmp[0] < 0.003 and big_near_gap_tmp[1] > 0.007:
                        arr.add(big_near_tmp[0])
            print('非常均衡')
    elif count['small'] >= 7:
        if midJudge(small_tmp, gapStat, -0.03, True):
            pos = gapStat[-0.03] - 1
            arr.add(small_tmp[pos])
            for i in range(pos - 1, -1, -1):
                if small_gap_tmp[pos] - small_gap_tmp[i] < 0.0001:
                    arr.add(small_tmp[i])
            arr.add(small_tmp[pos + 1])
            for i in range(pos + 2, len(small_tmp)):
                if small_gap_tmp[i] - small_gap_tmp[pos + 1] < 0.0001:
                    arr.add(small_tmp[i])
            if small_gap_tmp[pos + 1] < -0.0269 and pos + 2 < len(small_tmp):
                arr.add(small_tmp[pos + 2])
        if midJudge(small_tmp, gapStat, -0.04, False):
            pos = gapStat[-0.04]
            arr.add(small_tmp[pos])
        if midJudge(small_tmp, gapStat, -0.04, True):
            pos = gapStat[-0.04]
            arr.add(small_tmp[pos])
            for i in range(pos + 1, len(small_tmp)):
                if small_gap_tmp[i] - small_gap_tmp[pos] < 0.0001:
                    arr.add(small_tmp[i])
        if midJudge(small_tmp, gapStat, -0.02, True):
            pos = gapStat[-0.02] - 1
            arr.add(small_tmp[pos])
            for i in range(pos - 1, -1, -1):
                if small_gap_tmp[pos] - small_gap_tmp[i] < 0.0001:
                    arr.add(small_tmp[i])
        if midJudge(small_tmp, gapStat, -0.09, False):
            pos = gapStat[-0.09] - 1
            gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos, left=True)
        if midJudge(small_tmp, gapStat, -0.06, False):
            pos = gapStat[-0.06]
            gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos - 1, left=True)
            arr.add(small_tmp[pos])
            if small_gap_tmp[pos] < -0.0575 and small_gap_tmp[pos + 1] > -0.057:
                arr.add(small_tmp[pos + 1])
            for i in range(pos + 1, len(small_tmp)):
                if small_gap_tmp[i] - small_gap_tmp[pos] < 0.0001:
                    arr.add(small_tmp[i])
        if midJudge(small_tmp, gapStat, -0.07, True):
            findTurn(arr, small_tmp, small_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=False, choose_single=True)
        if midJudge(small_tmp, gapStat, -0.05, False):
            pos = gapStat[-0.05]
            if small_gap_tmp[pos] > -0.049:
                arr.add(small_tmp[pos])
            else:
                if small_gap_tmp[pos + 1] > -0.048:
                    arr.add(small_tmp[pos + 1])
        if len(big_near_tmp) > len(small_near_tmp):
            if len(big_near_tmp) == 2:
                if nearGapStat[0.01] == 0:
                    if big_near_gap_tmp[0] < 0.0035 and big_near_gap_tmp[1] > 0.006:
                        arr.add(big_near_tmp[0])
        print('大部分小')
    elif count['small'] >= 5 and maxConsecutiveCount['small'] >= 4:
        print('连续小' + restExcSmall(seq))
    else:
        print('不对呀', data_len)
    print(data_len, good_count, arr)
    del(seq['near'])
    show(gapStat, avg_window, data_len, range_stat, prob_cand_arr, pred, seq)
    return arr


