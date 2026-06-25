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
        if midJudge(big_tmp, gapStat, 0.04, False):
            if big_gap_tmp[-1] < 0.05 and big_gap_tmp[-1] > 0.049:
                arr.add(big_tmp[-2])
            if gapStat[0.05] == 0:
                for i in range(len(big_tmp) - 1, -1, -1):
                    if big_gap_tmp[i] > 0.04 and big_gap_tmp[i] < 0.0403:
                        if i + 1 < len(big_tmp) and big_gap_tmp[i + 1] > 0.042:
                            arr.add(big_tmp[i+1])
                            break
            pos = len(big_tmp) - gapStat[0.04] - 1
            gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos, left=True)
            gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos + 1, left=False)
        if midJudge(big_tmp, gapStat, 0.04, True):
            if len(big_tmp) == gapStat[0.03]:
                pos = len(big_tmp) - gapStat[0.04] - 1
                arr.add(big_tmp[pos])
                if pos - 1 > -1 and big_gap_tmp[pos] - big_gap_tmp[pos - 1] < 0.0001:
                        arr.add(big_tmp[pos - 1])
            pos = len(big_tmp) - gapStat[0.04]
            gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos, left=False)
            findTurn(arr, big_tmp, big_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=True, consecutive_at_left=False, choose_single=False)
        if midJudge(big_tmp, gapStat, 0.05, False):
            if big_gap_tmp[-1] > 0.058:
                arr.add(big_tmp[-1])
            if gapStat[0.06] == 0:
                if gapStat[0.05] == 2:
                    arr.add(big_tmp[-1])
            pos = len(big_tmp) - gapStat[0.05] - 1
            arr.add(big_tmp[pos])
            if pos - 1 > -1 and big_gap_tmp[pos] - big_gap_tmp[pos - 1] < 0.0001:
                arr.add(big_tmp[pos - 1])
            if pos + 1 < len(big_tmp):
                arr.add(big_tmp[pos + 1])
                for i in range(pos + 2, len(big_tmp)):
                    if big_gap_tmp[i] - big_gap_tmp[pos] < 0.0001:
                        arr.add(big_tmp[i])
        if midJudge(big_tmp, gapStat, 0.05, True):
            pos = len(big_tmp) - gapStat[0.05]
            gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos, left=False)
        if midJudge(big_tmp, gapStat, 0.09, True):
            pos = len(big_tmp) - gapStat[0.09]
            gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos, left=False)
        if midJudge(big_tmp, gapStat, 0.09, False):
            pos = len(big_tmp) - gapStat[0.09]
            gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos, left=False)
        if midJudge(big_tmp, gapStat, 0.08, False):
            pos = len(big_tmp) - gapStat[0.08]
            gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos, left=False)
        if midJudge(big_tmp, gapStat, 0.06, False):
            pos = len(big_tmp) - gapStat[0.06]
            if big_gap_tmp[pos] < 0.061:
                if pos + 1 < len(big_tmp):
                    arr.add(big_tmp[pos + 1])
        if midJudge(big_tmp, gapStat, 0.07, False):
            if big_gap_tmp[-1] > 0.076:
                arr.add(big_tmp[-1])
            pos = len(big_tmp) - gapStat[0.07] - 1
            arr.add(big_tmp[pos])
            for i in range(pos - 1, -1, -1):
                if big_gap_tmp[pos] - big_gap_tmp[i] < 0.0001:
                    arr.add(big_tmp[i])
            arr.add(big_tmp[pos + 1])
            if big_gap_tmp[pos + 1] < 0.071:
                if pos + 2 < len(big_tmp):
                    arr.add(big_tmp[pos + 2])
        if midJudge(big_tmp, gapStat, 0.02, True):
            findTurn(arr, big_tmp, big_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=True, choose_single=False)
            findTurn(arr, big_tmp, big_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=False, choose_single=False)
            pos = len(big_tmp) - gapStat[0.02]
            if big_gap_tmp[pos] < 0.0205:
                arr.add(big_tmp[pos + 1])
            arr.add(big_tmp[pos])
            for i in range(pos + 1, len(big_tmp)):
                if big_gap_tmp[i] - big_gap_tmp[pos] < 0.0001:
                    arr.add(big_tmp[i])
            arr.add(big_tmp[pos - 1])
            for i in range(pos - 2, -1, -1):
                if big_gap_tmp[pos - 1] - big_gap_tmp[i] < 0.0001:
                    arr.add(big_tmp[i])
        if len(big_tmp) == gapStat[0.02]:
            if big_gap_tmp[0] < 0.214:
                arr.add(big_tmp[0])
            if big_gap_tmp[0] < 0.03 and big_gap_tmp[1] < 0.03 and big_gap_tmp[1] - big_gap_tmp[0] > 0.0045:
                arr.add(big_tmp[0])
            if big_gap_tmp[1] - big_gap_tmp[0] < 0.0001 and big_gap_tmp[2] - big_gap_tmp[1] > 0.002:
                arr.add(big_tmp[2])
            if midJudge(big_tmp, gapStat, 0.04, True):
                arr.add(big_tmp[0])
                findTurn(arr, big_tmp, big_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=True, choose_single=False)
            if midJudge(big_tmp, gapStat, 0.03, True):
                findTurn(arr, big_tmp, big_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=False, choose_single=True)
            if midJudge(big_tmp, gapStat, 0.03, False):
                findTurn(arr, big_tmp, big_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=True, choose_single=False)
                findTurn(arr, big_tmp, big_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=False, choose_single=True)
        if midJudge(big_tmp, gapStat, 0.06, True):
            pos = len(big_tmp) - gapStat[0.06]
            gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos, left=False)
        if midJudge(big_tmp, gapStat, 0.06, False):
            if big_gap_tmp[-1] > 0.0671:
                arr.add(big_tmp[-1])
            pos = len(big_tmp) - gapStat[0.06] - 1
            arr.add(big_tmp[pos])
            if pos - 1 > -1 and big_gap_tmp[pos] - big_gap_tmp[pos - 1] < 0.0025:
                arr.add(big_tmp[pos - 1])
        if midJudge(big_tmp, gapStat, 0.03, False):
            pos = len(big_tmp) - gapStat[0.03] - 1
            arr.add(big_tmp[pos])
            if big_gap_tmp[pos] > 0.0295 and big_gap_tmp[pos] < 0.03:
                arr.add(big_tmp[pos - 1])
            for i in range(pos - 1, -1, -1):
                if big_gap_tmp[pos] - big_gap_tmp[i] < 0.0001:
                    arr.add(big_tmp[i])
            gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos + 1, left=False)
            findTurn(arr, big_tmp, big_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=True, consecutive_at_left=True, choose_single=True)
        if midJudge(big_tmp, gapStat, 0.03, True):
            if gapStat[0.02] == gapStat[0.03]:
                findTurn(arr, big_tmp, big_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=False, choose_single=True)
            pos = len(big_tmp) - gapStat[0.03]
            gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos - 1, left=True)
            arr.add(big_tmp[pos])
            arr.add(big_tmp[pos + 1])
            for i in range(pos + 2, len(big_tmp)):
                if big_gap_tmp[i] - big_gap_tmp[pos + 1] < 0.0001:
                    arr.add(big_tmp[i])
            arr.add(big_tmp[pos - 1])
            if big_gap_tmp[pos + 1] - big_gap_tmp[pos] < 0.0001:
                arr.add(big_tmp[pos + 1])
        if len(big_near_tmp) - len(small_tmp) >= -1 and len(big_near_tmp) - len(small_near_tmp) >= -1:
            if midJudge(big_near_tmp, nearGapStat, 0.01, True):
                pos = len(big_near_tmp) - nearGapStat[0.01]
                gapAndConsecutive(arr, big_near_tmp, big_near_gap_tmp, pos, left=False)
            if len(big_near_tmp) == 2:
                if nearGapStat[0.01] == 0:
                    arr.add(big_near_tmp[0])
                if nearGapStat[0.01] == 1:
                    arr.add(big_near_tmp[1])
            if nearGapStat[0.01] == 1:
                arr.add(big_near_tmp[0])
            if len(big_near_tmp) == 1:
                arr.add(big_near_tmp[0])
            if nearGapStat[0.01] == len(big_near_tmp) and len(big_near_tmp) > 0:
                arr.add(big_near_tmp[-1])
                if len(big_near_gap_tmp) > 1 and big_near_gap_tmp[-1] - big_near_gap_tmp[-2] < 0.00001:
                    arr.add(big_near_tmp[-2])
        if len(small_near_tmp) - len(big_near_tmp) >= -1:
            if len(small_near_tmp) == 1:
                if nearGapStat[-0.01] == 0:
                    arr.add(small_near_tmp[0])
        if len(small_tmp) >= len(big_near_tmp):
            if len(small_tmp) == 1:
                if gapStat[-0.03] == 0:
                    arr.add(small_tmp[0])
            if len(small_tmp) == 2:
                if gapStat[-0.02] == 1:
                    if gapStat[-0.03] == 0:
                        arr.add(small_tmp[0])
        print('大的全都要')
    #参差不齐接近
    elif count['near'] >= 5 and maxConsecutiveCount['near'] < 4:
        if len(seq['small']) + len(seq['smallNear']) >= 7:
            if len(big_tmp) == 1:
                if gapStat[0.03] == 0:
                    arr.add(big_tmp[0])
            if len(small_near_tmp) >= len(big_tmp) and len(small_near_tmp) >= len(big_near_tmp):
                if nearGapStat[-0.01] == len(small_near_tmp):
                    findTurn(arr, small_near_tmp, small_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=False, choose_single=True)
                if midJudge(small_near_tmp, nearGapStat, -0.01, True):
                    findTurn(arr, small_near_tmp, small_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=True, choose_single=False)
                    findTurn(arr, small_near_tmp, small_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=False, choose_single=True)
                    pos = nearGapStat[-0.01]
                    gapAndConsecutive(arr, small_near_tmp, small_near_gap_tmp, pos, left=False)
                    gapAndConsecutive(arr, small_near_tmp, small_near_gap_tmp, pos - 1, left=True)
                if midJudge(small_near_tmp, nearGapStat, -0.01, False):
                    arr.add(small_near_tmp[-1])
                    pos = nearGapStat[-0.01]
                    arr.add(small_near_tmp[pos])
                    if pos + 1 < len(small_near_tmp) and small_near_gap_tmp[pos + 1] - small_near_gap_tmp[pos] < 0.00001:
                        arr.add(small_near_tmp[pos + 1])
                    gapAndConsecutive(arr, small_near_tmp, small_near_gap_tmp, pos - 1, left=True)
                    findTurn(arr, small_near_tmp, small_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=True, choose_single=False)
                    findTurn(arr, small_near_tmp, small_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=False, choose_single=False)
                if nearGapStat[-0.01] == 0:
                    findTurn(arr, small_near_tmp, small_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=True, consecutive_at_left=False, choose_single=True)
                    if small_near_gap_tmp[-1] < -0.005:
                        arr.add(small_near_tmp[-1])
                        for i in range(len(small_near_tmp) - 2, -1, -1):
                            if small_near_gap_tmp[-1] - small_near_gap_tmp[i] < 0.0001:
                                arr.add(small_near_tmp[i])
            if len(big_near_tmp) >= len(small_near_tmp):
                if big_near_gap_tmp[0] == big_near_gap_tmp[-1]:
                    for v in big_near_tmp:
                        arr.add(v)
            if len(big_near_tmp) >= len(small_tmp):
                if midJudge(big_near_tmp, nearGapStat, 0.01, False):
                    pos = len(big_near_tmp) - nearGapStat[0.01]
                    gapAndConsecutive(arr, big_near_tmp, big_near_gap_tmp, pos, left=False)
            if len(big_near_tmp) == 1:
                if big_near_gap_tmp[0] < 0.012:
                    arr.add(big_near_tmp[0])
            if len(big_near_tmp) == 2:
                if big_near_gap_tmp[0] == big_near_gap_tmp[1]:
                    arr.add(big_near_tmp[0])
                    arr.add(big_near_tmp[1])
                if nearGapStat[0.01] == 1:
                    arr.add(big_near_tmp[0])
                if nearGapStat[0.01] == 0:
                    arr.add(big_near_tmp[0])
                    arr.add(big_near_tmp[-1])
            if len(small_tmp) >= len(big_tmp) and len(small_tmp) >= len(big_near_tmp):
                if gapStat[-0.02] == len(small_tmp):
                    if midJudge(small_tmp, gapStat, -0.03, False):
                        pos = gapStat[-0.03]
                        if small_gap_tmp[pos] < -0.029:
                            arr.add(small_tmp[pos + 1])
                if len(small_tmp) == 2:
                    if gapStat[-0.04] == 1:
                        if gapStat[-0.05] == 0:
                            arr.add(small_tmp[0])
                    if gapStat[-0.03] == 1:
                        arr.add(small_tmp[-1])
                if midJudge(small_tmp, gapStat, -0.02, True):
                    pos = gapStat[-0.02] - 1
                    arr.add(small_tmp[pos])
                    arr.add(small_tmp[pos + 1])
                if midJudge(small_tmp, gapStat, -0.03, True):
                    pos = gapStat[-0.03] - 1
                    arr.add(small_tmp[pos])
                    if pos - 1 > -1 and small_gap_tmp[pos] - small_gap_tmp[pos - 1] < 0.0001:
                        arr.add(small_tmp[pos - 1])
                    if pos + 1 < len(small_tmp):
                        arr.add(small_tmp[pos + 1])
                        for i in range(pos + 2, len(small_tmp)):
                            if small_gap_tmp[i] - small_gap_tmp[pos + 1] < 0.0001:
                                arr.add(small_tmp[i])
                if midJudge(small_tmp, gapStat, -0.05, False):
                    pos = gapStat[-0.05]
                    arr.add(small_tmp[pos])
                    if pos + 1 < len(small_tmp) and small_gap_tmp[pos + 1] - small_gap_tmp[pos] < 0.0001:
                        arr.add(small_tmp[pos + 1])
                    arr.add(small_tmp[pos - 1])
                    for i in range(pos - 2, -1, -1):
                        if small_gap_tmp[pos - 1] - small_gap_tmp[i] < 0.00001:
                            arr.add(small_tmp[i])
                if midJudge(small_tmp, gapStat, -0.04, True):
                    pos = gapStat[-0.04] - 1
                    arr.add(small_tmp[pos])
                    for i in range(pos - 1, -1, -1):
                        if small_gap_tmp[pos] - small_gap_tmp[i] < 0.0001:
                            arr.add(small_tmp[i])
                if midJudge(small_tmp, gapStat, -0.04, False):
                    pos = gapStat[-0.04]
                    arr.add(small_tmp[pos])
                    for i in range(pos + 1, len(small_tmp)):
                        if small_gap_tmp[i] - small_gap_tmp[pos] < 0.0001:
                            arr.add(small_tmp[i])
                    arr.add(small_tmp[pos - 1])
                    for i in range(pos - 2, -1, -1):
                        if small_gap_tmp[pos - 1] - small_gap_tmp[i] < 0.0001:
                            arr.add(small_tmp[i])
                if len(big_near_tmp) == 2:
                    if nearGapStat[0.01] == 1:
                        arr.add(big_near_tmp[-1])
            print('参差不齐接近时小的偏多' + extraSmall(seq))
        elif len(seq['big']) + len(seq['bigNear']) >= 7:
            if len(big_tmp) >= len(small_tmp) and len(big_tmp) >= len(small_near_tmp):
                if gapStat[0.02] == len(big_tmp):
                    if midJudge(big_tmp, gapStat, 0.03, False):
                        findTurn(arr, big_tmp, big_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=False, choose_single=True)
                if midJudge(big_tmp, gapStat, 0.02, False):
                    pos = len(big_tmp) - gapStat[0.02] - 1
                    if big_gap_tmp[pos] > 0.019:
                        if pos - 1 > -1:
                            arr.add(big_tmp[pos - 1])
                if midJudge(big_tmp, gapStat, 0.02, True):
                    pos = len(big_tmp) - gapStat[0.02] - 1
                    arr.add(big_tmp[pos - 1])
                    arr.add(big_tmp[pos])
                    arr.add(big_tmp[pos + 1])
                if midJudge(big_tmp, gapStat, 0.06, False):
                    if midJudge(big_tmp, gapStat, 0.02, True):
                        findTurn(arr, big_tmp, big_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=True, consecutive_at_left=True, choose_single=False)
                if midJudge(big_tmp, gapStat, 0.03, False):
                    pos = len(big_tmp) - gapStat[0.03]
                    gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos, left=False)
                    gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos - 1, left=True)
                if midJudge(big_tmp, gapStat, 0.03, True):
                    pos = len(big_tmp) - gapStat[0.03] - 1
                    arr.add(big_tmp[pos])
                    arr.add(big_tmp[pos + 1])
                if midJudge(big_tmp, gapStat, 0.05, False):
                    pos = len(big_tmp) - gapStat[0.05]
                    arr.add(big_tmp[pos])
                    arr.add(big_tmp[pos - 1])
                    if pos - 2 > -1 and big_gap_tmp[pos - 1] - big_gap_tmp[pos - 2] < 0.0001:
                        arr.add(big_tmp[pos - 2])
                if midJudge(big_tmp, gapStat, 0.04, False):
                    pos = len(big_tmp) - gapStat[0.04] - 1
                    arr.add(big_tmp[pos])
                if midJudge(big_tmp, gapStat, 0.04, True):
                    pos = len(big_tmp) - gapStat[0.04]
                    arr.add(big_tmp[pos])
                    if pos + 1 < len(big_tmp) and big_gap_tmp[pos + 1] - big_gap_tmp[pos] < 0.0001:
                        arr.add(big_tmp[pos + 1])
            if len(big_near_tmp) >= len(small_tmp) and len(big_near_tmp) >= len(small_near_tmp):
                if nearGapStat[0.01] == len(big_near_tmp):
                    findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=True, choose_single=False)
                    findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=True, consecutive_at_left=False, choose_single=False)
                if nearGapStat[0.01] == 0:
                    if noConsecutiveGap(big_gap_tmp):
                        arr.add(big_near_tmp[0])
                    findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=False, choose_single=False)
                    findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=True, choose_single=False)
                    findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=True, consecutive_at_left=True, choose_single=True)
                    if big_near_gap_tmp[0] == big_near_gap_tmp[-1]:
                        for v in big_near_tmp:
                            arr.add(v)
                if midJudge(big_near_tmp, nearGapStat, 0.01, False):
                    arr.add(big_near_tmp[0])
                    pos = len(big_near_tmp) - nearGapStat[0.01] - 1
                    arr.add(big_near_tmp[pos])
                    arr.add(big_near_tmp[pos + 1])
                    for i in range(pos - 1, -1, -1):
                        if big_near_gap_tmp[pos] - big_near_gap_tmp[i] < 0.00001:
                            arr.add(big_near_tmp[i])
                    findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=True, choose_single=False)
                if midJudge(big_near_tmp, nearGapStat, 0.01, False):
                    arr.add(big_near_tmp[-1])
                    pos = len(big_near_tmp) - nearGapStat[0.01]
                    arr.add(big_near_tmp[pos])
                    if pos + 1 < len(big_near_tmp) and  big_near_gap_tmp[pos + 1] - big_near_gap_tmp[pos] < 0.00001:
                        arr.add(big_near_tmp[pos + 1])
                if midJudge(big_near_tmp, nearGapStat, 0.01, True):
                    if noConsecutiveGap(big_near_gap_tmp):
                        arr.add(big_near_tmp[-1])
                    findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=True, consecutive_at_left=False, choose_single=False)
                    pos = len(big_near_tmp) - nearGapStat[0.01] - 1
                    arr.add(big_near_tmp[pos])
                    arr.add(big_near_tmp[pos + 1])
                    if pos + 2 < len(big_near_tmp) and big_near_gap_tmp[pos + 2] - big_near_gap_tmp[pos + 1] < 0.00001:
                        arr.add(big_near_tmp[pos + 2])
                    if big_near_gap_tmp[0] < 0.0032 and big_near_gap_tmp[1] > 0.005:
                        arr.add(big_near_tmp[0])
            if len(small_tmp) == 2:
                if gapStat[-0.03] == 1:
                    arr.add(small_tmp[1])
                if gapStat[-0.04] == 1 or gapStat[-0.02] == 1:
                    arr.add(small_tmp[-1])
            if len(small_near_tmp) == 1:
                arr.add(small_near_tmp[0])
            if len(small_near_tmp) == 2:
                if nearGapStat[-0.01] == 1:
                    arr.add(small_near_tmp[0])
                    arr.add(small_near_tmp[-1])
                if nearGapStat[-0.01] == 0:
                    arr.add(small_near_tmp[0])
                    if small_near_gap_tmp[1] - small_near_gap_tmp[0] < 0.0001:
                        arr.add(small_near_tmp[1])
            if len(big_near_tmp) == 2:
                if nearGapStat[0.01] == 1:
                    arr.add(big_near_tmp[0])
            if len(big_tmp) == 1:
                if gapStat[0.03] == 0:
                    arr.add(big_tmp[0])
            if len(big_tmp) == 2:
                if big_gap_tmp[0] == big_gap_tmp[1]:
                    arr.add(big_tmp[0])
                    arr.add(big_tmp[1])
                if gapStat[0.02] == 1:
                    arr.add(big_tmp[1])
                if gapStat[0.03] == 1:
                    arr.add(big_tmp[0])
                if gapStat[0.04] == 1:
                    if gapStat[0.02] == len(big_tmp):
                        arr.add(big_tmp[0])
            print('参差不齐接近时大的偏多' + extraBig(seq))
        elif len(seq['small']) + len(seq['smallNear']) > len(seq['big']) + len(seq['bigNear']):
            if len(small_tmp) >= len(big_tmp) and len(small_tmp) - len(big_near_tmp) >= -1:
                if len(small_tmp) == gapStat[-0.02]:
                    if small_gap_tmp[-1] > -0.0214:
                        arr.add(small_tmp[-1])
                if midJudge(small_tmp, gapStat, -0.04, False):
                    pos = gapStat[-0.04] - 1
                    arr.add(small_tmp[pos])
                    for i in range(pos - 1, -1, -1):
                        if small_gap_tmp[pos] - small_gap_tmp[i] < 0.0001:
                            arr.add(small_tmp[i])
                if midJudge(small_tmp, gapStat, -0.03, False):
                    pos = gapStat[-0.03]
                    if small_gap_tmp[pos] < -0.028 and small_gap_tmp[pos] > -0.03:
                        if pos + 1 < len(small_tmp):
                            arr.add(small_tmp[pos + 1])
                            for i in range(pos + 2, len(small_tmp)):
                                if small_gap_tmp[i] - small_gap_tmp[pos + 1] < 0.0001:
                                    arr.add(small_tmp[i])
                    else:
                        arr.add(small_tmp[pos])
                        for i in range(pos + 1, len(small_tmp)):
                            if small_gap_tmp[i] - small_gap_tmp[pos] < 0.00001:
                                arr.add(small_tmp[i])
                if midJudge(small_tmp, gapStat, -0.03, True):
                    pos = gapStat[-0.03]
                    arr.add(small_tmp[pos])
            if len(big_near_tmp) - len(small_near_tmp) >= -1 and len(big_near_tmp) - len(small_tmp) >= -1:
                if nearGapStat[0.01] == 0:
                    if len(big_near_tmp) > 2 and big_near_gap_tmp[2] - big_near_gap_tmp[1] < 0.0001 and big_near_gap_tmp[1] - big_near_gap_tmp[0] < 0.00001:
                        arr.add(big_near_tmp[0])
                        arr.add(big_near_tmp[1])
                        arr.add(big_near_tmp[2])
                    findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=True, choose_single=False)
                    findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=False, choose_single=False)
                    findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=False, choose_single=True)
                if midJudge(big_near_tmp, nearGapStat, 0.01, False):
                    pos = len(big_near_tmp) - nearGapStat[0.01] - 1
                    arr.add(big_near_tmp[pos])
                    if pos - 1 > -1 and big_near_gap_tmp[pos] - big_near_gap_tmp[pos - 1] < 0.00001:
                        arr.add(big_near_tmp[pos - 1])
                    gapAndConsecutive(arr, big_near_tmp, big_near_gap_tmp, pos + 1, left=False)
                if midJudge(big_near_tmp, nearGapStat, 0.01, True):
                    pos = len(big_near_tmp) - nearGapStat[0.01]
                    gapAndConsecutive(arr, big_near_tmp, big_near_gap_tmp, pos, left=False)
                    if pos + 1 < len(big_near_tmp) and big_near_gap_tmp[pos + 1] - big_near_gap_tmp[pos] < 0.0001:
                        arr.add(big_near_tmp[pos + 1])
            if len(small_tmp) == 2:
                if gapStat[-0.03] == len(small_tmp):
                    arr.add(small_tmp[-1])
                    if small_gap_tmp[-1] - small_gap_tmp[0] < 0.00001:
                        arr.add(small_tmp[0])
            if len(big_near_tmp) == 2:
                if nearGapStat[0.01] == 0:
                    if big_near_gap_tmp[0] < 0.003 and big_near_gap_tmp[1] > 0.006:
                        arr.add(big_near_tmp[0])
                    arr.add(big_near_tmp[-1])
                    if big_near_gap_tmp[-1] - big_near_gap_tmp[0] < 0.0001:
                        arr.add(big_near_tmp[0])
                if nearGapStat[0.01] == 1:
                    arr.add(big_near_tmp[1])
                    arr.add(big_near_tmp[0])
            if len(small_near_tmp) >= len(big_tmp) and len(small_near_tmp) - len(big_near_tmp) >= -1:
                if nearGapStat[-0.01] == 0:
                    if small_near_gap_tmp[0] == small_near_gap_tmp[-1]:
                        for v in small_near_tmp:
                            arr.add(v)
                    if noConsecutiveGap(small_near_gap_tmp):
                        if small_near_gap_tmp[0] < -0.005:
                            arr.add(small_near_tmp[0])
                    findTurn(arr, small_near_tmp, small_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=True, choose_single=True)
                    findTurn(arr, small_near_tmp, small_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=False, choose_single=True)
                    findTurn(arr, small_near_tmp, small_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=True, choose_single=False)
                    findTurn(arr, small_near_tmp, small_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=True, consecutive_at_left=False, choose_single=False)
                if midJudge(small_near_tmp, nearGapStat, -0.01, True):
                    pos = nearGapStat[-0.01]
                    gapAndConsecutive(arr, small_near_tmp, small_near_gap_tmp, pos, left=False)
                    gapAndConsecutive(arr, small_near_tmp, small_near_gap_tmp, pos - 1, left=True)
                if midJudge(small_near_tmp, nearGapStat, -0.01, False):
                    pos = nearGapStat[-0.01] - 1
                    gapAndConsecutive(arr, small_near_tmp, small_near_gap_tmp, pos + 1, left=False)
                    arr.add(small_near_tmp[pos])
                    arr.add(small_near_tmp[pos + 1])
                    findTurn(arr, small_near_tmp, small_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=True, consecutive_at_left=True, choose_single=True)
                    if noConsecutiveGap(small_near_gap_tmp):
                        arr.add(small_near_tmp[-1])
            elif len(small_near_tmp) >= len(big_tmp):
                if len(small_near_tmp) == 1:
                    arr.add(small_near_tmp[0])
            if len(big_tmp) == 2:
                if big_gap_tmp[0] == big_gap_tmp[1]:
                    arr.add(big_tmp[0])
                    arr.add(big_tmp[1])
                if gapStat[0.02] == 1:
                    arr.add(big_tmp[0])
            if len(big_tmp) == 1:
                if gapStat[0.03] == 0:
                    arr.add(big_tmp[0])
            if len(big_tmp) - len(small_tmp) >= -1 and len(big_tmp) - len(small_near_tmp) >= -1:
                if midJudge(big_tmp, gapStat, 0.02, True):
                    pos = len(big_tmp) - gapStat[0.02] - 1
                    gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos, left=True)
            print('参差不齐接近时小的比大的多一些' + extraSmall(seq))
        elif len(seq['small']) + len(seq['smallNear']) < len(seq['big']) + len(seq['bigNear']):
            if len(small_tmp) - len(big_tmp) >= -1 and len(small_tmp) - len(big_near_tmp) >= -2:
                if midJudge(small_tmp, gapStat, -0.02, True):
                    pos = gapStat[-0.02]
                    gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos, left=False)
                    gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos - 1, left=True)
                if len(small_tmp) == 2:
                    if gapStat[-0.03] == 1:
                        arr.add(small_tmp[0])
                        arr.add(small_tmp[1])
            if len(big_tmp) >= len(small_tmp) and len(big_tmp) >= len(small_near_tmp):
                if big_gap_tmp[0] == big_gap_tmp[-1]:
                    for v in big_tmp:
                        arr.add(v)
                if len(big_tmp) == gapStat[0.02]:
                    if gapStat[0.03] == 0:
                        if big_gap_tmp[-1] > 0.029:
                            arr.add(big_tmp[-1])
                if midJudge(big_tmp, gapStat, 0.02, False):
                    pos = len(big_tmp) - gapStat[0.02] - 1
                    arr.add(big_tmp[pos])
                    for i in range(pos - 1, -1, -1):
                        if big_gap_tmp[pos] - big_gap_tmp[i] < 0.0001:
                            arr.add(big_tmp[i])
                if midJudge(big_tmp, gapStat, 0.04, False):
                    pos = len(big_tmp) - gapStat[0.04] - 1
                    arr.add(big_tmp[pos])
                if midJudge(big_tmp, gapStat, 0.03, True):
                    pos = len(big_tmp) - gapStat[0.03] - 1
                    arr.add(big_tmp[pos])
                    if pos - 1 > -1 and big_gap_tmp[pos] - big_gap_tmp[pos - 1] < 0.0001:
                        arr.add(big_tmp[pos - 1])
                if midJudge(big_tmp, gapStat, 0.02, True):
                    pos = len(big_tmp) - gapStat[0.02] - 1
                    arr.add(big_tmp[pos])
                    arr.add(big_tmp[pos + 1])
            if len(small_near_tmp) >= len(big_tmp):
                if len(small_near_tmp) > 2:
                    if midJudge(small_near_tmp, nearGapStat, -0.01, False):
                        pos = nearGapStat[-0.01]
                        arr.add(small_near_tmp[pos])
                        for i in range(pos + 1, len(small_near_tmp)):
                            if small_near_gap_tmp[i] - small_near_gap_tmp[pos] < 0.0001:
                                arr.add(small_near_tmp[i])
                if len(small_near_tmp) == 2:
                    if nearGapStat[-0.01] <= 1:
                        arr.add(small_near_tmp[-1])
                        if small_near_gap_tmp[-1] - small_near_gap_tmp[-2] < 0.0001:
                            arr.add(small_near_tmp[-2])
            if len(big_near_tmp) >= len(small_tmp) and len(big_near_tmp) >= len(small_near_tmp):
                if big_near_gap_tmp[0] < 0.0017:
                    arr.add(big_near_tmp[0])
                if midJudge(big_near_tmp, nearGapStat, 0.01, True):
                    pos = len(big_near_tmp) - nearGapStat[0.01] - 1
                    arr.add(big_near_tmp[pos])
                    for i in range(pos - 1, -1, -1):
                        if big_near_gap_tmp[pos] - big_near_gap_tmp[i] < 0.0001:
                            arr.add(big_near_tmp[i])
                    findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=True, consecutive_at_left=False, choose_single=False)
                if midJudge(big_near_tmp, nearGapStat, 0.01, False):
                    findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=True, choose_single=False)
                    pos = len(big_near_tmp) - nearGapStat[0.01] - 1
                    arr.add(big_near_tmp[pos])
                    arr.add(big_near_tmp[pos + 1])
                    if pos - 1 > -1 and big_near_gap_tmp[pos] - big_near_gap_tmp[pos - 1] < 0.0001:
                        arr.add(big_near_tmp[pos - 1])
                    if big_near_gap_tmp[0] < 0.0029 and big_near_gap_tmp[1] > 0.006:
                        arr.add(big_near_tmp[0])
                if nearGapStat[0.01] == 0:
                    findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=True, consecutive_at_left=False, choose_single=False)
                    findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=False, choose_single=True)
                    if big_near_gap_tmp[1] - big_near_gap_tmp[0] < 0.0001:
                        arr.add(big_near_tmp[0])
                        arr.add(big_near_tmp[1])
            if len(small_near_tmp) == 1:
                arr.add(small_near_tmp[0])
            if len(big_tmp) == 2:
                if big_gap_tmp[0] == big_gap_tmp[1]:
                    arr.add(big_tmp[0])
                    arr.add(big_tmp[1])
                if gapStat[0.02] == 2:
                    if big_gap_tmp[1] > 0.0285:
                        arr.add(big_tmp[0])
                    if gapStat[0.03] == 1:
                        arr.add(big_tmp[0])
                if gapStat[0.03] == 2:
                    if big_gap_tmp[0] < 0.0308:
                        arr.add(big_tmp[0])
                    if gapStat[0.04] == 1 or gapStat[0.04] == 2:
                        arr.add(big_tmp[0])
            if len(small_near_tmp) - len(big_tmp) >= -1 and len(small_near_tmp) >= len(big_near_tmp):
                if midJudge(small_near_tmp, nearGapStat, -0.01, False):
                    pos = nearGapStat[-0.01]
                    arr.add(small_near_tmp[pos])
                if nearGapStat[-0.01] == 0:
                    findTurn(arr, small_near_tmp, small_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=False, choose_single=True)
            print('参差不齐接近时大的比小的多一些' + extraBig(seq))
        else:
            if len(small_near_tmp) == 2:
                if small_near_gap_tmp[0] > -0.011:
                    arr.add(small_near_tmp[0])
                if nearGapStat[-0.01] == 0:
                    arr.add(small_near_tmp[-1])
                    if small_near_gap_tmp[-1] - small_near_gap_tmp[-2] < 0.0001:
                        arr.add(small_near_tmp[-2])
                if nearGapStat[-0.01] == len(small_near_tmp):
                    arr.add(small_near_tmp[0])
                    if small_near_gap_tmp[1] - small_near_gap_tmp[0] < 0.0001:
                        arr.add(small_near_tmp[1])
            if len(small_near_tmp) >= len(big_tmp) and len(small_near_tmp) - len(big_near_tmp) >= -1:
                if midJudge(small_near_tmp, nearGapStat, -0.01, False):
                    pos = nearGapStat[-0.01] - 1
                    gapAndConsecutive(arr, small_near_tmp, small_near_gap_tmp, pos, left=True)
                    gapAndConsecutive(arr, small_near_tmp, small_near_gap_tmp, pos + 1, left=False)
                if nearGapStat[-0.01] == len(small_near_tmp):
                    findTurn(arr, small_near_tmp, small_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=False, choose_single=True)
                if midJudge(small_near_tmp, nearGapStat, -0.01, True):
                    for i in range(1, len(small_near_tmp)):
                        if small_near_gap_tmp[i] > -0.0106 and small_near_gap_tmp[i] < -0.01:
                            arr.add(small_near_tmp[i-1])
                            break
                    pos = nearGapStat[-0.01]
                    arr.add(small_near_tmp[pos])
                    arr.add(small_near_tmp[pos - 1])
                    for i in range(pos - 2, -1, -1):
                        if small_near_gap_tmp[pos - 1] - small_near_gap_tmp[i] < 0.0001:
                            arr.add(small_near_tmp[i])
                if nearGapStat[-0.01] == 0:
                    if small_near_gap_tmp[0] < -0.0085:
                        arr.add(small_near_tmp[0])
                    if len(small_near_tmp) == 2:
                        if small_near_gap_tmp[0] < -0.005 and small_near_gap_tmp[1] > -0.002:
                            arr.add(small_near_tmp[0])
                    findTurn(arr, small_near_tmp, small_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=True, choose_single=True)
                    findTurn(arr, small_near_tmp, small_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=False, choose_single=True)
                    findTurn(arr, small_near_tmp, small_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=False, choose_single=False)
                    if small_near_gap_tmp[1] - small_near_gap_tmp[0] < 0.0001:
                        arr.add(small_near_tmp[0])
                        arr.add(small_near_tmp[1])
            elif len(small_near_tmp) >= len(big_tmp):
                if len(small_near_tmp) == 1:
                    arr.add(small_near_tmp[0])
            if len(big_near_tmp) == 1 and len(big_near_tmp) >= len(small_tmp):
                arr.add(big_near_tmp[0])
            if len(big_near_tmp) >= len(small_near_tmp) and len(big_near_tmp) >= len(small_tmp):
                if midJudge(big_near_tmp, nearGapStat, 0.01, True):
                    pos = len(big_near_tmp) - nearGapStat[0.01]
                    arr.add(big_near_tmp[pos])
                    for i in range(pos + 1, len(big_near_tmp)):
                        if big_near_gap_tmp[i] - big_near_gap_tmp[pos] < 0.00001:
                            arr.add(big_near_tmp[i])
                    gapAndConsecutive(arr, big_near_tmp, big_near_gap_tmp, pos - 1, left=True)
                if midJudge(big_near_tmp, nearGapStat, 0.01, False):
                    findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=False, choose_single=True)
                    findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=True, choose_single=False)
                    pos = len(big_near_tmp) - nearGapStat[0.01]
                    arr.add(big_near_tmp[pos])
                    if pos + 1 < len(big_near_tmp) and big_near_gap_tmp[pos + 1] - big_near_gap_tmp[pos] < 0.0026:
                        arr.add(big_near_tmp[pos + 1])
                    for i in range(pos + 1, len(big_near_tmp)):
                        if big_near_gap_tmp[i] - big_near_gap_tmp[pos] < 0.0001:
                            arr.add(i)
                    arr.add(big_near_tmp[pos - 1])
                    for i in range(pos - 2, -1, -1):
                        if big_near_gap_tmp[pos - 1] - big_near_gap_tmp[i] < 0.0001:
                            arr.add(big_near_tmp[i])
                if nearGapStat[0.01] == len(big_near_tmp):
                    findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=True, choose_single=False)
                if nearGapStat[0.01] == 0:
                    if noConsecutiveGap(big_near_gap_tmp):
                        arr.add(big_near_tmp[int(len(big_near_tmp) / 2)])
                    findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=False, choose_single=False)
                    findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=True, choose_single=False)
                    findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=True, choose_single=True)
                    arr.add(big_near_tmp[-1])
                    for i in range(-2, -1, -1):
                        if big_near_gap_tmp[-1] - big_near_gap_tmp[i] < 0.0001:
                            arr.add(big_near_tmp[i])
            if len(small_tmp) == len(big_tmp):
                if len(small_tmp) == 2:
                    if gapStat[-0.03] == 1:
                        arr.add(small_tmp[-1])
            if len(small_tmp) >= len(big_tmp) and len(small_tmp) - len(big_near_tmp) >= -1:
                if midJudge(small_tmp, gapStat, -0.02, True):
                    pos = gapStat[-0.02] - 1
                    gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos, left=True)
                if midJudge(small_tmp, gapStat, -0.03, True):
                    pos = gapStat[-0.03]
                    arr.add(small_tmp[pos])
                if midJudge(small_tmp, gapStat, -0.05, False):
                    pos = gapStat[-0.05] - 1
                    arr.add(small_tmp[pos])
                    for i in range(pos - 1, -1, -1):
                        if small_gap_tmp[pos] - small_gap_tmp[i] < 0.0001:
                            arr.add(small_tmp[i])
            elif len(small_tmp) > len(big_tmp):
                if len(small_tmp) == 2:
                    if gapStat[-0.03] == 1:
                        arr.add(small_tmp[0])
                        arr.add(small_tmp[-1])
            if len(big_tmp) >= len(small_tmp) and len(big_tmp) - len(small_near_tmp) >= -1:
                if big_gap_tmp[0] == big_gap_tmp[-1]:
                    for v in big_tmp:
                        arr.add(v)
                if midJudge(big_tmp, gapStat, 0.02, False):
                    pos = len(big_tmp) - gapStat[0.02] - 1
                    gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos, left=True)
                if midJudge(big_tmp, gapStat, 0.02, True):
                    pos = len(big_tmp) - gapStat[0.02] - 1
                    arr.add(big_tmp[pos])
                    arr.add(big_tmp[pos + 1])
                if len(big_tmp) == gapStat[0.03]:
                    if big_gap_tmp[-1] - big_gap_tmp[-2] < 0.00001:
                        arr.add(big_tmp[-1])
                        arr.add(big_tmp[-2])
                if midJudge(big_tmp, gapStat, 0.04, False):
                    pos = len(big_tmp) - gapStat[0.04]
                    arr.add(big_tmp[pos])
            if len(big_tmp) == 1:
                if gapStat[0.03] == 0:
                    arr.add(big_tmp[0])
            if len(big_tmp) == 2:
                if big_gap_tmp[0] < 0.017 and big_gap_tmp[1] > 0.018:
                    arr.add(big_tmp[0])
                if big_gap_tmp[0] == big_gap_tmp[1]:
                    arr.add(big_tmp[0])
                    arr.add(big_tmp[1])
                if gapStat[0.02] == 1:
                    arr.add(big_tmp[0])
            if len(big_near_tmp) == 2:
                arr.add(big_near_tmp[1])
                arr.add(big_near_tmp[0])
            print('参差不齐接近时大小一样')
    #连续接近
    elif count['near'] >= 5 and maxConsecutiveCount['near'] >= 4:
        if len(seq['small']) + len(seq['smallNear']) >= 7:
            print('连续接近时小的偏多' + extraSmall(seq))
        elif len(seq['big']) + len(seq['bigNear']) >= 7:
            print('连续接近时大的偏多' + extraBig(seq))
        elif len(seq['small']) + len(seq['smallNear']) > len(seq['big']) + len(seq['bigNear']):
            if len(small_near_tmp) >= len(big_tmp) and len(small_near_tmp) >= len(big_near_tmp):
                if midJudge(small_near_tmp, nearGapStat, -0.01, False):
                    pos = nearGapStat[-0.01] - 1
                    gapAndConsecutive(arr, small_near_tmp, small_near_gap_tmp, pos, left=True)
            print('连续接近时小的比大的多一些' + extraSmall(seq))
        elif len(seq['small']) + len(seq['smallNear']) < len(seq['big']) + len(seq['bigNear']):
            print('连续接近时大的比小的多一些' + extraBig(seq))
        else:
            if len(small_near_tmp) - len(big_tmp) >= -1 and len(small_near_tmp) - len(big_near_tmp) >= -2:
                if midJudge(small_near_tmp, nearGapStat, -0.01, False):
                    findTurn(arr, small_near_tmp, small_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=True, consecutive_at_left=False, choose_single=False)
            if len(big_near_tmp) >= len(small_tmp) and len(big_near_tmp) >= len(small_near_tmp):
                if midJudge(big_near_tmp, nearGapStat, 0.01, True):
                    pos = len(big_near_tmp) - nearGapStat[0.01]
                    gapAndConsecutive(arr, big_near_tmp, big_near_gap_tmp, pos, left=False)
            if len(small_tmp) > len(big_tmp):
                if midJudge(small_tmp, gapStat, -0.03, True):
                    pos = gapStat[-0.03] - 1
                    gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos, left=True)
            print('连续接近时大小一样')
    elif count['small'] >= 5 and maxConsecutiveCount['small'] < 4:
        if midJudge(small_tmp, gapStat, -0.05, False):
            pos = gapStat[-0.05]
            arr.add(small_tmp[pos])
            for i in range(pos + 1, len(small_tmp)):
                if small_gap_tmp[i] - small_gap_tmp[pos] < 0.0001:
                    arr.add(small_tmp[i])
        if midJudge(small_tmp, gapStat, -0.05, True):
            pos = gapStat[-0.05] - 1
            arr.add(small_tmp[pos])
            if pos - 1 > -1 and small_gap_tmp[pos] - small_gap_tmp[pos - 1] < 0.001:
                arr.add(small_tmp[pos - 1])
        if midJudge(small_tmp, gapStat, -0.06, False):
            pos = gapStat[-0.06]
            arr.add(small_tmp[pos])
            if pos + 1 < len(small_tmp) and small_gap_tmp[pos + 1] - small_gap_tmp[pos] < 0.0001:
                arr.add(small_tmp[pos + 1])
            arr.add(small_tmp[pos - 1])
            for i in range(pos - 2, -1, -1):
                if small_gap_tmp[pos - 1] - small_gap_tmp[i] < 0.00001:
                    arr.add(small_tmp[i])
        if midJudge(small_tmp, gapStat, -0.02, True):
            if midJudge(small_tmp, gapStat, -0.03, False):
                pos = gapStat[-0.03]
                if small_gap_tmp[pos] > -0.03 and small_gap_tmp[pos] < -0.0295:
                    arr.add(small_tmp[pos + 1])
            pos = gapStat[-0.02]
            arr.add(small_tmp[pos])
            if pos + 1 < len(small_tmp) and small_gap_tmp[pos + 1] - small_gap_tmp[pos] < 0.0001:
                arr.add(small_tmp[pos + 1])
        if len(big_tmp) == 2:
            if gapStat[0.02] == 1:
                arr.add(big_tmp[-1])
        if len(big_tmp) == 1:
            if gapStat[0.03] == 0:
                arr.add(big_tmp[0])
            if gapStat[0.02] == 0:
                arr.add(big_tmp[0])
        if midJudge(small_tmp, gapStat, -0.03, False):
            pos = gapStat[-0.03]
            arr.add(small_tmp[pos])
        if midJudge(small_tmp, gapStat, -0.03, True):
            pos = gapStat[-0.03] - 1
            arr.add(small_tmp[pos])
            if pos - 1 > -1 and small_gap_tmp[pos] - small_gap_tmp[pos - 1] < 0.001:
                arr.add(small_tmp[pos - 1])
        if midJudge(small_tmp, gapStat, -0.04, True):
            pos = gapStat[-0.04]
            arr.add(small_tmp[pos])
        if midJudge(small_tmp, gapStat, -0.04, False):
            pos = gapStat[-0.04]
            arr.add(small_tmp[pos])
        if len(big_near_tmp) - len(small_tmp) >= -1 and len(big_near_tmp) >= len(small_near_tmp):
            if midJudge(big_near_tmp, nearGapStat, 0.01, False):
                pos = len(big_near_tmp) - nearGapStat[0.01] - 1
                arr.add(big_near_tmp[pos])
                if pos - 1 > -1 and big_near_gap_tmp[pos] - big_near_gap_tmp[pos - 1] < 0.0001:
                    arr.add(big_near_tmp[pos - 1])
        elif len(big_near_tmp) >= len(small_near_tmp):
            if nearGapStat[0.01] == 1:
                arr.add(big_near_tmp[0])
            if big_near_gap_tmp[0] == big_near_gap_tmp[-1]:
                for v in big_near_tmp:
                    arr.add(v)
        if len(small_near_tmp) >= len(big_tmp) and len(small_near_tmp) >= len(big_near_tmp):
            if len(small_near_tmp) == 2:
                arr.add(small_near_tmp[-1])
                arr.add(small_near_tmp[0])
            if midJudge(small_near_tmp, nearGapStat, -0.01, False):
                pos = nearGapStat[-0.01]
                gapAndConsecutive(arr, small_near_tmp, small_near_gap_tmp, pos - 1, left=True)
                arr.add(small_near_tmp[pos])
                if noConsecutiveGap(small_near_gap_tmp):
                    if small_near_gap_tmp[-1] > -0.0045:
                        arr.add(small_near_tmp[-1])
            if nearGapStat[-0.01] == 0:
                findTurn(arr, small_near_tmp, small_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.02, reverse=False, consecutive_at_left=False, choose_single=False)
                findTurn(arr, small_near_tmp, small_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.02, reverse=False, consecutive_at_left=False, choose_single=True)
        if len(big_tmp) == 2:
            if gapStat[0.02] == 2:
                arr.add(big_tmp[0])
        if len(big_tmp) - len(small_tmp) >= -2 and len(big_tmp) >= len(small_near_tmp):
            if midJudge(big_tmp, gapStat, 0.02, True):
                pos = len(big_tmp) - gapStat[0.02]
                gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos, left=False)
        print('参差不齐小' + restExcSmall(seq))
    elif count['big'] >= 5 and count['near'] >= 2:
        if gapStat[0.02] == len(big_tmp):
            if big_gap_tmp[0] < 0.0215:
                arr.add(big_tmp[0])
            if gapStat[0.03] == 0:
                findTurn(arr, big_tmp, big_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=True, choose_single=False)
                findTurn(arr, big_tmp, big_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=True, consecutive_at_left=True, choose_single=False)
            if midJudge(big_tmp, gapStat, 0.03, True):
                for i in range(1, len(big_tmp)):
                    if big_gap_tmp[i] > 0.0285 and big_gap_tmp[i] < 0.03:
                        arr.add(big_tmp[i-1])
                        break
                    if big_gap_tmp[i] > 0.026 and big_gap_tmp[i] < 0.03 and big_gap_tmp[i-1] < 0.022:
                        arr.add(big_tmp[i-1])
                        break
        if midJudge(big_tmp, gapStat, 0.02, False):
            pos = len(big_tmp) - gapStat[0.02] - 1
            gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos, left=True)
            findTurn(arr, big_tmp, big_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=True, choose_single=False)
            findTurn(arr, big_tmp, big_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=False, choose_single=True)
        if midJudge(big_tmp, gapStat, 0.02, True):
            if big_gap_tmp[1] > 0.018 and big_gap_tmp[1] < 0.02:
                arr.add(big_tmp[0])
            pos = len(big_tmp) - gapStat[0.02]
            if big_gap_tmp[pos] < 0.021:
                arr.add(big_tmp[pos + 1])
            arr.add(big_tmp[pos])
            if big_gap_tmp[pos + 1] - big_gap_tmp[pos] < 0.00001:
                arr.add(big_tmp[pos + 1])
            if pos - 1 > -1:
                arr.add(big_tmp[pos - 1])
                if pos - 2 > -1 and big_gap_tmp[pos - 1] - big_gap_tmp[pos - 2] < 0.00001:
                    arr.add(big_tmp[pos - 2])
            findTurn(arr, big_tmp, big_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=True, consecutive_at_left=False, choose_single=False)
        if midJudge(big_tmp, gapStat, 0.03, True):
            pos = len(big_tmp) - gapStat[0.03] - 1
            if big_gap_tmp[pos] > 0.0288:
                if pos - 1 > -1:
                    arr.add(big_tmp[pos - 1])
            if gapStat[0.04] == 0:
                for i in range(len(big_tmp) - 1, -1, -1):
                    if big_gap_tmp[i] > 0.039:
                        arr.add(big_tmp[i-1])
                        break
                findTurn(arr, big_tmp, big_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=True, consecutive_at_left=False, choose_single=True)
                findTurn(arr, big_tmp, big_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=True, consecutive_at_left=True, choose_single=True)
                findTurn(arr, big_tmp, big_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=True, consecutive_at_left=False, choose_single=False)
            pos = len(big_tmp) - gapStat[0.03]
            arr.add(big_tmp[pos])
            if big_gap_tmp[pos] < 0.0316 and big_gap_tmp[pos + 1] > 0.032:
                arr.add(big_tmp[pos + 1])
            arr.add(big_tmp[pos - 1])
            if big_gap_tmp[pos + 1] - big_gap_tmp[pos] < 0.00001:
                arr.add(big_tmp[pos + 1])
            if pos - 2 > -1 and big_gap_tmp[pos - 1] - big_gap_tmp[pos - 2] < 0.00001:
                arr.add(big_tmp[pos - 2])
        if midJudge(big_tmp, gapStat, 0.03, False):
            if big_gap_tmp[0] < 0.021 and big_gap_tmp[1] > 0.0245:
                arr.add(big_tmp[0])
            if big_gap_tmp[-1] > 0.036:
                arr.add(big_tmp[-1])
            if len(big_tmp) == gapStat[0.02]:
                findTurn(arr, big_tmp, big_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=False, choose_single=True)
                findTurn(arr, big_tmp, big_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=True, choose_single=False)
            pos = len(big_tmp) - gapStat[0.03] - 1
            arr.add(big_tmp[pos])
            for i in range(pos - 1, -1, -1):
                if big_gap_tmp[pos] - big_gap_tmp[i] < 0.0001:
                    arr.add(big_tmp[i])
            arr.add(big_tmp[pos + 1])
            for i in range(pos + 2, len(big_tmp)):
                if big_gap_tmp[i] - big_gap_tmp[pos + 1] < 0.0001:
                    arr.add(big_tmp[i])
        if midJudge(big_tmp, gapStat, 0.06, False):
            pos = len(big_tmp) - gapStat[0.06] - 1
            arr.add(big_tmp[pos])
            if big_gap_tmp[pos] - big_gap_tmp[pos - 1] < 0.0001:
                arr.add(big_tmp[pos - 1])
        if midJudge(big_tmp, gapStat, 0.05, False):
            pos = len(big_tmp) - gapStat[0.05] - 1
            arr.add(big_tmp[pos])
            if pos - 1 > -1 and big_gap_tmp[pos] - big_gap_tmp[pos - 1] < 0.00001:
                arr.add(big_tmp[pos - 1])
            arr.add(big_tmp[pos + 1])
            if pos + 2 < len(big_tmp) and big_gap_tmp[pos + 2] - big_gap_tmp[pos + 1] < 0.00001:
                arr.add(big_tmp[pos + 2])
        if midJudge(big_tmp, gapStat, 0.04, True):
            if gapStat[0.05] == 0:
                if gapStat[0.02] == len(big_tmp):
                    arr.add(big_tmp[0])
            pos = len(big_tmp) - gapStat[0.04]
            arr.add(big_tmp[pos])
        if midJudge(big_tmp, gapStat, 0.04, False):
            if gapStat[0.05] == 0:
                arr.add(big_tmp[-1])
                findTurn(arr, big_tmp, big_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=True, consecutive_at_left=True, choose_single=False)
            pos = len(big_tmp) - gapStat[0.04]
            arr.add(big_tmp[pos])
            arr.add(big_tmp[pos - 1])
            if pos - 2 > -1 and big_gap_tmp[pos - 1] - big_gap_tmp[pos - 2] < 0.0001:
                arr.add(big_tmp[pos - 2])
        if len(big_near_tmp) >= len(small_tmp) and len(big_near_tmp) >= len(small_near_tmp):
            if len(big_near_tmp) > 2:
                if big_near_gap_tmp[0] < 0.0019 and big_near_gap_tmp[2] > 0.0085:
                    arr.add(big_near_tmp[1])
                if big_near_gap_tmp[-1] > 0.0085 and big_near_gap_tmp[-3] < 0.0019:
                    arr.add(big_near_tmp[-2])
            if len(big_near_tmp) == 2:
                if big_near_gap_tmp[0] < 0.0105:
                    arr.add(big_near_tmp[0])
                if nearGapStat[0.01] == 0:
                    if big_near_gap_tmp[1] > 0.008 and big_near_gap_tmp[0] < 0.005:
                        arr.add(big_near_tmp[0])
                if nearGapStat[0.01] == 1:
                    arr.add(big_near_tmp[0])
                    arr.add(big_near_tmp[1])
                if big_near_gap_tmp[0] < 0.001 and big_near_gap_tmp[1] > 0.0035:
                    arr.add(big_near_tmp[0])
            if midJudge(big_near_tmp, nearGapStat, 0.01, True):
                pos = len(big_near_tmp) - nearGapStat[0.01] - 1
                arr.add(big_near_tmp[pos])
                arr.add(big_near_tmp[pos + 1])
                for i in range(pos + 2, len(big_near_tmp)):
                    if big_near_gap_tmp[i] - big_near_gap_tmp[pos + 1] < 0.0001:
                        arr.add(big_near_tmp[i])
            if midJudge(big_near_tmp, nearGapStat, 0.01, False):
                pos = len(big_near_tmp) - nearGapStat[0.01]
                gapAndConsecutive(arr, big_near_tmp, big_near_gap_tmp, pos - 1, left=True)
                if pos > -1 and pos < len(big_near_tmp):
                    arr.add(big_near_tmp[pos])
                if noConsecutiveGap(big_near_gap_tmp):
                    arr.add(big_near_tmp[0])
                findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=False, choose_single=False)
            if len(big_near_tmp) == nearGapStat[0.01]:
                findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=True, choose_single=False)
                if big_near_gap_tmp[-1] - big_near_gap_tmp[0] < 0.0001:
                    arr.add(big_near_tmp[0])
                    arr.add(big_near_tmp[1])
            if nearGapStat[0.01] == 0:
                if len(big_near_tmp) > 2:
                    if big_near_gap_tmp[0] == big_near_gap_tmp[1] and big_near_gap_tmp[1] == big_near_gap_tmp[2]:
                        arr.add(big_near_tmp[0])
                        arr.add(big_near_tmp[1])
                        arr.add(big_near_tmp[2])                        
                if noConsecutiveGap(big_near_gap_tmp):
                    arr.add(big_near_tmp[-1])
                if len(big_near_tmp) == 2:
                    arr.add(big_near_tmp[-1])
                findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=False, choose_single=True)
                findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=True, choose_single=True)
                findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=True, choose_single=False)
                findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=False, choose_single=False)
        if len(big_near_tmp) == 1:
            if nearGapStat[0.01] <= 1:
                arr.add(big_near_tmp[0])
        if len(small_near_tmp) - len(big_near_tmp) >= -1:
            if len(small_near_tmp) == 1:
                arr.add(small_near_tmp[0])
        if len(small_near_tmp) > len(big_near_tmp):
            if len(small_near_tmp) == 2:
                if nearGapStat[-0.01] == 0:
                    arr.add(small_near_tmp[0])
            if nearGapStat[-0.01] == 0:
                findTurn(arr, small_near_tmp, small_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=False, choose_single=False)
            if midJudge(small_near_tmp, nearGapStat, -0.01, True):
                pos = nearGapStat[-0.01] - 1
                arr.add(small_near_tmp[pos])
                if pos - 1 > -1 and small_near_gap_tmp[pos] - small_near_gap_tmp[pos - 1] < 0.00001:
                    arr.add(small_near_tmp[pos - 1])
            if midJudge(small_near_tmp, nearGapStat, -0.01, False):
                pos = nearGapStat[-0.01]
                gapAndConsecutive(arr, small_near_tmp, small_near_gap_tmp, pos, left=False)
            arr.add(small_near_tmp[0])
        if len(small_near_tmp) == 1:
            arr.add(small_near_tmp[0])
        if len(small_near_tmp) == 2:
            if nearGapStat[-0.01] == 0:
                arr.add(small_near_tmp[-1])
                if small_near_gap_tmp[-1] - small_near_gap_tmp[0] < 0.0001:
                    arr.add(small_near_tmp[0])
            if nearGapStat[-0.01] == 1:
                if small_near_gap_tmp[0] > -0.0145:
                    arr.add(small_near_tmp[0])
                    arr.add(small_near_tmp[1])
        if len(small_tmp) - len(big_near_tmp) >= -1:
            if midJudge(small_tmp, gapStat, -0.02, True):
                pos = gapStat[-0.02] - 1
                arr.add(small_tmp[pos])
            if len(small_tmp) == 1:
                if gapStat[-0.04] == 0:
                    arr.add(small_tmp[0])
        if len(small_tmp) == 2:
            if gapStat[-0.03] == 1:
                if gapStat[-0.04] == 0:
                    arr.add(small_tmp[0])
            if gapStat[-0.02] == 1:
                arr.add(small_tmp[-1])
        if len(small_tmp) == 1:
            if gapStat[-0.02] == 1:
                if gapStat[-0.03] == 0:
                    arr.add(small_tmp[0])
        flag = ':参差' if maxConsecutiveCount['big'] < 4 else ':连续'
        print('不是大的就是接近的(大的偏多)' + flag + restExcBig(seq))
    elif count['big'] >= 5 and count['small'] >= 2:
        if midJudge(big_tmp, gapStat, 0.03, False):
            pos = len(big_tmp) - gapStat[0.03] - 1
            gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos, left=True)
            gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos + 1, left=False)
        flag = ':参差' if maxConsecutiveCount['big'] < 4 else ':连续'
        print('不是大的就是小的(大的偏多)' + flag + restExcBig(seq))
    #大:接近:小很均衡
    elif count['big'] <= 4 and count['near'] <= 4 and count['small'] <= 4:
        if len(seq['small']) + len(seq['smallNear']) > len(seq['big']) + len(seq['bigNear']):
            if len(small_tmp) > len(big_tmp) and len(small_tmp) > len(big_near_tmp):
                if midJudge(small_tmp, gapStat, -0.03, True):
                    pos = gapStat[-0.03]
                    arr.add(small_tmp[pos])
                if midJudge(small_tmp, gapStat, -0.02, True):
                    pos = gapStat[-0.02]
                    arr.add(small_tmp[pos])
                if midJudge(small_tmp, gapStat, -0.04, False):
                    if gapStat[-0.05] == 0:
                        if small_gap_tmp[0] < -0.0489:
                            arr.add(small_tmp[0])
            if len(big_near_tmp) == 2:
                if nearGapStat[0.01] == 0:
                    arr.add(big_near_tmp[-1])
            if len(big_tmp) == 2:
                if gapStat[0.02] == 1:
                    arr.add(big_tmp[1])
                if gapStat[0.03] == 2 and gapStat[0.04] == 0:
                    arr.add(big_tmp[0])
                    if big_gap_tmp[1] - big_gap_tmp[0] < 0.00001:
                        arr.add(big_tmp[1])
            if len(small_near_tmp) >= len(big_tmp) and len(small_near_tmp) >= len(big_near_tmp):
                if midJudge(small_near_tmp, nearGapStat, -0.01, False):
                    pos = nearGapStat[-0.01]
                    arr.add(small_near_tmp[pos])
                    findTurn(arr, small_near_tmp, small_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=True, consecutive_at_left=False, choose_single=False)
                if nearGapStat[-0.01] == 0:
                    findTurn(arr, small_near_tmp, small_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=False, choose_single=False)
            if len(big_tmp) - len(small_tmp) >= -1 and len(big_tmp) - len(small_near_tmp) >= -1:
                if midJudge(big_tmp, gapStat, 0.03, False):
                    pos = len(big_tmp) - gapStat[0.03] - 1
                    arr.add(big_tmp[pos])
                    if pos - 1 > -1 and big_gap_tmp[pos] - big_gap_tmp[pos - 1] < 0.00001:
                        arr.add(big_tmp[pos - 1])
            print('很均衡时小的偏多' + extraSmall(seq))
        elif len(seq['small']) + len(seq['smallNear']) < len(seq['big']) + len(seq['bigNear']):
            if len(big_near_tmp) >= len(small_near_tmp) and len(big_near_tmp) >= len(small_tmp):
                if nearGapStat[0.01] == 0:
                    findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=True, choose_single=False)
                    findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=True, choose_single=True)
                    if big_near_gap_tmp[-1] - big_near_gap_tmp[-2] < 0.00001:
                        arr.add(big_near_tmp[-1])
                        for i in range(len(big_near_tmp) - 2, -1, -1):
                            if big_near_gap_tmp[-1] - big_near_gap_tmp[i] < 0.0001:
                                arr.add(big_near_tmp[i])
                if midJudge(big_near_tmp, nearGapStat, 0.01, False):
                    if big_near_gap_tmp[0] < 0.0004:
                        arr.add(big_near_tmp[1])
                    if big_near_gap_tmp[-1] > 0.014 and big_near_gap_tmp[-2] < 0.012:
                        arr.add(big_near_tmp[-1])
                    arr.add(big_near_tmp[0])
                    pos = len(big_near_tmp) - nearGapStat[0.01]
                    arr.add(big_near_tmp[pos])
                    arr.add(big_near_tmp[pos - 1])
                if midJudge(big_near_tmp, nearGapStat, 0.01, True):
                    pos = len(big_near_tmp) - nearGapStat[0.01]
                    arr.add(big_near_tmp[pos])
                    arr.add(big_near_tmp[pos - 1])
                    for i in range(pos + 1, len(big_near_tmp)):
                        if big_near_gap_tmp[i] - big_near_gap_tmp[pos] < 0.00001:
                            arr.add(big_near_tmp[i])
                    findTurn(arr, big_near_tmp, big_near_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=True, consecutive_at_left=True, choose_single=True)
                if len(big_near_tmp) == 2:
                    if nearGapStat[0.01] == 0:
                        arr.add(big_near_tmp[0])
                    if nearGapStat[0.01] == 1:
                        arr.add(big_near_tmp[1])
            if len(big_tmp) >= len(small_tmp) and len(big_tmp) >= len(small_near_tmp):
                if gapStat[0.02] == 0:
                    findTurn(arr, big_tmp, big_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=True, choose_single=False)
                if midJudge(big_tmp, gapStat, 0.02, True):
                    if gapStat[0.03] == 0:
                        findTurn(arr, big_tmp, big_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=True, consecutive_at_left=False, choose_single=False)
                    pos = len(big_tmp) - gapStat[0.02] - 1
                    arr.add(big_tmp[pos])
                    for i in range(pos - 1, -1, -1):
                        if big_gap_tmp[pos] - big_gap_tmp[i] < 0.00001:
                            arr.add(big_tmp[i])
                    arr.add(big_tmp[pos + 1])
                    if big_gap_tmp[pos] > 0.0175 and pos - 1 > -1 and big_gap_tmp[pos - 1] < 0.0157:
                        arr.add(big_tmp[pos - 1])
                if midJudge(big_tmp, gapStat, 0.02, False):
                    if gapStat[0.03] == 0:
                        if big_gap_tmp[-1] > 0.0271:
                            arr.add(big_tmp[-1])
                    findTurn(arr, big_tmp, big_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=True, choose_single=False)
                if midJudge(big_tmp, gapStat, 0.04, False):
                    pos = len(big_tmp) - gapStat[0.04] - 1
                    arr.add(big_tmp[pos])
                if midJudge(big_tmp, gapStat, 0.03, False):
                    pos = len(big_tmp) - gapStat[0.03] - 1
                    arr.add(big_tmp[pos])
                    for i in range(pos - 1, -1, -1):
                        if big_gap_tmp[pos] - big_gap_tmp[i] < 0.0001:
                            arr.add(big_tmp[i])
                    gapAndConsecutive(arr, big_tmp, big_gap_tmp, pos + 1, left=False)
                if len(big_tmp) == gapStat[0.02]:
                    if big_gap_tmp[0] < 0.022 and big_gap_tmp[1] > 0.026:
                        arr.add(big_tmp[0])
                    if big_gap_tmp[0] < 0.0202 and big_gap_tmp[1] > 0.022:
                        arr.add(big_tmp[1])
                    if midJudge(big_tmp, gapStat, 0.03, False):
                        findTurn(arr, big_tmp, big_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=True, choose_single=False)
                    if gapStat[0.03] == 0:
                        findTurn(arr, big_tmp, big_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=False, consecutive_at_left=False, choose_single=True)
            if len(small_tmp) - len(big_tmp) >= -1 and len(small_tmp) - len(big_near_tmp) >= -1:
                if gapStat[-0.02] == len(small_tmp):
                    if midJudge(small_tmp, gapStat, -0.03, True):
                        pos = len(small_tmp) - gapStat[-0.03]
                        if small_gap_tmp[pos] > -0.03 and small_gap_tmp[pos] < -0.026 and pos + 1 < len(small_tmp) and small_gap_tmp[pos + 1] > -0.022 and small_gap_tmp[pos + 1] < -0.02:
                            arr.add(small_tmp[pos + 1])
                if midJudge(small_tmp, gapStat, -0.02, True):
                    pos = gapStat[-0.02]
                    gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos, left=False)
                    gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos - 1, left=True)
                if midJudge(small_tmp, gapStat, -0.04, False):
                    pos = gapStat[-0.04]
                    gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos, left=False)
            elif len(small_tmp) - len(big_near_tmp) >= -1:
                if len(small_tmp) == 2:
                    if gapStat[-0.04] == 1:
                        arr.add(small_tmp[1])
                    if gapStat[-0.02] == 1:
                        arr.add(small_tmp[1])
                    if gapStat[-0.03] == 1:
                        if gapStat[-0.04] == 0:
                            if small_gap_tmp[0] < -0.0389:
                                arr.add(small_tmp[0])
            if len(small_near_tmp) >= len(big_near_tmp):
                if nearGapStat[-0.01] == 1:
                    arr.add(small_near_tmp[-1])
                if len(small_near_tmp) == 2:
                    if nearGapStat[-0.01] == 1:
                        arr.add(small_near_tmp[0])
            if len(small_near_tmp) == 1:
                arr.add(small_near_tmp[0])
            print('很均衡时大的偏多' + extraBig(seq))
        else:
            if len(small_near_tmp) == 1:
                if nearGapStat[-0.01] == 0:
                    arr.add(small_near_tmp[0])
            if len(big_tmp) >= len(small_tmp) and len(big_tmp) >= len(small_near_tmp):
                if len(big_tmp) == gapStat[0.02]:
                    findTurn(arr, big_tmp, big_gap_tmp, approach_threshold=0.0001, gap_threshold=0.01, reverse=False, consecutive_at_left=True, choose_single=True)
                if midJudge(big_tmp, gapStat, 0.02, False):
                    pos = len(big_tmp) - gapStat[0.02] - 1
                    arr.add(big_tmp[pos])
                    for i in range(pos - 1, -1, -1):
                        if big_gap_tmp[pos] - big_gap_tmp[i] < 0.00001:
                            arr.add(big_tmp[i])
                if midJudge(big_tmp, gapStat, 0.03, False):
                    pos = len(big_tmp) - gapStat[0.03]
                    arr.add(big_tmp[pos])
                    arr.add(big_tmp[pos - 1])
                    for i in range(pos - 2, -1, -1):
                        if big_gap_tmp[pos - 1] - big_gap_tmp[i] < 0.0001:
                            arr.add(big_tmp[i])
            if len(big_near_tmp) == 2:
                if nearGapStat[0.01] == 0:
                    arr.add(big_near_tmp[1])
                if nearGapStat[0.01] == 1:
                    arr.add(big_near_tmp[0])
                    arr.add(big_near_tmp[1])
                if nearGapStat[0.01] == 2:
                    arr.add(big_near_tmp[0])
                    if big_near_gap_tmp[1] - big_near_gap_tmp[0] < 0.0001:
                        arr.add(big_near_tmp[1])
            if len(big_near_tmp) == 1:
                arr.add(big_near_tmp[0])
            if len(small_near_tmp) > len(big_near_tmp) and len(small_near_tmp) - len(big_tmp) >= -1:
                if midJudge(small_near_tmp, nearGapStat, -0.01, False):
                    pos = nearGapStat[-0.01]
                    arr.add(small_near_tmp[pos])
                if nearGapStat[-0.01] == 0:
                    arr.add(small_near_tmp[0])
                    for i in range(1, len(small_near_tmp)):
                        if small_near_gap_tmp[i] - small_near_gap_tmp[0] < 0.0001:
                            arr.add(small_near_tmp[i])
            elif len(small_near_tmp) >= len(big_near_tmp):
                if nearGapStat[-0.01] == 1:
                    arr.add(small_near_tmp[1])
            if len(big_near_tmp) >= len(small_near_tmp) and len(big_near_tmp) - len(small_tmp) >= -1:
                if midJudge(big_near_tmp, nearGapStat, 0.01, False):
                    pos = len(big_near_tmp) - nearGapStat[0.01] - 1
                    arr.add(big_near_tmp[pos])
                    if pos - 1 > -1 and big_near_gap_tmp[pos] > big_near_gap_tmp[pos - 1]:
                        arr.add(big_near_tmp[pos - 1])
                if midJudge(big_near_tmp, nearGapStat, 0.01, True):
                    pos = len(big_near_tmp) - nearGapStat[0.01] - 1
                    arr.add(big_near_tmp[pos])
            if len(small_tmp) - len(big_tmp) >= -1 and len(small_tmp) >= len(big_near_tmp):
                if midJudge(small_tmp, gapStat, -0.05, False):
                    pos = gapStat[-0.05] - 1
                    arr.add(small_tmp[pos])
                    for i in range(pos - 1, -1, -1):
                        if small_gap_tmp[pos] - small_gap_tmp[i] < 0.0001:
                            arr.add(small_tmp[i])
                if midJudge(small_tmp, gapStat, -0.04, True):
                    pos = gapStat[-0.04]
                    arr.add(small_tmp[pos])
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
                if midJudge(small_tmp, gapStat, -0.02, True):
                    pos = gapStat[-0.02]
                    arr.add(small_tmp[pos])
                    if pos + 1 < len(small_tmp) and small_gap_tmp[pos + 1] - small_gap_tmp[pos] < 0.003:
                        arr.add(small_tmp[pos + 1])
                    for i in range(pos + 1, len(small_tmp)):
                        if small_gap_tmp[i] - small_gap_tmp[pos] < 0.0001:
                            arr.add(small_tmp[i])
            print('非常均衡')
    #大部分小
    elif count['small'] >= 7:
        if midJudge(small_tmp, gapStat, -0.08, False):
            pos = gapStat[-0.08] - 1
            arr.add(small_tmp[pos])
            for i in range(pos - 1, -1, -1):
                if small_gap_tmp[pos] - small_gap_tmp[i] < 0.0001:
                    arr.add(small_tmp[i])
        if midJudge(small_tmp, gapStat, -0.03, False):
            pos = gapStat[-0.03]
            gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos, left=False)
        if midJudge(small_tmp, gapStat, -0.02, True):
            pos = gapStat[-0.02]
            gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos, left=False)
        if midJudge(small_tmp, gapStat, -0.03, True):
            pos = gapStat[-0.03] - 1
            if small_gap_tmp[pos] > -0.031:
                arr.add(small_tmp[pos - 1])
            gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos + 1, left=False)
            findTurn(arr, small_tmp, small_gap_tmp, approach_threshold=0.0001, gap_threshold=0.05, reverse=True, consecutive_at_left=False, choose_single=True)
        if midJudge(small_tmp, gapStat, -0.04, False):
            pos = gapStat[-0.04] - 1
            arr.add(small_tmp[pos])
            for i in range(pos - 1, -1, -1):
                if small_gap_tmp[pos] - small_gap_tmp[i] < 0.0001:
                    arr.add(small_tmp[i])
        if midJudge(small_tmp, gapStat, -0.05, False):
            pos = gapStat[-0.05] - 1
            arr.add(small_tmp[pos])
            for i in range(pos - 1, -1, -1):
                if small_gap_tmp[pos] - small_gap_tmp[i] < 0.0001:
                    arr.add(small_tmp[i])
        if len(big_near_tmp) >= len(small_near_tmp):
            if len(big_near_tmp) == 1:
                if big_near_gap_tmp[0] < 0.005:
                    arr.add(big_near_tmp[0])
        print('大部分小')
    elif count['small'] >= 5 and maxConsecutiveCount['small'] >= 4:
        if len(small_near_tmp) >= len(big_tmp) and len(small_near_tmp) >= len(big_near_tmp):
            if len(small_near_tmp) == 2:
                if nearGapStat[-0.01] == 1:
                    arr.add(small_near_tmp[1])
            if midJudge(small_near_tmp, nearGapStat, -0.01, False):
                pos = nearGapStat[-0.01] - 1
                gapAndConsecutive(arr, small_near_tmp, small_near_gap_tmp, pos, left=True)
                gapAndConsecutive(arr, small_near_tmp, small_near_gap_tmp, pos + 1, left=False)
        if midJudge(small_tmp, gapStat, -0.03, True):
            pos = gapStat[-0.03] - 1
            gapAndConsecutive(arr, small_tmp, small_gap_tmp, pos, left=True)
            if small_gap_tmp[pos + 1] < -0.027:
                if pos + 2 < len(small_tmp):
                    arr.add(small_tmp[pos + 2])
        print('连续小' + restExcSmall(seq))
    else:
        print('不对呀', data_len)
    print(data_len, good_count, arr)
    del(seq['near'])
    show(gapStat, avg_window, data_len, range_stat, prob_cand_arr, pred, seq)
    return arr



