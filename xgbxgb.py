
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier
from xgboost import plot_importance
from base import *

data = load_obj('for_xgb')

### fit model for train data
model = XGBClassifier(learning_rate=0.01,
                     n_estimators=300,          # 树的个数--1000棵树建立xgboost
                     max_depth=6,                # 树的深度
                     min_child_weight = 1,       # 叶子节点最小权重
                     gamma=0.,                   # 惩罚项中叶子结点个数前的参数
                     subsample=0.8,              # 随机选择80%样本建立决策树
                     colsample_btree=0.8,        # 随机选择80%特征建立决策树
                     objective='binary:logistic',# 指定损失函数
                     scale_pos_weight=1,         # 解决样本个数不平衡的问题
                     random_state=27             # 随机数
                     )
model.fit(data['trainX'],
         data['trainY'],
         eval_set = [(data['testX'],data['testY'])],
         # eval_metric = "logloss",
         # early_stopping_rounds = 10,
         verbose = True)

y_pred = model.predict(data['testX'])

### model evaluate
accuracy = accuracy_score(data['testY'],y_pred)
print("accuarcy: %.2f%%" % (accuracy*100.0))