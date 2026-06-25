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
        if gapStat[0.02] == len(big_tmp) - 1:
            findTurn(arr, big_tmp, big_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=False, choose_single=False)
        if midJudge(big_tmp, gapStat, 0.03, False):
            pos = len(big_tmp) - gapStat[0.03]
            arr.add(big_tmp[pos])
            arr.add(big_tmp[pos - 1])
        if gapStat[0.03] == len(big_tmp):
            if midJudge(big_tmp, gapStat, 0.04, False):
                arr.add(big_tmp[1])
                findTurn(arr, big_tmp, big_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=False, choose_single=True)
            if midJudge(big_tmp, gapStat, 0.04, True):
                findTurn(arr, big_tmp, big_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=True, choose_single=False)
        if midJudge(big_tmp, gapStat, 0.08, False):
            pos = len(big_tmp) - gapStat[0.08]
            arr.add(big_tmp[pos])
            for i in range(pos + 1, len(big_tmp)):
                if big_gap_tmp[i] - big_gap_tmp[pos] < 0.0001:
                    arr.add(big_tmp[i])
        if midJudge(big_tmp, gapStat, 0.07, False):
            if big_gap_tmp[-1] > 0.0755 and big_gap_tmp[-2] < 0.0732:
                arr.add(big_tmp[-1])
        if midJudge(big_tmp, gapStat, 0.06, False):
            arr.add(big_tmp[len(big_tmp) - gapStat[0.06]])
            arr.add(big_tmp[len(big_tmp) - gapStat[0.06] - 1])
        if midJudge(big_tmp, gapStat, 0.02, True):
            arr.add(big_tmp[len(big_tmp) - gapStat[0.02]])
            pos = len(big_tmp) - gapStat[0.02] - 1
            if big_gap_tmp[pos] > 0.017:
                if pos - 1 > -1:
                    arr.add(big_tmp[pos - 1])
            arr.add(big_tmp[pos])
            for i in range(pos - 1, -1, -1):
                if big_gap_tmp[pos] - big_gap_tmp[i] < 0.0001:
                    arr.add(big_tmp[i])
        if gapStat[0.02] == len(big_tmp) and gapStat[0.03] <= len(big_tmp) / 2:
            findTurn(arr, big_tmp, big_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=False, choose_single=True)
            findTurn(arr, big_tmp, big_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=False, choose_single=False)
        if midJudge(big_tmp, gapStat, 0.03, True):
            arr.add(big_tmp[len(big_tmp) - gapStat[0.03]])
            arr.add(big_tmp[len(big_tmp) - gapStat[0.03] - 1])
            if len(big_tmp) - gapStat[0.03] + 1 < len(big_tmp) and big_gap_tmp[len(big_tmp) - gapStat[0.03] + 1] - big_gap_tmp[len(big_tmp) - gapStat[0.03]] < 0.00001:
                arr.add(big_tmp[len(big_tmp) - gapStat[0.03] + 1])
            arr.add(big_tmp[1])
        if len(big_near_tmp) > len(small_tmp) and len(big_near_tmp) > len(small_near_tmp):
            if nearGapStat[0.01] == 1:
                arr.add(big_near_tmp[-1])
        if len(small_near_tmp) >= len(big_near_tmp):
            if len(small_near_tmp) == 2:
                if nearGapStat[-0.01] == 1:
                    arr.add(small_near_tmp[-1])
                if nearGapStat[-0.01] == 0:
                    if small_near_gap_tmp[0] == small_near_gap_tmp[1]:
                        arr.add(small_near_tmp[0])
                        arr.add(small_near_tmp[1])
        if midJudge(big_tmp, gapStat, 0.05, False):
            pos = len(big_tmp) - gapStat[0.05]
            arr.add(big_tmp[pos])
            for i in range(pos + 1, len(big_tmp)):
                if big_gap_tmp[i] - big_gap_tmp[pos] < 0.0001:
                    arr.add(big_tmp[i])
            arr.add(big_tmp[pos - 1])
            for i in range(pos - 2, -1, -1):
                if big_gap_tmp[pos - 1] - big_gap_tmp[i] < 0.0001:
                    arr.add(big_tmp[i])
            if big_gap_tmp[-1] > 0.058:
                arr.add(big_tmp[-1])
        if midJudge(big_tmp, gapStat, 0.05, True):
            pos = len(big_tmp) - gapStat[0.05] - 1
            arr.add(big_tmp[pos])
            for i in range(pos - 1, -1, -1):
                if big_gap_tmp[pos] - big_gap_tmp[i] < 0.001:
                    arr.add(big_tmp[i])
            findTurn(arr, big_tmp, big_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=True, consecutive_at_left=True, choose_single=False)
        if midJudge(big_tmp, gapStat, 0.04, True):
            pos = len(big_tmp) - gapStat[0.04] - 1
            if big_gap_tmp[pos + 1] < 0.041:
                arr.add(big_tmp[pos + 2])
            arr.add(big_tmp[pos])
            for i in range(pos - 1, -1, -1):
                if big_gap_tmp[pos] - big_gap_tmp[i] < 0.001:
                    arr.add(big_tmp[i])
            findTurn(arr, big_tmp, big_gap_tmp, approach_threshold=0.0001, gap_threshold=0.04, reverse=True, consecutive_at_left=True, choose_single=False)
        if midJudge(big_tmp, gapStat, 0.04, False):
            pos = len(big_tmp) - gapStat[0.04] - 1
            arr.add(big_tmp[pos])
            for i in range(pos - 1, -1, -1):
                if big_gap_tmp[pos] - big_gap_tmp[i] < 0.0001:
                    arr.add(big_tmp[i])
            arr.add(big_tmp[pos + 1])
        if len(small_tmp) == 1:
            if gapStat[-0.03] == 0:
                arr.add(small_tmp[0])
        if len(small_tmp) >= len(big_near_tmp):
            if midJudge(small_tmp, gapStat, -0.02, True):
                pos = gapStat[-0.02]
                gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos, left=False)
            if midJudge(small_tmp, gapStat, -0.03, False):
                pos = gapStat[-0.03] - 1
                gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos, left=True)
            if len(small_tmp) == 2:
                if small_gap_tmp[1] > -0.022:
                    arr.add(small_tmp[1])
                if gapStat[-0.02] == 1:
                    arr.add(small_tmp[0])
                if gapStat[-0.02] == 0:
                    arr.add(small_tmp[-1])
                    if small_gap_tmp[-1] - small_gap_tmp[-2] < 0.0001:
                        arr.add(small_tmp[-2])
        if len(small_near_tmp) == 1:
            arr.add(small_near_tmp[0])
        if len(big_near_tmp) >= len(small_tmp) and len(big_near_tmp) >= len(small_near_tmp):
            if midJudge(big_near_tmp, nearGapStat, 0.01, False):
                pos = len(big_near_tmp) - nearGapStat[0.01] - 1
                if big_near_gap_tmp[pos] > 0.007 and big_near_gap_tmp[pos - 1] < 0.0055:
                    arr.add(big_near_tmp[pos - 1])
            if len(big_near_tmp) > 1 and big_near_gap_tmp[0] == big_near_gap_tmp[-1]:
                for v in big_near_tmp:
                    arr.add(v)
            if len(big_near_tmp) == 2:
                if big_near_gap_tmp[1] > 0.007 and big_near_gap_tmp[0] < 0.0023:
                    arr.add(big_near_tmp[1])
                if big_near_gap_tmp[0] < 0.011:
                    arr.add(big_near_tmp[1])
                if nearGapStat[0.01] == 1:
                    arr.add(big_near_tmp[0])
        if len(small_near_tmp) >= len(big_near_tmp):
            if nearGapStat[-0.01] == 0:
                if small_near_gap_tmp[0] < -0.0085 and small_near_gap_tmp[1] > -0.0069:
                    arr.add(small_near_tmp[1])
                if small_near_gap_tmp[0] < -0.007 and small_near_gap_tmp[1] > -0.0052:
                    arr.add(small_near_tmp[0])
            if len(small_near_tmp) == 2:
                if nearGapStat[-0.01] == 1:
                    arr.add(small_near_tmp[0])
                if small_near_gap_tmp[0] < -0.008 and small_near_gap_tmp[1] > -0.0065:
                    arr.add(small_near_tmp[1])
                if small_near_gap_tmp[0] < -0.006 and small_near_gap_tmp[1] > -0.003:
                    arr.add(small_near_tmp[1])
                if small_near_gap_tmp[0] < -0.009:
                    arr.add(small_near_tmp[1])
                if small_near_gap_tmp[1] > -0.0009:
                    arr.add(small_near_tmp[1])
                if small_near_gap_tmp[0] > -0.012:
                    arr.add(small_near_tmp[0])
                if small_near_gap_tmp[0] < -0.0065 and small_near_gap_tmp[1] > -0.005:
                    arr.add(small_near_tmp[1])
            if midJudge(small_near_tmp, nearGapStat, -0.01, False):
                pos = nearGapStat[-0.01] - 1
                gapAndConsecutive(arr, small_near_tmp, small_near_gap_tmp, pos, left=True)
            if midJudge(small_near_tmp, nearGapStat, -0.01, True):
                pos = nearGapStat[-0.01]
                gapAndConsecutive(arr, small_near_tmp, small_near_gap_tmp, pos, left=False)
        print('大的全都要')
    elif count['near'] >= 5 and maxConsecutiveCount['near'] < 4:
        if len(seq['small']) + len(seq['smallNear']) >= 7:
            if len(big_near_tmp) - len(small_near_tmp) >= -1:
                if len(big_near_tmp) == 2:
                    if nearGapStat[0.01] == 0:
                        if big_near_gap_tmp[1] > 0.007 and big_near_gap_tmp[0] < 0.004:
                            arr.add(big_near_tmp[1])
            if len(big_near_tmp) - len(small_tmp) >= -1:
                if len(big_near_tmp) == 2:
                    if nearGapStat[0.01] == 1:
                        arr.add(big_near_tmp[0])
                    if nearGapStat[0.01] == 0:
                        if big_near_gap_tmp[1] > 0.007:
                            arr.add(big_near_tmp[1])
            if len(big_near_tmp) >= len(small_near_tmp):
                if nearGapStat[0.01] == 0:
                    arr.add(big_near_tmp[0])
                    for i in range(1, len(big_near_tmp)):
                        if big_near_gap_tmp[i] - big_near_gap_tmp[0] < 0.0001:
                            arr.add(big_near_tmp[i])
                if midJudge(big_near_tmp, nearGapStat, 0.01, False):
                    pos = len(big_near_tmp) - nearGapStat[0.01]
                    arr.add(big_near_tmp[pos])
                    for i in range(pos + 1, len(big_near_tmp)):
                        if big_near_gap_tmp[i] - big_near_gap_tmp[pos] < 0.0001:
                            arr.add(big_near_tmp[i])
            if len(big_near_tmp) >= len(big_tmp):
                if len(big_near_tmp) == 2:
                    if nearGapStat[0.01] == 0:
                        arr.add(big_near_tmp[0])
                if len(big_near_tmp) > len(small_near_tmp):
                    if midJudge(big_near_tmp, nearGapStat, 0.01, False):
                        findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=True, choose_single=False)
            if len(small_tmp) >= len(big_near_tmp) and len(small_tmp) >= len(big_tmp):
                if len(small_tmp) == gapStat[-0.02]:
                    if small_gap_tmp[-1] > -0.021:
                        arr.add(small_tmp[-1])
                if midJudge(small_tmp, gapStat, -0.04, False):
                    pos = gapStat[-0.04] - 1
                    gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos, left=True)
                if midJudge(small_tmp, gapStat, -0.03, True):
                    pos = gapStat[-0.03]
                    gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos, left=False)
                if midJudge(small_tmp, gapStat, -0.02, True):
                    pos = gapStat[-0.02]
                    gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos, left=False)
                if midJudge(small_tmp, gapStat, -0.05, False):
                    pos = gapStat[-0.05] - 1
                    gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos, left=True)
                    gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos + 1, left=False)
                if midJudge(small_tmp, gapStat, -0.04, True):
                    if small_gap_tmp[0] < -0.0481:
                        arr.add(small_tmp[0])
                    pos = gapStat[-0.04]
                    gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos, left=False)
                    gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos - 1, left=True)
                    if small_gap_tmp[0] < -0.0475 and small_gap_tmp[1] > -0.044:
                        arr.add(small_tmp[0])
                if midJudge(small_tmp, gapStat, -0.05, True):
                    if gapStat[-0.06] == 0:
                        arr.add(small_tmp[0])
                    if gapStat[-0.02] == len(small_tmp):
                        arr.add(small_tmp[-1])
            if len(small_near_tmp) > len(big_tmp) and len(small_near_tmp) - len(big_near_tmp) >= -1:
                if nearGapStat[-0.01] == 0:
                    if small_near_gap_tmp[-1] > -0.0008:
                        arr.add(small_near_tmp[-1])
                    if noConsecutiveGap(small_near_gap_tmp):
                        if small_near_gap_tmp[-1] > -0.005 and small_near_gap_tmp[-2] < -0.005:
                            arr.add(small_near_tmp[-1])
                    findTurn(arr, small_near_tmp, small_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=True, consecutive_at_left=False, choose_single=False)
                    findTurn(arr, small_near_tmp, small_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=False, choose_single=False)
                    findTurn(arr, small_near_tmp, small_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.1, reverse=False, consecutive_at_left=False, choose_single=True)
                if midJudge(small_near_tmp, nearGapStat, -0.01, False):
                    if noConsecutiveGap(small_near_gap_tmp):
                        arr.add(small_near_tmp[nearGapStat[-0.01] + 1])
                    pos = nearGapStat[-0.01] - 1
                    gapAndConsecutive(arr, small_near_tmp, small_near_gap_tmp, pos, left=True)
                    gapAndConsecutive(arr, small_near_tmp, small_near_gap_tmp, pos + 1, left=False)
                    findTurn(arr, small_near_tmp, small_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.1, reverse=True, consecutive_at_left=False, choose_single=False)
                if midJudge(small_near_tmp, nearGapStat, -0.01, True) or nearGapStat[-0.01] == len(small_near_tmp): 
                    findTurn(arr, small_near_tmp, small_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.1, reverse=False, consecutive_at_left=True, choose_single=False)
                    findTurn(arr, small_near_tmp, small_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=False, choose_single=True)
                if len(small_near_tmp) == 2:
                    if small_near_gap_tmp[1] > -0.0108:
                        arr.add(small_near_tmp[1])
            if len(big_tmp) == 1:
                if gapStat[0.03] == 0:
                    arr.add(big_tmp[0])
            if len(big_near_tmp) == 1:
                if nearGapStat[0.01] == 0:
                    arr.add(big_near_tmp[0])
            print('参差不齐接近时小的偏多' + extraSmall(seq))
        elif len(seq['big']) + len(seq['bigNear']) >= 7:
            if len(big_near_tmp) - len(small_tmp) >= -1 and len(big_near_tmp) - len(small_near_tmp) >= -1:
                if big_near_gap_tmp[0] == big_near_gap_tmp[-1]:
                    for v in big_near_tmp:
                        arr.add(v)
                if midJudge(big_near_tmp, nearGapStat, 0.01, True):
                    pos = len(big_near_tmp) - nearGapStat[0.01] - 1
                    gapAndConsecutive(arr, big_near_tmp, big_near_gap_tmp, pos, left=True)
                    findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=False, choose_single=False)
                if midJudge(big_near_tmp, nearGapStat, 0.01, False):
                    pos = len(big_near_tmp) - nearGapStat[0.01] - 1
                    arr.add(big_near_tmp[pos])
                    arr.add(big_near_tmp[pos + 1])
                    if pos + 2 < len(big_near_tmp):
                        arr.add(big_near_tmp[pos + 2])
                    for i in range(pos - 1, -1, -1):
                        if big_near_gap_tmp[pos] - big_near_gap_tmp[i] < 0.00001:
                            arr.add(big_near_tmp[i])
                    arr.add(big_near_tmp[pos - 1])
                    findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=False, choose_single=False)
                    findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=False, choose_single=True)
                    findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=True, choose_single=False)
                if nearGapStat[0.01] == 1:
                    findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.5, reverse=False, consecutive_at_left=True, choose_single=False)
                if nearGapStat[0.01] == 0:
                    findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.1, reverse=True, consecutive_at_left=False, choose_single=False)
            if len(big_tmp) >= len(small_tmp) and len(big_tmp) >= len(small_near_tmp):
                if midJudge(big_tmp, gapStat, 0.05, False):
                    pos = len(big_tmp) - gapStat[0.05] - 1
                    arr.add(big_tmp[pos])
                    for i in range(pos - 1, -1, -1):
                        if big_gap_tmp[pos] - big_gap_tmp[i] < 0.0001:
                            arr.add(big_tmp[i])
                if midJudge(big_tmp, gapStat, 0.03, True):
                    pos = len(big_tmp) - gapStat[0.03]
                    arr.add(big_tmp[pos])
                    for i in range(pos + 1, len(big_tmp)):
                        if big_gap_tmp[i] - big_gap_tmp[pos] < 0.0001:
                            arr.add(big_tmp[i])
                if gapStat[0.03] == len(big_tmp):
                    if midJudge(big_tmp, gapStat, 0.04, False):
                        findTurn(arr, big_tmp, big_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=False, choose_single=False)
                if gapStat[0.02] == len(big_tmp):
                    if big_gap_tmp[0] < 0.0212:
                        arr.add(big_tmp[0])
                    if gapStat[0.03] < 2:
                        findTurn(arr, big_tmp, big_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=True, choose_single=False)
                    if gapStat[0.03] <= 2:
                        arr.add(big_tmp[len(big_tmp) - gapStat[0.03] - 1])
                if gapStat[0.02] >= len(big_tmp) / 2 and gapStat[0.02] < len(big_tmp):
                    arr.add(big_tmp[len(big_tmp) - gapStat[0.02]])
                if gapStat[0.03] == 1:
                    arr.add(big_tmp[-2])
                if gapStat[0.04] == 1:
                    arr.add(big_tmp[-1])
                if gapStat[0.05] >= 2 and gapStat[0.05] <= len(big_tmp) / 2:
                    arr.add(big_tmp[len(big_tmp) - gapStat[0.05] - 1])
            elif len(big_tmp) >= len(small_near_tmp):
                if len(big_tmp) == 1:
                    if gapStat[0.03] == 0:
                        arr.add(big_tmp[0])
            if len(small_near_tmp) == 2:
                if nearGapStat[-0.01] == 1:
                    arr.add(small_near_tmp[-1])
                elif nearGapStat[-0.01] == 0:
                    arr.add(small_near_tmp[0])
                    if small_near_gap_tmp[1] - small_near_gap_tmp[0] < 0.00001:
                        arr.add(small_near_gap_tmp[1])
            if len(small_near_tmp) - len(big_near_tmp) >= -1:
                if nearGapStat[-0.01] == 0:
                    if small_near_gap_tmp[0] < -0.007 and small_near_gap_tmp[1] > -0.0023:
                        arr.add(small_near_tmp[0])
                if midJudge(small_near_tmp, nearGapStat, -0.01, True):
                    arr.add(small_near_tmp[0])
                if len(small_near_tmp) == 2:
                    if small_near_gap_tmp[-1] > -0.001 and small_near_gap_tmp[-2] < -0.005:
                        arr.add(small_near_tmp[-1])
            if len(small_tmp) >= len(big_tmp):
                if len(small_tmp) == 2:
                    if gapStat[-0.03] == 1:
                        arr.add(small_tmp[1])
                if midJudge(small_tmp, gapStat, -0.03, True):
                    if small_gap_tmp[0] < -0.038:
                        arr.add(small_tmp[0])
                    pos = gapStat[-0.03] - 1
                    if small_gap_tmp[pos] > -0.031:
                        if pos - 1 > -1:
                            arr.add(small_tmp[pos - 1])
                    gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos, left=True)
                    gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos + 1, left=False)
                if gapStat[-0.03] == 1:
                    arr.add(small_tmp[0])
                if gapStat[-0.03] == len(small_tmp):
                    arr.add(small_tmp[-1])
            if len(small_tmp) <= 2 and len(small_tmp) > 0:
                if gapStat[-0.03] == 1:
                    arr.add(small_tmp[0])
                if len(small_tmp) == 2:
                    if gapStat[-0.02] == 2:
                        if gapStat[-0.03] == 0:
                            if small_gap_tmp[0] == small_gap_tmp[1]:
                                arr.add(small_tmp[0])
                                arr.add(small_tmp[1])
            if len(big_tmp) == 2:
                if gapStat[0.03] == 1:
                    arr.add(big_tmp[-1])
            print('参差不齐接近时大的偏多' + extraBig(seq))
        elif len(seq['small']) + len(seq['smallNear']) > len(seq['big']) + len(seq['bigNear']):
            if len(big_near_tmp) - len(small_near_tmp) >= -1 and len(big_near_tmp) - len(small_tmp) >= -1:
                if nearGapStat[0.01] == 0:
                    if len(big_near_tmp) > 2:
                        if big_near_gap_tmp[0] == big_near_gap_tmp[1] and big_near_gap_tmp[1] == big_near_gap_tmp[2]:
                            arr.add(big_near_tmp[0])
                            arr.add(big_near_tmp[1])
                            arr.add(big_near_tmp[2])
                    findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.1, reverse=False, consecutive_at_left=True, choose_single=True)
                    findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.1, reverse=False, consecutive_at_left=False, choose_single=True)
                    findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.1, reverse=False, consecutive_at_left=False, choose_single=False)
                    if noConsecutiveGap(big_near_gap_tmp):
                        arr.add(big_near_tmp[int(len(big_near_tmp) / 2)])
                    else:
                        findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=True, choose_single=False)
                if midJudge(big_near_tmp, nearGapStat, 0.01, False):
                    findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.1, reverse=False, consecutive_at_left=True, choose_single=False)
                    pos = len(big_near_tmp) - nearGapStat[0.01]
                    arr.add(big_near_tmp[pos])
                    for i in range(pos + 1, len(big_near_tmp)):
                        if big_near_gap_tmp[i] - big_near_gap_tmp[pos] < 0.0001:
                            arr.add(big_near_tmp[i])
                    arr.add(big_near_tmp[pos - 1])
                    for i in range(pos - 2, -1, -1):
                        if big_near_gap_tmp[pos - 1] - big_near_gap_tmp[i] < 0.0001:
                            arr.add(big_near_tmp[i])
                    if noConsecutiveGap(big_near_gap_tmp):
                        if big_near_gap_tmp[pos - 1] > 0.008:
                            if pos - 2 > -1:
                                arr.add(big_near_tmp[pos - 2])
                if len(big_near_tmp) == 2:
                    if nearGapStat[0.01] == 1 or big_near_gap_tmp[1] > 0.0081:
                        arr.add(big_near_tmp[0])
            if len(big_tmp) - len(small_tmp) >= -1 and len(big_tmp) - len(small_near_tmp) >= -1:
                if len(big_tmp) == 2:
                    if gapStat[0.02] == 1:
                        arr.add(big_tmp[0])
                if gapStat[0.03] == 1:
                    arr.add(big_tmp[-2])
                    if len(big_tmp) > 2 and big_gap_tmp[-2] - big_gap_tmp[-3] < 0.00001:
                        arr.add(big_tmp[-3])
            if len(small_tmp) >= len(big_tmp) and len(small_tmp) >= len(big_near_tmp):
                if gapStat[-0.03] == 1 and len(small_tmp) == 2:
                    arr.add(small_tmp[0])
                if midJudge(small_tmp, gapStat, -0.03, True):
                    pos = gapStat[-0.03] - 1
                    gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos, left=True)
                if midJudge(small_tmp, gapStat, -0.03, False):
                    pos = gapStat[-0.03] - 1
                    gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos, left=True)
                    findTurn(arr, small_tmp, small_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=True, consecutive_at_left=False, choose_single=False)
                if midJudge(small_tmp, gapStat, -0.04, False):
                    pos = gapStat[-0.04] - 1
                    gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos, left=True)
                    gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos + 1, left=False)
                if midJudge(small_tmp, gapStat, -0.02, True):
                    arr.add(small_tmp[gapStat[-0.02]])
                    arr.add(small_tmp[gapStat[-0.02] - 1])
                if gapStat[-0.04] == len(small_tmp):
                    if gapStat[-0.05] == 0:
                        findTurn(arr, small_tmp, small_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=False, choose_single=True)
            if len(big_tmp) > len(small_tmp):
                if len(big_tmp) == 2:
                    if gapStat[0.03] == 1:
                        arr.add(big_tmp[-1])
            if len(big_tmp) == 1:
                if gapStat[0.03] == 0:
                    arr.add(big_tmp[0])
            if len(small_near_tmp) - len(big_tmp) >= -1 and len(small_near_tmp) - len(big_near_tmp) >= -1:
                if small_near_gap_tmp[0] == small_near_gap_tmp[-1]:
                    for v in small_near_tmp:
                        arr.add(v)
                if len(small_near_tmp) == 2:
                    if small_near_gap_tmp[0] < -0.0085:
                        arr.add(small_near_tmp[1])
                    if small_near_gap_tmp[1] > -0.011 and small_near_gap_tmp[1] < -0.01:
                        arr.add(small_near_tmp[0])
                if nearGapStat[-0.01] == 0:
                    findTurn(arr, small_near_tmp, small_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=True, choose_single=True)
                    findTurn(arr, small_near_tmp, small_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=False, choose_single=False)
                if midJudge(small_near_tmp, nearGapStat, -0.01, False):
                    findTurn(arr, small_near_tmp, small_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=True, consecutive_at_left=False, choose_single=False)
                if midJudge(small_near_tmp, nearGapStat, -0.01, True):
                    findTurn(arr, small_near_tmp, small_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=True, choose_single=False)
            elif len(small_near_tmp) >= len(big_tmp):
                if len(small_near_tmp) == 2:
                    if small_near_gap_tmp[0] > -0.0116:
                        arr.add(small_near_tmp[1])
            print('参差不齐接近时小的比大的多一些' + extraSmall(seq))
        elif len(seq['small']) + len(seq['smallNear']) < len(seq['big']) + len(seq['bigNear']):
            if len(small_near_tmp) == 1:
                if nearGapStat[-0.01] == 0:
                    arr.add(small_near_tmp[0])
            if len(small_near_tmp) - len(small_tmp) >= -1 and len(small_near_tmp) - len(big_near_tmp) >= -2:
                if midJudge(small_near_tmp, nearGapStat, -0.01, False):
                    pos = nearGapStat[-0.01] - 1
                    gapAndConsecutive(arr, small_near_tmp, small_near_gap_tmp, pos, left=True)
                if midJudge(small_near_tmp, nearGapStat, -0.01, True):
                    pos = nearGapStat[-0.01] - 1
                    gapAndConsecutive(arr, small_near_tmp, small_near_gap_tmp, pos, left=True)
                if len(small_near_tmp) == 2:
                    if nearGapStat[-0.01] <= 1:
                        arr.add(small_near_tmp[0])
                        if small_near_gap_tmp[1] - small_near_gap_tmp[0] < 0.0001:
                            arr.add(small_near_tmp[1])
                        if small_near_gap_tmp[0] < -0.005 and small_near_gap_tmp[1] > -0.005:
                            arr.add(small_near_tmp[1])
                if nearGapStat[-0.01] == 0:
                    findTurn(arr, small_near_tmp, small_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=False, choose_single=False)
                    findTurn(arr, small_near_tmp, small_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=True, choose_single=False)
                elif nearGapStat[-0.01] == 1:
                    arr.add(small_near_tmp[1])
                if midJudge(small_near_tmp, nearGapStat, -0.01, False):
                    findTurn(arr, small_near_tmp, small_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=False, choose_single=False)
            if len(big_tmp) - len(small_tmp) >= -1 and len(big_tmp) >= len(small_near_tmp):
                if gapStat[0.02] == len(big_tmp):
                    if big_gap_tmp[0] < 0.023:
                        arr.add(big_tmp[0])
                if len(big_tmp) == 2:
                    if gapStat[0.03] == 1:
                        arr.add(big_tmp[1])
                if midJudge(big_tmp, gapStat, 0.02, True):
                    pos = len(big_tmp) - gapStat[0.02]
                    if big_gap_tmp[pos] < 0.0204:
                        if pos + 1 < len(big_tmp):
                            arr.add(big_tmp[pos + 1])
                if midJudge(big_tmp, gapStat, 0.04, True):
                    pos = len(big_tmp) - gapStat[0.04]
                    gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos, left=False)
                    findTurn(arr, big_tmp, big_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=True, consecutive_at_left=False, choose_single=False)
                if midJudge(big_tmp, gapStat, 0.03, True):
                    pos = len(big_tmp) - gapStat[0.03] - 1
                    gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos, left=True)
                    gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos + 1, left=False)
                if midJudge(big_tmp, gapStat, 0.03, False):
                    pos = len(big_tmp) - gapStat[0.03]
                    gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos, left=False)
            if len(big_near_tmp) == 2:
                if nearGapStat[0.01] == 1:
                    arr.add(big_near_tmp[1])
            if len(small_tmp) == 2:
                if gapStat[-0.02] == 1:
                    arr.add(small_tmp[0])
                if gapStat[-0.03] == 2:
                    if small_gap_tmp[0] == small_gap_tmp[1]:
                        arr.add(small_tmp[0])
                        arr.add(small_tmp[1])
            if len(small_tmp) - len(big_near_tmp) >= -1:
                if len(small_tmp) == 1:
                    if small_gap_tmp[0] > -0.041 and small_gap_tmp[0] < -0.04:
                        arr.add(small_tmp[0])
            if len(small_tmp) >= len(big_tmp):
                if len(small_tmp) == gapStat[-0.03]:
                    if small_gap_tmp[-2] > -0.04 and small_gap_tmp[-2] < -0.039:
                        arr.add(small_tmp[-2])
                if midJudge(small_tmp, gapStat, -0.03, True):
                    pos = gapStat[-0.03] - 1
                    gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos, left=True)
                if midJudge(small_tmp, gapStat, -0.04, True):
                    pos = gapStat[-0.04]
                    gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos, left=False)
                if midJudge(small_tmp, gapStat, -0.04, False):
                    pos = gapStat[-0.04]
                    gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos, left=False)
                    gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos - 1, left=True)
            if len(big_tmp) == 1:
                if gapStat[0.03] == 0:
                    arr.add(big_tmp[0])
            if len(big_near_tmp) >= len(small_tmp) and len(big_near_tmp) >= len(small_near_tmp):
                if nearGapStat[0.01] <= 1:
                    findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=True, choose_single=False)
                    if big_near_gap_tmp[-1] > 0.0091:
                        arr.add(big_near_tmp[-2])
                if midJudge(big_near_tmp, nearGapStat, 0.01, True):
                    pos = len(big_near_tmp) - nearGapStat[0.01] - 1
                    gapAndConsecutive(arr, big_near_tmp, big_near_gap_tmp, pos, left=True)
                    gapAndConsecutive(arr, big_near_tmp, big_near_gap_tmp, pos + 1, left=False)
                if midJudge(big_near_tmp, nearGapStat, 0.01, False):
                    arr.add(big_near_tmp[0])
                    pos = len(big_near_tmp) - nearGapStat[0.01]
                    gapAndConsecutive(arr, big_near_tmp, big_near_gap_tmp, pos, left=False)
                    findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=False, choose_single=True)
                    if big_near_gap_tmp[pos] < 0.011:
                        arr.add(big_near_tmp[pos + 1])
            print('参差不齐接近时大的比小的多一些' + extraBig(seq))
        else:
            if len(big_tmp) >= len(small_tmp) and len(big_tmp) >= len(small_near_tmp):
                if gapStat[0.02] < len(big_tmp):
                    arr.add(big_tmp[gapStat[0.02] - 1])
                if midJudge(big_tmp, gapStat, 0.03, False):
                    pos = len(big_tmp) - gapStat[0.03]
                    arr.add(big_tmp[pos])
                    for i in range(pos + 1, len(big_tmp)):
                        if big_gap_tmp[i] - big_gap_tmp[pos] < 0.0001:
                            arr.add(big_tmp[i])
                if midJudge(big_tmp, gapStat, 0.03, True):
                    if gapStat[0.04] == 0:
                        findTurn(arr, big_tmp, big_gap_tmp, approach_threshold=0.0001, gap_threshold=0.1, reverse=True, consecutive_at_left=True, choose_single=True)
                        pos = len(big_tmp) - gapStat[0.03]
                        arr.add(big_tmp[pos])
                        if pos + 1 < len(big_tmp) and big_gap_tmp[pos + 1] - big_gap_tmp[pos] < 0.00001:
                            arr.add(big_tmp[pos + 1])
            elif len(big_tmp) > len(small_tmp) and len(big_tmp) > len(big_near_tmp):
                if gapStat[0.03] >= len(big_tmp) / 2 and gapStat[0.03] < len(big_tmp):
                    if gapStat[0.04] == 0:
                        arr.add(big_tmp[len(big_tmp) - gapStat[0.03]])
            if len(small_near_tmp) - len(big_near_tmp) >= -1 and len(small_near_tmp) >= len(big_tmp):
                if nearGapStat[-0.01] == 1:
                    arr.add(small_near_tmp[0])
                    arr.add(small_near_tmp[1])
                if midJudge(small_near_tmp, nearGapStat, -0.01, True):
                    pos = nearGapStat[-0.01] - 1
                    gapAndConsecutive(arr, small_near_tmp, small_near_gap_tmp, pos + 1, left=False)
                    arr.add(small_near_tmp[pos])
                    for i in range(pos - 1, -1, -1):
                        if small_near_gap_tmp[pos] - small_near_gap_tmp[i] < 0.0001:
                            arr.add(small_near_tmp[i])
            if len(small_near_tmp) > len(big_tmp):
                if len(small_near_tmp) == 2:
                    if nearGapStat[-0.01] == 0:
                        arr.add(small_near_tmp[0])
                        arr.add(small_near_tmp[1])
                    if nearGapStat[-0.01] == 1:
                        arr.add(small_near_tmp[1])
            if len(small_tmp) - len(big_near_tmp) >= -1 and len(small_tmp) >= len(big_tmp):
                if len(small_tmp) == gapStat[-0.03]:
                    if small_gap_tmp[-1] > -0.032:
                        arr.add(small_tmp[-1])
                if gapStat[-0.02] == len(small_tmp) - 1:
                    arr.add(small_tmp[-1])
                if midJudge(small_tmp, gapStat, -0.02, True):
                    pos = gapStat[-0.02] - 1
                    gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos, left=True)
                    if small_gap_tmp[pos] > -0.022:
                        if pos - 1 > -1:
                            arr.add(small_tmp[pos - 1])
                if midJudge(small_tmp, gapStat, -0.04, True):
                    pos = gapStat[-0.04]
                    gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos, left=False)
                if midJudge(small_tmp, gapStat, -0.03, False):
                    pos = gapStat[-0.03]
                    gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos, left=False)
                if midJudge(small_tmp, gapStat, -0.03, True):
                    arr.add(small_tmp[0])
                    arr.add(small_tmp[gapStat[-0.03] - 1])
            if len(big_near_tmp) >= len(small_tmp) and len(big_near_tmp) >= len(small_near_tmp):
                if midJudge(big_near_tmp, nearGapStat, 0.01, False):
                    pos = len(big_near_tmp) - nearGapStat[0.01] - 1
                    gapAndConsecutive(arr, big_near_tmp, big_near_gap_tmp, pos, left=True)
                    gapAndConsecutive(arr, big_near_tmp, big_near_gap_tmp, pos + 1, left=False)
                    if big_near_gap_tmp[pos] > 0.0089:
                        if pos - 1 > -1:
                            arr.add(big_near_tmp[pos - 1])
                    findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=False, choose_single=True)
                    findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=True, choose_single=False)
                    if noConsecutiveGap(big_near_gap_tmp):
                        arr.add(big_near_tmp[0])
                if midJudge(big_near_tmp, nearGapStat, 0.01, True):
                    arr.add(big_near_tmp[len(big_near_tmp) - nearGapStat[0.01] - 1])
                    pos = len(big_near_tmp) - nearGapStat[0.01]
                    arr.add(big_near_tmp[pos])
                    for i in range(pos + 1, len(big_near_tmp)):
                        if big_near_gap_tmp[i] - big_near_gap_tmp[pos] < 0.00001:
                            arr.add(big_near_tmp[i])
                    if big_near_gap_tmp[pos] < 0.011:
                        if pos + 1 < len(big_near_tmp):
                            arr.add(big_near_tmp[pos + 1])
                    findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=True, consecutive_at_left=True, choose_single=True)
                if nearGapStat[0.01] == 0:
                    if big_near_gap_tmp[-1] > 0.005 and big_near_gap_tmp[-2] < 0.005:
                        arr.add(big_near_tmp[-1])
                    if big_near_gap_tmp[-1] > 0.009:
                        arr.add(big_near_tmp[-1])
                    findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=True, choose_single=False)
                    findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.1, reverse=True, consecutive_at_left=False, choose_single=False)
                    if noConsecutiveGap(big_near_gap_tmp):
                        if len(big_near_tmp) > 2:
                            arr.add(big_near_tmp[1])
                if nearGapStat[0.01] == len(big_near_tmp):
                    findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=False, choose_single=True)
            if len(small_near_tmp) >= len(big_near_tmp) and len(small_near_tmp) >= len(big_tmp):
                if nearGapStat[-0.01] == 0:
                    findTurn(arr, small_near_tmp, small_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.1, reverse=False, consecutive_at_left=False, choose_single=False)
                elif midJudge(small_near_tmp, nearGapStat, -0.01, True):
                    arr.add(small_near_tmp[0])
                elif nearGapStat[-0.01] == len(small_near_tmp):
                    findTurn(arr, small_near_tmp, small_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.1, reverse=False, consecutive_at_left=True, choose_single=False)
            if len(small_tmp) == 2:
                if gapStat[-0.03] == 1:
                    arr.add(small_tmp[0])
                if gapStat[-0.04] == 1:
                    arr.add(small_tmp[0])
            if len(big_near_tmp) == 2:
                arr.add(big_near_tmp[0])
            if len(big_tmp) == 1:
                if gapStat[0.04] == 0:
                    arr.add(big_tmp[0])
            if len(big_tmp) == 2:
                if gapStat[0.03] == 1:
                    arr.add(big_tmp[-1])
                if gapStat[0.02] == 1:
                    arr.add(big_tmp[0])
                    arr.add(big_tmp[1])
                if gapStat[0.02] == 2:
                    if gapStat[0.03] == 0:
                        if big_gap_tmp[0] < 0.021:
                            arr.add(big_tmp[0])
            print('参差不齐接近时大小一样')
    #连续接近
    elif count['near'] >= 5 and maxConsecutiveCount['near'] >= 4:
        if len(seq['small']) + len(seq['smallNear']) >= 7:
            print('连续接近时小的偏多' + extraSmall(seq))
        elif len(seq['big']) + len(seq['bigNear']) >= 7:
            if len(big_near_tmp) >= len(small_tmp) and len(big_near_tmp) >= len(small_near_tmp):
                if nearGapStat[0.01] == 0:
                    findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=False, choose_single=True)
                if midJudge(big_near_tmp, nearGapStat, 0.01, False):
                    if big_near_gap_tmp[0] < 0.0024 and big_near_gap_tmp[1] > 0.005:
                        arr.add(big_near_tmp[0])
                    pos = len(big_near_tmp) - nearGapStat[0.01] - 1
                    arr.add(big_near_tmp[pos])
                    if pos - 1 > -1 and big_near_gap_tmp[pos] - big_near_gap_tmp[pos - 1] < 0.0001:
                        arr.add(big_near_tmp[pos - 1])
                    findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=True, consecutive_at_left=False, choose_single=False)
                    findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=False, choose_single=True)
            if len(small_near_tmp) == 1:
                if nearGapStat[-0.01] == 0:
                    arr.add(small_near_tmp[0])
            if len(small_tmp) - len(big_tmp) >= -1:
                if len(small_tmp) == 2:
                    if gapStat[-0.03] == 1:
                        arr.add(small_tmp[0])
            if len(big_tmp) >= len(small_tmp) and len(big_tmp) >= len(small_near_tmp):
                if midJudge(big_tmp, gapStat, 0.04, False):
                    pos = len(big_tmp) - gapStat[0.04] - 1
                    arr.add(big_tmp[pos])
                if midJudge(big_tmp, gapStat, 0.03, True):
                    pos = len(big_tmp) - gapStat[0.03]
                    arr.add(big_tmp[pos])
                    for i in range(pos + 1, len(big_tmp)):
                        if big_gap_tmp[i] - big_gap_tmp[pos] < 0.00001:
                            arr.add(big_tmp[i])
            print('连续接近时大的偏多' + extraBig(seq))
        elif len(seq['small']) + len(seq['smallNear']) > len(seq['big']) + len(seq['bigNear']):
            if len(big_near_tmp) - len(small_near_tmp) >= -1 and len(big_near_tmp) > len(small_tmp):
                if nearGapStat[0.01] == 1:
                    arr.add(big_near_tmp[-2])
                elif nearGapStat[0.01] == len(big_near_tmp):
                    findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.25, reverse=False, consecutive_at_left=False, choose_single=False)
            if len(small_near_tmp) >= len(big_near_tmp) and len(small_near_tmp) >= len(big_tmp):
                if nearGapStat[-0.01] == 1:
                    arr.add(small_near_tmp[0])
                if midJudge(small_near_tmp, nearGapStat, -0.01, False):
                    findTurn(arr, small_near_tmp, small_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.1, reverse=False, consecutive_at_left=True, choose_single=False)
            if len(big_near_tmp) >= len(small_tmp) and len(big_near_tmp) >= len(small_near_tmp):
                if nearGapStat[0.01] == 1:
                    arr.add(big_near_tmp[-1])
            if len(big_tmp) >= len(small_tmp):
                if gapStat[0.02] <= len(big_tmp) / 2:
                    arr.add(big_tmp[len(big_tmp) - gapStat[0.02] - 1])
            if len(small_tmp) >= len(big_tmp) and len(small_tmp) - len(big_near_tmp) >= -1:
                if len(small_tmp) == 2:
                    if gapStat[-0.03] == 1:
                        arr.add(small_tmp[0])
            print('连续接近时小的比大的多一些' + extraSmall(seq))
        elif len(seq['small']) + len(seq['smallNear']) < len(seq['big']) + len(seq['bigNear']):
            if len(small_near_tmp) - len(big_tmp) >= -1 and len(small_near_tmp) - len(big_near_tmp) >= -1:
                if len(small_near_tmp) == 2:
                    if nearGapStat[-0.01] == 0:
                        arr.add(small_near_tmp[0])
                        if small_near_gap_tmp[1] - small_near_gap_tmp[0] < 0.0001:
                            arr.add(small_near_tmp[1])
                if nearGapStat[-0.01] == 1:
                    arr.add(small_near_tmp[1])
                if midJudge(small_near_tmp, nearGapStat, -0.01, False):
                    pos = nearGapStat[-0.01] - 1
                    arr.add(small_near_tmp[pos])
                    for i in range(pos - 1, -1, -1):
                        if small_near_gap_tmp[pos] - small_near_gap_tmp[i] < 0.00001:
                            arr.add(small_near_tmp[i])
                if nearGapStat[-0.01] == 0:
                    if small_near_gap_tmp[-1] > -0.0025 and small_near_gap_tmp[-2] < -0.0051:
                        arr.add(small_near_tmp[-1])
            elif len(small_near_tmp) >= len(big_tmp):
                if nearGapStat[-0.01] == 1:
                    findTurn(arr, small_near_tmp, small_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.1, reverse=False, consecutive_at_left=False, choose_single=True)
            if len(small_near_tmp) == 2:
                if nearGapStat[-0.01] == 1:
                    arr.add(small_near_tmp[0])
                elif nearGapStat[-0.01] == 2:
                    arr.add(small_near_tmp[-1])
            if len(big_tmp) >= len(small_tmp) and len(big_tmp) >= len(small_near_tmp):
                if gapStat[0.02] == 1:
                    arr.add(big_tmp[-1])
                if midJudge(big_tmp, gapStat, 0.02, True):
                    pos = len(big_tmp) - gapStat[0.02] - 1
                    gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos, left=True)
            if len(big_near_tmp) >= len(small_tmp) and len(big_near_tmp) >= len(small_near_tmp):
                if midJudge(big_near_tmp, nearGapStat, 0.01, True):
                    pos = len(big_near_tmp) - nearGapStat[0.01]
                    arr.add(big_near_tmp[pos])
                    for i in range(pos + 1, len(big_near_tmp)):
                        if big_near_gap_tmp[i] - big_near_gap_tmp[pos] < 0.0001:
                            arr.add(big_near_tmp[i])
                    arr.add(big_near_tmp[pos - 1])
                    for i in range(pos - 2, -1, -1):
                        if big_near_gap_tmp[pos - 1] - big_near_gap_tmp[i] < 0.00001:
                            arr.add(big_near_tmp[i])
                    findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=True, consecutive_at_left=True, choose_single=True)
            if len(small_tmp) == 1:
                if gapStat[-0.04] == 0:
                    arr.add(small_tmp[0])
            if len(small_tmp) == 2:
                if gapStat[-0.03] == 1:
                    arr.add(small_tmp[0])
                if gapStat[-0.04] == 1:
                    arr.add(small_tmp[1])
            print('连续接近时大的比小的多一些' + extraBig(seq))
        else:
            if len(big_near_tmp) >= len(small_tmp) and len(big_near_tmp) >= len(small_near_tmp):
                if nearGapStat[0.01] < len(big_near_tmp):
                    pos = len(big_near_tmp) - nearGapStat[0.01]
                    if pos > -1 and pos < len(big_near_tmp):
                        arr.add(big_near_tmp[pos])
                        for i in range(pos + 1, len(big_near_tmp)):
                            if big_near_gap_tmp[i] - big_near_gap_tmp[pos] < 0.00001:
                                arr.add(big_near_tmp[i])
                if nearGapStat[0.01] == 0:
                    if 0.01 - big_near_gap_tmp[-1] < 0.0002:
                        if 0.01 - big_near_gap_tmp[-2] > 0.001:
                            arr.add(big_near_tmp[-2])
            if len(small_near_tmp) - len(big_near_tmp) >= -1 and len(small_near_tmp) > len(big_tmp):
                if nearGapStat[-0.01] == 1:
                    arr.add(small_near_tmp[1])
            if len(small_tmp) == len(big_tmp):
                if gapStat[-0.03] >= len(small_tmp) / 2 and gapStat[-0.03] < len(small_tmp):
                    arr.add(small_tmp[gapStat[-0.03]])
                if gapStat[0.02] == len(big_tmp):
                    if gapStat[0.03] == 0:
                        arr.add(big_tmp[0])
            if len(small_tmp) - len(big_tmp) >= -1:
                if len(small_tmp) == 2:
                    if gapStat[-0.03] == 1:
                        arr.add(small_tmp[0])
                        arr.add(small_tmp[1])
                    if gapStat[-0.04] == 1:
                        arr.add(small_tmp[1])
            print('连续接近时大小一样')
    elif count['small'] >= 5 and maxConsecutiveCount['small'] < 4:
        if gapStat[-0.02] == len(small_tmp):
            if small_gap_tmp[-1] <= -0.0199 and small_gap_tmp[-1] > -0.02:
                arr.add(small_tmp[-2])
            if gapStat[-0.03] < 3:
                findTurn(arr, small_tmp, small_gap_tmp, approach_threshold=0.0001, gap_threshold=0.2, reverse=True, consecutive_at_left=True, choose_single=False)
            if gapStat[-0.03] == len(small_tmp) - 1:
                arr.add(small_tmp[-2])
            if gapStat[-0.03] == len(small_tmp) / 2:
                findTurn(arr, small_tmp, small_gap_tmp, approach_threshold=0.0001, gap_threshold=0.2, reverse=True, consecutive_at_left=True, choose_single=True)
        elif gapStat[-0.02] < len(small_tmp):
            if gapStat[-0.03] <= len(small_tmp) / 2:
                arr.add(small_tmp[-1])
        if gapStat[-0.03] == 2:
            arr.add(small_tmp[2])
        if gapStat[-0.03] == len(small_tmp) - 1:
            if gapStat[-0.02] == len(small_tmp) - 1:
                arr.add(small_tmp[-1])
                arr.add(small_tmp[-2])
        if gapStat[-0.03] == len(small_tmp):
            if gapStat[-0.04] > 0 and gapStat[-0.04] < len(small_tmp):
                arr.add(small_tmp[gapStat[-0.04]])
                if gapStat[-0.04] + 1 < len(small_gap_tmp) and small_gap_tmp[gapStat[-0.04] + 1] - small_gap_tmp[gapStat[-0.04]] < 0.00001:
                    arr.add(small_tmp[gapStat[-0.04] + 1])
        if midJudge(small_tmp, gapStat, -0.02, True):
            pos = gapStat[-0.02] - 1
            arr.add(small_tmp[pos])
        if midJudge(small_tmp, gapStat, -0.02, False):
            arr.add(small_tmp[gapStat[-0.02] - 1])
            pos = gapStat[-0.02]
            arr.add(small_tmp[pos])
            for i in range(pos + 1, len(small_tmp)):
                if small_gap_tmp[i] - small_gap_tmp[pos] < 0.0001:
                    arr.add(small_tmp[i])
        if midJudge(small_tmp, gapStat, -0.05, False):
            arr.add(small_tmp[gapStat[-0.05] - 1])
        if midJudge(small_tmp, gapStat, -0.04, True):
            findTurn(arr, small_tmp, small_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=False, choose_single=True)
        if midJudge(small_tmp, gapStat, -0.04, False):
            arr.add(small_tmp[gapStat[-0.04]])
            arr.add(small_tmp[gapStat[-0.04] - 1])
        if midJudge(small_tmp, gapStat, -0.03, True):
            findTurn(arr, small_tmp, small_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=False, choose_single=False)
            findTurn(arr, small_tmp, small_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=True, choose_single=False)
            pos = gapStat[-0.03]
            gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos, left=False)
            gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos - 1, left=True)
        if midJudge(small_tmp, gapStat, -0.03, False):
            arr.add(small_tmp[gapStat[-0.03]])
        if len(big_near_tmp) > len(big_tmp) and len(big_near_tmp) >= len(small_near_tmp):
            if nearGapStat[0.01] == 0:
                if (big_near_gap_tmp[1] - big_near_gap_tmp[0]) / big_near_gap_tmp[0] > 5:
                    arr.add(big_near_tmp[1])
                findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=True, choose_single=False)
        if len(small_near_tmp) >= len(big_tmp) and len(small_near_tmp) >= len(big_near_tmp):
            if nearGapStat[-0.01] == 0 or nearGapStat[-0.01] == len(small_near_tmp):
                if noConsecutiveGap(small_near_gap_tmp):
                    arr.add(small_near_tmp[0])
                findTurn(arr, small_near_tmp, small_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=True, consecutive_at_left=False, choose_single=False)
            if midJudge(small_near_tmp, nearGapStat, -0.01, True):
                findTurn(arr, small_near_tmp, small_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=True, choose_single=False)
            if nearGapStat[-0.01] == 0:
                mid = int(len(small_near_tmp) / 2)
                arr.add(small_near_tmp[mid])
                if mid == 0 and mid + 1 < len(small_near_tmp):
                    if small_near_gap_tmp[mid + 1] - small_near_gap_tmp[mid] < 0.0001:
                        arr.add(small_near_tmp[mid + 1])
                if mid == len(small_near_tmp) - 1 and mid - 1 > -1:
                    if small_near_gap_tmp[mid] - small_near_gap_tmp[mid - 1] < 0.0001:
                        arr.add(small_near_tmp[mid - 1])
                findTurn(arr, small_near_tmp, small_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=True, choose_single=False)
                findTurn(arr, small_near_tmp, small_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=True, choose_single=True)
            if midJudge(small_near_tmp, nearGapStat, -0.01, False):
                pos = nearGapStat[-0.01]
                arr.add(small_near_tmp[pos])
                if pos + 1 < len(small_near_tmp) and small_near_gap_tmp[pos + 1] - small_near_gap_tmp[pos] < 0.00001:
                    arr.add(small_near_tmp[pos + 1])
        if len(big_tmp) >= len(small_near_tmp):
            if gapStat[0.03] == 0:
                if big_gap_tmp[0] == big_gap_tmp[-1]:
                    for v in big_tmp:
                        arr.add(v)
            if len(big_tmp) == 2:
                if gapStat[0.02] == 1:
                    arr.add(big_tmp[0])
            if len(big_tmp) >= 3:
                if midJudge(big_tmp, gapStat, 0.03, False):
                    pos = len(big_tmp) - gapStat[0.03] - 1
                    arr.add(big_tmp[pos])
                if midJudge(big_tmp, gapStat, 0.02, True):
                    arr.add(big_tmp[len(big_tmp) - gapStat[0.02]])
                if midJudge(big_tmp, gapStat, 0.02, False):
                    findTurn(arr, big_tmp, big_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=True, consecutive_at_left=True, choose_single=False)
        if len(big_near_tmp) - len(small_tmp) >= -1 and len(big_near_tmp) >= len(small_near_tmp):
            if nearGapStat[0.01] == 0:
                arr.add(big_near_tmp[-1])
            if nearGapStat[0.01] <= 1:
                findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.1, reverse=False, consecutive_at_left=False, choose_single=True)
            if midJudge(big_near_tmp, nearGapStat, 0.01, False):
                pos = len(big_near_tmp) - nearGapStat[0.01]
                arr.add(big_near_tmp[pos])
        elif len(big_near_tmp) >= len(small_near_tmp):
            if len(big_near_tmp) == 2:
                if big_near_gap_tmp[0] < 0.0002:
                    arr.add(big_near_tmp[0])
            if midJudge(big_near_tmp, nearGapStat, 0.01, True):
                pos = len(big_near_tmp) - nearGapStat[0.01]
                if big_near_gap_tmp[pos] < 0.012:
                    arr.add(big_near_tmp[pos + 1])
        if len(small_near_tmp) == 1:
            if small_near_gap_tmp[0] > -0.013:
                arr.add(small_near_tmp[0])
        if len(big_near_tmp) == 1:
            arr.add(big_near_tmp[0])
        if len(big_tmp) == 1:
            if gapStat[0.03] == 0:
                arr.add(big_tmp[0])
        if len(big_near_tmp) >= len(small_near_tmp):
            if len(big_near_tmp) == 2:
                if nearGapStat[0.01] <= 1:
                    arr.add(big_near_tmp[-1])
                    if big_near_gap_tmp[-1] - big_near_gap_tmp[0] < 0.0001:
                        arr.add(big_near_tmp[0])
                if nearGapStat[0.01] == 1:
                    arr.add(big_near_tmp[0])
                if nearGapStat[0.01] == 2:
                    arr.add(big_near_tmp[0])
                    if big_near_gap_tmp[1] - big_near_gap_tmp[0] < 0.0001:
                        arr.add(big_near_tmp[1])
            elif len(big_near_tmp) > 2:
                if midJudge(big_near_tmp, nearGapStat, 0.01, False):
                    pos = len(big_near_tmp) - nearGapStat[0.01] - 1
                    arr.add(big_near_tmp[pos])
                if nearGapStat[0.01] == 1:
                    if noConsecutiveGap(big_near_gap_tmp):
                        arr.add(big_near_tmp[0])
                if nearGapStat[0.01] == 0:
                    arr.add(big_near_tmp[int(len(big_near_tmp) / 2)])
                    findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=False, choose_single=True)
                    findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=False, choose_single=False)
                if midJudge(big_near_tmp, nearGapStat, 0.01, False):
                    findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=True, choose_single=False)
        print('参差不齐小' + restExcSmall(seq))
    elif count['big'] >= 5 and count['near'] >= 2:
        if gapStat[0.02] < len(big_tmp):
            if gapStat[0.02] == len(big_tmp) - 1:
                arr.add(big_tmp[0])
                if gapStat[0.03] <= 2:
                    arr.add(big_tmp[1])
        if len(small_near_tmp) > len(big_near_tmp):
            if len(small_near_tmp) == 2:
                if nearGapStat[-0.01] == 0:
                    arr.add(small_near_tmp[-1])
            if nearGapStat[-0.01] == 0:
                findTurn(arr, small_near_tmp, small_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.5, reverse=True, consecutive_at_left=True, choose_single=False)
        if len(big_near_tmp) > len(small_near_tmp):
            if len(big_near_tmp) == 2:
                if nearGapStat[0.01] == 1:
                    pos = len(big_near_tmp) - nearGapStat[0.01]
                    arr.add(big_near_tmp[pos])
        if len(big_tmp) > len(small_tmp) and len(big_tmp) > len(big_near_tmp):
            if gapStat[0.02] == len(big_tmp):
                if big_gap_tmp[0] < 0.022:
                    arr.add(big_tmp[0])
                if midJudge(big_tmp, gapStat, 0.03, False):
                    findTurn(arr, big_tmp, big_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=False, choose_single=True)
                    findTurn(arr, big_tmp, big_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=True, choose_single=False)
            if gapStat[0.04] == 1:
                arr.add(big_tmp[-1])
                arr.add(big_tmp[-2])
                if big_gap_tmp[-2] - big_gap_tmp[-3] < 0.00001:
                    arr.add(big_tmp[-3])
            if gapStat[0.05] >= 2 and gapStat[0.05] < len(big_tmp):
                pos = len(big_tmp) - gapStat[0.05]
                arr.add(big_tmp[pos])
                if big_gap_tmp[pos + 1] - big_gap_tmp[pos] < 0.00001:
                    arr.add(big_tmp[pos + 1])
                if gapStat[0.05] <= len(big_tmp) / 2:
                    findTurn(arr, big_tmp, big_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=True, consecutive_at_left=False, choose_single=False)
            if gapStat[0.04] <= len(big_tmp) / 2 and gapStat[0.04] >= 2:
                if gapStat[0.05] == 0:
                    arr.add(big_tmp[-1])
                arr.add(big_tmp[len(big_tmp) - gapStat[0.04] - 1])
                findTurn(arr, big_tmp, big_gap_tmp, approach_threshold=0.0001, gap_threshold=0.1, reverse=True, consecutive_at_left=False, choose_single=False)
            if gapStat[0.03] == 0 and gapStat[0.02] < len(big_tmp):
                findTurn(arr, big_tmp, big_gap_tmp, approach_threshold=0.0001, gap_threshold=0.1, reverse=False, consecutive_at_left=False, choose_single=True)
                if gapStat[0.02] == 1:
                    arr.add(big_tmp[-2])
                    if len(big_tmp) > 2:
                        for i in range(len(big_tmp) - 3, -1, -1):
                            if big_gap_tmp[-2] - big_gap_tmp[i] < 0.00001:
                                arr.add(big_tmp[i])
            if gapStat[0.03] >= 1 and gapStat[0.03] <= 2:
                arr.add(big_tmp[-1])
            if midJudge(big_tmp, gapStat, 0.05, False):
                if len(big_tmp) > 4:
                    if big_gap_tmp[-1] > 0.059 and big_gap_tmp[-3] < 0.051:
                        arr.add(big_tmp[-2])
                pos = len(big_tmp) - gapStat[0.05] - 1
                arr.add(big_tmp[pos])
                for i in range(pos - 1, -1, -1):
                    if big_gap_tmp[pos] - big_gap_tmp[i] < 0.0001:
                        arr.add(big_tmp[i])
            if midJudge(big_tmp, gapStat, 0.04, False):
                pos = len(big_tmp) - gapStat[0.04]
                arr.add(big_tmp[pos])
                for i in range(pos + 1, len(big_tmp)):
                    if big_gap_tmp[i] - big_gap_tmp[pos] < 0.0001:
                        arr.add(big_tmp[i])
            if midJudge(big_tmp, gapStat, 0.04, True):
                if gapStat[0.05] == 0:
                    arr.add(big_tmp[-2])
                    pos = len(big_tmp) - gapStat[0.04]
                    arr.add(big_tmp[pos])
                    if pos + 1 < len(big_tmp) and big_gap_tmp[pos + 1] - big_gap_tmp[pos] < 0.00001:
                        arr.add(big_tmp[pos + 1])
            if midJudge(big_tmp, gapStat, 0.03, True):
                arr.add(big_tmp[len(big_tmp) - gapStat[0.03]])
            if midJudge(big_tmp, gapStat, 0.03, False):
                if gapStat[0.04] == 0:
                    arr.add(big_tmp[-1])
                    pos = len(big_tmp) - gapStat[0.03]
                    arr.add(big_tmp[pos])
                pos = len(big_tmp) - gapStat[0.03] - 1
                arr.add(big_tmp[pos])
                for i in range(pos - 1, -1, -1):
                    if big_gap_tmp[pos] - big_gap_tmp[i] < 0.0001:
                        arr.add(big_tmp[i])
            if gapStat[0.02] - len(big_tmp) >= -1:
                if midJudge(big_tmp, gapStat, 0.03, True):
                    pos = len(big_tmp) - gapStat[0.03] - 1
                    arr.add(big_tmp[pos])
                if gapStat[0.03] == 0:
                    arr.add(big_tmp[-1])
                if gapStat[0.03] < len(big_tmp) / 2:
                    findTurn(arr, big_tmp, big_gap_tmp, approach_threshold=0.0001, gap_threshold=0.1, reverse=False, consecutive_at_left=False, choose_single=False)
                    findTurn(arr, big_tmp, big_gap_tmp, approach_threshold=0.0001, gap_threshold=0.1, reverse=False, consecutive_at_left=True, choose_single=True)
            if midJudge(big_tmp, gapStat, 0.02, False):
                pos = len(big_tmp) - gapStat[0.02] - 1
                arr.add(big_tmp[pos])
                for i in range(pos - 1, -1, -1):
                    if big_gap_tmp[pos] - big_gap_tmp[i] < 0.0001:
                        arr.add(big_tmp[i])
            if midJudge(big_tmp, gapStat, 0.02, True):
                arr.add(big_tmp[0])
                if noConsecutiveGap(big_gap_tmp):
                    arr.add(big_tmp[len(big_tmp) - gapStat[0.02] + 1])
                arr.add(big_tmp[len(big_tmp) - gapStat[0.02]])
                arr.add(big_tmp[len(big_tmp) - gapStat[0.02] - 1])
                findTurn(arr, big_tmp, big_gap_tmp, approach_threshold=0.0001, gap_threshold=0.1, reverse=False, consecutive_at_left=True, choose_single=False)
        if len(small_near_tmp) == 1:
            arr.add(small_near_tmp[0])
        if len(big_near_tmp) >= len(small_tmp) and len(big_near_tmp) >= len(small_near_tmp):
            if len(big_near_tmp) == 2:
                if nearGapStat[0.01] == 0:
                    arr.add(big_near_tmp[0])
                if nearGapStat[0.01] == 2:
                    arr.add(big_near_tmp[-1])
        if len(big_near_tmp) > len(small_near_tmp) and len(big_near_tmp) == 2:
            if nearGapStat[0.01] == len(big_near_tmp):
                arr.add(big_near_tmp[1])
            else:
                arr.add(big_near_tmp[0])
        if len(big_near_tmp) >= len(small_tmp) and len(big_near_tmp) >= len(small_near_tmp):
            if len(big_near_tmp) == 2:
                if big_near_gap_tmp[0] < 0.0105 and big_near_gap_tmp[1] > 0.0141:
                    arr.add(big_near_tmp[0])
                if big_near_gap_tmp[0] < 0.0024 and big_near_gap_tmp[1] > 0.008:
                    arr.add(big_near_tmp[1])
            if midJudge(big_near_tmp, nearGapStat, 0.01, True):
                pos = len(big_near_tmp) - nearGapStat[0.01]
                arr.add(big_near_tmp[pos])
                for i in range(pos + 1, len(big_near_tmp)):
                    if big_near_gap_tmp[i] - big_near_gap_tmp[pos] < 0.0001:
                        arr.add(big_near_tmp[i])
                gapAndConsecutive(arr, big_near_tmp, big_near_gap_tmp, pos - 1, left=False)
            if midJudge(big_near_tmp, nearGapStat, 0.01, False):
                pos = len(big_near_tmp) - nearGapStat[0.01] - 1
                if big_near_gap_tmp[pos] > 0.0085:
                    if pos - 1 > -1:
                        arr.add(big_near_tmp[pos - 1])
                arr.add(big_near_tmp[pos])
                if pos - 1 > -1 and big_near_gap_tmp[pos] - big_near_gap_tmp[pos - 1] < 0.00001:
                    arr.add(big_near_tmp[pos - 1])
                pos2 = len(big_near_tmp) - nearGapStat[0.01]
                if pos2 + 1 < len(big_near_tmp):
                    arr.add(big_near_tmp[pos2])
                    if pos2 + 1 < len(big_near_tmp) and big_near_gap_tmp[pos2 + 1] - big_near_gap_tmp[pos2] < 0.0001:
                        arr.add(big_near_tmp[pos2 + 1])
            if nearGapStat[0.01] == 0:
                if big_near_gap_tmp[-1] > 0.009:
                    arr.add(big_near_tmp[-1])
                arr.add(big_near_tmp[0])
                for i in range(1, len(big_near_tmp)):
                    if big_near_gap_tmp[i] - big_near_gap_tmp[0] < 0.0001:
                        arr.add(big_near_tmp[i])
            if nearGapStat[0.01] == 1:
                arr.add(big_near_tmp[-1])
        if len(small_near_tmp) >= len(big_near_tmp):
            if nearGapStat[-0.01] == 0:
                findTurn(arr, small_near_tmp, small_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.1, reverse=False, consecutive_at_left=True, choose_single=True)
            if midJudge(small_near_tmp, nearGapStat, -0.01, False):
                arr.add(small_near_tmp[-1])
                pos = nearGapStat[-0.01] - 1
                gapAndConsecutive(arr, small_near_tmp, small_near_gap_tmp, pos, left=True)
            if len(small_near_tmp) == 2:
                if nearGapStat[-0.01] == 2 and small_near_gap_tmp[0] > -0.012:
                    arr.add(small_near_tmp[0])
                    if small_near_gap_tmp[1] - small_near_gap_tmp[0] < 0.00001:
                        arr.add(small_near_tmp[1])
                elif nearGapStat[-0.01] <= 1:
                    arr.add(small_near_tmp[0])
                    arr.add(small_near_tmp[1])
            if len(small_near_tmp) - len(big_tmp) >= -1:
                if nearGapStat[-0.01] <= 1:
                    findTurn(arr, small_near_tmp, small_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.1, reverse=True, consecutive_at_left=True, choose_single=False)
        if len(small_tmp) >= len(big_near_tmp):
            if len(small_tmp) == 2:
                if gapStat[-0.02] == 1:
                    arr.add(small_tmp[1])
            if gapStat[-0.02] == len(small_tmp):
                if len(small_tmp) > 0:
                    arr.add(small_tmp[-1])
                if len(small_tmp) > 1:
                    arr.add(small_tmp[-2])
                if gapStat[-0.03] == 0:
                    if len(small_tmp) > 1 and small_gap_tmp[0] < -0.025 and small_gap_tmp[1] > -0.023:
                        arr.add(small_tmp[0])
            if gapStat[-0.02] == 1:
                arr.add(small_tmp[0])
            if midJudge(small_tmp, gapStat, -0.02, True):
                arr.add(small_tmp[gapStat[-0.02]])
            if len(small_tmp) == 2:
                if gapStat[-0.02] == 0:
                    arr.add(small_tmp[-1])
            if midJudge(small_tmp, gapStat, -0.03, False):
                arr.add(small_tmp[gapStat[-0.03] - 1])
        if len(small_tmp) == 1:
            if gapStat[-0.03] == 1:
                arr.add(small_tmp[0])
        if len(small_tmp) <= 2 and len(small_tmp) > 0:
            if gapStat[-0.02] <= 1:
                arr.add(small_tmp[0])
            if len(small_tmp) == 2:
                if gapStat[-0.02] == 2:
                    if small_gap_tmp[1] > -0.021:
                        arr.add(small_tmp[0])
        if len(big_near_tmp) == 1:
            if big_near_gap_tmp[0] > 0.0141:
                arr.add(big_near_tmp[0])
            if big_near_gap_tmp[0] < 0.011:
                arr.add(big_near_tmp[0])
        flag = ':参差' if maxConsecutiveCount['big'] < 4 else ':连续'
        print('不是大的就是接近的(大的偏多)' + flag + restExcBig(seq))
    elif count['big'] >= 5 and count['small'] >= 2:
        if gapStat[0.02] == len(big_tmp):
            if gapStat[0.03] <= 1:
                findTurn(arr, big_tmp, big_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=False, choose_single=True)
                findTurn(arr, big_tmp, big_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=True, choose_single=False)
        if midJudge(big_tmp, gapStat, 0.02, True):
            pos = len(big_tmp) - gapStat[0.02] - 1
            arr.add(big_tmp[pos])
        if len(big_tmp) == gapStat[0.02]:
            if midJudge(big_tmp, gapStat, 0.03, False):
                findTurn(arr, big_tmp, big_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=False, choose_single=False)
                findTurn(arr, big_tmp, big_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=True, choose_single=False)
        if midJudge(big_tmp, gapStat, 0.03, False):
            pos = len(big_tmp) - gapStat[0.03]
            gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos, left=False)
            findTurn(arr, big_tmp, big_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=True, consecutive_at_left=True, choose_single=True)
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
        if len(small_tmp) > len(big_near_tmp) and len(small_tmp) - len(big_tmp) >= -1:
            if midJudge(small_tmp, gapStat, -0.03, False):
                pos = gapStat[-0.03]
                gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos, left=False)
            if midJudge(small_tmp, gapStat, -0.02, False):
                arr.add(small_tmp[0])
            if midJudge(small_tmp, gapStat, -0.02, True):
                pos = gapStat[-0.02] - 1
                gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos, left=True)
        elif len(small_tmp) > len(big_near_tmp):
            if midJudge(small_tmp, gapStat, -0.02, False):
                pos = gapStat[-0.02] - 1
                arr.add(small_tmp[pos])
        if len(big_near_tmp) >= len(small_near_tmp):
            if nearGapStat[0.01] == 0:
                arr.add(big_near_tmp[0])
        flag = ':参差' if maxConsecutiveCount['big'] < 4 else ':连续'
        print('不是大的就是小的(大的偏多)' + flag + restExcBig(seq))
    #大:接近:小很均衡
    elif count['big'] <= 4 and count['near'] <= 4 and count['small'] <= 4:
        if len(seq['small']) + len(seq['smallNear']) > len(seq['big']) + len(seq['bigNear']):
            if len(big_tmp) == 2:
                if gapStat[0.03] == 1:
                    arr.add(big_tmp[1])
            if len(big_near_tmp) >= len(small_near_tmp):
                if len(big_near_tmp) == 2:
                    if nearGapStat[0.01] == 0:
                        if big_near_gap_tmp[0] == big_near_gap_tmp[1]:
                            arr.add(big_near_tmp[0])
                            arr.add(big_near_tmp[1])
            if len(big_tmp) >= len(small_tmp) and len(big_tmp) - len(small_near_tmp) >= -1:
                if gapStat[0.02] == len(big_tmp):
                    if gapStat[0.03] == 0:
                        findTurn(arr, big_tmp, big_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=True, choose_single=False)
                if midJudge(big_tmp, gapStat, 0.02, False):
                    pos = len(big_tmp) - gapStat[0.02]
                    if big_gap_tmp[pos - 1] == big_gap_tmp[pos - 2] or big_gap_tmp[pos - 1] == big_gap_tmp[pos]:
                        arr.add(big_tmp[pos])
                        for i in range(pos - 1, -1, -1):
                            if big_gap_tmp[pos] - big_gap_tmp[i] < 0.00001:
                                arr.add(big_tmp[i])
            elif len(big_tmp) >= len(small_near_tmp):
                if len(big_tmp) == 2:
                    if gapStat[0.02] == 1:
                        arr.add(big_tmp[0])
            if len(small_tmp) >= len(big_tmp) and len(small_tmp) >= len(big_near_tmp):
                if midJudge(small_tmp, gapStat, -0.02, True):
                    pos = gapStat[-0.02]
                    gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos, left=False)
                if midJudge(small_tmp, gapStat, -0.03, True):
                    pos = gapStat[-0.03] - 1
                    gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos, left=True)
                if midJudge(small_tmp, gapStat, -0.04, True):
                    pos = gapStat[-0.04] - 1
                    arr.add(small_tmp[pos])
                    for i in range(pos - 1, -1, -1):
                        if small_gap_tmp[pos] - small_gap_tmp[i] < 0.0001:
                            arr.add(small_tmp[i])
                if midJudge(small_tmp, gapStat, -0.04, False):
                    if gapStat[-0.03] == len(small_tmp):
                        findTurn(arr, small_tmp, small_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=True, consecutive_at_left=False, choose_single=False)
                    arr.add(small_tmp[gapStat[-0.04] - 1])
                    if gapStat[-0.04] - 2 > -1 and small_gap_tmp[gapStat[-0.04] - 1] - small_gap_tmp[gapStat[-0.04] - 2] < 0.0001:
                        arr.add(small_tmp[gapStat[-0.04] - 2])
                    pos = gapStat[-0.04]
                    gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos, left=False)
            if len(small_near_tmp) - len(big_tmp) >= -1 and len(small_near_tmp) >= len(big_near_tmp):
                if len(small_near_tmp) == 2:
                    if small_near_gap_tmp[0] == small_near_gap_tmp[-1]:
                        arr.add(small_near_tmp[0])
                        arr.add(small_near_tmp[1])
                    if small_near_gap_tmp[0] > -0.011:
                        arr.add(small_near_tmp[0])
                    if nearGapStat[-0.01] == 0:
                        arr.add(small_near_tmp[0])
                if midJudge(small_near_tmp, nearGapStat, -0.01, True):
                    pos = nearGapStat[-0.01] - 1
                    gapAndConsecutive(arr, small_near_tmp, small_near_gap_tmp, pos, left=True)
                if midJudge(small_near_tmp, nearGapStat, -0.01, False):
                    pos = nearGapStat[-0.01]
                    gapAndConsecutive(arr, small_near_tmp, small_near_gap_tmp, pos, left=False)
            elif len(small_near_tmp) >= len(big_near_tmp):
                if len(small_near_tmp) == 2:
                    if small_near_gap_tmp[0] < -0.007 and small_near_gap_tmp[1] > -0.0024:
                        arr.add(small_near_tmp[1])
                    if nearGapStat[-0.01] == 1:
                        arr.add(small_near_tmp[1])
            print('很均衡时小的偏多' + extraSmall(seq))
        elif len(seq['small']) + len(seq['smallNear']) < len(seq['big']) + len(seq['bigNear']):
            if len(big_tmp) >= len(small_tmp) and len(big_tmp) >= len(small_near_tmp):
                if gapStat[0.04] == 1:
                    arr.add(big_tmp[-2])
                if midJudge(big_tmp, gapStat, 0.04, False):
                    pos = len(big_tmp) - gapStat[0.04]
                    gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos, left=False)
                if midJudge(big_tmp, gapStat, 0.03, False):
                    pos = len(big_tmp) - gapStat[0.03]
                    gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos, left=False)
                    gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos - 1, left=True)
                if midJudge(big_tmp, gapStat, 0.03, True):
                    findTurn(arr, big_tmp, big_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=True, consecutive_at_left=True, choose_single=True)
                if midJudge(big_tmp, gapStat, 0.02, True):
                    pos = len(big_tmp) - gapStat[0.02]
                    arr.add(big_tmp[pos])
                    for i in range(pos + 1, len(big_tmp)):
                        if big_gap_tmp[i] - big_gap_tmp[pos] < 0.0001:
                            arr.add(big_tmp[i])
                    gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos - 1, left=True)
            elif len(big_tmp) >= len(small_near_tmp):
                if len(big_tmp) == 2:
                    if big_gap_tmp[0] < 0.031:
                        arr.add(big_tmp[1])
            if len(small_tmp) == 2:
                if len(small_tmp) == gapStat[-0.02]:
                    if small_gap_tmp[0] > -0.03 and small_gap_tmp[0] < -0.027:
                        arr.add(small_tmp[0])
                    if gapStat[-0.03] == 0 and small_gap_tmp[0] == small_gap_tmp[1]:
                        arr.add(small_tmp[0])
                        arr.add(small_tmp[1])
                if gapStat[-0.02] == 1:
                    arr.add(small_tmp[-1])
                if gapStat[-0.03] >= 1:
                    arr.add(small_tmp[0])
                if gapStat[-0.04] == 1:
                    arr.add(small_tmp[1])
            if len(big_near_tmp) >= len(small_near_tmp) and len(big_near_tmp) >= len(small_tmp):
                if big_near_gap_tmp[0] == big_near_gap_tmp[-1]:
                    for v in big_near_tmp:
                        arr.add(v)
                if nearGapStat[0.01] == len(big_near_tmp):
                    findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=True, consecutive_at_left=True, choose_single=True)
                if midJudge(big_near_tmp, nearGapStat, 0.01, False):
                    pos = len(big_near_tmp) - nearGapStat[0.01] - 1
                    arr.add(big_near_tmp[pos])
                    for i in range(pos - 1, -1, -1):
                        if big_near_gap_tmp[pos] - big_near_gap_tmp[i] < 0.001:
                            arr.add(big_near_tmp[i])
                    gapAndConsecutive(arr, big_near_tmp, big_near_gap_tmp, pos + 1, left=False)
                    findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=True, choose_single=False)
                if midJudge(big_near_tmp, nearGapStat, 0.01, True):
                    pos = len(big_near_tmp) - nearGapStat[0.01]
                    gapAndConsecutive(arr, big_near_tmp, big_near_gap_tmp, pos, left=False)
                    gapAndConsecutive(arr, big_near_tmp, big_near_gap_tmp, pos - 1, left=True)
                    if big_near_gap_tmp[pos] < 0.012:
                        arr.add(big_near_tmp[pos + 1])
                if nearGapStat[0.01] == 0:
                    findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=True, choose_single=True)
                    findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=False, choose_single=False)
            elif len(big_near_tmp) >= len(small_near_tmp):
                if nearGapStat[0.01] == 1:
                    arr.add(big_near_tmp[0])
                if big_near_gap_tmp[0] == big_near_gap_tmp[-1]:
                    for v in big_near_tmp:
                        arr.add(v)
            if len(small_tmp) - len(big_tmp) >= -1 and len(small_tmp) - len(big_near_tmp) >= -1:
                if midJudge(small_tmp, gapStat, -0.02, True):
                    if small_gap_tmp[0] < -0.0277:
                        arr.add(small_tmp[0])
                    pos = gapStat[-0.02] - 1
                    gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos, left=True)
                    gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos + 1, left=False)
                if midJudge(small_tmp, gapStat, -0.04, False):
                    pos = gapStat[-0.04] - 1
                    gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos, left=True)
                if midJudge(small_tmp, gapStat, -0.03, False):
                    pos = gapStat[-0.03]
                    gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos, left=False)
                    gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos - 1, left=True)
                    if small_gap_tmp[pos] > -0.0299:
                        arr.add(small_tmp[pos + 1])
                if midJudge(small_tmp, gapStat, -0.03, True):
                    findTurn(arr, small_tmp, small_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=False, choose_single=True)
                if len(small_tmp) == gapStat[-0.02]:
                    findTurn(arr, small_tmp, small_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=False, choose_single=True)
                    findTurn(arr, small_tmp, small_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=False, choose_single=False)
            if len(small_near_tmp) == 1:
                if small_near_gap_tmp[0] > -0.0125:
                    arr.add(small_near_tmp[0])
            print('很均衡时大的偏多' + extraBig(seq))
        else:
            if len(big_tmp) > len(small_near_tmp):
                if len(big_tmp) == 2:
                    if gapStat[0.03] == 1:
                        arr.add(big_tmp[1])
                    if gapStat[0.02] == 1:
                        arr.add(big_tmp[0])
            if len(big_tmp) >= len(small_tmp) and len(big_tmp) > len(small_near_tmp):
                if midJudge(big_tmp, gapStat, 0.04, True):
                    findTurn(arr, big_tmp, big_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=True, choose_single=False)
                if midJudge(big_tmp, gapStat, 0.03, False):
                    arr.add(big_tmp[len(big_tmp) - gapStat[0.03]])
                if midJudge(big_tmp, gapStat, 0.02, False):
                    pos = len(big_tmp) - gapStat[0.02] - 1
                    arr.add(big_tmp[pos])
                    for i in range(pos - 1, -1, -1):
                        if big_gap_tmp[pos] - big_gap_tmp[i] < 0.0001:
                            arr.add(big_tmp[i])
                    findTurn(arr, big_tmp, big_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=True, consecutive_at_left=True, choose_single=True)
                if gapStat[0.03] == 1:
                    arr.add(big_tmp[-1])
                    arr.add(big_tmp[-2])
                if len(small_tmp) == len(big_tmp):
                    if gapStat[-0.04] == 1:
                        findTurn(arr, small_tmp, small_gap_tmp, approach_threshold=0.0001, gap_threshold=0.5, reverse=False, consecutive_at_left=False, choose_single=False)
            elif len(big_tmp) > len(small_near_tmp) and len(big_tmp) > len(big_near_tmp):
                if gapStat[0.02] == len(big_tmp):
                    if midJudge(big_tmp, gapStat, 0.03, False):
                        arr.add(big_tmp[len(big_tmp) - gapStat[0.03] - 1])
            if len(small_tmp) > len(big_tmp) and len(small_tmp) > len(big_near_tmp):
                if midJudge(small_tmp, gapStat, -0.02, True):
                    arr.add(small_tmp[gapStat[-0.02] - 1])
                    arr.add(small_tmp[gapStat[-0.02]])
                if midJudge(small_tmp, gapStat, -0.03, False):
                    if small_gap_tmp[0] < -0.0382:
                        arr.add(small_tmp[0])
                    pos = gapStat[-0.03] - 1
                    arr.add(small_tmp[pos])
            if len(big_near_tmp) == len(small_near_tmp):
                if midJudge(small_tmp, gapStat, -0.02, True):
                    pos = gapStat[-0.02]
                    arr.add(small_tmp[pos])
                if len(big_near_tmp) == 2:
                    if nearGapStat[0.01] == 0:
                        arr.add(big_near_tmp[0])
                if midJudge(big_tmp, gapStat, 0.02, True):
                    arr.add(big_tmp[0])
                if midJudge(small_tmp, gapStat, -0.03, True):
                    arr.add(small_tmp[gapStat[-0.03] - 1])
            if len(small_tmp) > len(big_near_tmp):
                if len(small_tmp) == 2:
                    if gapStat[-0.02] == 1:
                        arr.add(small_tmp[0])
                if len(small_tmp) > 2:
                    if gapStat[-0.02] == len(small_tmp):
                        arr.add(small_tmp[-1])
            if len(big_near_tmp) == 1:
                if nearGapStat[0.01] <= 1:
                    arr.add(big_near_tmp[0])
            if len(big_near_tmp) > len(small_near_tmp) and len(big_near_tmp) - len(small_tmp) >= -1:
                if midJudge(big_near_tmp, nearGapStat, 0.01, True):
                    pos = len(big_near_tmp) - nearGapStat[0.01]
                    arr.add(big_near_tmp[pos])
                    for i in range(pos + 1, len(big_near_tmp)):
                        if big_near_gap_tmp[i] - big_near_gap_tmp[pos] < 0.0001:
                            arr.add(big_near_tmp[i])
                if nearGapStat[0.01] == 0:
                    findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=True, choose_single=False)
                    findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=True, choose_single=True)
            elif len(big_near_tmp) >= len(small_near_tmp):
                if len(big_near_tmp) == 2:
                    if nearGapStat[0.01] == 1:
                        arr.add(big_near_tmp[0])
            print('非常均衡')
    elif count['small'] >= 7:
        if midJudge(small_tmp, gapStat, -0.04, False):
            pos = gapStat[-0.04] - 1
            gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos, left=True)
        if midJudge(small_tmp, gapStat, -0.04, True):
            if small_gap_tmp[-1] > -0.0305:
                arr.add(small_tmp[-1])
            arr.add(small_tmp[gapStat[-0.04]])
            if small_gap_tmp[gapStat[-0.04] - 1] > -0.04:
                arr.add(small_tmp[gapStat[-0.04] - 2])
            else:
                arr.add(small_tmp[gapStat[-0.04] - 1])
        if midJudge(small_tmp, gapStat, -0.05, False):
            if small_gap_tmp[0] < -0.0577:
                arr.add(small_tmp[0])
            findTurn(arr, small_tmp, small_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=True, choose_single=False)
            pos = gapStat[-0.05]
            if small_gap_tmp[pos] < -0.0361 and small_gap_tmp[pos + 1] > -0.0348:
                arr.add(small_tmp[pos + 1])
        if midJudge(small_tmp, gapStat, -0.07, False):
            pos = gapStat[-0.07] - 1
            gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos + 1, left=False)
            if small_gap_tmp[pos] > -0.0715:
                if pos - 1 > -1:
                    arr.add(small_tmp[pos - 1])
            if small_gap_tmp[pos] > -0.0721:
                arr.add(small_tmp[pos])
        if midJudge(small_tmp, gapStat, -0.06, False):
            pos = gapStat[-0.06] - 1
            gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos, left=True)
            gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos + 1, left=False)
            if small_gap_tmp[0] < -0.067 and small_gap_tmp[1] > -0.0615:
                arr.add(small_tmp[0])
        if midJudge(small_tmp, gapStat, -0.03, False):
            pos = gapStat[-0.03]
            arr.add(small_tmp[pos])
            for i in range(pos + 1, len(small_tmp)):
                if small_gap_tmp[i] - small_gap_tmp[pos] < 0.0001:
                    arr.add(small_tmp[i])
        if midJudge(small_tmp, gapStat, -0.03, True):
            pos = gapStat[-0.03]
            arr.add(small_tmp[pos])
            for i in range(pos + 1, len(small_tmp)):
                if small_gap_tmp[i] - small_gap_tmp[pos] < 0.001:
                    arr.add(small_tmp[i])
            if small_gap_tmp[pos] <= -0.028:
                if pos + 1 < len(small_tmp):
                    arr.add(small_tmp[pos + 1])
            arr.add(small_tmp[pos - 1])
            for i in range(pos - 2, -1, -1):
                if small_gap_tmp[pos - 1] - small_gap_tmp[i] < 0.0001:
                    arr.add(small_tmp[i])
        if midJudge(small_tmp, gapStat, -0.02, True):
            pos = gapStat[-0.02]
            gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos, left=False)
            if pos + 1 < len(small_tmp) and small_gap_tmp[pos + 1] - small_gap_tmp[pos] < 0.00001:
                arr.add(small_tmp[pos + 1])
            pos2 = pos - 1
            if pos2 > 0 and pos2 - 1 > 0:
                arr.add(small_tmp[pos2])
                if small_gap_tmp[pos2] - small_gap_tmp[pos2 - 1] < 0.0001:
                    arr.add(small_tmp[pos2 - 1])
        if gapStat[-0.03] == len(small_tmp):
            if midJudge(small_tmp, gapStat, -0.04, False):
                findTurn(arr, small_tmp, small_gap_tmp, approach_threshold=0.0001, gap_threshold=0.1, reverse=True, consecutive_at_left=True, choose_single=False)
        if gapStat[-0.02] == len(small_tmp):
            if midJudge(small_tmp, gapStat, -0.03, False):
                findTurn(arr, small_tmp, small_gap_tmp, approach_threshold=0.0001, gap_threshold=0.1, reverse=True, consecutive_at_left=False, choose_single=False)
            if midJudge(small_tmp, gapStat, -0.03, True):
                findTurn(arr, small_tmp, small_gap_tmp, approach_threshold=0.0001, gap_threshold=0.1, reverse=True, consecutive_at_left=False, choose_single=False)
        if len(small_near_tmp) >= len(big_tmp) and len(small_near_tmp) >= len(big_near_tmp):
            if nearGapStat[-0.01] == 0:
                if int(len(small_near_tmp) / 2) > -1 and int(len(small_near_tmp) / 2) < len(small_near_tmp):
                    arr.add(small_near_tmp[int(len(small_near_tmp) / 2)])
                findTurn(arr, small_near_tmp, small_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=True, choose_single=False)
            if nearGapStat[-0.01] == 1:
                arr.add(small_near_tmp[0])
            if len(small_near_tmp) == 2:
                if nearGapStat[-0.01] == 1:
                    arr.add(small_near_tmp[1])
            if midJudge(small_near_tmp, nearGapStat, -0.01, False):
                pos = nearGapStat[-0.01]
                gapAndConsecutive(arr, small_near_tmp, small_near_gap_tmp, pos, left=False)
        if len(big_near_tmp) == 1:
            arr.add(big_near_tmp[0])
        if len(small_near_tmp) == 1:
            arr.add(small_near_tmp[0])
        if len(big_near_tmp) >= len(small_near_tmp):
            if len(big_near_gap_tmp) > 1 and big_near_gap_tmp[0] == big_near_gap_tmp[-1]:
                for v in big_near_tmp:
                    arr.add(v)
            if len(big_near_gap_tmp) == 2:
                if big_near_gap_tmp[1] > 0.0065 and big_near_gap_tmp[0] < 0.0041:
                    arr.add(big_near_tmp[1])
            if len(big_near_tmp) > 2:
                if nearGapStat[0.01] == 0:
                    if noConsecutiveGap(big_near_gap_tmp):
                        if big_near_gap_tmp[0] < 0.003 and big_near_gap_tmp[1] > 0.005:
                            arr.add(big_near_tmp[0])
            if nearGapStat[0.01] == 0:
                findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=True, choose_single=False)
        print('大部分小')
    elif count['small'] >= 5 and maxConsecutiveCount['small'] >= 4:
        if midJudge(small_tmp, gapStat, -0.05, False):
            arr.add(small_tmp[gapStat[-0.05] - 1])
        if midJudge(small_tmp, gapStat, -0.03, True):
            arr.add(small_tmp[gapStat[-0.03]])
        if midJudge(small_tmp, gapStat, -0.02, True):
            arr.add(small_tmp[gapStat[-0.02] - 1])
            pos = gapStat[-0.02]
            if small_gap_tmp[pos] < -0.0195:
                if pos + 1 < len(small_tmp):
                    arr.add(small_tmp[pos + 1])
        if len(small_near_tmp) >= len(big_near_tmp) and len(small_near_tmp) >= len(big_tmp):
            if midJudge(small_near_tmp, nearGapStat, -0.01, True):
                arr.add(small_near_tmp[nearGapStat[-0.01]])
            if len(small_near_tmp) == 2:
                if nearGapStat[-0.01] == 1:
                    arr.add(small_near_tmp[1])
        print('连续小' + restExcSmall(seq))
    else:
        print('不对呀', data_len)
    print(data_len, good_count, arr)
    del(seq['near'])
    show(gapStat, avg_window, data_len, range_stat, prob_cand_arr, pred, seq)
    return arr








