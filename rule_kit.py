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
    #print(avg_window, data_len, s, gapStat)


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

def edge_gt(v):
    if v is None:
        return False
    if abs(v) >= 0.01 and abs(v) < 0.015:
        jump_big = 3
    elif abs(v) >= 0.015 and abs(v) < 0.02:
        jump_big = 8
    else:
        jump_big = 6
    return int(str(abs(v))[4]) >= jump_big

def edge_lt(v):
    if v is None:
        return False
    if abs(v) >= 0.01 and abs(v) < 0.015:
        jump_small = 2
    elif abs(v) >= 0.015 and abs(v) < 0.02:
        jump_small = 6
    else:
        jump_small = 2
    return int(str(abs(v))[4]) <= jump_small

def edge_single(v):
    return -1 if v is None else int(str(abs(v))[4])

def edge_more(v):
    return -1 if v is None else int(str(abs(v))[4:8])

def refine_rst_gap_stat_val(rst, val):
    if val is not None and abs(val) < 0.01:
        rst['gap_stat_val'] = '+0' if val >= 0 else '-0'

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

grow_big = 0.0025
grow_small = 0.00025

# only for SINGLE and PAIR
def seq_merge(seq, seq_gap, label, flag):
    current_consecutive = False
    non_current_consecutive = False
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
    if len(seq_gap_single) == 2 and pos_single is not None:
        if pos_single == 1:
            pos_single = -1
        if len(fv_dict[seq_gap_single[pos_single]]) > 1:
            current_consecutive = True
        if len(fv_dict[seq_gap_single[1 + pos_single]]) > 1:
            non_current_consecutive = True
    if len(seq_gap_single) == 1 and pos_single is not None:
        if len(fv_dict[seq_gap_single[pos_single]]) > 1:
            current_consecutive = True
    return fv_dict, seq_gap_single, pos_single, current_consecutive, non_current_consecutive


def train(seq, seq_gap, gap_stat, label, data_len, avg_window, dt, debug=True):
    fv_dict, seq_gap_single, pos_single, current_consecutive, non_current_consecutive = seq_merge(seq, seq_gap, label, 'train')
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
    ref_left_gap_val = None
    ref_right_gap_val = None
    if len(seq_gap_single) == 1:
        if debug:
            print('SINGLE吗')
        return 'SINGLE', {
            'gap_stat_val' : fmt(seq_gap[pos]), 
            'single_val' :  seq_gap[pos] + ((grow_big if fmt(seq_gap[pos]) != 0 else grow_small) if big or bigNear else (-grow_big if fmt(seq_gap[pos]) != 0 else -grow_small)), 
            'single_opt' : ('<' if bigNear or big else '>'),
            'consecutive' : current_consecutive
        }
    if len(seq_gap_single) == 2:
        if debug:
            print('PAIR吗', pos_single, seq)
        if fmt(seq_gap[0] + eps) != fmt(seq_gap[-1] + eps):
            gap_stat_val = fmt(seq_gap[-1] + eps) if big or bigNear else fmt(seq_gap[0] + eps)
            if gap_stat_val == 0:
                gap_stat_val = '+0' if (big or bigNear) else '-0'
            return 'PAIR', {
                'gap_stat_val' : gap_stat_val, 
                'pos' : pos_single,
                'current_consecutive' : current_consecutive,
                'non_current_consecutive' : non_current_consecutive,
                'mid_judge_over' : gap_stat[gap_stat_val] >= len(seq) / 2.0
            }
        else:
            gap_stat_val = fmt(seq_gap[0] + eps)
            if gap_stat_val == 0:
                gap_stat_val = '+0' if (big or bigNear) else '-0'
            return 'PAIR', {
                'gap_stat_val' : gap_stat_val, 
                'left_val' : seq_gap[0] + (grow_big if fmt(seq_gap[0]) != 0 else grow_small),
                'right_val' : seq_gap[-1] - (grow_big if fmt(seq_gap[-1]) != 0 else grow_small),
                'pos' : pos_single,
                'current_consecutive' : current_consecutive,
                'non_current_consecutive' : non_current_consecutive
            }
    left_current_consecutive = False
    left_non_current_consecutive = False
    right_current_consecutive = False
    right_non_current_consecutive = False
    if pos - 1 > -1:
        no_gap = False
        for i in range(pos + 1, len(seq)):
            if abs(seq_gap[i] - seq_gap[pos]) < 0.0000001:
                left_current_consecutive = True
        for i in range(pos - 1, -1, -1):
            if abs(seq_gap[i] - seq_gap[pos]) < 0.0000001:
                left_current_consecutive = True
            elif fmt(seq_gap[i] + eps) != fmt(seq_gap[pos] + eps) and (not no_gap):
                for ii in range(i - 1, -1, -1):
                    if abs(seq_gap[ii] - seq_gap[i]) < 0.0000001:
                        left_non_current_consecutive = True
                        break
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
                        'gap_and_consecutive' : {'pos' : 'gap_stat[' + str(gap_val) + ']' if smallNear else 'len(seq) - gap_stat[' + str(gap_val) + ']', 'left' : False},
                        'current_consecutive' : left_current_consecutive,
                        'non_current_consecutive' : left_non_current_consecutive
                    }
                break
            else:
                no_gap = True
                break
    if pos + 1 < len(seq):
        no_gap = False
        for i in range(pos - 1, -1, -1):
            if abs(seq_gap[i] - seq_gap[pos]) < 0.0000001:
                right_current_consecutive = True
        for i in range(pos + 1, len(seq)):
            if abs(seq_gap[i] - seq_gap[pos]) < 0.0000001:
                 right_current_consecutive = True
            elif fmt(seq_gap[i] + eps) != fmt(seq_gap[pos] + eps) and (not no_gap):
                for ii in range(i + 1, len(seq)):
                    if abs(seq_gap[ii] - seq_gap[i]) < 0.0000001:
                        right_non_current_consecutive = True
                        break
                right_gap_val = seq_gap[i] + eps
                if small:
                    ref_right_gap_val = float(fmt(seq_gap[pos] + eps))
                elif big:
                    ref_right_gap_val = float(fmt(seq_gap[i] + eps))
                else:
                    gap_val = -0.01 if smallNear else 0.01
                    if debug:
                        print('NEAR GAP RIGHT')
                    return 'GAP', {
                        'gap_stat_val' : gap_val,
                        'mid_judge_over' : gap_stat[gap_val] >= len(seq) / 2,
                        'gap_and_consecutive' : {'pos' : 'gap_stat[' + str(gap_val) + '] - 1' if smallNear else 'len(seq) - gap_stat[' + str(gap_val) + '] - 1', 'left' : True},
                        'current_consecutive' : right_current_consecutive,
                        'non_current_consecutive' : right_non_current_consecutive
                    }
                break
            else:
                no_gap = True
                break
    rst = {
        'gap_stat_val' : None,
        'mid_judge_over' : None,
        'gap_and_consecutive' : None
    }
    if left_gap_val is not None or right_gap_val is not None:
        if (edge_gt(left_gap_val) or edge_lt(left_gap_val)) and (edge_gt(right_gap_val) or edge_lt(right_gap_val)):
            if edge_gt(left_gap_val) and edge_more(left_gap_val) >= edge_more(right_gap_val) or edge_lt(left_gap_val) and edge_more(left_gap_val) <= edge_more(right_gap_val):
                rst['current_consecutive'] = left_current_consecutive
                rst['non_current_consecutive'] = left_non_current_consecutive
                rst['gap_stat_val'] = ref_left_gap_val
                rst['gap_and_consecutive'] = {'pos' : 'gap_stat[' + str(rst['gap_stat_val']) + ']' if small else 'len(seq)-gap_stat[' + str(rst['gap_stat_val']) + ']', 'left' : False}
            else:
                rst['current_consecutive'] = right_current_consecutive
                rst['non_current_consecutive'] = right_non_current_consecutive
                rst['gap_stat_val'] = ref_right_gap_val
                rst['gap_and_consecutive'] = {'pos' : 'len(seq)-gap_stat[' + str(rst['gap_stat_val']) + '] - 1' if big else 'gap_stat[' + str(rst['gap_stat_val']) + '] - 1', 'left' : True}
        elif edge_gt(left_gap_val) or edge_lt(left_gap_val):
            rst['current_consecutive'] = left_current_consecutive
            rst['non_current_consecutive'] = left_non_current_consecutive
            rst['gap_stat_val'] = ref_left_gap_val
            rst['gap_and_consecutive'] = {'pos' : 'gap_stat[' + str(rst['gap_stat_val']) + ']' if small else 'len(seq)-gap_stat[' + str(rst['gap_stat_val']) + ']', 'left' : False}
        elif edge_gt(right_gap_val) or edge_lt(right_gap_val):
            rst['current_consecutive'] = right_current_consecutive
            rst['non_current_consecutive'] = right_non_current_consecutive
            rst['gap_stat_val'] = ref_right_gap_val
            rst['gap_and_consecutive'] = {'pos' : 'len(seq)-gap_stat[' + str(rst['gap_stat_val']) + '] - 1' if big else 'gap_stat[' + str(rst['gap_stat_val']) + '] - 1', 'left' : True}
        elif right_gap_val is None:
            rst['current_consecutive'] = left_current_consecutive
            rst['non_current_consecutive'] = left_non_current_consecutive
            rst['gap_stat_val'] = ref_left_gap_val
            rst['gap_and_consecutive'] = {'pos' : 'gap_stat[' + str(rst['gap_stat_val']) + ']' if small else 'len(seq)-gap_stat[' + str(rst['gap_stat_val']) + ']', 'left' : False}
        elif left_gap_val is None:
            rst['current_consecutive'] = right_current_consecutive
            rst['non_current_consecutive'] = right_non_current_consecutive
            rst['gap_stat_val'] = ref_right_gap_val
            rst['gap_and_consecutive'] = {'pos' : 'len(seq)-gap_stat[' + str(rst['gap_stat_val']) + '] - 1' if big else 'gap_stat[' + str(rst['gap_stat_val']) + '] - 1', 'left' : True}
        elif abs(left_gap_val - seq_gap[pos]) >= abs(right_gap_val - seq_gap[pos]):
            rst['current_consecutive'] = left_current_consecutive
            rst['non_current_consecutive'] = left_non_current_consecutive
            rst['gap_stat_val'] = ref_left_gap_val
            rst['gap_and_consecutive'] = {'pos' : 'gap_stat[' + str(rst['gap_stat_val']) + ']' if small else 'len(seq)-gap_stat[' + str(rst['gap_stat_val']) + ']', 'left' : False}
        else:
            rst['current_consecutive'] = right_current_consecutive
            rst['non_current_consecutive'] = right_non_current_consecutive
            rst['gap_stat_val'] = ref_right_gap_val
            rst['gap_and_consecutive'] = {'pos' : 'len(seq)-gap_stat[' + str(rst['gap_stat_val']) + '] - 1' if big else 'gap_stat[' + str(rst['gap_stat_val']) + '] - 1', 'left' : True}
        rst['mid_judge_over'] = gap_stat[rst['gap_stat_val']] >= len(seq) / 2.0
        if gap_stat[rst['gap_stat_val']] == len(seq):
            raise RuntimeError('gap_stat_val is invalid, gap_stat_val: {}, gap_stat: {}, seq: {}'.format(rst['gap_stat_val'], gap_stat, seq))
        if debug:
            print('GAP吗')
        return 'GAP', rst
    rst = {
        'gap_stat_val' : None,
        'skip_pos' : None,
        'shift' : None,
        'skip_val' : None,
        'mid_judge_over' : None,
        'value_consecutive' : False,
        'pos_1_consecutive' : False
    }
    pos_1 = None
    pos_2 = None
    pos_1_consecutive = False
    value_consecutive = False
    for i in range(pos - 1, -1, -1):
        if abs(seq_gap[i] - seq_gap[pos]) < 0.0000001:
            value_consecutive = True
        elif fmt(seq_gap[i] + eps) == fmt(seq_gap[pos] + eps):
            pos_1 = i
            break
    for i in range(pos + 1, len(seq)):
        if abs(seq_gap[i] - seq_gap[pos]) < 0.0000001:
             value_consecutive = True
             break
    if pos_1 is not None:
        for i in range(pos_1 -1, -1, -1):
            if abs(seq_gap[i] - seq_gap[pos_1]) < 0.0000001:
                pos_1_consecutive = True
            elif fmt(seq_gap[i] + eps) == fmt(seq_gap[pos_1] + eps):
                break
            elif fmt(seq_gap[i] + eps) != fmt(seq_gap[pos_1] + eps):
                pos_2 = i
                break
    if pos_1 is not None and pos_2 is not None:
        if edge_gt(seq_gap[pos_1] + eps) or edge_lt(seq_gap[pos_1] + eps):
            rst['pos_1_consecutive'] = pos_1_consecutive
            rst['value_consecutive'] = value_consecutive
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
            if gap_stat[rst['gap_stat_val']] == len(seq):
                raise RuntimeError('gap_stat_val is invalid, gap_stat_val: {}, gap_stat: {}, seq: {}'.format(rst['gap_stat_val'], gap_stat, seq))
    pos_1 = None
    pos_2 = None
    pos_1_consecutive = False
    value_consecutive = False
    for i in range(pos + 1, len(seq)):
        if abs(seq_gap[i] - seq_gap[pos]) < 0.0000001:
           value_consecutive = True
        elif fmt(seq_gap[i] + eps) == fmt(seq_gap[pos] + eps):
            pos_1 = i
            break
    for i in range(pos - 1, -1, -1):
        if abs(seq_gap[i] - seq_gap[pos]) < 0.0000001:
            value_consecutive = True
            break
    if pos_1 is not None:
        for i in range(pos_1 + 1, len(seq)):
            if abs(seq_gap[i] - seq_gap[pos_1]) < 0.0000001:
                pos_1_consecutive = True
            elif fmt(seq_gap[i] + eps) == fmt(seq_gap[pos_1] + eps):
                break
            elif fmt(seq_gap[i] + eps) != fmt(seq_gap[pos_1] + eps):
                pos_2 = i
                break
    if pos_1 is not None and pos_2 is not None:
        if edge_gt(seq_gap[pos_1] + eps) or edge_lt(seq_gap[pos_1] + eps):
            if rst['gap_stat_val'] is None or edge_gt(seq_gap[pos_1]) and edge_gt(rst['skip_val']) and edge_more(seq_gap[pos_1]) >= edge_more(rst['skip_val']) or edge_lt(seq_gap[pos_1]) and edge_lt(rst['skip_val']) and edge_more(seq_gap[pos_1]) <= edge_more(rst['skip_val']):
                rst['pos_1_consecutive'] = pos_1_consecutive
                rst['value_consecutive'] = value_consecutive
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
                if gap_stat[rst['gap_stat_val']] == len(seq):
                    raise RuntimeError('gap_stat_val is invalid, gap_stat_val: {}, gap_stat: {}, seq: {}'.format(rst['gap_stat_val'], gap_stat, seq))
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
    refine_rst_gap_stat_val(rst, seq_gap[pos])
    if pos_single == 0:
        rst['end_point'] = {'opt' : '<', 'val' : seq_gap[pos] + (grow_small if fmt(seq_gap[pos]) == 0 else grow_big), 'pos' : 0}
        if big or bigNear:
            for j in range(pos + 1, len(seq)):
                if fmt(seq_gap[j] + eps) != fmt(seq_gap[0] + eps):
                    rst['gap_stat_val'] = fmt(seq_gap[j] + eps)
                    rst['mid_judge_over'] = gap_stat[rst['gap_stat_val']] * 1.0 / len(seq) >= 0.5
                    break
        elif small or smallNear:
            if rst['gap_stat_val'] != 0 and gap_stat[rst['gap_stat_val']] < len(seq) and fmt(seq_gap[0] + eps) != fmt(seq_gap[-1] + eps):
                    rst['mid_judge_over'] = gap_stat[rst['gap_stat_val']] * 1.0 / len(seq) >= 0.5
    elif pos_single == len(seq_gap_single) - 1:
        rst['end_point'] = {'opt' : '>', 'val' : seq_gap[pos] - (grow_small if fmt(seq_gap[pos]) == 0 else grow_big), 'pos' : -1}
        if big or bigNear:
            if rst['gap_stat_val'] != 0 and gap_stat[rst['gap_stat_val']] < len(seq) and fmt(seq_gap[0] + eps) != fmt(seq_gap[-1] + eps):
                    rst['mid_judge_over'] = gap_stat[rst['gap_stat_val']] * 1.0 / len(seq) >= 0.5
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
        'gap' : 0,
        'left_consecutive' : False,
        'right_consecutive' : False,
        'this_consecutive' : False
    }
    refine_rst_gap_stat_val(rst, seq_gap[pos])
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
        if fmt(seq_gap[pos]) == fmt(seq_gap[0]) and big:
            rst['gap_stat_val'] += 0.01
            rst['gap'] = -0.01
        elif fmt(seq_gap[pos]) == fmt(seq_gap[-1]) and small:
            rst['gap_stat_val'] -= 0.01
            rst['gap'] = 0.01
        rst['mid_judge_over'] = gap_stat[rst['gap_stat_val']] * 1.0 / len(seq) >= 0.5
        if data_len == 1495 and dt == '20260522':
            print('训练时', gap_stat[rst['gap_stat_val']], len(seq), rst['mid_judge_over'], rst)
    if 'left_val' in rst and 'right_val' in rst:
        return 'BETWEEN', rst
    if debug:
        print('什么都没有吗')
    raise ValueError('train type not cover!', seq, seq_gap, label)

def gap_stat_val_refine(config):
    if isinstance(config['gap_stat_val'], str):
        return config['gap_stat_val']
    else:
        return round(config['gap_stat_val'] + config['gap'], 2)

def predict(
        arr,
        seq, 
        seq_gap,
        gap_stat,
        config_arr,
        config_type,
        data_len,
        avg_window,
        dt,
        debug=True
    ):
    if len(seq) == 0:
        return
    fv_dict, seq_gap_single, pos_single, current_consecutive, non_current_consecutive = seq_merge(seq, seq_gap, None, 'predict')
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
                if eval("seq_gap[0] " + config['single_opt'] + " " + str(config['single_val'])) and (len(seq) == 1 and not config['consecutive'] or len(seq) > 1 and config['consecutive']):
                    for v in seq:
                        arr.add(v)
    elif config_type == 'PAIR':
        if len(seq_gap_single) == 2:
            for config in config_arr:
                head_consecutive = False
                tail_consecutive = False
                for i in range(1, len(seq)):
                    if abs(seq_gap[i] - seq_gap[0]) < 0.0000001:
                        head_consecutive = True
                for i in range(len(seq) - 2, -1, -1):
                    if abs(seq_gap[i] - seq_gap[-1]) < 0.0000001:
                        tail_consecutive = True
                if fmt(seq_gap[0] + eps) != fmt(seq_gap[-1] + eps):
                    if 'pos' in config and 'left_val' not in config:
                        if gap_stat[config['gap_stat_val']] > 0 and midJudge(seq, gap_stat, config['gap_stat_val'], config['mid_judge_over']):
                            if config['pos'] == 0:
                                current_cond = head_consecutive and config['current_consecutive'] or (not head_consecutive) and (not config['current_consecutive'])
                                non_current_cond = tail_consecutive and config['non_current_consecutive'] or (not tail_consecutive) and (not config['non_current_consecutive'])
                                if current_cond and non_current_cond:
                                    for i in range(len(seq)):
                                        if abs(seq_gap[i] - seq_gap[0]) < 0.0000001:
                                            arr.add(seq[i])
                            elif config['pos'] == -1:
                                current_cond = tail_consecutive and config['current_consecutive'] or (not tail_consecutive) and (not config['current_consecutive'])
                                non_current_cond = head_consecutive and config['non_current_consecutive'] or (not head_consecutive) and (not config['non_current_consecutive'])
                                if current_cond and non_current_cond:
                                    for i in range(len(seq) - 1, -1, -1):
                                        if abs(seq_gap[i] - seq_gap[-1]) < 0.0000001:
                                            arr.add(seq[i])
                            else:
                                raise ValueError('pair pos not valid!', config['pos'])
                else:
                    if 'left_val' in config:
                        if seq_gap[0] <= config['left_val'] and seq_gap[-1] >= config['right_val']:
                            if config['pos'] == 0:
                                current_cond = head_consecutive and config['current_consecutive'] or (not head_consecutive) and (not config['current_consecutive'])
                                non_current_cond = tail_consecutive and config['non_current_consecutive'] or (not tail_consecutive) and (not config['non_current_consecutive'])
                                if current_cond and non_current_cond:
                                    for i in range(len(seq)):
                                        if abs(seq_gap[i] - seq_gap[0]) < 0.0000001:
                                            arr.add(seq[i])
                            elif config['pos'] == -1:
                                current_cond = tail_consecutive and config['current_consecutive'] or (not tail_consecutive) and (not config['current_consecutive'])
                                non_current_cond = head_consecutive and config['non_current_consecutive'] or (not head_consecutive) and (not config['non_current_consecutive'])
                                if current_cond and non_current_cond:
                                    for i in range(len(seq) - 1, -1, -1):
                                        if abs(seq_gap[i] - seq_gap[-1]) < 0.0000001:
                                            arr.add(seq[i])
                            else:
                                raise ValueError('pair pos not valid!', config['pos'])
    elif config_type == 'GAP':
        for config in config_arr:
            if midJudge(seq, gap_stat, config['gap_stat_val'], config['mid_judge_over']):
                pos = eval(config['gap_and_consecutive']['pos'])
                gapAndConsecutive(arr, seq, seq_gap, pos, left=config['gap_and_consecutive']['left'])
    elif config_type == 'SKIP':
        for config in config_arr:
            if midJudge(seq, gap_stat, config['gap_stat_val'], config['mid_judge_over']):
                pos = eval(config['skip_pos'])
                if eval('seq_gap[pos] ' + config['opt'] + ' ' + str(config['skip_val'])):
                    pos_1_consecutive = False
                    value_consecutive = False
                    if config['shift'] == -1:
                        for i in range(pos - 1, -1, -1):
                            if fmt(seq_gap[i] + eps) == fmt(seq_gap[pos] + eps) and abs(seq_gap[i] - seq_gap[pos]) >= 0.0000001:
                                for ii in range(i - 1, -1, -1):
                                    if abs(seq_gap[ii] - seq_gap[i]) < 0.0000001:
                                        value_consecutive = True
                                break
                            elif abs(seq_gap[i] - seq_gap[pos]) < 0.0000001:
                                pos_1_consecutive = True
                        for i in range(pos - 1, -1, -1):
                            if fmt(seq_gap[i] + eps) == fmt(seq_gap[pos] + eps) and abs(seq_gap[i] - seq_gap[pos]) >= 0.0000001:
                                if value_consecutive == config['value_consecutive'] and pos_1_consecutive == config['pos_1_consecutive']:
                                    arr.add(int(seq[i]))
                                for ii in range(i - 1, -1, -1):
                                    if abs(seq_gap[ii] - seq_gap[i]) < 0.0000001:
                                        if value_consecutive == config['value_consecutive'] and pos_1_consecutive == config['pos_1_consecutive']:
                                            arr.add(int(seq[ii]))
                                break
                    elif config['shift'] == 1:
                        for i in range(pos + 1, len(seq)):
                            if fmt(seq_gap[i] + eps) == fmt(seq_gap[pos] + eps) and abs(seq_gap[i] - seq_gap[pos]) >= 0.0000001:
                                for ii in range(i + 1, len(seq)):
                                    if abs(seq_gap[ii] - seq_gap[i]) < 0.0000001:
                                        value_consecutive = True
                                break
                            elif abs(seq_gap[i] - seq_gap[pos]) < 0.0000001:
                                pos_1_consecutive = True
                        for i in range(pos + 1, len(seq)):
                            if fmt(seq_gap[i] + eps) == fmt(seq_gap[pos] + eps) and abs(seq_gap[i] - seq_gap[pos]) >= 0.0000001:
                                if value_consecutive == config['value_consecutive'] and pos_1_consecutive == config['pos_1_consecutive']:
                                    arr.add(int(seq[i]))
                                for ii in range(i + 1, len(seq)):
                                    if abs(seq_gap[ii] - seq_gap[i]) < 0.0000001:
                                        if value_consecutive == config['value_consecutive'] and pos_1_consecutive == config['pos_1_consecutive']:
                                            arr.add(int(seq[ii]))
                                break
                    else:
                        raise ValueError('skip shift not valid!', config['shift'])
    elif config_type == 'END_POINT':
        for config in config_arr:
            if config['gap_stat_val'] in gap_stat and (isinstance(config['mid_judge_over'], bool) and midJudge(seq, gap_stat, config['gap_stat_val'], config['mid_judge_over']) or config['mid_judge_over'] == 'equal'):
                pos = config['end_point']['pos']
                if eval('seq_gap[pos] ' + config['end_point']['opt'] + ' ' + str(config['end_point']['val'])):
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
                if config['gap_stat_val'] in gap_stat and (isinstance(config['mid_judge_over'], bool) and midJudge(seq, gap_stat, config['gap_stat_val'], config['mid_judge_over']) or config['mid_judge_over'] == 'equal'):
                    for p in range(len(seq)):
                        if data_len == 1495 and dt == '20260522' and p == 7:
                            print('这里吗看', seq_gap[p], gap_stat_val_refine(config), fmt(seq_gap[p]), config['gap_stat_val'], config['gap'])
                        if fmt(seq_gap[p]) == gap_stat_val_refine(config) or (fmt(seq_gap[p]) == 0 and (seq_gap[p] < 0 and config['gap_stat_val'] == '-0' or seq_gap[p] >= 0 and config['gap_stat_val'] == '+0')):
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
    else:
        raise ValueError('config type not valid!', config_type)


def range_confirm(big_tmp, small_tmp, big_near_tmp, small_near_tmp, label, label_pos):
    diff = -1 if label_pos < 6 else -2
    label = int(label)
    if label in big_tmp:
        condition_arr = [
            # 'len(big_tmp) >= len(small_tmp) and len(big_tmp) >= len(small_near_tmp)',
            'len(big_tmp) - len(small_tmp) >= %s and len(big_tmp) - len(small_near_tmp) >= %s' % (diff, diff),
            # 'len(big_tmp) >= len(small_tmp)',
            # 'len(big_tmp) >= len(small_near_tmp)',
            'len(big_tmp) - len(small_tmp) >= %s' % diff,
            'len(big_tmp) - len(small_near_tmp) >= %s' % diff
        ]
        for condition in condition_arr:
            if eval(condition):
                return condition
        return 'big_tmp'
    if label in small_tmp:
        condition_arr = [
            # 'len(small_tmp) >= len(big_tmp) and len(small_tmp) >= len(big_near_tmp)',
            'len(small_tmp) - len(big_tmp) >= %s and len(small_tmp) - len(big_near_tmp) >= %s' % (diff, diff),
            # 'len(small_tmp) >= len(big_tmp)',
            # 'len(small_tmp) >= len(big_near_tmp)',
            'len(small_tmp) - len(big_tmp) >= %s' % diff,
            'len(small_tmp) - len(big_near_tmp) >= %s' % diff
        ]
        for condition in condition_arr:
            if eval(condition):
                return condition
        return 'small_tmp'
    if label in big_near_tmp:
        condition_arr = [
            # 'len(big_near_tmp) >= len(small_tmp) and len(big_near_tmp) >= len(small_near_tmp)',
            'len(big_near_tmp) - len(small_tmp) >= %s and len(big_near_tmp) - len(small_near_tmp) >= %s' % (diff, diff),
            # 'len(big_near_tmp) >= len(small_tmp)',
            # 'len(big_near_tmp) >= len(small_near_tmp)',
            'len(big_near_tmp) - len(small_tmp) >= %s' % diff,
            'len(big_near_tmp) - len(small_near_tmp) >= %s' % diff
        ]
        for condition in condition_arr:
            if eval(condition):
                return condition
        return 'big_near_tmp'
    if label in small_near_tmp:
        condition_arr = [
            # 'len(small_near_tmp) >= len(big_tmp) and len(small_near_tmp) >= len(big_near_tmp)',
            'len(small_near_tmp) - len(big_tmp) >= %s and len(small_near_tmp) - len(big_near_tmp) >= %s' % (diff, diff),
            # 'len(small_near_tmp) >= len(big_tmp)',
            # 'len(small_near_tmp) >= len(big_near_tmp)',
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
        label_pos,
        data_len,
        avg_window,
        dt,
        debug=True):
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
                        config_type,
                        data_len,
                        avg_window,
                        dt
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
                        config_type,
                        data_len,
                        avg_window,
                        dt
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
            label,
            data_len,
            avg_window,
            dt,
            debug
        )
        if config_type not in config[strategy_name][condition]:
            config[strategy_name][condition][config_type] = []
        merge_rule(config[strategy_name][condition][config_type], config_type, rule)
        predict(arr,
            eval(seq),
            eval(seq_gap), 
            near_gap_stat if 'near' in seq else gap_stat,
            config[strategy_name][condition][config_type],
            config_type,
            data_len,
            avg_window,
            dt,
            debug
        )
    return not hit


def merge_rule(rule_arr, rule_type, new_rule):
    grow = None
    if 'gap_stat_val' in new_rule:
        grow = grow_small if new_rule['gap_stat_val'] in ('+0', '-0') else grow_big
    merge_hit=False
    if rule_type == 'SINGLE':
        for old_rule in rule_arr:
            if old_rule['gap_stat_val'] == new_rule['gap_stat_val'] and old_rule['single_opt'] == new_rule['single_opt'] and old_rule['consecutive'] == new_rule['consecutive']:
                if abs(new_rule['single_val'] - old_rule['single_val']) <= grow:
                    merge_hit = True
                    if old_rule['single_opt'] == '<' and new_rule['single_val'] > old_rule['single_val']:
                        old_rule['single_val'] = new_rule['single_val']
                    if old_rule['single_opt'] == '>' and new_rule['single_val'] < old_rule['single_val']:
                        old_rule['single_val'] = new_rule['single_val']
    elif rule_type == 'PAIR' and 'right_val' in new_rule and 'left_val' in new_rule:
        for old_rule in rule_arr:
            if old_rule['pos'] == new_rule['pos'] and old_rule['current_consecutive'] == new_rule['current_consecutive'] and old_rule['non_current_consecutive'] == new_rule['non_current_consecutive']:
                if 'right_val' in old_rule and 'left_val' in old_rule and abs(old_rule['right_val'] - new_rule['right_val']) <= grow and abs(old_rule['left_val'] - new_rule['right_val']) <= grow:
                    merge_hit = True
                    old_rule['right_val'] = min(old_rule['right_val'], new_rule['right_val'])
                    old_rule['left_val'] = max(old_rule['left_val'], new_rule['left_val'])
    elif rule_type == 'SKIP':
        for old_rule in rule_arr:
            if old_rule['mid_judge_over'] == new_rule['mid_judge_over'] and old_rule['gap_stat_val'] == new_rule['gap_stat_val'] and old_rule['opt'] == new_rule['opt'] and old_rule['pos_1_consecutive'] == new_rule['pos_1_consecutive'] and old_rule['value_consecutive'] == new_rule['value_consecutive']:
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
            if old_rule['gap_stat_val'] == new_rule['gap_stat_val'] and old_rule['mid_judge_over'] == new_rule['mid_judge_over'] and old_rule['gap'] == new_rule['gap']:
                if abs(old_rule['right_val'] - new_rule['right_val']) <= grow and abs(old_rule['left_val'] - new_rule['right_val']) <= grow:
                    merge_hit = True
                    old_rule['right_val'] = min(old_rule['right_val'], new_rule['right_val'])
                    old_rule['left_val'] = max(old_rule['left_val'], new_rule['left_val'])
    if not merge_hit:
        rule_arr.append(new_rule)
