import sys, numpy as np
import json, copy

def pattern_sort(prob_cand_arr, pred, seq, r=False, pos=None):
    seq = [v[0] for v in sorted([(pos, prob_cand_arr[pos]) for pos in seq], key=lambda pair : pair[1], reverse=r)]
    if pos is not None:
        if pos > 0:
            return set(seq[:pos])
        elif pos < 0:
            return set(seq[pos:])
        else:
            return seq
    if len(seq) <= 3:
        return set(seq)
    result = [seq[0]]
    for i in range(1, len(seq)):
        if abs(prob_cand_arr[seq[i]] - prob_cand_arr[result[-1]]) <= 0.0143 or len(result) < round(len(seq) / 2):
            result.append(seq[i])
    return set(result)


def pattern_check_detail(count, previousPos, consecutiveCount, maxConsecutiveCount, name, pos):
    count[name] = count[name] + 1
    if pos - previousPos[name] == 1:
        consecutiveCount[name] = consecutiveCount[name] + 1
        maxConsecutiveCount[name] = max(maxConsecutiveCount[name], consecutiveCount[name])
    else:
        consecutiveCount[name] = 0
    previousPos[name] = pos


def remove_fake_small(arr, prob_cand_arr, pred, seq):
    seq = pattern_sort(prob_cand_arr, pred, seq['small'], False, 0)
    if len(seq) > 1 and prob_cand_arr[seq[1]] - prob_cand_arr[seq[0]] < 0.02:
        if seq[0] in arr:
            arr.remove(seq[0])

def add_near_small(arr, prob_cand_arr, pred, seq):
    for pos in pattern_sort(prob_cand_arr, pred, seq['small'], True, 0):
        if prob_cand_arr[pos] - pred > -0.018 or (len(seq['small']) < 3 and prob_cand_arr[pos] - pred > -0.021):
            arr.add(pos)


def diff_stat(arr, pred):
    cnt = 0
    for v in arr:
        if abs(v - pred) >= 0.02:
            cnt += 1
    return cnt

def sort_show(arr):
    return sorted(arr, key=lambda x : float(x.split(':')[1]))


def findTurnInner(i, arr, tmp, tmp_gap, approach_threshold=0.0001, gap_threshold=0.2, reverse=True, consecutive_at_left=True, choose_single=False, remove_tiny=False):
    if consecutive_at_left:
        if i >= 2:
            if tmp_gap[i-1] - tmp_gap[i-2] < approach_threshold:
                if (tmp_gap[i] - tmp_gap[i-1]) / min(abs(tmp_gap[i]), abs(tmp_gap[i-1])) > gap_threshold:
                    if choose_single:
                        arr.add(tmp[i])
                    else:
                        if not remove_tiny or (remove_tiny and abs(tmp_gap[i-1]) > 0.0006):
                            arr.add(tmp[i-1])
                            arr.add(tmp[i-2])
                            for j in range(i-3, -1, -1):
                                if j > -1 and abs(tmp_gap[i-2] - tmp_gap[j]) < 0.00001:
                                    arr.add(tmp[j])
                    return True
    else:
        if i < len(tmp) - 2:
            if tmp_gap[i+2] - tmp_gap[i+1] < approach_threshold:
                if (tmp_gap[i + 1] - tmp_gap[i]) / min(abs(tmp_gap[i]), abs(tmp_gap[i+1])) > gap_threshold:
                    if choose_single:
                        arr.add(tmp[i])
                    else:
                        if not remove_tiny or (remove_tiny and abs(tmp_gap[i+1]) > 0.0006):
                            arr.add(tmp[i + 1])
                            arr.add(tmp[i + 2])
                            for j in range(i+3, len(tmp)):
                                if j < len(tmp) and abs(tmp_gap[j] - tmp_gap[i+2]) < 0.00001:
                                    arr.add(tmp[j])
                    return True
    return False


def findTurn(arr, tmp, tmp_gap, approach_threshold=0.0001, gap_threshold=0.2, reverse=True, consecutive_at_left=True, choose_single=False, remove_tiny=False):
    if reverse:
        for i in range(len(tmp) - 1, -1, -1):
            if findTurnInner(i, arr, tmp, tmp_gap, approach_threshold, gap_threshold, reverse, consecutive_at_left, choose_single, remove_tiny):
                break
    else:
        for i in range(len(tmp)):
            if findTurnInner(i, arr, tmp, tmp_gap, approach_threshold, gap_threshold, reverse, consecutive_at_left, choose_single, remove_tiny):
                break



def midJudge(tmp, gapStat, kind, over=True):
    if len(tmp) < 3:
        return False
    if gapStat[kind] == int(len(tmp) / 2) and len(tmp) % 2 == 0:
        return True
    if over:
        if gapStat[kind] >= len(tmp) / 2 and gapStat[kind] < len(tmp):
            return True
        return False
    else:
        if gapStat[kind] <= len(tmp) / 2 and gapStat[kind] > 0:
            return True
        return False


def noConsecutiveGap(tmp_gap):
    for i in range(0, len(tmp_gap) - 1):
        if tmp_gap[i + 1] - tmp_gap[i] < 0.00001:
            return False
    return True


def gapAndConsecutive(arr, tmp, tmp_gap, pos, left=True):
    arr.add(tmp[pos])
    if left:
        for i in range(pos - 1, -1, -1):
            if tmp_gap[pos] - tmp_gap[i] < 0.00001:
                arr.add(tmp[i])
    else:
        for i in range(pos + 1, len(tmp)):
            if tmp_gap[i] - tmp_gap[pos] < 0.00001:
                arr.add(tmp[i])


def show(gapStat, avg_window, data_len, range_stat, prob_cand_arr, pred, seq):
    s = {k : sort_show([str(bi) + ':' + "{:.4f}".format(prob_cand_arr[bi] - pred) for bi in seq[k]]) for k in seq}
    if range_stat is not None:
        for r in s:
            for v in s[r]:
                l = v.split(':')[0]
                if l not in range_stat:
                    range_stat[l] = {}
                if r in range_stat[l]:
                    range_stat[l][r] += 1
                else:
                    range_stat[l][r] = 1
    for k in s:
        if len(s[k]) > 1 and s[k][0].split(':')[1] == s[k][-1].split(':')[1]:
            s[k] = str(s[k]).replace('[', '【').replace(']', '】')
    print(avg_window, data_len, s, gapStat)


def extraSmall(seq, ratio=None):
    if ratio is None:
        ratio = 1
    if len(seq['small']) - len(seq['smallNear']) >= 2 * ratio:
        flag = ':偏向小'
    elif len(seq['smallNear']) - len(seq['small']) >= 2 * ratio:
        flag = ':偏向接近'
    else:
        flag = ''
    if len(seq['bigNear']) - len(seq['small']) >= 2 * ratio or len(seq['bigNear']) - len(seq['smallNear']) >= 2 * ratio:
        rest = ':剩下是大的'
    elif len(seq['big']) - len(seq['small']) >= 2 * ratio or len(seq['big']) - len(seq['smallNear']) >= 2 * ratio:
        rest = ':剩下是大接近的'
    else:
        rest = ''
    return flag + rest


def extraBig(seq, ratio=None):
    if ratio is None:
        ratio = 1
    if len(seq['big']) - len(seq['bigNear']) >= 2 * ratio:
        flag = ':偏向大'
    elif len(seq['bigNear']) - len(seq['big']) >= 2 * ratio:
        flag = ':偏向接近'
    else:
        flag = ''
    if len(seq['small']) - len(seq['big']) >= 2 * ratio or len(seq['small']) - len(seq['bigNear']) >= 2 * ratio:
        rest = ':剩下是小的'
    elif len(seq['smallNear']) - len(seq['big']) >= 2 * ratio or len(seq['smallNear']) - len(seq['bigNear']) >= 2 * ratio:
        rest = ':剩下是小接近的'
    else:
        rest = ''
    return flag + rest


def restExcSmall(seq, ratio=None):
    if ratio is None:
        ratio = 1
    if len(seq['smallNear']) >= 3 * ratio:
        return ':剩下是小接近'
    elif len(seq['big']) >= 3 * ratio:
        return ':剩下是大'
    elif len(seq['bigNear']) >= 3 * ratio:
        return ':剩下是大接近'
    else:
        return ''


def restExcBig(seq, ratio=None):
    if ratio is None:
        ratio = 1
    if len(seq['smallNear']) >= 3 * ratio:
        return ':剩下是小接近'
    elif len(seq['small']) >= 3 * ratio:
        return ':剩下是小'
    elif len(seq['bigNear']) >= 3 * ratio:
        return ':剩下是大接近'
    else:
        return ''

def fmt(val):
    neg_or_pos = 1 if val >= 0 else -1
    return neg_or_pos * float(str(val).replace('-', '')[:4]) if 'e' not in str(val) else 0.0

def edge(v):
    return v is not None and (int(str(abs(v))[4]) >= jump_big or int(str(abs(v))[4]) <= jump_small)

def edge_single(v):
    return -1 if v is None else int(str(abs(v))[4])

def edge_more(v):
    return -1 if v is None else int(str(abs(v))[4:8])

def cut_by_boundary(seq, seq_gap, gap_val):
    pos_boundary_left = -1
    pos_boundary_right = -1
    big = max(seq_gap) >= 0.015
    small = min(seq_gap) <= -0.015
    eps = 0.0
    if big:
        eps = 0.0001
    elif small:
        eps = -0.0001
    for i in range(len(seq)):
        if fmt(seq_gap[i] + eps) == gap_val:
            if pos_boundary_left == -1:
                pos_boundary_left = i
        if pos_boundary_left > -1 and pos_boundary_right == -1 and fmt(seq_gap[i] + eps) != gap_val:
            pos_boundary_right = i
    if pos_boundary_left == -1:
        pos_boundary_left = 0
    if pos_boundary_right == -1:
        pos_boundary_right = len(seq)
    return seq[pos_boundary_left:pos_boundary_right], seq_gap[pos_boundary_left:pos_boundary_right]


# seq_gap = [-0.0134,-0.0127,-0.0109,-0.0089,-0.0078,-0.0065,-0.0055,-0.0024]
# label = 4
# gap_stat = {
#     -0.05 : sum([1 if v <= -0.05 else 0 for v in seq_gap]),
#     -0.04 : sum([1 if v <= -0.04 else 0 for v in seq_gap]),
#     -0.03 : sum([1 if v <= -0.03 else 0 for v in seq_gap]),
#     -0.02 : sum([1 if v <= -0.02 else 0 for v in seq_gap]),
#     0.05 : sum([1 if v >= 0.05 else 0 for v in seq_gap]),
#     0.04 : sum([1 if v >= 0.04 else 0 for v in seq_gap]),
#     0.03 : sum([1 if v >= 0.03 else 0 for v in seq_gap]),
#     0.02 : sum([1 if v >= 0.02 else 0 for v in seq_gap]),
#     0.01 : sum([1 if v >= 0.01 and v < 0.015 else 0 for v in seq_gap]),
#     -0.01 : sum([1 if v > -0.015 and v <= -0.01 else 0 for v in seq_gap]),
# }
# seq = [i for i in range(len(seq_gap))]

grow_big = 0.0015
grow_small = 0.00015
jump_big = 6
jump_small = 2


def seq_merge(seq, seq_gap, label, flag):
    pos_single = None
    fv_dict = {}
    seq_gap_single = []
    for i in range(len(seq)):
        fv = "{:.6f}".format(seq_gap[i])[:(9 if seq_gap[i] >= 0 else 10)]
        if fv not in fv_dict:
            fv_dict[fv] = []
            seq_gap_single.append(fv)
        fv_dict[fv].append(seq[i])
    for i in range(len(seq_gap_single)):
        if label is not None and int(label) in fv_dict[seq_gap_single[i]]:
            pos_single = i
            break
    if len(seq_gap_single) == 2 and pos_single == 1:
        pos_single = -1
    return fv_dict, seq_gap_single, pos_single


def train(seq, seq_gap, gap_stat, label, debug=True):
    fv_dict, seq_gap_single, pos_single = seq_merge(seq, seq_gap, label, 'train')
    if debug:
        print('开始train')
    label = int(label)
    if len(set(seq)) != len(seq_gap):
        raise ValueError("invalid seq:", seq)
    pos = seq.index(label)
    big = min(seq_gap) >= 0.015
    small = max(seq_gap) <= -0.015
    bigNear = min(seq_gap) >= 0 and max(seq_gap) < 0.015
    smallNear = min(seq_gap) > -0.015 and max(seq_gap) < 0
    eps = 0.0
    if big:
        eps = 0.0001
    elif small:
        eps = -0.0001
    left_gap_val = None
    right_gap_val = None
    left_turn_val = None
    right_turn_val = None
    ref_left_gap_val = None
    ref_right_gap_val = None
    turn = False
    # if seq_gap[0] == seq_gap[-1] and len(seq) > 1:
    #     if debug:
    #         print('ALL吗')
    #     return 'ALL', {'all' : True}
    if len(seq_gap_single) == 1:
        if debug:
            print('SINGLE吗')
        return 'SINGLE', {
            'gap_stat_val' : fmt(seq_gap[pos]), 
            'single_val' :  seq_gap[pos] + ((grow_big if fmt(seq_gap[pos]) != 0 else grow_small) if big or bigNear else (-grow_big if fmt(seq_gap[pos]) != 0 else -grow_small)), 
            'single_opt' : ('<' if bigNear or big else '>'),
            'consecutive' : False
        }
    if len(seq_gap_single) == 2:
        if debug:
            print('PAIR吗', pos_single, seq)
        if fmt(seq_gap[0] + eps) != fmt(seq_gap[-1] + eps):
            return 'PAIR', {
                'gap_stat_val' : fmt(seq_gap[-1] + eps) if big or bigNear else fmt(seq_gap[0] + eps), 
                'pos' : pos_single,
                'current_consecutive' : False,
                'non_current_consecutive' : False
            }
        else:
            return 'PAIR', {
                'gap_stat_val' : fmt(seq_gap[0] + eps), 
                'left_val' : seq_gap[0] + (grow_big if fmt(seq_gap[0]) != 0 else grow_small),
                'right_val' : seq_gap[-1] - (grow_big if fmt(seq_gap[-1]) != 0 else grow_small),
                'pos' : pos_single,
                'left_consecutive' : False,
                'right_consecutive' : False
            }
    if pos - 1 > -1:
        no_gap = False
        for i in range(pos - 1, -1, -1):
            if abs(seq_gap[i] - seq_gap[pos]) < 0.0000001:
                turn = True
            elif fmt(seq_gap[i] + eps) != fmt(seq_gap[pos] + eps) and (not no_gap):
                left_gap_val = seq_gap[i] + eps
                if small:
                    ref_left_gap_val = float(fmt(seq_gap[i] + eps))
                elif big:
                    ref_left_gap_val = float(fmt(seq_gap[pos] + eps))
                else:
                    gap_val = -0.01 if smallNear else 0.01
                    if debug:
                        print('NEAR GAP LEFT')
                    return 'GAP', {
                        'gap_stat_val' : gap_val,
                        'mid_judge_over' : gap_stat[gap_val] >= len(seq) / 2,
                        'gap_and_consecutive' : {'pos' : 'gap_stat[' + str(gap_val) + ']' if smallNear else 'len(seq) - gap_stat[' + str(gap_val) + ']', 'left' : False}
                    }
                break
            else:
                if left_turn_val is None:
                    left_turn_val = seq_gap[i]
                no_gap = True
                break
    if pos + 1 < len(seq):
        no_gap = False
        for i in range(pos + 1, len(seq)):
            if abs(seq_gap[i] - seq_gap[pos]) < 0.0000001:
                turn = True
            elif fmt(seq_gap[i] + eps) != fmt(seq_gap[pos] + eps) and (not no_gap):
                right_gap_val = seq_gap[i] + eps
                if small:
                    ref_right_gap_val = float(fmt(seq_gap[pos] + eps))
                elif big:
                    ref_right_gap_val = float(fmt(seq_gap[i] + eps))
                else:
                    gap_val =  -0.01 if smallNear else 0.01
                    if debug:
                        print('NEAR GAP RIGHT')
                    return 'GAP', {
                        'gap_stat_val' : gap_val,
                        'mid_judge_over' : gap_stat[gap_val] >= len(seq) / 2,
                        'gap_and_consecutive' : {'pos' : 'gap_stat[' + str(gap_val) + '] - 1' if smallNear else 'len(seq) - gap_stat[' + str(gap_val) + '] - 1', 'left' : True}
                    }
                break
            else:
                if right_turn_val is None:
                    right_turn_val = seq_gap[i]
                no_gap = True
                break
    if not turn:
        right_turn_val = None
        left_turn_val = None
    rst = {
            'gap_stat_val' : None,
            'mid_judge_over' : None,
            'gap_and_consecutive' : None
        }
    if left_gap_val is not None or right_gap_val is not None:
        if edge(left_gap_val) and edge(right_gap_val):
            if edge_single(left_gap_val) >= jump_big and edge_more(left_gap_val) >= edge_more(right_gap_val) or edge_single(left_gap_val) <= jump_small and edge_more(left_gap_val) <= edge_more(right_gap_val):
                rst['gap_stat_val'] = ref_left_gap_val
                rst['gap_and_consecutive'] = {'pos' : 'gap_stat[' + str(rst['gap_stat_val']) + ']' if small else 'len(seq)-gap_stat[' + str(rst['gap_stat_val']) + ']', 'left' : False}
            else:
                rst['gap_stat_val'] = ref_right_gap_val
                rst['gap_and_consecutive'] = {'pos' : 'len(seq)-gap_stat[' + str(rst['gap_stat_val']) + '] - 1' if big else 'gap_stat[' + str(rst['gap_stat_val']) + '] - 1', 'left' : True}
        elif edge(left_gap_val):
            rst['gap_stat_val'] = ref_left_gap_val
            rst['gap_and_consecutive'] = {'pos' : 'gap_stat[' + str(rst['gap_stat_val']) + ']' if small else 'len(seq)-gap_stat[' + str(rst['gap_stat_val']) + ']', 'left' : False}
        elif edge(right_gap_val):
            rst['gap_stat_val'] = ref_right_gap_val
            rst['gap_and_consecutive'] = {'pos' : 'len(seq)-gap_stat[' + str(rst['gap_stat_val']) + '] - 1' if big else 'gap_stat[' + str(rst['gap_stat_val']) + '] - 1', 'left' : True}
        elif right_gap_val is None:
            rst['gap_stat_val'] = ref_left_gap_val
            rst['gap_and_consecutive'] = {'pos' : 'gap_stat[' + str(rst['gap_stat_val']) + ']' if small else 'len(seq)-gap_stat[' + str(rst['gap_stat_val']) + ']', 'left' : False}
        elif left_gap_val is None:
            rst['gap_stat_val'] = ref_right_gap_val
            rst['gap_and_consecutive'] = {'pos' : 'len(seq)-gap_stat[' + str(rst['gap_stat_val']) + '] - 1' if big else 'gap_stat[' + str(rst['gap_stat_val']) + '] - 1', 'left' : True}
        elif abs(left_gap_val - seq_gap[pos]) >= abs(right_gap_val - seq_gap[pos]):
            rst['gap_stat_val'] = ref_left_gap_val
            rst['gap_and_consecutive'] = {'pos' : 'gap_stat[' + str(rst['gap_stat_val']) + ']' if small else 'len(seq)-gap_stat[' + str(rst['gap_stat_val']) + ']', 'left' : False}
        else:
            rst['gap_stat_val'] = ref_right_gap_val
            rst['gap_and_consecutive'] = {'pos' : 'len(seq)-gap_stat[' + str(rst['gap_stat_val']) + '] - 1' if big else 'gap_stat[' + str(rst['gap_stat_val']) + '] - 1', 'left' : True}
        rst['mid_judge_over'] = gap_stat[rst['gap_stat_val']] >= len(seq) / 2
        if debug:
            print('GAP吗')
        return 'GAP', rst
    # rst = {
    #     'gap_stat_val' : float(fmt(seq_gap[pos])),
    #     'find_turn' : None
    # }
    # new_seq, new_seq_gap = cut_by_boundary(seq, seq_gap, rst['gap_stat_val'])
    # if left_turn_val is not None or right_turn_val is not None:
    #     if edge(left_turn_val) and edge(right_turn_val):
    #         if edge_single(left_gap_val) >= jump_big and edge_more(left_gap_val) >= edge_more(right_gap_val) or edge_single(left_gap_val) <= jump_small and edge_more(left_gap_val) <= edge_more(right_gap_val):
    #             rst['find_turn'] = {'consecutive_at_left' : False, 'choose_single' : False}
    #         else:
    #             rst['find_turn'] = {'consecutive_at_left' : True, 'choose_single' : False}
    #     elif edge(left_turn_val):
    #         rst['find_turn'] = {'consecutive_at_left' : False, 'choose_single' : False}
    #     elif edge(right_turn_val):
    #         rst['find_turn'] = {'consecutive_at_left' : True, 'choose_single' : False}
    #     elif right_turn_val is None:
    #         rst['find_turn'] = {'consecutive_at_left' : False, 'choose_single' : False}
    #     elif left_turn_val is None:
    #         rst['find_turn'] = {'consecutive_at_left' : True, 'choose_single' : False}
    #     elif abs(left_turn_val - seq_gap[pos]) >= abs(right_turn_val - seq_gap[pos]):
    #         rst['find_turn'] = {'consecutive_at_left' : False, 'choose_single' : False}
    #     else:
    #         rst['find_turn'] = {'consecutive_at_left' : True, 'choose_single' : False}
    #     if debug:
    #         print('第一次TURN吗', rst)
    #     rst['find_turn']['reverse'] = (new_seq.index(label) + 1) * 1.0 / len(new_seq) > 0.5
    #     return 'TURN', rst
    # edge_label_left = None
    # edge_label_right = None
    # edge_label = None
    # if pos - 1 > -1 and pos - 2 > -1:
    #     if abs(seq_gap[pos - 1] - seq_gap[pos - 2]) < 0.0000001:
    #         left_turn_val = seq_gap[pos - 1]
    #         for z in range(pos - 2, -1, -1):
    #             if abs(seq_gap[pos - 1] - seq_gap[z]) < 0.0000001:
    #                 edge_label_left = seq[z]
    # if pos + 1 < len(seq) and pos + 2 < len(seq):
    #     if abs(seq_gap[pos + 1] - seq_gap[pos + 2]) < 0.0000001:
    #         right_turn_val = seq_gap[pos + 1]
    #         for z in range(pos + 2, len(seq)):
    #             if abs(seq_gap[z] - seq_gap[pos + 1]) < 0.0000001:
    #                 edge_label_right = seq[z]
    # if left_turn_val is not None or right_turn_val is not None:
    #     if edge(left_turn_val) and edge(right_turn_val):
    #         if edge_single(left_gap_val) >= jump_big and edge_more(left_gap_val) >= edge_more(right_gap_val) or edge_single(left_gap_val) <= jump_small and edge_more(left_gap_val) <= edge_more(right_gap_val):
    #             rst['find_turn'] = {'consecutive_at_left' : True, 'choose_single' : True}
    #             edge_label = edge_label_left
    #         else:
    #             rst['find_turn'] = {'consecutive_at_left' : False, 'choose_single' : True}
    #             edge_label = edge_label_right
    #     elif edge(left_turn_val):
    #         rst['find_turn'] = {'consecutive_at_left' : True, 'choose_single' : True}
    #         edge_label = edge_label_left
    #     elif edge(right_turn_val):
    #         rst['find_turn'] = {'consecutive_at_left' : False, 'choose_single' : True}
    #         edge_label = edge_label_right
    #     elif right_turn_val is None:
    #         rst['find_turn'] = {'consecutive_at_left' : True, 'choose_single' : True}
    #         edge_label = edge_label_left
    #     elif left_turn_val is None:
    #         rst['find_turn'] = {'consecutive_at_left' : False, 'choose_single' : True}
    #         edge_label = edge_label_right
    #     elif abs(left_turn_val - seq_gap[pos]) >= abs(right_turn_val - seq_gap[pos]):
    #         rst['find_turn'] = {'consecutive_at_left' : True, 'choose_single' : True}
    #         edge_label = edge_label_left
    #     else:
    #         rst['find_turn'] = {'consecutive_at_left' : False, 'choose_single' : True}
    #         edge_label = edge_label_right
    #     if debug:
    #         print('第二次TURN吗', left_turn_val, right_turn_val, new_seq.index(edge_label), len(new_seq))
    #     rst['find_turn']['reverse'] = (new_seq.index(label)) * 1.0 / len(new_seq) > 0.5
    #     return 'TURN', rst
    rst = {
        'gap_stat_val' : None,
        'skip_pos' : None,
        'shift' : None,
        'skip_val' : None,
        'mid_judge_over' : None,
        'pos_1_consecutive' : False,
        'pos_2_consecutive' : False
    }
    pos_1 = None
    pos_2 = None
    for i in range(pos - 1, -1, -1):
        if abs(seq_gap[i] - seq_gap[pos]) < 0.0000001:
            pass
        elif fmt(seq_gap[i] + eps) == fmt(seq_gap[pos] + eps):
            pos_1 = i
            break
    if pos_1 is not None:
        for i in range(pos_1 -1, -1, -1):
            if abs(seq_gap[i] - seq_gap[pos_1]) < 0.0000001:
                pass
            elif fmt(seq_gap[i] + eps) == fmt(seq_gap[pos_1] + eps):
                break
            elif fmt(seq_gap[i] + eps) != fmt(seq_gap[pos_1] + eps):
                pos_2 = i
                break
    if pos_1 is not None and pos_2 is not None:
        if edge_single(seq_gap[pos_1] + eps) >= jump_big or edge_single(seq_gap[pos_1] + eps) <= jump_small:
            rst['shift'] = 1
            rst['skip_val'] = seq_gap[pos_1]
            rst['opt'] = '<'
            # >= jump_big
            if small or smallNear:
                rst['gap_stat_val'] = fmt(seq_gap[pos_2] + eps)
                rst['skip_pos'] = 'gap_stat[' + str(rst['gap_stat_val']) + ']'
            # <= jump_small
            elif big or bigNear:
                rst['gap_stat_val'] = fmt(seq_gap[pos_1] + eps)
                rst['skip_pos'] = 'len(seq)-gap_stat[' + str(rst['gap_stat_val']) + ']'
            rst['mid_judge_over'] = gap_stat[rst['gap_stat_val']] * 1.0 / len(seq) >= 0.5
    # if pos - 2 > -1 and fmt(seq_gap[pos - 2] + eps) != fmt(seq_gap[pos] + eps):
    #     if edge_single(seq_gap[pos - 1] + eps) >= jump_big or edge_single(seq_gap[pos - 1] + eps) <= jump_small:
    #         rst['shift'] = 1
    #         rst['skip_val'] = seq_gap[pos - 1]
    #         rst['opt'] = '<'
    #         # >= jump_big
    #         if small or smallNear:
    #             rst['gap_stat_val'] = fmt(seq_gap[pos - 2] + eps)
    #             rst['skip_pos'] = 'gap_stat[' + str(rst['gap_stat_val']) + ']'
    #         # <= jump_small
    #         elif big or bigNear:
    #             rst['gap_stat_val'] = fmt(seq_gap[pos - 1] + eps)
    #             rst['skip_pos'] = 'len(seq)-gap_stat[' + str(rst['gap_stat_val']) + ']'
    #         rst['mid_judge_over'] = gap_stat[rst['gap_stat_val']] * 1.0 / len(seq) >= 0.5
    pos_1 = None
    pos_2 = None
    for i in range(pos + 1, len(seq)):
        if abs(seq_gap[i] - seq_gap[pos]) < 0.0000001:
            pass
        elif fmt(seq_gap[i] + eps) == fmt(seq_gap[pos] + eps):
            pos_1 = i
            break
    if pos_1 is not None:
        for i in range(pos_1 + 1, len(seq)):
            if abs(seq_gap[i] - seq_gap[pos_1]) < 0.0000001:
                pass
            elif fmt(seq_gap[i] + eps) == fmt(seq_gap[pos_1] + eps):
                break
            elif fmt(seq_gap[i] + eps) != fmt(seq_gap[pos_1] + eps):
                pos_2 = i
                break
    if pos_1 is not None and pos_2 is not None:
        if edge_single(seq_gap[pos_1] + eps) >= jump_big or edge_single(seq_gap[pos_1] + eps) <= jump_small:
            if rst['gap_stat_val'] is None or edge_single(seq_gap[pos_1]) >= jump_big and edge_single(rst['skip_val']) >= jump_big and edge_more(seq_gap[pos_1]) >= edge_more(rst['skip_val']) or edge_single(seq_gap[pos_1]) <= jump_small and edge_single(rst['skip_val']) <= jump_small and edge_more(seq_gap[pos_1]) <= edge_more(rst['skip_val']):
                rst['shift'] = -1
                rst['skip_val'] = seq_gap[pos_1]
                rst['opt'] = '>'
                # <= jump_small
                if small or smallNear:
                    rst['gap_stat_val'] = fmt(seq_gap[pos_1] + eps)
                    rst['skip_pos'] = 'gap_stat[' + str(rst['gap_stat_val']) + '] - 1'
                # >= jump_big
                elif big or bigNear:
                    rst['gap_stat_val'] = fmt(seq_gap[pos_2] + eps)
                    rst['skip_pos'] = 'len(seq)-gap_stat[' + str(rst['gap_stat_val']) + '] - 1'
                rst['mid_judge_over'] = gap_stat[rst['gap_stat_val']] * 1.0 / len(seq) >= 0.5
    # if pos + 2 < len(seq) and fmt(seq_gap[pos + 2] + eps) != fmt(seq_gap[pos] + eps):
    #     if edge_single(seq_gap[pos + 1] + eps) >= jump_big or edge_single(seq_gap[pos + 1] + eps) <= jump_small:
    #         if rst['gap_stat_val'] is None or edge_single(seq_gap[pos + 1]) >= jump_big and edge_single(rst['skip_val']) >= jump_big and edge_more(seq_gap[pos + 1]) >= edge_more(rst['skip_val']) or edge_single(seq_gap[pos + 1]) <= jump_small and edge_single(rst['skip_val']) <= jump_small and edge_more(seq_gap[pos + 1]) <= edge_more(rst['skip_val']):
    #             rst['shift'] = -1
    #             rst['skip_val'] = seq_gap[pos + 1]
    #             rst['opt'] = '>'
    #             # <= jump_small
    #             if small or smallNear:
    #                 rst['gap_stat_val'] = fmt(seq_gap[pos + 1] + eps)
    #                 rst['skip_pos'] = 'gap_stat[' + str(rst['gap_stat_val']) + '] - 1'
    #             # >= jump_big
    #             elif big or bigNear:
    #                 rst['gap_stat_val'] = fmt(seq_gap[pos + 2] + eps)
    #                 rst['skip_pos'] = 'len(seq)-gap_stat[' + str(rst['gap_stat_val']) + '] - 1'
    #             rst['mid_judge_over'] = gap_stat[rst['gap_stat_val']] * 1.0 / len(seq) >= 0.5
    if rst['gap_stat_val'] is not None:
        if rst['opt'] == '<':
            rst['skip_val'] = rst['skip_val'] + (grow_small if fmt(rst['skip_val']) == 0 else grow_big)
        else:
            rst['skip_val'] = rst['skip_val'] - (grow_small if fmt(rst['skip_val']) == 0 else grow_big)
        if debug:
            print('SKIP吗')
        return 'SKIP', rst
    rst = {
        'gap_stat_val' : fmt(seq_gap[pos]),
        'end_point' : None,
        'mid_judge_over' : 'equal',
        'end_point_consecutive' : False,
        'non_end_point_consecutive' : False
    }
    if pos_single == 0:
        rst['end_point'] = {'opt' : '<', 'val' : seq_gap[pos] + (grow_small if fmt(seq_gap[pos]) == 0 else grow_big), 'pos' : 0}
        if big or bigNear:
            for j in range(pos + 1, len(seq)):
                if fmt(seq_gap[j] + eps) != fmt(seq_gap[0] + eps):
                    rst['gap_stat_val'] = fmt(seq_gap[j] + eps)
                    rst['mid_judge_over'] = gap_stat[rst['gap_stat_val']] * 1.0 / len(seq) >= 0.5
                    break
        elif small or smallNear:
            rst['gap_stat_val'] = fmt(seq_gap[0])
            if rst['gap_stat_val'] != 0 and gap_stat[rst['gap_stat_val']] < len(seq):
                if fmt(seq_gap[0] + eps) != fmt(seq_gap[-1] + eps):
                    rst['mid_judge_over'] = gap_stat[rst['gap_stat_val']] * 1.0 / len(seq) >= 0.5 and gap_stat[rst['gap_stat_val']] < len(seq)
    elif pos_single == len(seq_gap_single) - 1:
        rst['end_point'] = {'opt' : '>', 'val' : seq_gap[pos] - (grow_small if fmt(seq_gap[pos]) == 0 else grow_big), 'pos' : -1}
        if big or bigNear:
            rst['gap_stat_val'] = fmt(seq_gap[-1])
            print('看一看', seq, seq_gap, pos, big, small, bigNear, smallNear, gap_stat)
            if rst['gap_stat_val'] != 0 and gap_stat[rst['gap_stat_val']] < len(seq):
                if fmt(seq_gap[0] + eps) != fmt(seq_gap[-1] + eps):
                    rst['mid_judge_over'] = gap_stat[rst['gap_stat_val']] * 1.0 / len(seq) >= 0.5 and gap_stat[rst['gap_stat_val']] < len(seq)
        elif small or smallNear:
            for j in range(pos - 1, -1, -1):
                if fmt(seq_gap[j] + eps) != fmt(seq_gap[-1] + eps):
                    rst['gap_stat_val'] = fmt(seq_gap[j] + eps)
                    rst['mid_judge_over'] = gap_stat[rst['gap_stat_val']] * 1.0 / len(seq) >= 0.5
                    break
    if rst['end_point'] is not None:
        if debug:
            print('ENDPOINT吗')
        return 'END_POINT', rst
    rst = {
        'gap_stat_val' : fmt(seq_gap[pos]),
        'mid_judge_over' : 'equal',
        'left_consecutive' : False,
        'right_consecutive' : False,
        'this_consecutive' : False
    }
    if debug:
        print('BETWEEN吗')
    for i in range(pos - 1, -1, -1):
        if abs(seq_gap[i] - seq_gap[pos]) < 0.0000001:
            pass
        elif fmt(seq_gap[i] + eps) == fmt(seq_gap[pos] + eps):
            rst['left_val'] = seq_gap[i] + (grow_big if fmt(seq_gap[pos]) != 0 else grow_small)
            break
    for i in range(pos + 1, len(seq)):
        if abs(seq_gap[i] - seq_gap[pos]) < 0.0000001:
            pass
        elif fmt(seq_gap[i] + eps) == fmt(seq_gap[pos] + eps):
            rst['right_val'] = seq_gap[i] - (grow_big if fmt(seq_gap[pos]) != 0 else grow_small)
            break
    if fmt(seq_gap[0] + eps) != fmt(seq_gap[-1] + eps):
        if rst['gap_stat_val'] not in gap_stat:
            if rst['gap_stat_val'] == 0:
                if bigNear:
                    rst['mid_judge_over'] = gap_stat[0.01] * 1.0 / len(seq) >= 0.5 and gap_stat[0.01] < len(seq)
                else:
                    rst['mid_judge_over'] = gap_stat[-0.01] * 1.0 / len(seq) >= 0.5 and gap_stat[-0.01] < len(seq)
            # since rst['gap_stat_val'] not in gap_stat and rst['gap_stat_val'] is greater than 0, so must be big
            elif rst['gap_stat_val'] == 0.01:
                rst['mid_judge_over'] = gap_stat[0.02] * 1.0 / len(seq) >= 0.5 and gap_stat[0.01] < len(seq)
            # since rst['gap_stat_val'] not in gap_stat and rst['gap_stat_val'] is less than 0, so must be small
            elif rst['gap_stat_val'] == -0.01:
                rst['mid_judge_over'] = gap_stat[-0.02] * 1.0 / len(seq) >= 0.5 and gap_stat[-0.01] < len(seq)
            else:
                raise ValueError('mid_judge_over value error', rst['gap_stat_val'])
        elif fmt(seq_gap[0] + eps) == rst['gap_stat_val'] and big:
            rst['mid_judge_over'] = 'big_equal'
        elif fmt(seq_gap[-1] + eps) == rst['gap_stat_val'] and small:
            rst['mid_judge_over'] = 'small_equal'
        else:
            rst['mid_judge_over'] = gap_stat[rst['gap_stat_val']] * 1.0 / len(seq) >= 0.5 and gap_stat[rst['gap_stat_val']] < len(seq)
    if 'left_val' in rst and 'right_val' in rst:
        return 'BETWEEN', rst
    # if pos - 1 > -1 and pos + 1 < len(seq):
    #     if debug:
    #         print('BETWEEN吗')
    #     return 'BETWEEN', {
    #         'gap_stat_val' : fmt(seq_gap[pos]),
    #         'left_val' : seq_gap[pos - 1] + (grow_big if fmt(seq_gap[pos]) != 0 else grow_small),
    #         'right_val' : seq_gap[pos + 1] - (grow_big if fmt(seq_gap[pos]) != 0 else grow_small)
    #     }
    if debug:
        print('什么都没有吗')
    raise ValueError('train type not cover!', seq, seq_gap, label)

def predict(
        arr,
        seq, 
        seq_gap,
        gap_stat,
        config_arr,
        config_type,
        debug=True
    ):
    if len(seq) == 0:
        return
    fv_dict, seq_gap_single, pos_single = seq_merge(seq, seq_gap, None, 'predict')
    big = min(seq_gap) >= 0.015
    small = max(seq_gap) <= -0.015
    bigNear = min(seq_gap) >= 0 and max(seq_gap) < 0.015
    smallNear = min(seq_gap) > -0.015 and max(seq_gap) < 0
    eps = 0.0
    if big:
        eps = 0.0001
    elif small:
        eps = -0.0001
    if config_type == 'SINGLE':
        if len(seq_gap_single) == 1:
            for config in config_arr:
                if eval("seq_gap[0] " + config['single_opt'] + " " + str(config['single_val'])):
                    for v in seq:
                        arr.add(v)
    elif config_type == 'PAIR':
        if len(seq_gap_single) == 2:
            for config in config_arr:
                if fmt(seq_gap[0] + eps) != fmt(seq_gap[-1] + eps):
                    if 'pos' in config and 'left_val' not in config:
                        if gap_stat[config['gap_stat_val']] >= 1:
                            if config['pos'] == 0:
                                for i in range(len(seq)):
                                    if abs(seq_gap[i] - seq_gap[0]) < 0.0000001:
                                        arr.add(seq[i])
                            elif config['pos'] == -1:
                                for i in range(len(seq) - 1, -1, -1):
                                    if abs(seq_gap[i] - seq_gap[-1]) < 0.0000001:
                                        arr.add(seq[i])
                            else:
                                raise ValueError('pair pos not valid!', config['pos'])
                            # arr.add(int(seq[config['pos']]))
                else:
                    if 'left_val' in config:
                        if seq_gap[0] <= config['left_val'] and seq_gap[-1] >= config['right_val']:
                            if config['pos'] == 0:
                                for i in range(len(seq)):
                                    if abs(seq_gap[i] - seq_gap[0]) < 0.0000001:
                                        arr.add(seq[i])
                            elif config['pos'] == -1:
                                for i in range(len(seq) - 1, -1, -1):
                                    if abs(seq_gap[i] - seq_gap[-1]) < 0.0000001:
                                        arr.add(seq[i])
                            else:
                                raise ValueError('pair pos not valid!', config['pos'])
                            #arr.add(int(seq[config['pos']]))
    elif config_type == 'GAP':
        for config in config_arr:
            if midJudge(seq, gap_stat, config['gap_stat_val'], config['mid_judge_over']):
                pos = eval(config['gap_and_consecutive']['pos'])
                gapAndConsecutive(arr, seq, seq_gap, pos, left=config['gap_and_consecutive']['left'])
    # elif config_type == 'TURN':
    #     for config in config_arr:
    #         if ((config['gap_stat_val'] == 0 and (bigNear or smallNear)) or config['gap_stat_val'] in gap_stat or (small or big) and abs(config['gap_stat_val']) == 0.01):
    #             new_seq, new_seq_gap = cut_by_boundary(seq, seq_gap, config['gap_stat_val'])
    #             if len(new_seq) > 2:
    #                 findTurn(arr,
    #                     new_seq, 
    #                     new_seq_gap, 
    #                     approach_threshold=0.0001, 
    #                     gap_threshold=0.01,
    #                     reverse=config['find_turn']['reverse'], 
    #                     consecutive_at_left=config['find_turn']['consecutive_at_left'], 
    #                     choose_single=config['find_turn']['choose_single']
    #                 )
    elif config_type == 'SKIP':
        for config in config_arr:
            if midJudge(seq, gap_stat, config['gap_stat_val'], config['mid_judge_over']):
                pos = eval(config['skip_pos'])
                if eval('seq_gap[pos] ' + config['opt'] + ' ' + str(config['skip_val'])):
                    if config['shift'] == -1:
                        for i in range(pos - 1, -1, -1):
                            if fmt(seq_gap[i] + eps) == fmt(seq_gap[pos] + eps) and abs(seq_gap[i] - seq_gap[pos]) >= 0.0000001:
                                arr.add(int(seq[i]))
                                for ii in range(i - 1, -1, -1):
                                    if abs(seq_gap[ii] - seq_gap[i]) < 0.0000001:
                                        arr.add(int(seq[ii]))
                                break
                    elif config['shift'] == 1:
                        for i in range(pos + 1, len(seq)):
                            if fmt(seq_gap[i] + eps) == fmt(seq_gap[pos] + eps) and abs(seq_gap[i] - seq_gap[pos]) >= 0.0000001:
                                arr.add(int(seq[i]))
                                for ii in range(i + 1, len(seq)):
                                    if abs(seq_gap[ii] - seq_gap[i]) < 0.0000001:
                                        arr.add(int(seq[ii]))
                                break
                    else:
                        raise ValueError('skip shift not valid!', config['shift'])
                    # if pos + config['shift'] > -1 and pos + config['shift'] < len(seq):
                    #     arr.add(int(seq[pos + config['shift']]))
    elif config_type == 'END_POINT':
        for config in config_arr:
            cond_a = ((config['gap_stat_val'] == 0 and (bigNear or smallNear)) or config['gap_stat_val'] in gap_stat or (small or big) and abs(config['gap_stat_val']) == 0.01) and config['mid_judge_over'] == 'equal' and fmt(seq_gap[0] + eps) == fmt(seq_gap[-1] + eps)
            cond_b = config['gap_stat_val'] in gap_stat and midJudge(seq, gap_stat, config['gap_stat_val'], config['mid_judge_over'])
            if cond_a or cond_b:
                pos = config['end_point']['pos']
                if eval('seq_gap[pos] ' + config['end_point']['opt'] + ' ' + str(config['end_point']['val'])):
                    # arr.add(int(seq[pos]))
                    if pos == 0:
                        for i in range(len(seq)):
                            if abs(seq_gap[i] - seq_gap[0]) < 0.0000001:
                                arr.add(seq[i])
                    elif pos == -1:
                        for i in range(len(seq) - 1, -1, -1):
                            if abs(seq_gap[i] - seq_gap[-1]) < 0.0000001:
                                arr.add(seq[i])
                    else:
                        raise ValueError('endpint pos not valid!', pos)
    elif config_type == 'BETWEEN':
        left_valid = False
        right_valid = False
        if len(seq_gap_single) > 2:
            for config in config_arr:
                cond_a = ((config['gap_stat_val'] == 0 and (bigNear or smallNear)) or config['gap_stat_val'] in gap_stat or (small or big) and abs(config['gap_stat_val']) == 0.01) and config['mid_judge_over'] == 'equal' and fmt(seq_gap[0] + eps) == fmt(seq_gap[-1] + eps)
                cond_b = config['gap_stat_val'] in gap_stat and midJudge(seq, gap_stat, config['gap_stat_val'], config['mid_judge_over'])
                cond_c = config['gap_stat_val'] == 0 and bigNear and midJudge(seq, gap_stat, 0.01, config['mid_judge_over'])
                cond_d = config['gap_stat_val'] == 0 and smallNear and midJudge(seq, gap_stat, -0.01, config['mid_judge_over'])
                cond_e = config['gap_stat_val'] == 0.01 and big and midJudge(seq, gap_stat, 0.02, config['mid_judge_over'])
                cond_f = config['gap_stat_val'] == -0.01 and small and midJudge(seq, gap_stat, -0.02, config['mid_judge_over'])
                cond_g = config['gap_stat_val'] == fmt(seq_gap[0] + eps) and config['mid_judge_over'] == 'big_equal' and big and fmt(seq_gap[0] + eps) != fmt(seq_gap[-1] + eps)
                cond_h = config['gap_stat_val'] == fmt(seq_gap[-1] + eps) and config['mid_judge_over'] == 'small_equal' and small and fmt(seq_gap[0] + eps) != fmt(seq_gap[-1] + eps)
                if cond_a or cond_b or cond_c or cond_d or cond_e or cond_f or cond_g or cond_h:
                    for p in range(len(seq)):
                        if fmt(seq_gap[p]) == config['gap_stat_val']:
                            left_valid = False
                            right_valid = False
                            seq_cand = [seq[p]]
                            for l in range(p - 1, -1, -1):
                                if fmt(seq_gap[l] + eps) == fmt(seq_gap[p] + eps):
                                    if abs(seq_gap[l] - seq_gap[p]) < 0.0000001:
                                        seq_cand.append(seq[l])
                                    elif abs(seq_gap[l] - seq_gap[p]) >= 0.0000001 and seq_gap[l] <= config['left_val']:
                                        left_valid = True
                                        break
                            for r in range(p + 1, len(seq)):
                                if fmt(seq_gap[r] + eps) == fmt(seq_gap[p] + eps):
                                    if abs(seq_gap[r] - seq_gap[p]) < 0.0000001:
                                        seq_cand.append(seq[r])
                                    elif abs(seq_gap[r] - seq_gap[p]) >= 0.0000001 and seq_gap[r] >= config['right_val']:
                                        right_valid = True
                                        break
                            if left_valid and right_valid:
                                for v in seq_cand:
                                    arr.add(int(v))
                                # break
                        # if p - 1 > -1 and p + 1 < len(seq) and fmt(seq_gap[p]) == config['gap_stat_val'] and seq_gap[p-1] <= config['left_val'] and seq_gap[p+1] >= config['right_val']:
                        #     arr.add(int(seq[p]))
                        #     break
    # elif config_type == 'ALL':
    #     if len(seq) > 1:
    #         if seq_gap[0] == seq_gap[-1]:
    #             for v in seq:
    #                 arr.add(int(v))
    else:
        raise ValueError('config type not valid!', config_type)


def range_confirm(big_tmp, small_tmp, big_near_tmp, small_near_tmp, label, label_pos):
    diff = -1 if label_pos < 6 else -2
    label = int(label)
    if label in big_tmp:
        condition_arr = [
            'len(big_tmp) >= len(small_tmp) and len(big_tmp) >= len(small_near_tmp)',
            'len(big_tmp) - len(small_tmp) >= %s and len(big_tmp) - len(small_near_tmp) >= %s' % (diff, diff),
            'len(big_tmp) >= len(small_tmp)',
            'len(big_tmp) >= len(small_near_tmp)',
            'len(big_tmp) - len(small_tmp) >= %s' % diff,
            'len(big_tmp) - len(small_near_tmp) >= %s' % diff
        ]
        for condition in condition_arr:
            if eval(condition):
                return condition
        return 'big_tmp'
    if label in small_tmp:
        condition_arr = [
            'len(small_tmp) >= len(big_tmp) and len(small_tmp) >= len(big_near_tmp)',
            'len(small_tmp) - len(big_tmp) >= %s and len(small_tmp) - len(big_near_tmp) >= %s' % (diff, diff),
            'len(small_tmp) >= len(big_tmp)',
            'len(small_tmp) >= len(big_near_tmp)',
            'len(small_tmp) - len(big_tmp) >= %s' % diff,
            'len(small_tmp) - len(big_near_tmp) >= %s' % diff
        ]
        for condition in condition_arr:
            if eval(condition):
                return condition
        return 'small_tmp'
    if label in big_near_tmp:
        condition_arr = [
            'len(big_near_tmp) >= len(small_tmp) and len(big_near_tmp) >= len(small_near_tmp)',
            'len(big_near_tmp) - len(small_tmp) >= %s and len(big_near_tmp) - len(small_near_tmp) >= %s' % (diff, diff),
            'len(big_near_tmp) >= len(small_tmp)',
            'len(big_near_tmp) >= len(small_near_tmp)',
            'len(big_near_tmp) - len(small_tmp) >= %s' % diff,
            'len(big_near_tmp) - len(small_near_tmp) >= %s' % diff
        ]
        for condition in condition_arr:
            if eval(condition):
                return condition
        return 'big_near_tmp'
    if label in small_near_tmp:
        condition_arr = [
            'len(small_near_tmp) >= len(big_tmp) and len(small_near_tmp) >= len(big_near_tmp)',
            'len(small_near_tmp) - len(big_tmp) >= %s and len(small_near_tmp) - len(big_near_tmp) >= %s' % (diff, diff),
            'len(small_near_tmp) >= len(big_tmp)',
            'len(small_near_tmp) >= len(big_near_tmp)',
            'len(small_near_tmp) - len(big_tmp) >= %s' % diff,
            'len(small_near_tmp) - len(big_near_tmp) >= %s' % diff
        ]
        for condition in condition_arr:
            if eval(condition):
                return condition
        return 'small_near_tmp'
    raise ValueError('invalid label:', label, big_tmp, small_tmp, big_near_tmp, small_near_tmp)


def train_and_predict(config, 
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
        gap_stat,
        near_gap_stat,
        arr,
        arr_copy,
        name,
        label,
        label_pos):
    hit = False
    if config_copy is not None and strategy_name in config_copy:
        for condition in config_copy[strategy_name]:
            if eval(condition):
                seq = condition.split(' ')[0].replace('len(', '').replace(')', '')
                seq_gap = '_'.join(seq.split('_')[:-1]) + '_gap_tmp'
                for config_type in config_copy[strategy_name][condition]:
                    predict(arr_copy,
                        eval(seq),
                        eval(seq_gap), 
                        near_gap_stat if 'near' in seq else gap_stat,
                        config_copy[strategy_name][condition][config_type],
                        config_type
                    )
    if strategy_name in config:
        for condition in config[strategy_name]:
            if eval(condition):
                seq = condition.split(' ')[0].replace('len(', '').replace(')', '')
                seq_gap = '_'.join(seq.split('_')[:-1]) + '_gap_tmp'
                for config_type in config[strategy_name][condition]:
                    predict(arr,
                        eval(seq),
                        eval(seq_gap), 
                        near_gap_stat if 'near' in seq else gap_stat,
                        config[strategy_name][condition][config_type],
                        config_type
                    )
                if label is not None and int(label) in arr:
                    hit = True
    else:
        config[strategy_name] = {}
    if not hit and label is not None:
        condition = range_confirm(big_tmp, small_tmp, big_near_tmp, small_near_tmp, label, label_pos)
        if condition not in config[strategy_name]:
            config[strategy_name][condition] = {}
        seq = condition.split(' ')[0].replace('len(', '').replace(')', '')
        seq_gap = '_'.join(seq.split('_')[:-1]) + '_gap_tmp'
        config_type, rule = train(
            eval(seq), 
            eval(seq_gap), 
            near_gap_stat if 'near' in seq else gap_stat, 
            label)
        if config_type not in config[strategy_name][condition]:
            config[strategy_name][condition][config_type] = []
        merge_rule(config[strategy_name][condition][config_type], config_type, rule)
        predict(arr,
            eval(seq),
            eval(seq_gap), 
            near_gap_stat if 'near' in seq else gap_stat,
            config[strategy_name][condition][config_type],
            config_type
        )
    return not hit


def merge_rule(rule_arr, rule_type, new_rule):
    grow = None
    if 'gap_stat_val' in new_rule:
        grow = grow_small if fmt(new_rule['gap_stat_val']) == 0 else grow_big
    merge_hit=False
    if rule_type == 'SINGLE':
        for old_rule in rule_arr:
            if old_rule['gap_stat_val'] == new_rule['gap_stat_val'] and old_rule['single_opt'] == new_rule['single_opt']:
                if abs(new_rule['single_val'] - old_rule['single_val']) <= grow:
                    merge_hit = True
                    if old_rule['single_opt'] == '<' and new_rule['single_val'] > old_rule['single_val']:
                        old_rule['single_val'] = new_rule['single_val']
                    if old_rule['single_opt'] == '>' and new_rule['single_val'] < old_rule['single_val']:
                        old_rule['single_val'] = new_rule['single_val']
    elif rule_type == 'PAIR' and 'right_val' in new_rule and 'left_val' in new_rule:
        for old_rule in rule_arr:
            if old_rule['pos'] == new_rule['pos']:
                if 'right_val' in old_rule and 'left_val' in old_rule and abs(old_rule['right_val'] - new_rule['right_val']) <= grow and abs(old_rule['left_val'] - new_rule['right_val']) <= grow:
                    merge_hit = True
                    old_rule['right_val'] = min(old_rule['right_val'], new_rule['right_val'])
                    old_rule['left_val'] = max(old_rule['left_val'], new_rule['left_val'])
    elif rule_type == 'SKIP':
        for old_rule in rule_arr:
            if old_rule['mid_judge_over'] == new_rule['mid_judge_over'] and old_rule['gap_stat_val'] == new_rule['gap_stat_val'] and old_rule['opt'] == new_rule['opt']:
                 if abs(new_rule['skip_val'] - old_rule['skip_val']) <= grow:
                    merge_hit = True
                    if old_rule['opt'] == '<' and new_rule['skip_val'] > old_rule['skip_val']:
                        old_rule['skip_val'] = new_rule['skip_val']
                    if old_rule['opt'] == '>' and new_rule['skip_val'] < old_rule['skip_val']:
                        old_rule['skip_val'] = new_rule['skip_val']
    elif rule_type == 'END_POINT':
        for old_rule in rule_arr:
            if old_rule['mid_judge_over'] == new_rule['mid_judge_over'] and old_rule['gap_stat_val'] == new_rule['gap_stat_val'] and old_rule['end_point']['opt'] == new_rule['end_point']['opt']:
                if abs(new_rule['end_point']['val'] - old_rule['end_point']['val']) <= grow:
                    merge_hit = True
                    if old_rule['end_point']['opt'] == '<' and new_rule['end_point']['val'] > old_rule['end_point']['val']:
                        old_rule['end_point']['val'] = new_rule['end_point']['val']
                    if old_rule['end_point']['opt'] == '>' and new_rule['end_point']['val'] < old_rule['end_point']['val']:
                        old_rule['end_point']['val'] = new_rule['end_point']['val']
    elif rule_type == 'BETWEEN':
        for old_rule in rule_arr:
            if old_rule['gap_stat_val'] == new_rule['gap_stat_val']:
                if abs(old_rule['right_val'] - new_rule['right_val']) <= grow and abs(old_rule['left_val'] - new_rule['right_val']) <= grow:
                    merge_hit = True
                    old_rule['right_val'] = min(old_rule['right_val'], new_rule['right_val'])
                    old_rule['left_val'] = max(old_rule['left_val'], new_rule['left_val'])
    if not merge_hit:
        rule_arr.append(new_rule)
