from math import sqrt
import math
import datetime
import numpy as np
import os, re
import pandas as pd
from sklearn.preprocessing import StandardScaler
import requests
import json
import time
import numpy as np
from math import log
from sklearn.model_selection import KFold
import random
import warnings
from feature_kit import *
import os, sys, shutil
# from darts import TimeSeries
from datetime import date
from base_kit import *


# def generateSegmentForPureTimeSeries(arr, input_chunk_length, output_chunk_length, test_set_size, val_set_size, skip=True):
#     arr = np.array(arr).T
#     train_set = None
#     test_set = None
#     val_set = None
#     pred = None
#     all_len = len(arr)
#     test_len = input_chunk_length + output_chunk_length + test_set_size
#     val_len = input_chunk_length + output_chunk_length + ((val_set_size * (output_chunk_length) - output_chunk_length) if skip else val_set_size)
#     train_set = arr[:all_len - test_len - val_len - input_chunk_length]
#     test_set = arr[all_len - test_len - val_len - input_chunk_length : all_len - val_len - input_chunk_length]
#     val_set = arr[all_len - val_len - input_chunk_length : all_len - input_chunk_length]
#     pred = arr[-input_chunk_length:]
#     train_series = TimeSeries.from_values(train_set)
#     test_series = TimeSeries.from_values(test_set)
#     val_series_arr = []
#     for i in range(val_set_size):
#         pos = (i * output_chunk_length) if skip else i
#         val_series_arr.append({'train' : TimeSeries.from_values(val_set[pos : pos + input_chunk_length]), 'val' : val_set[pos + input_chunk_length : pos + input_chunk_length + output_chunk_length]})
#     pred_series = TimeSeries.from_values(pred)
#     return train_series, test_series, val_series_arr, pred_series


def reverseArr(arr):
    result = []
    for i in range(len(arr)):
        result.append(arr[i].T)
    return np.array(result)


def generateProbRaw(start, combine, name, label_pos):
    lookbacks = combine
    with open(name) as file:
        label = []
        for line in file:
            line = line.replace('\n', '').split(' ')
            label.append(int(line[label_pos+1]))
        print('最后', line, label_pos, line[label_pos+1])
        x_raw = [[] for i in range(len(lookbacks))]
        y_raw = [[] for i in range(len(lookbacks))]
        for lookback_pos in range(len(lookbacks)):
            lookback = lookbacks[lookback_pos]
            for i in range(start, len(label) + 1):
                stat = [0.0 for l in (range(10) if label_pos < 6 else range(15))]
                current = label[i] if i < len(label) else -1
                for v in label[i - lookback : i]:
                    stat[v] += 1.0
                mx = max(stat)
                mi = min(stat)
                if mx == mi:
                    print(stat, label[i - lookback : i], lookback, i)
                for k in range(len(stat)):
                    stat[k] = (stat[k] - mi) / (mx - mi)
                x_raw[lookback_pos].append([stat[s] for s in range(len(stat))])
                y_raw[lookback_pos].append(stat[current] if current > -1 else current)
    # for i in range(len(x_raw)):
    #     y_raw[i] = y_raw[i][0::2] if len(y_raw[i]) % 2 == 0 else y_raw[i][1::2]
    #     x_raw[i] = x_raw[i][0::2] if len(x_raw[i]) % 2 == 0 else x_raw[i][1::2]
    return x_raw, y_raw


def generateProbRawByLabel(start, combine, name, label_pos_array):
    lookbacks = combine
    with open(name) as file:
        labels = []
        for line in file:
            line = line.replace('\n', '').split(' ');
            labels.append([int(line[label_pos_array[0]+1]), int(line[label_pos_array[1]+1])]);
        x_raw = [[] for i in range(len(lookbacks))]
        y_raw = [[] for i in range(len(lookbacks))]
        for lookback_pos in range(len(lookbacks)):
            lookback = lookbacks[lookback_pos]
            for i in range(start, len(labels) + 1):
                stat = [0.0 for l in (range(10) if label_pos_array[lookback_pos] < 6 else range(15))]
                current = labels[i][lookback_pos] if i < len(labels) else - 1
                for v in labels[i - lookback : i]:
                    stat[v[lookback_pos]] += 1.0
                mx = max(stat)
                mi = min(stat)
                if mx == mi:
                    print(stat, labels[i - lookback : i], lookback, i)
                for k in range(len(stat)):
                    stat[k] = (stat[k] - mi) / (mx - mi)
                x_raw[lookback_pos].append([stat[s] for s in range(len(stat))])
                y_raw[lookback_pos].append(stat[current] if current > -1 else current)
    return x_raw, y_raw


''' RMEMBER!!! ODD X EVEN, NOT COMPATIABLE!!!!!!!! '''
def loadProbRaw(start, combine, names, name, label_pos, time_window, avg_window, mode='ALL_LABEL', enrich=None, reverse=False, sample_mode='random', debug=True, shrink=True, label_pos_array=None, output_chunk_length=None, pred_len=7):
    test_rate = 0.01
    if names:
        y_raw = [[] for i in range(len(names))]
        y_on_prob_raw = [[] for i in range(len(names))]
        x_raw = [[] for i in range(len(names))]
        for i in range(len(names)):
            with open(names[i], 'r') as file:
                for line in file:
                    line = line.replace('\n', '')
                    if len(line) > 0:
                        raws = line.split(':')
                        y = float(raws[-1])
                        x = [float(v) for v in raws[0].split(',')]
                        y_raw[i].append(y)
                        x_raw[i].append(x)
    else:
        y_on_prob_raw = [[] for i in range(len(combine))]
        if label_pos_array:
            x_raw, y_raw = generateProbRawByLabel(start, combine, name, label_pos_array)
        else:
            x_raw, y_raw = generateProbRaw(start, combine, name, label_pos)
    v_len = len(y_raw[0])
    h_len = len(y_raw)
    if debug:
        print('current label prob:')
        for i in range(v_len):
            print([y_raw[h][i] for h in range(h_len)])
    #train
    y_all_label = []
    y_time_series = []
    y_on_prob_time_series = []
    x_all_label = []
    x_time_series = []
    x_on_prob_time_series = []
    #pred
    py_all_label = []
    py_time_series = []
    py_on_prob_time_series = []
    px_all_label = []
    px_time_series = []
    px_on_prob_time_series = []
    all_label_prob = []
    all_label_prob_accum = []
    show = []
    for i in range(v_len):
        if y_raw[0][i] == -1:
            py_all_label.append([y_raw[j][i] for j in range(h_len)])
            px_all_label.append([x_raw[j][i] for j in range(h_len)])
            for al in range(len(x_raw[0][0])):
                all_label_prob.append([x_raw[j][i][al] for j in range(h_len)])
        else:
            y_all_label.append([y_raw[j][i] for j in range(h_len)])
            x_all_label.append([x_raw[j][i] for j in range(h_len)])
        #prepare time series on prob
        if i >= avg_window - 1:
            if y_raw[0][i] != -1:
                for j in range(h_len):
                    y_on_prob_raw[j].append(np.mean(y_raw[j][i + 1 - avg_window : i + 1]))
                    #y_on_prob_raw[j].append(exp_avg(y_raw[j][i + 1 - avg_window : i + 1], 0.5))
            else:
                for al in range(len(x_raw[0][0])):
                    all_label_prob_accum.append([np.mean(y_raw[j][i - avg_window + 1: i] + [x_raw[j][i][al]]) for j in range(h_len)])
        # direct time series
        if i >= avg_window:
            segment = [y_raw[j][i - avg_window : i] for j in range(h_len)]
            if y_raw[0][i] == -1:
                px_time_series.append(segment)
                py_time_series.append([y_raw[j][i] for j in range(h_len)])
            else:
                x_time_series.append(segment)
                y_time_series.append([y_raw[j][i] for j in range(h_len)])
    for j in range(h_len):
        y_on_prob_raw[j].append(-1)
    if debug:
        print('accum prob:')
    # time series on prob
    for i in range(len(y_on_prob_raw[0])):
        if i >= time_window:
            if y_on_prob_raw[0][i] == -1:
                px_on_prob_time_series.append([y_on_prob_raw[j][i - time_window : i] for j in range(h_len)])
                py_on_prob_time_series.append([y_on_prob_raw[j][i] for j in range(h_len)])
            else:
                x_on_prob_time_series.append([y_on_prob_raw[j][i - time_window : i] for j in range(h_len)])
                y_on_prob_time_series.append([y_on_prob_raw[j][i] for j in range(h_len)])
        if debug:
            print([y_on_prob_raw[h][i] for h in range(h_len)])
    for k in range(len(all_label_prob)):
        left = k
        middle = ["%.10f" % n for n in all_label_prob[k]]
        right = ["%.10f" % n for n in all_label_prob_accum[k]]
        #print(left, middle, right)
        show.append([left, middle, right])
    if mode == 'PURE_TIME_SERIES':
        if shrink:
            y_on_prob_raw = [v[0::2] if len(v) % 2 == 0 else v[1::2] for v in y_on_prob_raw]
        #train_series, test_series, val_series_arr, pred_series = generateSegmentForPureTimeSeries(y_on_prob_raw, time_window, output_chunk_length, int(len(y_on_prob_raw) * test_rate), int(pred_len / output_chunk_length))
        #return {'train_series' : train_series, 'test_series' : test_series, 'val_series_arr' : val_series_arr, 'pred_series' : pred_series}, show
    elif mode == 'ALL_LABEL':
        x_all_label = np.array(x_all_label)
        y_all_label = np.array(y_all_label)
        test_len = int(len(x_all_label) * test_rate)
        return {'train' : {'x' : x_all_label[:-test_len], 'y' : y_all_label[:-test_len]}, 'test' : {'x' : x_all_label[-test_len:], 'y' : y_all_label[-test_len:]}}, show
    elif mode == 'TIME_SERIES':
        if enrich:
            for i in range(len(x_time_series)):
                nested = [smooth(v, enrich['name'], False, enrich['param']) for v in x_time_series[i]]
                x_time_series[i] = [item for sub in nested for item in sub]
        x_time_series = np.array(x_time_series)
        if reverse:
            x_time_series = reverseArr(x_time_series)
        y_time_series = np.array(y_time_series)
        # shrink
        if shrink:
            x_time_series = x_time_series[0::2] if len(x_time_series) % 2 == 0 else x_time_series[1::2]
            y_time_series = y_time_series[0::2] if len(y_time_series) % 2 == 0 else y_time_series[1::2]
        x_pred = x_time_series[-pred_len:]
        y_pred = y_time_series[-pred_len:]
        x_data = x_time_series[:-pred_len]
        y_data = y_time_series[:-pred_len]
        all_pos = [i for i in range(len(y_data))]
        test_len = int(len(all_pos) * test_rate)
        test_pos = np.random.choice(all_pos, test_len)
        train_pos = [v for v in all_pos if v not in test_pos]
        if sample_mode == 'random':
            return {'train' : { 'x' : np.array([x_data[pos] for pos in train_pos]), 'y' : np.array([y_data[pos] for pos in train_pos])}, 'test' : {'x' : np.array([x_data[pos] for pos in test_pos]), 'y' : np.array([y_data[pos] for pos in test_pos])}, 'pred' : {'x' : x_pred, 'y' : y_pred}, 'target' : {'x' : np.array(px_time_series), 'y' : np.array(py_time_series)}}, show
        elif sample_mode == 'latest':
            return {'train' : { 'x' : x_data[:-test_len], 'y' : y_data[:-test_len]}, 'test' : {'x' : x_data[-test_len:], 'y' : y_data[-test_len:]}, 'pred' : {'x' : x_pred, 'y' : y_pred}, 'target' : {'x' : np.array(px_time_series), 'y' : np.array(py_time_series)}}, show
    elif mode == 'PROB_TIME_SERIES':
        if enrich:
            for i in range(len(x_on_prob_time_series)):
                nested = [smooth(v, enrich['name'], False, enrich['param']) for v in x_on_prob_time_series[i]]
                x_on_prob_time_series[i] = [item for sub in nested for item in sub]
        x_on_prob_time_series = np.array(x_on_prob_time_series)
        px_on_prob_time_series = np.array(px_on_prob_time_series)
        if reverse:
            x_on_prob_time_series = reverseArr(x_on_prob_time_series)
            px_on_prob_time_series = reverseArr(px_on_prob_time_series)
        y_on_prob_time_series = np.array(y_on_prob_time_series)
        # shrink
        if shrink:
            x_on_prob_time_series = x_on_prob_time_series[0::2] if len(x_on_prob_time_series) % 2 == 0 else x_on_prob_time_series[1::2]
            y_on_prob_time_series = y_on_prob_time_series[0::2] if len(y_on_prob_time_series) % 2 == 0 else y_on_prob_time_series[1::2]
            # x_on_prob_time_series = x_on_prob_time_series[0::3] if len(x_on_prob_time_series) % 2 == 0 else x_on_prob_time_series[1::3]
            # y_on_prob_time_series = y_on_prob_time_series[0::3] if len(y_on_prob_time_series) % 2 == 0 else y_on_prob_time_series[1::3]
        x_pred = x_on_prob_time_series[-pred_len:]
        y_pred = y_on_prob_time_series[-pred_len:]
        y_pred_previous = y_on_prob_time_series[-(pred_len*5):-pred_len:]
        gap = int(time_window + 4)
        x_data = x_on_prob_time_series[:-(pred_len + gap)]
        y_data = y_on_prob_time_series[:-(pred_len + gap)]
        all_pos = [i for i in range(len(y_data))]
        test_len = int(len(all_pos) * test_rate)
        test_pos = np.random.choice(all_pos, test_len, replace=False)
        #test_pos = all_pos[0::10]
        train_pos = [v for v in all_pos if v not in test_pos]
        if sample_mode == 'random':
            return {'train' : { 'x' : np.array([x_data[pos] for pos in train_pos]), 'y' : np.array([y_data[pos] for pos in train_pos])}, 'test' : {'x' : np.array([x_data[pos] for pos in test_pos]), 'y' : np.array([y_data[pos] for pos in test_pos])}, 'pred' : {'x' : x_pred, 'y' : y_pred}, 'target' : {'x' : np.array(px_on_prob_time_series), 'y' : np.array(py_on_prob_time_series)}}, y_pred_previous, show
        elif sample_mode == 'latest':
            return {'train' : {'x' : x_data[:-(test_len + gap)], 'y' : y_data[:-(test_len + gap)]}, 'test' : {'x' : x_data[-test_len:], 'y' : y_data[-test_len:]}, 'pred' : {'x' : x_pred, 'y' : y_pred}, 'target' : {'x' : np.array(px_on_prob_time_series), 'y' : np.array(py_on_prob_time_series)}}, y_pred_previous, show

def mean(arr):
    return np.mean(arr) if len(arr) > 0 else 0

def max(arr):
    return np.max(arr) if len(arr) > 0 else 0

def min(arr):
    return np.min(arr) if len(arr) > 0 else 0

def std(arr):
    return np.std(arr) if len(arr) > 0 else 0

def stat_diff(diff):
    return [
        # np.mean(diff), 
        # np.max(diff), 
        # np.min(diff), 
        # np.std(diff), 
        mean([ v for v in diff if v < 0]), 
        max([ v for v in diff if v < 0]), 
        min([ v for v in diff if v < 0]), 
        std([ v for v in diff if v < 0]),
        mean([ v for v in diff if v >= 0]), 
        max([ v for v in diff if v >= 0]), 
        min([ v for v in diff if v >= 0]), 
        std([ v for v in diff if v >= 0]),
        len([v for v in diff if v == 0]) / 10.0,
        len([v for v in diff if v > 0]) / 10.0,
        len([v for v in diff if v < 0]) / 10.0,
        len([v for v in diff if v > 0.015]) / 10.0,
        len([v for v in diff if v < -0.015]) / 10.0,
        len([v for v in diff if v >= 0 and v <= 0.015]) / 10.0,
        len([v for v in diff if v < 0 and v >= -0.015]) / 10.0
    ]

import math

def enrich_diff(diff):
    #return [math.sqrt(abs(v)) * (1 if v >= 0 else -1) for v in diff]
    return []

def get_x_line(v):
    x = []
    # previous_pred_arr
    # previous_truth_arr
    # previous_truth_gap_arr
    previous_diff = None
    for i in range(7):
        diff = [vv - v['previous_pred_arr'][i] for vv in v['previous_prob_cand_arr'][i]]
        diff_diff = 0.0
        if previous_diff is not None:
            #diff_diff = [diff[i] - previous_diff[i] for i in range(len(diff))]
            diff_diff = np.corrcoef(diff, previous_diff)[0][1]
        previous_diff = diff
        # if diff_diff is not None:
        #     x.append(np.diff(diff_diff).tolist() + np.diff(diff_diff, 2).tolist() + np.diff(diff_diff, 3).tolist() + diff_diff + enrich_diff(diff_diff) + [v['previous_truth_gap_arr'][i]] + stat_diff(diff_diff))
        x.append(np.diff(diff).tolist() + np.diff(diff, 2).tolist() + np.diff(diff, 3).tolist() + diff + enrich_diff(diff) + [v['previous_truth_gap_arr'][i]] + stat_diff(diff))
    diff = [vv - v['pred'] for vv in v['prob_cand_arr']]
    #diff_diff = [diff[i] - previous_diff[i] for i in range(len(diff))]
    diff_diff = np.corrcoef(diff, previous_diff)[0][1]
    current_stat_diff = stat_diff(diff)
    #x.append(np.diff(diff_diff).tolist() + np.diff(diff_diff, 2).tolist() + np.diff(diff_diff, 3).tolist() + diff_diff + enrich_diff(diff_diff) + [v['previous_truth_gap_arr'][i]] + stat_diff(diff_diff))
    x.append(np.diff(diff).tolist() + np.diff(diff, 2).tolist() + np.diff(diff, 3).tolist() + diff + enrich_diff(diff) + [v['pred']] + current_stat_diff)
    return x, current_stat_diff[-7:]


def load_secondary(name, exclude, acc_sample_num, target_dt, pred_dt, test_ratio, cv=-1):
    label_dim_cand = {
        0 : [i for i in range(10)],
        1 : [i for i in range(10)],
        2 : [i for i in range(10)],
        3 : [i for i in range(10)],
        4 : [i for i in range(10)],
        5 : [i for i in range(10)],
        6 : [i for i in range(15)]
    }
    date_list = []
    label_list = []
    date_and_label = {}
    date_pattern = re.compile(r'^\d{4}\d{2}\d{2}$')
    with open(name.replace('_full', '') + '_raw_txt', 'r') as f:
        for line in f:
            row = line.replace('\n', '').split(' ')
            dt = row[0].replace('-', '')
            date_list.append(dt)
            label_list.append([dt] + [int(v) for v in row[1:]])
            date_and_label[dt] = [int(v) for v in row[1:]]
    data = {}
    new_date = set()
    if os.path.exists(name + '/secondary_global_data.pkl'):
        data = load_obj(name + '/secondary_global_data')
    for folder_name in os.listdir(name):
        if date_pattern.match(folder_name) and folder_name not in data and folder_name in date_list:
            new_date.add(folder_name)
    for folder_name in new_date:
        if os.path.isdir(name + '/' + folder_name) and date_pattern.match(folder_name) and (exclude is None or folder_name not in exclude):
            if os.path.exists(name + '/secondary_global_data.pkl'):
                data = load_obj(name + '/secondary_global_data')
            print('process:', folder_name)
            data[folder_name] = {}
            for file_name in os.listdir(name + '/' + folder_name):
                if 'detail_' in file_name:
                    label_dim = int(file_name.replace('detail_', '').replace('.pkl', ''))
                    data[folder_name][label_dim] = {'data' : [], 'true_pos' : -1}
                    if acc_sample_num is None:
                        for item in get_best_item(name, label_dim, True, folder_name, date_list, label_list)[1]:
                            data[folder_name][label_dim]['data'].append(item)
                    else:
                        best_item = get_best_item(name, label_dim, True, folder_name, date_list, label_list)[1]
                        std_item = get_best_item(name, label_dim, False, folder_name, date_list, label_list)[1]
                        for item in best_item[:acc_sample_num]:
                            data[folder_name][label_dim]['data'].append(item)
                        for item in std_item[:acc_sample_num]:
                            data[folder_name][label_dim]['data'].append(item)
            for label_dim in data[folder_name]:
                data[folder_name][label_dim]['true_pos'] = date_and_label[folder_name][label_dim]
            persist_obj(data, name + '/secondary_global_data')
    target = {}
    pred = {}
    print(target_dt)
    invalid_pos_arr = [6]
    target_data = {}
    for dt in target_dt:
        if os.path.exists(name + '/secondary_global_target.pkl'):
            target_data = load_obj(name + '/secondary_global_target')
        if dt not in target_data:
            print('target:', dt)
            if dt not in date_list:
                date_list.append(dt)
            target_data[dt] = {}
            for file_name in os.listdir(name + '/' + dt):
                if 'detail_' in file_name:
                    label_dim = int(file_name.replace('detail_', '').replace('.pkl', ''))
                    target_data[dt][label_dim] = {'data' : [], 'best_data_len' : [], 'std_data_len' : []}
                    best_item = get_best_item(name, label_dim, True, dt, date_list, label_list)[1]
                    std_item = get_best_item(name, label_dim, False, dt, date_list, label_list)[1]
                    for item in best_item:
                        target_data[dt][label_dim]['data'].append(item)
                    for v in best_item[:10]:
                        target_data[dt][label_dim]['best_data_len'].append(v['data_len'])
                    for v in std_item[:10]:
                        target_data[dt][label_dim]['std_data_len'].append(v['data_len'])
            persist_obj(target_data, name + '/secondary_global_target')
    print("prepare")
    x_info = []
    sorted_date = sorted(data)
    # sorted_date = sorted_date[3::7]
    pred_date = sorted_date[-int(len(sorted_date) * test_ratio):]
    test_date = pred_date#sorted_date[-int(len(sorted_date) * test_ratio + 5):-int(len(sorted_date) * test_ratio - 0)]
    train_date = sorted_date[:-int(len(sorted_date) * test_ratio)]
    train_date = train_date[25:]
    x_data_train = []
    y_data_train = []
    x_data_test = []
    y_data_test = []
    x_info_train = []
    x_info_test = []
    del_dt = []
    for dt in target:
        if dt not in target_dt:
            del_dt.append(dt)
    for dt in del_dt:
        del(target[dt])
    result = []
    if cv == 1:
        for label_dim_arr in [[0,1,2,3,4],[1,2,3,4,5],[3,4,5,0,1]]:
            x_data_train = []
            y_data_train = []
            x_data_test = []
            y_data_test = []
            x_info_train = []
            x_info_test = []
            for dt in test_date:
                for label_dim in label_dim_arr:
                    for v in data[dt][label_dim]['data']:
                        v['label_pos'] = label_dim
                        row, stat_diff_info = get_x_line(v)
                        x_info_test.append({'data_len' : v['data_len'], 'avg_window' : v['avg_window'], 'good_count' : v['best'], 'qxc' : v['qxc'], 'label_pos' : label_dim, 'prob_cand_arr' : v['prob_cand_arr']})
                        x_data_test.append(row)
                        if data[dt][label_dim]['true_pos'] not in label_dim_cand[label_dim]:
                            print('不对了', data[dt][label_dim]['true_pos'], label_dim)
                            exit(0)
                        y_data_test.append([category_label_by_comparison(v['prob_cand_arr'][data[dt][label_dim]['true_pos']], v['pred'])])
                        #y_data_test.append([1] if v['prob_cand_arr'][data[dt][label_dim]['true_pos']] >= v['pred'] else [0])
            for dt in train_date:
                for label_dim in label_dim_arr:
                    for v in data[dt][label_dim]['data']:
                        v['label_pos'] = label_dim
                        row, stat_diff_info = get_x_line(v)
                        x_info_train.append({'data_len' : v['data_len'], 'avg_window' : v['avg_window'], 'good_count' : v['best'], 'qxc' : v['qxc'], 'label_pos' : label_dim, 'prob_cand_arr' : v['prob_cand_arr']})
                        x_data_train.append(row)
                        if data[dt][label_dim]['true_pos'] not in label_dim_cand[label_dim]:
                            print('不对了', data[dt][label_dim]['true_pos'], label_dim)
                            exit(0)
                        y_data_train.append(category_label_by_comparison(v['prob_cand_arr'][data[dt][label_dim]['true_pos']], v['pred']))
                        #y_data_train.append([1] if v['prob_cand_arr'][data[dt][label_dim]['true_pos']] >= v['pred'] else [0])
            result.append({'train' : {'x' : np.array(x_data_train), 'y' : np.array(y_data_train)}, 'test' : {'x' : np.array(x_data_test), 'y' : np.array(y_data_test)}, 'x_info_train' : x_info_train, 'x_info_test' : x_info_test})
    elif cv==2:
        pred_date = sorted_date[-8:]
        pred_dt_len = len(pred_date)
        val_len = 8
        split_num = 4
        train_len = len(sorted_date) - pred_dt_len - val_len * split_num
        candidate = sorted_date[:-pred_dt_len]
        for i in range(split_num):
            x_data_train = []
            y_data_train = []
            x_data_test = []
            y_data_test = []
            x_info_train = []
            x_info_test = []
            cv_train = candidate[val_len * i : val_len * i + train_len]
            cv_val = candidate[val_len * i + train_len : val_len * i + train_len + val_len]
            for dt in cv_val:
                for label_dim in data[dt]:
                    if label_dim not in invalid_pos_arr:
                        for v in data[dt][label_dim]['data']:
                            v['label_pos'] = label_dim
                            row, stat_diff_info = get_x_line(v)
                            x_info_test.append({'data_len' : v['data_len'], 'avg_window' : v['avg_window'], 'good_count' : v['best'], 'qxc' : v['qxc'], 'label_pos' : label_dim, 'prob_cand_arr' : v['prob_cand_arr']})
                            x_data_test.append(row)
                            if data[dt][label_dim]['true_pos'] not in label_dim_cand[label_dim]:
                                print('不对了', data[dt][label_dim]['true_pos'], label_dim)
                                exit(0)
                            y_data_test.append([category_label_by_comparison(v['prob_cand_arr'][data[dt][label_dim]['true_pos']], v['pred'])])
                            #y_data_test.append([1] if v['prob_cand_arr'][data[dt][label_dim]['true_pos']] >= v['pred'] else [0])
            for dt in cv_train:
                for label_dim in data[dt]:
                    if label_dim not in invalid_pos_arr:
                        for v in data[dt][label_dim]['data']:
                            v['label_pos'] = label_dim
                            row, stat_diff_info = get_x_line(v)
                            x_info_train.append({'data_len' : v['data_len'], 'avg_window' : v['avg_window'], 'good_count' : v['best'], 'qxc' : v['qxc'], 'label_pos' : label_dim, 'prob_cand_arr' : v['prob_cand_arr']})
                            x_data_train.append(row)
                            if data[dt][label_dim]['true_pos'] not in label_dim_cand[label_dim]:
                                print('不对了', data[dt][label_dim]['true_pos'], label_dim)
                                exit(0)
                            y_data_train.append(category_label_by_comparison(v['prob_cand_arr'][data[dt][label_dim]['true_pos']], v['pred']))
                            #y_data_train.append([1] if v['prob_cand_arr'][data[dt][label_dim]['true_pos']] >= v['pred'] else [0])
            result.append({'train' : {'x' : np.array(x_data_train), 'y' : np.array(y_data_train)}, 'test' : {'x' : np.array(x_data_test), 'y' : np.array(y_data_test)}, 'x_info_train' : x_info_train, 'x_info_test' : x_info_test})
    else:
        for dt in sorted_date:
            if exclude is not None and dt in exclude:
                pass
            elif target_dt is not None and dt in target_dt:
                pass                
            elif dt in test_date:
                pred[dt] = {}
                for label_dim in data[dt]:
                    if label_dim not in invalid_pos_arr:
                        pred[dt][label_dim] = {'x' : [], 'y' : [], 'data_len' : [], 'avg_window' : [], 'good_count' : [], 'qxc':[]}
                        for v in data[dt][label_dim]['data']:
                            v['label_pos'] = label_dim
                            row, stat_diff_info = get_x_line(v)
                            x_info_test.append({'data_len' : v['data_len'], 'avg_window' : v['avg_window'], 'good_count' : v['best'], 'qxc' : v['qxc'], 'label_pos' : label_dim, 'prob_cand_arr' : v['prob_cand_arr']})
                            x_data_test.append(row)
                            if data[dt][label_dim]['true_pos'] not in label_dim_cand[label_dim]:
                                print('不对了', data[dt][label_dim]['true_pos'], label_dim)
                                exit(0)
                            y_data_test.append([category_label_by_comparison(v['prob_cand_arr'][data[dt][label_dim]['true_pos']], v['pred'])])
                            #y_data_test.append([1] if v['prob_cand_arr'][data[dt][label_dim]['true_pos']] >= v['pred'] else [0])
                            pred[dt][label_dim]['x'].append(row)
                            pred[dt][label_dim]['y'].append([1] if v['prob_cand_arr'][data[dt][label_dim]['true_pos']] >= v['pred'] else [0])
                            pred[dt][label_dim]['data_len'].append(v['data_len'])
                            pred[dt][label_dim]['avg_window'].append(v['avg_window'])
                            pred[dt][label_dim]['good_count'].append(v['best'])
                            pred[dt][label_dim]['qxc'].append(v['qxc'])
            elif dt in train_date:
                for label_dim in data[dt]:
                    if label_dim not in invalid_pos_arr:
                        for v in data[dt][label_dim]['data']:
                            v['label_pos'] = label_dim
                            row, stat_diff_info = get_x_line(v)
                            x_info_train.append({'data_len' : v['data_len'], 'avg_window' : v['avg_window'], 'good_count' : v['best'], 'qxc' : v['qxc'], 'label_pos' : label_dim, 'prob_cand_arr' : v['prob_cand_arr']})
                            x_data_train.append(row)
                            if data[dt][label_dim]['true_pos'] not in label_dim_cand[label_dim]:
                                print('不对了', data[dt][label_dim]['true_pos'], label_dim)
                                exit(0)
                            y_data_train.append(category_label_by_comparison(v['prob_cand_arr'][data[dt][label_dim]['true_pos']], v['pred']))
                            #y_data_train.append([1] if v['prob_cand_arr'][data[dt][label_dim]['true_pos']] >= v['pred'] else [0])
        print('train label distribution:', category_distribution(y_data_train))
        print('test label distribution:', category_distribution(y_data_test))
        result = [{'train' : {'x' : np.array(x_data_train), 'y' : np.array(y_data_train)}, 'test' : {'x' : np.array(x_data_test), 'y' : np.array(y_data_test)}, 'x_info_train' : x_info_train, 'x_info_test' : x_info_test}]
    target_data_mode = 'BEST_STD'
    for dt in target_dt:
        target[dt] = {}
        for label_dim in target_data[dt]:
            if label_dim not in invalid_pos_arr:
                target[dt][label_dim] = {'x' : [], 'y' : [], 'data_len' : [], 'avg_window' : [], 'good_count' : [], 'qxc':[], 'prob_cand_arr' : [], 'pred' : [], 'stat_diff_info' : []}
                if target_data_mode == 'BEST_STD':
                    tmp = {}
                    for v in target_data[dt][label_dim]['data']:
                        tmp[v['data_len']] = v
                    for dl in target_data[dt][label_dim]['best_data_len']:
                        v = tmp[dl]
                        v['label_pos'] = label_dim
                        row, stat_diff_info = get_x_line(v)
                        target[dt][label_dim]['x'].append(row)
                        target[dt][label_dim]['data_len'].append(v['data_len'])
                        target[dt][label_dim]['avg_window'].append(v['avg_window'])
                        target[dt][label_dim]['good_count'].append(v['best'])
                        target[dt][label_dim]['qxc'].append(v['qxc'])
                        target[dt][label_dim]['stat_diff_info'].append(stat_diff_info)
                        target[dt][label_dim]['prob_cand_arr'].append(v['prob_cand_arr'])
                        target[dt][label_dim]['pred'].append(v['pred'])
                    for dl in target_data[dt][label_dim]['std_data_len']:
                        v = tmp[dl]
                        v['label_pos'] = label_dim
                        row, stat_diff_info = get_x_line(v)
                        target[dt][label_dim]['x'].append(row)
                        target[dt][label_dim]['data_len'].append(v['data_len'])
                        target[dt][label_dim]['avg_window'].append(v['avg_window'])
                        target[dt][label_dim]['good_count'].append(v['best'])
                        target[dt][label_dim]['qxc'].append(v['qxc'])
                        target[dt][label_dim]['stat_diff_info'].append(stat_diff_info)
                        target[dt][label_dim]['prob_cand_arr'].append(v['prob_cand_arr'])
                        target[dt][label_dim]['pred'].append(v['pred'])
                else:
                    for v in target_data[dt][label_dim]['data']:
                        v['label_pos'] = label_dim
                        row, stat_diff_info = get_x_line(v)
                        target[dt][label_dim]['x'].append(row)
                        target[dt][label_dim]['data_len'].append(v['data_len'])
                        target[dt][label_dim]['avg_window'].append(v['avg_window'])
                        target[dt][label_dim]['good_count'].append(v['best'])
                        target[dt][label_dim]['qxc'].append(v['qxc'])
                        target[dt][label_dim]['stat_diff_info'].append(stat_diff_info)
                        target[dt][label_dim]['prob_cand_arr'].append(v['prob_cand_arr'])
                        target[dt][label_dim]['pred'].append(v['pred'])
    for dt in [xxx for xxx in pred_date if xxx not in target]:
        pred[dt] = {}
        for label_dim in data[dt]:
            if label_dim not in invalid_pos_arr:
                pred[dt][label_dim] = {'x' : [], 'y' : [], 'data_len' : [], 'avg_window' : [], 'good_count' : [], 'qxc':[], 'stat_diff_info' : [], 'prob_cand_arr' : [], 'pred' : []}
                for v in data[dt][label_dim]['data']:
                    v['label_pos'] = label_dim
                    row, stat_diff_info = get_x_line(v)
                    pred[dt][label_dim]['x'].append(row)
                    pred[dt][label_dim]['y'].append([category_label_by_comparison(v['prob_cand_arr'][data[dt][label_dim]['true_pos']],v['pred'])])
                    pred[dt][label_dim]['data_len'].append(v['data_len'])
                    pred[dt][label_dim]['avg_window'].append(v['avg_window'])
                    pred[dt][label_dim]['good_count'].append(v['best'])
                    pred[dt][label_dim]['qxc'].append(v['qxc'])
                    pred[dt][label_dim]['stat_diff_info'].append(stat_diff_info)
                    pred[dt][label_dim]['prob_cand_arr'].append(v['prob_cand_arr'])
                    pred[dt][label_dim]['pred'].append(v['pred'])
    for dt in pred:
        for label in pred[dt]:
            pred[dt][label]['x'] = np.array(pred[dt][label]['x'])
            pred[dt][label]['y'] = np.array(pred[dt][label]['y'])
    for dt in target:
        for label in target[dt]:
            target[dt][label]['x'] = np.array(target[dt][label]['x'])
    return result, {'pred' : pred, 'target' : target}


def val(data):
    return data['left_01'] + data['right_01'] + data['left_02'] + data['right_02']


basic_date_pattern = re.compile(r'^\d{4}\d{2}\d{2}$')

def merge_sort_metadata(name, target):
    dts = set()
    labels = []
    cnts = []
    for label_dim in range(5 if 'plw' in name else (7 if 'qxc' in name else 3)):
        if not os.path.exists(name + '/' + target + '/confirm_' + str(label_dim) + '.txt'):
            latest_dict = {}
            for filename in os.listdir(name + '/' + target):
                if 'find_best_' + str(label_dim) in filename:
                    with open(name + '/' + target + '/' + filename) as f:
                        for line in f:
                            if len(line) > 5:
                                data = eval(line.replace('\n', ''))
                                if data['combine'][0] in latest_dict:
                                    if val(data) > val(latest_dict[data['combine'][0]]):
                                        latest_dict[data['combine'][0]].update(data)
                                else:
                                    latest_dict[data['combine'][0]] = data
            result = ''
            for v in sorted(latest_dict.values(), key=lambda x : (-val(x), x['combine'][0])):
                result += str(v) + '\n'
            with open(name + '/' + target + '/confirm_' + str(label_dim) + '.txt', 'w') as f:
                f.write(result)
        dtr, labelr, cnt = check_valid(name, target, label_dim)
        if 'N' not in dtr:
            dts.add(str(dtr))
        if labelr != 'N':
            labels.append(labelr)
        else:
            labels.append({'N'})
        cnts.append(cnt)
    print(dts, labels, cnts)

def general_merge_sort(name):
    for dt in sorted(os.listdir(name)):
        if basic_date_pattern.match(dt):
            merge_sort_metadata(name, dt)

def general_merge_detail(name):
    for dt in sorted(os.listdir(name + '/source')):
        if basic_date_pattern.match(dt):
            for label_dim in range(5 if 'plw' in name else (7 if 'qxc' in name else 3)):
                merge_detail(label_dim, name, dt, 'source/' + dt)

def merge_metadata(backup, latest):
    latest_dict = {}
    with open(latest, 'r') as f:
        for line in f:
            if len(line) > 5:
                data = eval(line.replace('\n', ''))
                latest_dict[data['combine'][0]] = data
    with open(backup, 'r') as f:
        for line in f:
            if len(line) > 5:
                data = eval(line.replace('\n', ''))
                if data['combine'][0] in latest_dict:
                    if val(data) > val(latest_dict[data['combine'][0]]):
                        latest_dict[data['combine'][0]].update(data)
                else:
                    latest_dict[data['combine'][0]] = data
    result = ''
    for v in latest_dict.values():
        result += str(v) + '\n'
    with open(latest, 'w') as f:
        f.write(result)

def merge_detail(label_dim, name, target, source):
    meta_set = set()
    data_set = set()
    data_move = False
    source_exist = False
    if not os.path.exists(name + '/' + target):
        os.makedirs(name + '/' + target)
    for filename in os.listdir(name + '/' + target):
        if 'find_best_' + str(label_dim) in filename:
            meta_set.add(filename)
        if 'detail_' + str(label_dim) in filename:
            data_set.add(filename)
    for filename in os.listdir(name + '/' + source):
        if 'find_best_' + str(label_dim) in filename:
            source_exist = True
            if filename not in meta_set:
                shutil.move(name + '/' + source + '/' + filename, name + '/' + target + '/' + filename)
            else:
                merge_metadata(name + '/' + source + '/' + filename, name + '/' + target + '/' + filename)
        if 'detail_' + str(label_dim) in filename:
            source_exist = True
            if filename not in data_set:
                shutil.move(name + '/' + source + '/' + filename, name + '/' + target + '/' + filename)
                data_move = True
    if source_exist:
        if (not data_move):
            print('merge')
            old = load_obj(name + '/' + target + '/detail_' + str(label_dim))
            new = load_obj(name + '/' + source + '/detail_' + str(label_dim))
            for i in range(len(new)):
                insert = True
                for j in range(len(old)):
                    if new[i]['data_len'] == old[j]['data_len']:
                        insert = False
                        cmp_cnt = 0
                        pattern_old = ''
                        pattern_new = ''
                        for k in ['left_01', 'right_01', 'left_02', 'right_02']:
                            pattern_new += str(new[i][k])
                            pattern_old += str(old[j][k])
                            if int(new[i][k]) >= int(old[j][k]):
                                cmp_cnt += 1
                        if cmp_cnt >= 3 or (pattern_new == '5566' and pattern_old == '4477'):
                            old[j] = new[i]
                        break
                if insert:
                    old.append(new[i])
            persist_obj(old, name + '/' + target + '/detail_' + str(label_dim))
        else:
            print('append')
        print(len(load_obj(name + '/' + target + '/detail_' + str(label_dim))))
        dts, labels, cnt = check_valid(name, target, str(label_dim))
        print('check valid:', dts, labels, cnt)
    else:
        print('no source')


def get_exist_combines(name):
    s = set()
    with open(name) as f:
        for line in f:
            pair = eval(line)['combine']
            s.add(str(pair[0]) + ',' + str(pair[1]))
    return s




def export_html_unit(name, item, metric_folder, date, label_dim, html_base):
    mp = {
        0 : 'ONE_HTML',
        1 : 'TWO_HTML',
        2 : 'THREE_HTML'
    }
    data_lens = [int(v) for v in item.split(',')]
    data = load_obj(name + '/' + metric_folder + '/detail_' + str(label_dim))
    cand = []
    for data_len in data_lens:
        for v in data:
            if v['data_len'] == data_len:
                cand.append([str(v['data_len']), v['prob_cand_html'].replace("'", '').replace('<br\\>', '<br>'), v['validate_html'].replace("'", '').replace('<br\\>', '<br>') + str(v['left_02']) + " - " + str(v['right_02']) + " - " + str(v['left_01']) + " - " + str(v['right_01']) + "-" + str(v['avg_window']) + "-" + str(v['drop_rate'])])
                break
    print(label_dim, len(cand))
    html_base = html_base.replace(mp[label_dim], str(cand)).replace('NOW_DATE', date)
    return html_base


def export_html(name, metric_folder, date):
    html_base_std = None
    html_base_acc = None
    html_base_gap = None
    with open('template.html', 'r', encoding='UTF-8') as f:
        html_base_std = f.read()
    with open('template.html', 'r', encoding='UTF-8') as f:
        html_base_acc = f.read()
    for l in range(5 if name == 'plw' else (7 if 'qxc' in name else 3)):
        html_base_acc = export_html_unit(name, get_best_item(name, l, True, metric_folder)[0], metric_folder, date, l, html_base_acc)
        html_base_std = export_html_unit(name, get_best_item(name, l, False, metric_folder)[0], metric_folder, date, l, html_base_std)
    with open(name + '/archive/latest/accuracy/pred_' + date + '.html', 'w', encoding='UTF-8') as f:
        f.write(html_base_acc)
    with open(name + '/archive/latest/std/pred_' + date + '.html', 'w', encoding='UTF-8') as f:
        f.write(html_base_std)

def check_valid(name, target, label):
    if not os.path.exists(name + '/' +target + '/detail_' + str(label) + '.pkl'):
        return 'N', 'N', -1
    data = load_obj(name + '/' +target + '/detail_' + str(label))
    dt = set()
    l = set()
    for v in data:
        dt.add(v['qxc'][0])
        l.add(v['qxc'][int(label) + 1])
    return dt, l, len(data)

if __name__ == '__main__':
    args = sys.argv
    if args[1] == 'HTML':
        export_html(args[2], args[3], args[4])
    elif args[1] == 'MERGE':
        merge_detail(args[2], args[3], args[4], args[5])




# python base.py HTML qxc 20260104 2026-01-06
# python base.py PROCESS qxc 0
# python base.py MERGE 0 qxc 20260417 metric