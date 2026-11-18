
from base import *
import sys,os
import uuid
import shutil
import ssl
import builtins
import numpy
ssl._create_default_https_context = ssl._create_unverified_context

try:
    from tensorflow.keras.backend import clear_session
    import tensorflow as tf
    from keras_kit import *
    # tf.config.experimental.set_visible_devices([], 'GPU')
except:
    pass

from sklearn.metrics import accuracy_score


MODE_FIND = 'MODE_FIND'
MODE_SHOW = 'MODE_SHOW'
USE_MODE_CNN = 'USE_MODE_CNN'
USE_MODE_DART = 'USE_MODE_DART'

def previous_draw_date(date_str: str) -> str:
    if len(date_str) != 8 or not date_str.isascii() or not date_str.isdigit():
        raise ValueError("日期必须是 YYYYMMDD 格式的 8 位数字")
    input_date = datetime.strptime(date_str, "%Y%m%d").date()
    target_weekdays = (1, 4, 6)
    days_back = builtins.min(
        (input_date.weekday() - weekday) % 7 or 7
        for weekday in target_weekdays
    )
    return (input_date - timedelta(days=days_back)).strftime("%Y%m%d")


def prepare_cnn_inner(raw, label_dim, drop_rate):
    dim_size = DIMENSION
    inputs = raw['x']
    use1d = len(inputs.shape) < 4
    outputs = Conv1D(filters=dim_size, kernel_size=5, activation=PReLU())(inputs) if use1d else Conv2D(filters=dim_size, kernel_size=(1,1),strides=(1,1), activation=PReLU())(inputs)
    outputs = Conv1D(filters=dim_size, kernel_size=1, activation=PReLU())(outputs) if use1d else Conv2D(filters=dim_size, kernel_size=(1,1),strides=(1,1), activation=PReLU())(outputs)
    outputs = Flatten()(outputs)
    outputs = Dropout(drop_rate)(outputs)
    outputs = Dense(label_dim)(outputs)
    print('what drop rate:', drop_rate)
    return outputs


def for_secondary_train(train_x, train_pred, train_y, test_x, test_pred, test_y, pred_x, pred_pred, pred_y, target_x, target_pred):
    train_y_new = []
    test_y_new = []
    pred_y_new = []
    for i in range(len(train_y)):
        train_y_new.append(1 if float(train_y[i][0]) >= float(train_pred[i][0]) else 0)
    for i in range(len(test_y)):
        test_y_new.append(1 if float(test_y[i][0]) >= float(test_pred[i][0]) else 0)
    for i in range(len(pred_y)):
        pred_y_new.append(1 if float(pred_y[i][0]) >= float(pred_pred[i][0]) else 0)
    return {'train' : {'x' : train_x, 'y' : np.array(train_y_new)}, 'test' : {'x' : test_x, 'y' : np.array(test_y_new)}, 'pred' : {'x' : pred_x, 'y' : np.array(pred_y_new)}, 'target' : {'x' : target_x, 'y' : None}}


from sklearn import svm
from sklearn.svm import *
from sklearn.linear_model import *
from sklearn.gaussian_process import *
from sklearn.gaussian_process.kernels import *
from sklearn.naive_bayes import *
from sklearn.tree import *
from sklearn.ensemble import *



def debug_pred_target(result, result_merge):
    stat = {}
    for dt in sorted(result):
        for label in result[dt]:
            result_item = result[dt][label]
            current_len = len(result[dt][label]['x'])
            for i in range(current_len):
                merge_value = result_merge[dt][label][i]
                aw = result_item['avg_window'][i]
                gc = result_item['good_count'][i]
                if result_item['data_len'][i] < 200:
                    dl = 'a'
                elif result_item['data_len'][i] < 400:
                    dl = 'b'
                elif result_item['data_len'][i] < 600:
                    dl = 'c'
                elif result_item['data_len'][i] < 800:
                    dl = 'd'
                elif result_item['data_len'][i] < 1000:
                    dl = 'e'
                elif result_item['data_len'][i] < 1200:
                    dl = 'f'
                elif result_item['data_len'][i] < 1400:
                    dl = 'g'
                elif result_item['data_len'][i] < 1600:
                    dl = 'h'
                if dt in stat:
                    if 'total' in stat[dt]:
                        stat[dt]['total'] += 1
                    else:
                        stat[dt]['total'] = 1
                else:
                    stat[dt] = {
                        'neg' : 0.0,
                        'pos' : 0.0,
                        'total' :  1.0, 
                        'aw' : {}, 
                        'gc' : {}, 
                        'dl' : {}, 
                        'label' : {
                            0:{
                                'neg' : 0.0, 
                                'pos' : 0.0,
                                'stat_diff_info' : [0.0,0.0,0.0,0.0,0.0,0.0,0.0],
                                'coarse_acc_rate' : [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                                'pred_category' : {0:0,1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0},
                                'merge_value_arr' : [],
                                'aw' : {},
                                'gc' : {},
                                'dl' : {},
                                'norm_diff_arr' : [[] for z in range(10)]
                            },
                            1:{
                                'neg' : 0.0, 
                                'pos' : 0.0,
                                'stat_diff_info' : [0.0,0.0,0.0,0.0,0.0,0.0,0.0],
                                'coarse_acc_rate' : [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                                'pred_category' : {0:0,1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0},
                                "merge_value_arr" : [],
                                'aw' : {},
                                'gc' : {},
                                'dl' : {},
                                'norm_diff_arr' : [[] for z in range(10)]
                            },
                            2:{
                                'neg' : 0.0, 
                                'pos' : 0.0,
                                'stat_diff_info' : [0.0,0.0,0.0,0.0,0.0,0.0,0.0],
                                'coarse_acc_rate' : [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                                'pred_category' : {0:0,1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0},
                                "merge_value_arr" : [],
                                'aw' : {},
                                'gc' : {},
                                'dl' : {},
                                'norm_diff_arr' : [[] for z in range(10)]
                            },
                            3:{
                                'neg' : 0.0, 
                                'pos' : 0.0,
                                'stat_diff_info' : [0.0,0.0,0.0,0.0,0.0,0.0,0.0],
                                'coarse_acc_rate' : [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                                'pred_category' : {0:0,1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0},
                                "merge_value_arr" : [],
                                'aw' : {},
                                'gc' : {},
                                'dl' : {},
                                'norm_diff_arr' : [[] for z in range(10)]
                            },
                            4:{
                                'neg' : 0.0, 
                                'pos' : 0.0,
                                'stat_diff_info' : [0.0,0.0,0.0,0.0,0.0,0.0,0.0],
                                'coarse_acc_rate' : [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                                'pred_category' : {0:0,1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0},
                                "merge_value_arr" : [],
                                'aw' : {},
                                'gc' : {},
                                'dl' : {},
                                'norm_diff_arr' : [[] for z in range(10)]
                            },
                            5:{
                                'neg' : 0.0, 
                                'pos' : 0.0,
                                'stat_diff_info' : [0.0,0.0,0.0,0.0,0.0,0.0,0.0],
                                'coarse_acc_rate' : [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                                'pred_category' : {0:0,1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0},
                                "merge_value_arr" : [],
                                'aw' : {},
                                'gc' : {},
                                'dl' : {},
                                'norm_diff_arr' : [[] for z in range(10)]
                            },
                            6:{
                                'neg' : 0.0, 
                                'pos' : 0.0,
                                'stat_diff_info' : [0.0,0.0,0.0,0.0,0.0,0.0,0.0],
                                'coarse_acc_rate' : [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                                'pred_category' : {0:0,1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0,13:0,14:0},
                                "merge_value_arr" : [],
                                'aw' : {},
                                'gc' : {},
                                'dl' : {},
                                'norm_diff_arr' : [[] for z in range(15)]
                            }
                        }
                    }
                stat[dt]['label'][label]['merge_value_arr'].append(merge_value)
                if merge_value < 0.1:
                    stat[dt]['label'][label]['pred_category'][0] += 1.0 / current_len
                elif merge_value < 0.2:
                    stat[dt]['label'][label]['pred_category'][1] += 1.0 / current_len
                elif merge_value < 0.3:
                    stat[dt]['label'][label]['pred_category'][2] += 1.0 / current_len
                elif merge_value < 0.4:
                    stat[dt]['label'][label]['pred_category'][3] += 1.0 / current_len
                elif merge_value < 0.5:
                    stat[dt]['label'][label]['pred_category'][4] += 1.0 / current_len
                elif merge_value < 0.6:
                    stat[dt]['label'][label]['pred_category'][5] += 1.0 / current_len
                elif merge_value < 0.7:
                    stat[dt]['label'][label]['pred_category'][6] += 1.0 / current_len
                elif merge_value < 0.8:
                    stat[dt]['label'][label]['pred_category'][7] += 1.0 / current_len
                elif merge_value < 0.9:
                    stat[dt]['label'][label]['pred_category'][8] += 1.0 / current_len
                else:
                    stat[dt]['label'][label]['pred_category'][9] += 1.0 / current_len
                current_sdi = result_item['stat_diff_info'][i]
                current_prob_cand_arr = result_item['prob_cand_arr'][i]
                current_pred = result_item['pred_as_label'][i]
                ###搞事情开始
                # current_diff = [v - current_pred for v in current_prob_cand_arr]
                # current_diff_abs = [abs(v) for v in current_diff]
                # current_diff_max  = max(current_diff_abs)
                # current_diff_min = min(current_diff_abs)
                # current_diff_value = [(current_diff_abs[i] * (1.0 if current_diff[i] >= 0 else -1.0) - current_diff_min) / (current_diff_max - current_diff_min) for i in range(len(current_diff_abs))]
                # for j in range(len(current_diff)):
                #     stat[dt]['label'][label]['norm_diff_arr'][j].append(current_diff_value[j])
                ###搞事情结束
                for j in range(len(current_prob_cand_arr)):
                    stat[dt]['label'][label]['coarse_acc_rate'][j] += ((1.0 / current_len) if (merge_value >= 0.5 and current_prob_cand_arr[j] >= current_pred or merge_value < 0.5 and current_prob_cand_arr[j] < current_pred) else 0.0)
                for j in range(len(current_sdi)):
                    stat[dt]['label'][label]['stat_diff_info'][j] += (current_sdi[j] * 1.0 / current_len)
                dict_stat(stat[dt]['aw'], aw)
                dict_stat(stat[dt]['gc'], gc)
                dict_stat(stat[dt]['dl'], dl)
                dict_stat(stat[dt]['label'][label]['aw'], aw)
                dict_stat(stat[dt]['label'][label]['dl'], dl)
                dict_stat(stat[dt]['label'][label]['gc'], gc)
                if i < len(result_item['y']):
                    if merge_value < 0.5 and int(result_item['y'][i]) == 1 or merge_value >= 0.5 and int(result_item['y'][i]) == 0:
                        if 'neg' in stat[dt]['label'][label]:
                            stat[dt]['label'][label]['neg'] += 1
                        else:
                            stat[dt]['label'][label]['neg'] = 1
                        if 'neg' in stat[dt]:
                            stat[dt]['neg'] += 1
                        else:
                            stat[dt]['neg'] = 1
                    if merge_value >= 0.5 and int(result_item['y'][i]) == 1 or merge_value < 0.5 and int(result_item['y'][i]) == 0:
                        if 'pos' in stat[dt]['label'][label]:
                            stat[dt]['label'][label]['pos'] += 1
                        else:
                            stat[dt]['label'][label]['pos'] = 1
                        if 'pos' in stat[dt]:
                            stat[dt]['pos'] += 1
                        else:
                            stat[dt]['pos'] = 1
            stat[dt]['label'][label]['coarse_acc_rate'] = ['{:.2f}'.format(1.0 - v) for v in stat[dt]['label'][label]['coarse_acc_rate']]
            stat[dt]['label'][label]['stat_diff_info'] = ['{:.2f}'.format(v) for v in stat[dt]['label'][label]['stat_diff_info']]
            pc = stat[dt]['label'][label]['pred_category']
            stat[dt]['label'][label]['pred_category'] = {k : '{:.2f}'.format(pc[k]) for k in pc}
    for dt in sorted(result):
        print('\n')
        total = stat[dt]['neg'] + stat[dt]['pos']
        total = total if total > 0 else 1.0
        print(dt, ['{:.2f}'.format(stat[dt]['neg'] / total)], '{:.2f}'.format(stat[dt]['pos'] / total), stat[dt]['neg'], stat[dt]['pos'], stat[dt]['total'])
        for label in range(7):
            label_total = stat[dt]['label'][label]['neg'] + stat[dt]['label'][label]['pos']
            label_total = label_total if label_total > 0 else 1.0
            # pc = []
            # for i in range(10 if label < 6 else 15):
            #     pc.append('{:.2f}'.format(np.corrcoef(stat[dt]['label'][label]['merge_value_arr'], stat[dt]['label'][label]['norm_diff_arr'][i])[0][1]))
            print(label, ['{:.2f}'.format(stat[dt]['label'][label]['neg'] / label_total)], stat[dt]['label'][label]['neg'], stat[dt]['label'][label]['pos'], stat[dt]['label'][label]['stat_diff_info'], stat[dt]['label'][label]['coarse_acc_rate'], stat[dt]['label'][label]['pred_category'])
            #print(label, ['{:.2f}'.format(stat[dt]['label'][label]['neg'] / label_total)], stat[dt]['label'][label]['neg'], stat[dt]['label'][label]['pos'], pc)


def model_vote(name_list, data_arr, verbose=True, method='AVG', label_pos=None, pred_target=None, debug=True):
    result_merge = {
        'pred' : {},
        'target' : {}
    }
    for k in result_merge:
        pred = pred_target[k]
        for dt in pred:
            result_merge[k][dt] = {}
            for label in pred[dt]:
                result_merge[k][dt][label] = [0 for i in range(len(pred[dt][label]['x']))] if method=='AVG' else [{1:0,0:0} for i in range(len(pred[dt][label]['x']))]
    accuracy_list = []
    y = {'pred' : [], 'target' : []}
    pred = {'pred' : [], 'target' : []}
    num = 0
    for name in name_list:
        for data in data_arr:
            print('当前是cv第:%s轮' % num)
            num += 1
            accuracy, pred_result, target_result = model_select(name, data, True, label_pos, pred_target)
            accuracy_list.append(accuracy)
            for dt in result_merge['pred']:
                for label in result_merge['pred'][dt]:
                    for i in range(len(result_merge['pred'][dt][label])):
                        if method == 'AVG':
                            result_merge['pred'][dt][label][i] += pred_result[dt][label]['pred'][i] * accuracy
                        else:
                            if pred_result[dt][label]['pred'][i] >= 0.5:
                                result_merge['pred'][dt][label][i][1] += 1
                            else:
                                result_merge['pred'][dt][label][i][0] += 1
            for dt in result_merge['target']:
                for label in result_merge['target'][dt]:
                    for i in range(len(result_merge['target'][dt][label])):
                        if method == 'AVG':
                            result_merge['target'][dt][label][i] += target_result[dt][label]['pred'][i] * accuracy
                        else:
                            if target_result[dt][label]['pred'][i] >= 0.5:
                                result_merge['target'][dt][label][i][1] += 1
                            else:
                                result_merge['target'][dt][label][i][0] += 1
    for k in result_merge:
        for dt in result_merge[k]:
            for label in result_merge[k][dt]:
                if method == 'AVG':
                    result_merge[k][dt][label] = [v / float(sum(accuracy_list)) for v in result_merge[k][dt][label]]
                else:
                    result_merge[k][dt][label] = [1 if v[1] >= v[0] else 0 for v in result_merge[k][dt][label]]
                for v in result_merge[k][dt][label]:
                    pred[k].append(1 if v >= 0.5 else 0)
                #只有pred有标签,target没有
                if k == 'pred':
                    for v in pred_result[dt][label]['y']:
                        y[k].append(1 if v >= 0.5 else 0)
    accuracy = accuracy_score(pred['pred'], y['pred'])
    print("\npred_merge_accuarcy: %.2f%%" % (accuracy*100.0))
    if debug:
        print('here is pred:', len(pred_result))
        debug_pred_target(pred_result, result_merge['pred'])
        print('here is target:', len(target_result))
        debug_pred_target(target_result, result_merge['target'])




def model_select(name, data, verbose=False, label_pos=None, pred_target=None):
    if name == 'XGB':
        model = XGBClassifier(
            learning_rate=0.01,
            n_estimators=300,           # 树的个数--1000棵树建立xgboost
            max_depth=6,                # 树的深度
            min_child_weight = 1,       # 叶子节点最小权重
            gamma=0.,                   # 惩罚项中叶子结点个数前的参数
            subsample=0.8,              # 随机选择80%样本建立决策树
            colsample_btree=0.8,        # 随机选择80%特征建立决策树
            objective='binary:logistic',# 指定损失函数
            scale_pos_weight=1,         # 解决样本个数不平衡的问题
            # random_state=27             # 随机数
        )
    elif name == 'SVM':
        model = svm.SVC(
            kernel='linear',
            verbose=verbose,
            tol=0.00001,
            gamma='scale',
            max_iter=7500,
            probability=True,
            C=0.4,
            )
    elif name == 'SGD':
        model = SGDClassifier(
            epsilon=0.08, 
            loss="epsilon_insensitive", 
            penalty="l2", 
            verbose=1 if verbose else 0, 
            max_iter=1000, 
            alpha=0.0001, 
            tol=0.00001, 
            n_jobs=-1
            )
    elif name == 'LINEAR':
        model = RidgeClassifier(
            alpha=1, 
            fit_intercept=True, 
            copy_X=True, 
            max_iter=None, 
            tol=0.0001, 
            class_weight=None, 
            solver='lsqr', 
            positive=False,
            random_state=None
            )
    elif name == 'LOGISTIC':
        model = LogisticRegression(
            penalty='l2', 
            C=2.5, 
            l1_ratio=0.5,
            dual=False, 
            tol=0.0001, 
            fit_intercept=True, 
            intercept_scaling=1, 
            class_weight=None, 
            random_state=None, 
            solver='liblinear', 
            max_iter=7500, 
            verbose=1 if verbose else 0, 
            warm_start=False, 
            n_jobs=100)
    elif name == 'TREE':
        model = DecisionTreeClassifier(
            criterion='gini', 
            splitter='best', 
            max_depth=None, 
            min_samples_split=2, 
            min_samples_leaf=2, 
            min_weight_fraction_leaf=0.45, 
            max_features=None, 
            random_state=None, 
            max_leaf_nodes=None, 
            min_impurity_decrease=0.1, 
            class_weight=None, 
            ccp_alpha=0.09, 
            monotonic_cst=None)
    elif name == 'GBDT':
        model = HistGradientBoostingClassifier(
            loss='log_loss', 
            learning_rate=0.04, 
            max_iter=100, 
            max_leaf_nodes=31, 
            max_depth=None, 
            min_samples_leaf=25, 
            l2_regularization=0.0, 
            max_features=1.0, 
            max_bins=255, 
            categorical_features='from_dtype', 
            monotonic_cst=None, 
            interaction_cst=None, 
            warm_start=False, 
            early_stopping=False, 
            scoring=None, 
            validation_fraction=0.1, 
            n_iter_no_change=10, 
            tol=1e-07, 
            verbose=1 if verbose else 0, 
            random_state=None, 
            class_weight=None)
    if name == 'CNN':
        train_result, test_result, pred_result, target_result, secondary_data = model_train_and_predict(train=data['train'], test=data['test'], pred=pred_target['pred'], target=pred_target['target'], debug=(mode==MODE_SHOW), label_mode='CAT', drop_rate=0.01, remaining=None, checkpoint=True, for_secondary_train=None, direct=False)
        train_result['y'] = train_result['y'].flatten().tolist()
        train_result['pred'] = train_result['pred'].flatten().tolist()
        test_result['y'] = test_result['y'].flatten().tolist()
        test_result['pred'] = test_result['pred'].flatten().tolist()
        for dt in pred_result:
            for label in pred_result[dt]:
                pred_result[dt][label]['x'] = pred_result[dt][label]['x'].tolist()
                pred_result[dt][label]['y'] = pred_result[dt][label]['y'].flatten().tolist()
                pred_result[dt][label]['pred'] = pred_result[dt][label]['pred'].flatten().tolist()
        for dt in target_result:
            for label in target_result[dt]:
                target_result[dt][label]['x'] = target_result[dt][label]['x'].tolist()
                #target_result[dt][label]['y'] = target_result[dt][label]['y'].flatten().tolist()
                target_result[dt][label]['pred'] = target_result[dt][label]['pred'].flatten().tolist()
    else:
        if name == 'XGB':
            model.fit(
                data['trainX'],
                data['trainY'],
                eval_set = [(data['testX'],data['testY'])],
                # eval_metric = "logloss",
                # early_stopping_rounds = 10,
                verbose = verbose)
        else:
            model.fit(data['trainX'],data['trainY'])
        test_pred = model.predict(data['testX']).tolist() if name in ['LINEAR', 'SGD'] else [v[1] for v in model.predict_proba(data['testX']).tolist()]
        target_pred = {}
        for dt in data['target']:
            target_pred[dt] = {}
            for label_dim in data['target'][dt]:
                target_pred[dt][label_dim] = {'data_len' : data['target'][dt][label_dim]['data_len'], 'avg_window' : data['target'][dt][label_dim]['avg_window']}
                target_pred[dt][label_dim]['pred'] = model.predict(data['target'][dt][label_dim]['x']).tolist() if name in ['LINEAR', 'SGD'] else [v[1] for v in model.predict_proba(data['target'][dt][label_dim]['x']).tolist()]
    y = []
    pred = []
    for dt in pred_result:
        for label in pred_result[dt]:
            for i in range(len(pred_result[dt][label]['y'])):
                y.append(pred_result[dt][label]['y'][i])
                pred.append(pred_result[dt][label]['pred'][i])
    pred_acc = accuracy_score([1 if v >= 0.5 else 0 for v in y], [1 if v >= 0.5 else 0 for v in pred])
    test_acc = accuracy_score([1 if v >= 0.5 else 0 for v in test_result['y']], [1 if v >= 0.5 else 0 for v in test_result['pred']])
    print("\npred accuarcy: %.2f%%" % (pred_acc*100.0))
    print("\ntest accuarcy: %.2f%%" % (test_acc*100.0))
    return test_acc, pred_result, target_result

def prepare_cnn_category_model(raw, label_dim, drop_rate):
    outputs = prepare_cnn_inner(raw, label_dim, drop_rate)
    outputs = Activation(activation='sigmoid')(outputs)
    return outputs

def prepare_cnn_regression_model(raw, label_dim, drop_rate):
    outputs = prepare_cnn_inner(raw, label_dim, drop_rate)
    outputs = Activation(PReLU())(outputs)
    return outputs


def model_train_and_predict(train=None, test=None, pred=None, target=True, debug=True, label_mode='REG', drop_rate=None, direct=True, remaining=None):
    train['x'] = np.transpose(train['x'], (0, 2, 1))
    test['x'] = np.transpose(test['x'], (0, 2, 1))
    pred['x'] = np.transpose(pred['x'], (0, 2, 1))
    target['x'] = np.transpose(target['x'], (0, 2, 1))
    if label_mode not in ['REG', 'CAT']:
        raise ValueError('label_mode must be REG, CAT')
    label_dim = len(train['y'][0]) if (isinstance(train['y'][0], list) or isinstance(train['y'][0], numpy.ndarray)) else 1
    inputs = {
        'x' : Input(shape=(train['x'][0].shape), name='x'),
    }
    if debug:
        print('input shape')
        print('train', train['x'].shape)
        print('test', test['x'].shape)
        print('pred', pred['x'].shape)
        print('target', target['x'].shape)
    outputs = None
    if label_mode == 'CAT':
        output_dim = label_dim
        prepare_model_func = prepare_cnn_category_model
    else:
        output_dim = label_dim
        prepare_model_func = prepare_cnn_regression_model
    outputs = prepare_model_func(inputs, output_dim, drop_rate)
    model = Model(inputs=inputs, outputs=outputs)
    #categorical_focal_crossentropy
    #categorical_accuracy
    #binary_focal_crossentropy
    #binary_crossentropy
    #binary_accuracy
    #AdamW
    focalLoss = BinaryFocalCrossentropy(alpha=0.85,gamma=2)
    #focalLoss = CategoricalFocalCrossentropy(alpha=0.75,gamma=2)
    normalLoss = BinaryCrossentropy()
    #normalLoss = CategoricalCrossentropy()
    batch_size=32
    if label_mode == 'CAT':
        monitor_name = 'val_binary_accuracy'
        monitor_mode = 'max'
        model.compile(optimizer=AdamW(learning_rate=0.00001), loss=focalLoss, metrics=["binary_accuracy"])
    else:
        monitor_name = 'val_loss'
        monitor_mode = 'min'
        model.compile(optimizer=AdamW(learning_rate=0.0001), loss='log_cosh')
    if debug:
        print(model.summary())
    print('real length:', 'train', len(train['x']), 'test', len(test['x']))
    if remaining is not None:
        print('remaining: ' + str(remaining) +' rounds')
    checkpoint_filepath = label_mode + '_' + str(uuid.uuid1()).replace('-', '') + '.weights.h5'
    model_checkpoint_callback = keras.callbacks.ModelCheckpoint(
        filepath=checkpoint_filepath,
        save_weights_only=True,
        monitor=monitor_name,
        mode=monitor_mode,
        save_best_only=True)
    history = model.fit({'x': train['x']}, train['y'], 
        validation_data=({'x': test['x']}, test['y']),
        batch_size=batch_size,
        callbacks=[model_checkpoint_callback],
        epochs=120,
        verbose=debug)
    # if debug and label_mode=='CAT':
    #     import matplotlib.pyplot as plt
    #     # 获取训练和验证的准确率
    #     acc = history.history['binary_accuracy']
    #     val_acc = history.history['val_binary_accuracy']
    #     # 获取每个epoch的索引
    #     epochs = range(1, len(acc) + 1)
    #     # 绘制训练和验证的准确率
    #     plt.plot(epochs, acc, 'bo', label='Training acc')
    #     plt.plot(epochs, val_acc, 'b', label='Validation acc')
    #     plt.title('Training and validation accuracy')
    #     plt.xlabel('Epochs')
    #     plt.ylabel('Accuracy')
    #     plt.legend()
    #     plt.show()
    model.load_weights(checkpoint_filepath)
    secondary_data = None
    test_pred = model.predict({'x': test['x']}, batch_size=batch_size)
    train_pred = model.predict({'x': train['x']}, batch_size=batch_size)
    train_result = {'y' : train['y'], 'pred' : train_pred}
    test_result = {'y' : test['y'], 'pred' : test_pred}
    pred_result = {}
    target_result = {}
    if direct:
        if pred is not None and 'y' in pred:
            pred_y = [pred['y'][i] for i in range(len(pred['y']))]
            del pred['y']
            pred_pred = model.predict(pred, batch_size=batch_size)
            pred_result['y'] = pred_y
            pred_result['pred'] = pred_pred
        else:
            pred_pred = None
            pred_y = None
        if target is not None and 'y' in target:
            target_y = [target['y'][i] for i in range(len(target['y']))]
            del target['y']
            target_pred = model.predict(target, batch_size=batch_size)
            target_result['y'] = target_y
            target_result['pred'] = target_pred
        else:
            target_pred = None
            target_y = None
    else:
        for dt in pred:
            pred_result[dt] = {}
            pred_x = {}
            for label_dim in pred[dt]:
                pred_x[label_dim] = {'x' : pred[dt][label_dim]['x']}
                pred_result[dt][label_dim] = {'data_len' : pred[dt][label_dim]['data_len'], 'avg_window' : pred[dt][label_dim]['avg_window'], 'good_count' : pred[dt][label_dim]['good_count'], 'qxc' : pred[dt][label_dim]['qxc'], 'stat_diff_info' : pred[dt][label_dim]['stat_diff_info'], 'prob_cand_arr' : pred[dt][label_dim]['prob_cand_arr'], 'pred_as_label' : pred[dt][label_dim]['pred']}
                pred_result[dt][label_dim]['y'] = pred[dt][label_dim]['y']
                pred_result[dt][label_dim]['x'] = pred[dt][label_dim]['x']
                pred_result[dt][label_dim]['pred'] = model.predict(pred_x[label_dim], batch_size=batch_size)
        for dt in target:
            target_result[dt] = {}
            target_x = {}
            for label_dim in target[dt]:
                target_x[label_dim] = {'x' : target[dt][label_dim]['x']} 
                target_result[dt][label_dim] = {'data_len' : target[dt][label_dim]['data_len'], 'avg_window' : target[dt][label_dim]['avg_window'], 'good_count' : target[dt][label_dim]['good_count'], 'qxc' : target[dt][label_dim]['qxc'], 'stat_diff_info' : target[dt][label_dim]['stat_diff_info'], 'prob_cand_arr' : target[dt][label_dim]['prob_cand_arr'], 'pred_as_label' : target[dt][label_dim]['pred']}
                target_result[dt][label_dim]['y'] = target[dt][label_dim]['y']
                target_result[dt][label_dim]['x'] = target[dt][label_dim]['x']
                target_result[dt][label_dim]['pred'] = model.predict(target_x[label_dim], batch_size=batch_size)
    clear_session()
    del model
    try:
        os.remove(checkpoint_filepath)
    except:
        pass
    return train_result, test_result, pred_result, target_result


def model_train_and_predict_by_torch(train=None, test=None, pred=None, target=True, debug=True, label_mode='REG', drop_rate=None, direct=True, remaining=None, device=None, torch_num_threads=1):
    """Train and predict with the CNN topology used by model_train_and_predict.

    The function keeps model state, tensors, and the best checkpoint in the current
    process. Set ``device='cuda:0'`` to require the first CUDA GPU. Limiting each
    independent process to one PyTorch CPU thread prevents eight GPU jobs from
    oversubscribing the host CPU.
    """
    import torch
    import torch.nn as nn
    import torch.nn.functional as torch_functional
    from torch.utils.data import DataLoader, TensorDataset

    if label_mode not in ['REG', 'CAT']:
        raise ValueError('label_mode must be REG or CAT')
    if drop_rate is None:
        raise ValueError('drop_rate must be provided')
    if torch_num_threads is not None:
        torch.set_num_threads(int(torch_num_threads))

    if device is None:
        device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
    torch_device = torch.device(device)
    if torch_device.type == 'cuda':
        if not torch.cuda.is_available():
            raise RuntimeError('CUDA was requested but is not available to PyTorch')
        torch.cuda.set_device(torch_device)

    def prepare_x(values):
        values = np.asarray(values, dtype=np.float32)
        if values.ndim == 3:
            # This is the same (batch, axis_2, axis_1) layout produced by the
            # TensorFlow implementation's np.transpose(..., (0, 2, 1)).
            return np.transpose(values, (0, 2, 1)).copy()
        if values.ndim == 4:
            # The TensorFlow Conv2D branch expects channels-last NHWC input.
            return values.copy()
        raise ValueError('CNN inputs must be rank-3 for Conv1D or rank-4 for Conv2D')

    train_x = prepare_x(train['x'])
    test_x = prepare_x(test['x'])
    train_y = np.asarray(train['y'], dtype=np.float32)
    test_y = np.asarray(test['y'], dtype=np.float32)
    if train_y.ndim == 1:
        train_y = train_y.reshape(-1, 1)
    if test_y.ndim == 1:
        test_y = test_y.reshape(-1, 1)
    label_dim = train_y.shape[1]
    is_1d = train_x.ndim == 3

    class ElementwisePReLU(nn.Module):
        def __init__(self, shape):
            super().__init__()
            self.weight = nn.Parameter(torch.zeros(shape))

        def forward(self, values):
            return torch.where(values >= 0, values, self.weight * values)

    class TorchCNN(nn.Module):
        def __init__(self):
            super().__init__()
            if is_1d:
                # Keras Conv1D consumes (batch, steps, channels); PyTorch uses
                # (batch, channels, steps), hence the conversion in forward().
                input_length, input_channels = train_x.shape[1:]
                output_length = input_length - 4
                if output_length < 1:
                    raise ValueError('Conv1D requires an input length of at least 5')
                self.conv1 = nn.Conv1d(input_channels, DIMENSION, kernel_size=5)
                self.prelu1 = ElementwisePReLU((1, DIMENSION, output_length))
                self.conv2 = nn.Conv1d(DIMENSION, DIMENSION, kernel_size=1)
                self.prelu2 = ElementwisePReLU((1, DIMENSION, output_length))
                flattened_size = DIMENSION * output_length
            else:
                input_height, input_width, input_channels = train_x.shape[1:]
                self.conv1 = nn.Conv2d(input_channels, DIMENSION, kernel_size=(1, 1), stride=(1, 1))
                self.prelu1 = ElementwisePReLU((1, DIMENSION, input_height, input_width))
                self.conv2 = nn.Conv2d(DIMENSION, DIMENSION, kernel_size=(1, 1), stride=(1, 1))
                self.prelu2 = ElementwisePReLU((1, DIMENSION, input_height, input_width))
                flattened_size = DIMENSION * input_height * input_width
            self.is_1d = is_1d
            self.dropout = nn.Dropout(drop_rate)
            self.output = nn.Linear(flattened_size, label_dim)
            self.output_activation = nn.Sigmoid() if label_mode == 'CAT' else ElementwisePReLU((1, label_dim))

        def forward(self, values):
            if self.is_1d:
                values = values.permute(0, 2, 1)
            else:
                values = values.permute(0, 3, 1, 2)
            values = self.prelu1(self.conv1(values))
            values = self.prelu2(self.conv2(values))
            values = torch.flatten(values, start_dim=1)
            values = self.dropout(values)
            return self.output_activation(self.output(values))

    def loss_function(outputs, labels):
        if label_mode == 'CAT':
            # Keras BinaryFocalCrossentropy defaults apply_class_balancing=False;
            # alpha=0.85 in the existing function therefore does not affect loss.
            clipped = outputs.clamp(min=1e-7, max=1.0 - 1e-7)
            probability_of_truth = labels * clipped + (1.0 - labels) * (1.0 - clipped)
            return (-(1.0 - probability_of_truth).pow(2) * torch.log(probability_of_truth)).mean()
        difference = outputs - labels
        return (difference + torch_functional.softplus(-2.0 * difference) - np.log(2.0)).mean()

    def predict(values, batch_size):
        value_tensor = torch.as_tensor(prepare_x(values), dtype=torch.float32)
        value_loader = DataLoader(
            TensorDataset(value_tensor),
            batch_size=batch_size,
            shuffle=False,
            num_workers=0,
            pin_memory=torch_device.type == 'cuda',
        )
        chunks = []
        model.eval()
        with torch.no_grad():
            for (batch_x,) in value_loader:
                batch_x = batch_x.to(torch_device, non_blocking=True)
                chunks.append(model(batch_x).cpu())
        return torch.cat(chunks).numpy()

    batch_size = 32
    train_dataset = TensorDataset(torch.as_tensor(train_x), torch.as_tensor(train_y))
    test_dataset = TensorDataset(torch.as_tensor(test_x), torch.as_tensor(test_y))
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=0, pin_memory=torch_device.type == 'cuda')
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False, num_workers=0, pin_memory=torch_device.type == 'cuda')
    model = TorchCNN().to(torch_device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=0.00001 if label_mode == 'CAT' else 0.0001)
    best_monitor = float('-inf') if label_mode == 'CAT' else float('inf')
    best_state = None
    if debug:
        print(model)
    print('real length:', 'train', len(train_x), 'test', len(test_x))
    if remaining is not None:
        print('remaining: ' + str(remaining) + ' rounds')

    for epoch in range(120):
        model.train()
        for batch_x, batch_y in train_loader:
            batch_x = batch_x.to(torch_device, non_blocking=True)
            batch_y = batch_y.to(torch_device, non_blocking=True)
            optimizer.zero_grad(set_to_none=True)
            loss = loss_function(model(batch_x), batch_y)
            loss.backward()
            optimizer.step()

        model.eval()
        validation_loss = 0.0
        validation_correct = 0
        validation_values = 0
        with torch.no_grad():
            for batch_x, batch_y in test_loader:
                batch_x = batch_x.to(torch_device, non_blocking=True)
                batch_y = batch_y.to(torch_device, non_blocking=True)
                outputs = model(batch_x)
                validation_loss += loss_function(outputs, batch_y).item() * batch_y.shape[0]
                if label_mode == 'CAT':
                    validation_correct += ((outputs >= 0.5) == (batch_y >= 0.5)).sum().item()
                    validation_values += batch_y.numel()
        validation_loss /= len(test_dataset)
        monitor_value = validation_correct / validation_values if label_mode == 'CAT' else validation_loss
        is_better = monitor_value > best_monitor if label_mode == 'CAT' else monitor_value < best_monitor
        if is_better:
            best_monitor = monitor_value
            best_state = {key: value.detach().cpu().clone() for key, value in model.state_dict().items()}
        if debug:
            metric_name = 'val_binary_accuracy' if label_mode == 'CAT' else 'val_loss'
            print('Epoch {}/120, {}: {:.6f}'.format(epoch + 1, metric_name, monitor_value))

    model.load_state_dict(best_state)
    train_pred = predict(train['x'], batch_size)
    test_pred = predict(test['x'], batch_size)
    train_result = {'y': train['y'], 'pred': train_pred}
    test_result = {'y': test['y'], 'pred': test_pred}
    pred_result = {}
    target_result = {}
    if direct:
        if pred is not None and 'y' in pred:
            pred_result['y'] = [pred['y'][index] for index in range(len(pred['y']))]
            pred_result['pred'] = predict(pred['x'], batch_size)
        if target is not None and 'y' in target:
            target_result['y'] = [target['y'][index] for index in range(len(target['y']))]
            target_result['pred'] = predict(target['x'], batch_size)
    else:
        for dt in pred:
            pred_result[dt] = {}
            for label in pred[dt]:
                item = pred[dt][label]
                pred_result[dt][label] = {
                    'data_len': item['data_len'], 'avg_window': item['avg_window'],
                    'good_count': item['good_count'], 'qxc': item['qxc'],
                    'stat_diff_info': item['stat_diff_info'], 'prob_cand_arr': item['prob_cand_arr'],
                    'pred_as_label': item['pred'], 'y': item['y'], 'x': item['x'],
                    'pred': predict(item['x'], batch_size),
                }
        for dt in target:
            target_result[dt] = {}
            for label in target[dt]:
                item = target[dt][label]
                target_result[dt][label] = {
                    'data_len': item['data_len'], 'avg_window': item['avg_window'],
                    'good_count': item['good_count'], 'qxc': item['qxc'],
                    'stat_diff_info': item['stat_diff_info'], 'prob_cand_arr': item['prob_cand_arr'],
                    'pred_as_label': item['pred'], 'y': item['y'], 'x': item['x'],
                    'pred': predict(item['x'], batch_size),
                }
    del best_state
    del model
    if torch_device.type == 'cuda':
        torch.cuda.empty_cache()
    return train_result, test_result, pred_result, target_result



def execute_secondary_global(name, exclude_dt, acc_sample_num, target_dt, pred_dt, test_ratio, label_pos):
    data, pred_target = load_secondary(name, exclude_dt, acc_sample_num, target_dt, pred_dt, test_ratio)
    model_vote(['CNN'], data, verbose=True, method='AVG', label_pos=label_pos, pred_target=pred_target)
    


def execute_single(name, mode, shrink, label_and_combine, metric_mode, avg_window, drop_rate, pred_len, smoothing_mode=SMOOTH_EMA_STATE, ema_alpha=None, target_date=None):
    last_date = None
    if target_date is not None:
        last_date = previous_draw_date(target_date)
    with open(name.split('_')[0] + ('_raw_txt' if last_date is None else '_raw_history/' + last_date)) as file:
        for line in file:
            line = line.replace('\n', '').split(' ')
    output_chunk_length=2
    data_mode = 'PROB_TIME_SERIES'
    cv_len = 1
    time_window=int(avg_window*3)
    label_dim = label_and_combine[0]
    combine = [int(v) for v in label_and_combine[1:]]
    dr = str(drop_rate).replace('.','')
    aw = str(avg_window)
    result = {'combine' : [combine[-1],combine[-1]], 'left_02' : 0, 'right_02' : 0, 'left_01' : 0, 'right_01' : 0, 'qxc' : line}
    if mode == MODE_FIND:
        exist = set()
        if os.path.exists(name + '/%s/find_best_' % ('metric' if target_date is None else target_date) + str(label_dim) + '_' + metric_mode + '_' + dr + '_' + aw + '.txt'):
            exist = get_exist_combines(name + '/%s/find_best_' % ('metric' if target_date is None else target_date) + str(label_dim) + '_' + metric_mode + '_' + dr + '_' + aw + '.txt')
            if str(combine[0]) + ',' in exist:
                exit(0)
    final_pred_pred = None
    final_target_pred = None
    prob_cand_html = ''
    validate_html = ''
    for i in range(cv_len):
        if ':' in label_dim:
            data,y_pred_previous,show = loadProbRaw(combine[-1], combine, None, name.split('_')[0] + ('_raw_txt' if last_date is None else '_raw_history/' + last_date), None, time_window, avg_window, mode=data_mode, enrich=None, reverse=False, sample_mode=metric_mode, debug=False, shrink=shrink, label_pos_array=[int(v) for v in label_dim.split(':')], output_chunk_length=output_chunk_length, pred_len=pred_len, smoothing_mode=smoothing_mode, ema_alpha=ema_alpha)
        else:
            data,y_pred_previous,show = loadProbRaw(combine[-1], combine, None, name.split('_')[0] + ('_raw_txt' if last_date is None else '_raw_history/' + last_date), int(label_dim), time_window, avg_window, mode=data_mode, enrich=None, reverse=False, sample_mode=metric_mode, debug=False, shrink=shrink, output_chunk_length=output_chunk_length, pred_len=pred_len, smoothing_mode=smoothing_mode, ema_alpha=ema_alpha)
        if data_mode == 'PURE_TIME_SERIES':
            pass#pred_pred, pred_y, target_pred = dart_test(data, model_use=DART_MODEL_N_LINEAR,input_chunk_length=time_window,output_chunk_length=output_chunk_length)
        else:
            train_result, test_result, pred_result, target_result = model_train_and_predict_by_torch(train=data['train'], test=data['test'], pred=data['pred'], target=data['target'], debug=(mode==MODE_SHOW), label_mode=label_mode, drop_rate=drop_rate)
        for row in show:
            print(row)
            prob_cand_html += str(row) + '<br\\>'
        del data
        if final_pred_pred is None:
            final_pred_pred = pred_result['pred']
            final_target_pred = target_result['pred']
        else:
            final_pred_pred += pred_result['pred']
            final_target_pred += target_result['pred']
        if cv_len > 1:
            print('round:', i)
    final_pred_pred /= cv_len
    final_target_pred /= cv_len
    print('\n\n')
    for j in range(len(y_pred_previous)):
        ypp = np.append(y_pred_previous[j], y_pred_previous[j][0])
        validate_html += str(ypp) + '----' + str(ypp) + '<br\\>'
        print(ypp, '----', ypp)
    for i in range(len(final_pred_pred)):
        if len(final_pred_pred[i]) == 1 and len(pred_result['y'][i]) == 1:
            fpp = np.append(final_pred_pred[i], final_pred_pred[i][0])
            py = np.append(pred_result['y'][i], pred_result['y'][i][0])
        validate_html += str(fpp) + '----' + str(py) + '<br\\>'
        print(fpp, '----', py)
        pair = abs(fpp - py)
        if pair[0] <= 0.02:
            result['left_02'] += 1
        if len(pair) > 1 and pair[1] <= 0.02:
            result['right_02'] += 1
        if pair[0] <= 0.01:
            result['left_01'] += 1
        if len(pair) > 1 and pair[1] <= 0.01:
            result['right_01'] += 1
    print(result)
    print('\n\n')
    print(final_target_pred)
    validate_html += str(final_target_pred) + '<br\\>'
    if mode == MODE_FIND and ((pred_len < 7 and result['right_01'] >= pred_len) or ('qxc' in name and result['left_02'] >= 5 and result['right_01'] >= 4) or ('pls' in name and (result['left_02'] >= 7 and result['right_01'] >= 4 or result['left_02'] >= 6 and result['right_01'] >= 4 or result['left_02'] >= 5 and result['right_01'] >= 5))):
        record = {
            'prob_cand_html' : prob_cand_html, 
            'validate_html' : validate_html, 
            'drop_rate' : dr, 
            'avg_window' : aw, 
            'data_len' : combine[0],
            'smoothing_mode': smoothing_mode,
            'ema_alpha': (
                resolve_ema_alpha(
                    avg_window,
                    ema_alpha
                )
                if smoothing_mode != SMOOTH_SMA
                else None
            )
        }
        record.update(result)
        fn = name + '/%s/detail_' % ('metric' if target_date is None else target_date) + str(label_dim)
        if os.path.exists(fn + '.pkl'):
            exist = load_obj(fn)
            if 'qxc' in name and len(exist) >= 20 and int(aw) >= 15:
                return
            has = False
            for i in range(len(exist)):
                if record['data_len'] == exist[i]['data_len']:
                    has = True
                    cmp_cnt = 0
                    pattern_old = ''
                    pattern_new = ''
                    for k in ['left_01', 'right_01', 'left_02', 'right_02']:
                        pattern_new += str(record[k])
                        pattern_old += str(exist[i][k])
                        if int(record[k]) >= int(exist[i][k]):
                            cmp_cnt += 1
                    if cmp_cnt >= 3 or (pattern_new == '5566' and pattern_old == '4477') or (pattern_new == '5555' and pattern_old == '4466') or (pattern_new == '6666' and pattern_old == '5577'):
                        exist[i] = record
                    break
            if not has:
                exist.append(record)
            persist_obj(exist, fn)
        else:
            persist_obj([record], fn)
        fe = open(name + '/%s/find_best_' % ('metric' if target_date is None else target_date) + str(label_dim) + '_' + metric_mode + '_' + dr + '_' + aw + '.txt', 'a')
        fe.write(str(result) + '\n')
        fe.close()


if __name__ == '__main__':
    args = sys.argv
    shrink=(args[2] == '1')
    mode = args[1]
    metric_mode = args[4]
    label_and_combine = args[3].split(',')
    avg_window=int(args[5])
    drop_rate = float(args[6])
    name = args[7]
    label_mode='REG'
    feature_mode='COMMON'
    DIMENSION=256
    pred_len = 7
    smoothing_mode = (
    args[8].upper()
    if len(args) > 8
        else SMOOTH_EMA_STATE
    )
    ema_alpha = None
    if (
        len(args) > 9
        and args[9].lower() != 'auto'
    ):
        ema_alpha = float(
            args[9]
        )
    target_date = None
    if len(args) > 10:
        target_date = args[10]
    execute_single(name, mode, shrink, label_and_combine, metric_mode, avg_window, drop_rate, pred_len, smoothing_mode=smoothing_mode, ema_alpha=ema_alpha, target_date=target_date)
    #execute_secondary_global('qxc', ['20251228', '20251230'], None, ['20260630'], None, 0.1, int(label_and_combine[0]), 'CAT', 0.01)
    #execute_secondary_current(name, '20260501', 'CAT', 0.03)


