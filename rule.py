from rule_kit import *
from rule_e import process as auto_process
from qxc_rule_0 import process as qxc_process_0
from qxc_rule_1 import process as qxc_process_1
from qxc_rule_2 import process as qxc_process_2
from qxc_rule_3 import process as qxc_process_3
from qxc_rule_4 import process as qxc_process_4
from qxc_rule_5 import process as qxc_process_5
from qxc_rule_6 import process as qxc_process_6
# from plw_rule_0 import process as plw_process_0
# from plw_rule_1 import process as plw_process_1
# from plw_rule_2 import process as plw_process_2
# from plw_rule_3 import process as plw_process_3
# from plw_rule_4 import process as plw_process_4
# from plw_full_rule_0 import process as plw_full_process_0
# from plw_full_rule_1 import process as plw_full_process_1
# from plw_full_rule_2 import process as plw_full_process_2
# from plw_full_rule_3 import process as plw_full_process_3
# from plw_full_rule_4 import process as plw_full_process_4
# from sd_rule_0 import process as sd_process_0
# from sd_rule_1 import process as sd_process_1
# from sd_rule_2 import process as sd_process_2
# from sd_full_rule_0 import process as sd_full_process_0
# from sd_full_rule_1 import process as sd_full_process_1
# from sd_full_rule_2 import process as sd_full_process_2
# from pls_rule_0 import process as pls_process_0
# from pls_rule_1 import process as pls_process_1
# from pls_rule_2 import process as pls_process_2
from pls_full_rule_0 import process as pls_full_process_0
from pls_full_rule_1 import process as pls_full_process_1
from pls_full_rule_2 import process as pls_full_process_2

process_map = {
    'qxc' : {
        0 : qxc_process_0,
        1 : qxc_process_1,
        2 : qxc_process_2,
        3 : qxc_process_3,
        4 : qxc_process_4,
        5 : qxc_process_5,
        6 : qxc_process_6
    },
    'qxc_full' : {
    },
    'plw_full' : {

    },
    'plw' : {

    },
    'sd' : {

    },
    'sd_full' : {

    },
    'pls' : {

    },
    'pls_full' : {
        0 : pls_full_process_0,
        1 : pls_full_process_1,
        2 : pls_full_process_2
    }
}


def pattern_check(name, prob_cand_arr, pred, label_dim, avg_window, data_len, good_count, true_label, mode=None, range_stat=None, config=None, config_copy=None):
    count = {'big' : 0, 'small' : 0, 'near' : 0}
    previousPos = {'big' : -(sys.maxsize) - 1, 'small' : -(sys.maxsize) - 1, 'near' : -(sys.maxsize) - 1}
    consecutiveCount = {'big' : 0, 'small' : 0, 'near' : 0}
    maxConsecutiveCount = {'big' : 0, 'small' : 0, 'near' : 0}
    seq = {'big' : [], 'small' : [], 'near' : [], 'smallNear' : [], 'bigNear' : []}
    smallNear = []
    bigNear = []
    gapStat = {0.02 : 0, 0.03 : 0, 0.04 : 0, 0.05 : 0, 0.06 : 0, 0.07 : 0, 0.08 : 0, 0.09 : 0, -0.02 : 0, -0.03 : 0, -0.04 : 0, -0.05 : 0, -0.06 : 0, -0.07 : 0, -0.08 : 0, -0.09 : 0}
    nearGapStat = {-0.01 : 0, 0.01 : 0}
    for i in range(len(prob_cand_arr)):
        v = prob_cand_arr[i]
        if v - pred >= 0.015:
            seq['big'].append(i)
            pattern_check_detail(count, previousPos, consecutiveCount, maxConsecutiveCount, 'big', i)
            for key in gapStat:
                if key > 0 and v - pred >= key - 0.0001:
                    gapStat[key] += 1
        elif v - pred <= -0.015:
            seq['small'].append(i)
            pattern_check_detail(count, previousPos, consecutiveCount, maxConsecutiveCount, 'small', i)
            for key in gapStat:
                if key < 0 and v - pred <= key + 0.0001:
                    gapStat[key] += 1
        else:
            seq['near'].append(i)
            pattern_check_detail(count, previousPos, consecutiveCount, maxConsecutiveCount, 'near', i)
            if v - pred < 0:
                seq['smallNear'].append(i)
                if v - pred <= -0.01:
                    nearGapStat[-0.01] += 1
            else:
                seq['bigNear'].append(i)
                if v - pred >= 0.01:
                    nearGapStat[0.01] += 1
    # 自动生成
    if 'AUTO' in mode:
        return auto_process(count, maxConsecutiveCount, seq, nearGapStat, gapStat, prob_cand_arr, pred, avg_window, data_len, good_count, range_stat, name, true_label, label_dim, config, config_copy)
    # 用原始人工方法预测
    elif mode == 'MANUALLY_PREDICT':
        return process_map[name][label_dim](count, maxConsecutiveCount, seq, nearGapStat, gapStat, prob_cand_arr, pred, avg_window, data_len, good_count, range_stat, name, true_label, label_dim), None, False