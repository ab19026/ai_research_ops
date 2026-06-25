from rule_kit import *


def genKey(big_tmp, small_tmp, big_near_tmp, small_near_tmp, nearGapStat, gapStat, strategy_name):
    key = str(len(big_tmp)) + '_' + str(len(big_near_tmp)) + '_' + str(len(small_tmp)) + '_' + str(len(small_near_tmp))
    key += '_'
    key += str(gapStat[0.02]) + '_' + str(gapStat[0.03]) + '_' + str(gapStat[0.04]) + '_' + str(gapStat[0.05])
    key += '_'
    key += str(gapStat[-0.02]) + '_' + str(gapStat[-0.03]) + '_' + str(gapStat[-0.04]) + '_' + str(gapStat[-0.05])
    key += '_'
    key += str(nearGapStat[0.01])
    key += '_'
    key += str(nearGapStat[-0.01])
    key += '_' + strategy_name
    return key


def train(key, stat, big_tmp, small_tmp, big_near_tmp, small_near_tmp, true_label):
    # true_label = int(true_label)
    # if key not in stat:
    #     stat[key] = set()
    if true_label in big_tmp:
        stat[key].add('big:' + str(big_tmp.index(true_label)))
    elif true_label in small_tmp:
        stat[key].add('small:' + str(small_tmp.index(true_label)))
    elif true_label in big_near_tmp:
        stat[key].add('big_near:' + str(big_near_tmp.index(true_label)))
    elif true_label in small_near_tmp:
        stat[key].add('small_near:' + str(small_near_tmp.index(true_label)))


def predict(big_tmp, small_tmp, big_near_tmp, small_near_tmp, arr, key, stat):
    if key in stat:
        for v in stat[key]:
            vs = v.split(':')
            if vs[0] == 'big':
                arr.add(big_tmp[int(vs[1])])
            elif vs[0] == 'big_near':
                arr.add(big_near_tmp[int(vs[1])])
            elif vs[0] == 'small':
                arr.add(small_tmp[int(vs[1])])
            elif vs[0] == 'small_near':
                arr.add(small_near_tmp[int(vs[1])])


def processDetail(arr, stat, true_label, big_tmp, small_tmp, big_near_tmp, small_near_tmp, nearGapStat, gapStat, strategy_name, mode):
    key = genKey(big_tmp, small_tmp, big_near_tmp, small_near_tmp, nearGapStat, gapStat, strategy_name)
    if mode == 'PREDICT_SECOND':
        predict(big_tmp, small_tmp, big_near_tmp, small_near_tmp, arr, key, stat)
    elif mode == 'TRAIN_SECOND':
        train(key, stat, big_tmp, small_tmp, big_near_tmp, small_near_tmp, true_label)


def process(count, maxConsecutiveCount, seq, nearGapStat, gapStat, prob_cand_arr, pred, data_len, good_count, stat, true_label, mode):
    big_tmp = pattern_sort(prob_cand_arr, pred, seq['big'], False, 0)
    small_tmp = pattern_sort(prob_cand_arr, pred, seq['small'], False, 0)
    big_near_tmp = pattern_sort(prob_cand_arr, pred, seq['bigNear'], False, 0)
    small_near_tmp = pattern_sort(prob_cand_arr, pred, seq['smallNear'], False, 0)
    arr = set()
    hit = False
    current_strategy = None
    #大部分大
    if count['big'] >= 7:
        current_strategy = '大的全都要'
        processDetail(arr, stat, true_label, big_tmp, small_tmp, big_near_tmp, small_near_tmp, nearGapStat, gapStat, current_strategy, mode)
        if mode == 'PREDICT_SECOND':
            print(current_strategy)
    #参差不齐接近
    elif count['near'] >= 5 and maxConsecutiveCount['near'] < 4:
        if len(seq['small']) + len(seq['smallNear']) >= 7:
            current_strategy = '参差不齐接近时小的偏多'
            processDetail(arr, stat, true_label, big_tmp, small_tmp, big_near_tmp, small_near_tmp, nearGapStat, gapStat, current_strategy, mode)
            if mode == 'PREDICT_SECOND':
                print(current_strategy)
        elif len(seq['big']) + len(seq['bigNear']) >= 7:
            current_strategy = '参差不齐接近时大的偏多'
            processDetail(arr, stat, true_label, big_tmp, small_tmp, big_near_tmp, small_near_tmp, nearGapStat, gapStat, current_strategy, mode)
            if mode == 'PREDICT_SECOND':
                print(current_strategy)
        elif len(seq['small']) + len(seq['smallNear']) > len(seq['big']) + len(seq['bigNear']):
            current_strategy = '参差不齐接近时小的比大的多一些'
            processDetail(arr, stat, true_label, big_tmp, small_tmp, big_near_tmp, small_near_tmp, nearGapStat, gapStat, current_strategy, mode)
            if mode == 'PREDICT_SECOND':
                print(current_strategy)
        elif len(seq['small']) + len(seq['smallNear']) < len(seq['big']) + len(seq['bigNear']):
            current_strategy = '参差不齐接近时大的多一些'
            processDetail(arr, stat, true_label, big_tmp, small_tmp, big_near_tmp, small_near_tmp, nearGapStat, gapStat, current_strategy, mode)
            if mode == 'PREDICT_SECOND':
                print(current_strategy)
        else:
            current_strategy = '参差不齐接近时大小一样'
            processDetail(arr, stat, true_label, big_tmp, small_tmp, big_near_tmp, small_near_tmp, nearGapStat, gapStat, current_strategy, mode)
            if mode == 'PREDICT_SECOND':
                print(current_strategy)
    #连续接近
    elif count['near'] >= 5 and maxConsecutiveCount['near'] >= 4:
        if len(seq['small']) + len(seq['smallNear']) >= 7:
            current_strategy = '连续接近时小的偏多'
            processDetail(arr, stat, true_label, big_tmp, small_tmp, big_near_tmp, small_near_tmp, nearGapStat, gapStat, current_strategy, mode)
            if mode == 'PREDICT_SECOND':
                print(current_strategy)
        elif len(seq['big']) + len(seq['bigNear']) >= 7:
            current_strategy = '连续接近时大的偏多'
            processDetail(arr, stat, true_label, big_tmp, small_tmp, big_near_tmp, small_near_tmp, nearGapStat, gapStat, current_strategy, mode)
            if mode == 'PREDICT_SECOND':
                print(current_strategy)
        elif len(seq['small']) + len(seq['smallNear']) > len(seq['big']) + len(seq['bigNear']):
            current_strategy = '连续接近时小的比大的多一些'
            processDetail(arr, stat, true_label, big_tmp, small_tmp, big_near_tmp, small_near_tmp, nearGapStat, gapStat, current_strategy, mode)
            if mode == 'PREDICT_SECOND':
                print(current_strategy)
        elif len(seq['small']) + len(seq['smallNear']) < len(seq['big']) + len(seq['bigNear']):
            current_strategy = '连续接近时大的多一些'
            processDetail(arr, stat, true_label, big_tmp, small_tmp, big_near_tmp, small_near_tmp, nearGapStat, gapStat, current_strategy, mode)
            if mode == 'PREDICT_SECOND':
                print(current_strategy)
        else:
            current_strategy = '连续接近时大小一样'
            processDetail(arr, stat, true_label, big_tmp, small_tmp, big_near_tmp, small_near_tmp, nearGapStat, gapStat, current_strategy, mode)
            if mode == 'PREDICT_SECOND':
                print(current_strategy)
    #参差不齐小
    elif count['small'] >= 5 and maxConsecutiveCount['small'] < 4:
        current_strategy = '参差不齐小'
        processDetail(arr, stat, true_label, big_tmp, small_tmp, big_near_tmp, small_near_tmp, nearGapStat, gapStat, current_strategy, mode)
        if mode == 'PREDICT_SECOND':
            print(current_strategy)
    #不是大的就是接近的(大的偏多)
    elif count['big'] >= 5 and count['near'] >= 2:
        current_strategy = '不是大的就是接近的(大的偏多)'
        processDetail(arr, stat, true_label, big_tmp, small_tmp, big_near_tmp, small_near_tmp, nearGapStat, gapStat, current_strategy, mode)
        if mode == 'PREDICT_SECOND':
            print(current_strategy)
    #不是大的就是小的(大的偏多)
    elif count['big'] >= 5 and count['small'] >= 2:
        current_strategy = '不是大的就是小的(大的偏多)'
        processDetail(arr, stat, true_label, big_tmp, small_tmp, big_near_tmp, small_near_tmp, nearGapStat, gapStat, current_strategy, mode)
        if mode == 'PREDICT_SECOND':
            print(current_strategy)
    #大:接近:小很均衡
    elif count['big'] <= 4 and count['near'] <= 4 and count['small'] <= 4:
        if len(seq['small']) + len(seq['smallNear']) > len(seq['big']) + len(seq['bigNear']):
            current_strategy = '很均衡时小的偏多'
            processDetail(arr, stat, true_label, big_tmp, small_tmp, big_near_tmp, small_near_tmp, nearGapStat, gapStat, current_strategy, mode)
            if mode == 'PREDICT_SECOND':
                print(current_strategy)
        elif len(seq['small']) + len(seq['smallNear']) < len(seq['big']) + len(seq['bigNear']):
            current_strategy = '很均衡时大的偏多'
            processDetail(arr, stat, true_label, big_tmp, small_tmp, big_near_tmp, small_near_tmp, nearGapStat, gapStat, current_strategy, mode)
            if mode == 'PREDICT_SECOND':
                print(current_strategy)
        else:
            current_strategy = '非常均衡'
            processDetail(arr, stat, true_label, big_tmp, small_tmp, big_near_tmp, small_near_tmp, nearGapStat, gapStat, current_strategy, mode)
            if mode == 'PREDICT_SECOND':
                print(current_strategy)
    #大部分小
    elif count['small'] >= 7:
        current_strategy = '大部分小'
        processDetail(arr, stat, true_label, big_tmp, small_tmp, big_near_tmp, small_near_tmp, nearGapStat, gapStat, current_strategy, mode)
        if mode == 'PREDICT_SECOND':
            print(current_strategy)
    #连续小
    elif count['small'] >= 5 and maxConsecutiveCount['small'] >= 4:
        current_strategy = '连续小'
        processDetail(arr, stat, true_label, big_tmp, small_tmp, big_near_tmp, small_near_tmp, nearGapStat, gapStat, current_strategy, mode)
        if mode == 'PREDICT_SECOND':
            print(current_strategy)
    else:
        current_strategy = '不对呀'
        processDetail(arr, stat, true_label, big_tmp, small_tmp, big_near_tmp, small_near_tmp, nearGapStat, gapStat, current_strategy, mode)
        if mode == 'PREDICT_SECOND':
            print(current_strategy)
    if current_strategy == '不是大的就是接近的(大的偏多)':
        del(seq['near'])
        print({k : sort_show([('hit-' + str(bi) if bi == int(true_label) else str(bi)) + ':' + "{:.4f}".format(prob_cand_arr[bi] - pred) for bi in seq[k]]) for k in seq}, gapStat)
    return arr
