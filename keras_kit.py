from tensorflow.keras.layers import Layer, Dense, Flatten, Reshape, Add, LayerNormalization, Dropout, Lambda, BatchNormalization, Embedding, Conv1D, LeakyReLU, Input, MultiHeadAttention, Add, GroupNormalization
import tensorflow as tf
import keras
from keras import layers
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Dense, Flatten, Reshape, Add, LayerNormalization, Dropout, Lambda, BatchNormalization, Embedding
from tensorflow.keras.layers import LSTM, SimpleRNN, GRU
from tensorflow.keras.layers import MaxPooling1D, MaxPool1D, Conv1D, Conv2D, MaxPooling2D, GlobalMaxPooling1D, GlobalAveragePooling1D, AveragePooling1D
from tensorflow.keras.layers import Activation, ELU, LeakyReLU, ReLU, PReLU
from tensorflow.keras.initializers import HeNormal, Constant
from tensorflow.keras import Input
from tensorflow.keras.callbacks import *
from keras.optimizers import Adam, RMSprop, SGD, AdamW, Adadelta, Adagrad, Adamax, Adafactor, Nadam, Ftrl, Lion, LossScaleOptimizer
from keras.applications import *
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras import backend as K
from keras.src import backend
from tensorflow.keras.losses import *
from keras.src import ops
from keras.src.losses.loss import squeeze_or_expand_to_same_rank
import numpy as np
from sklearn.preprocessing import MinMaxScaler
# from darts.models import BlockRNNModel,CatBoostModel,DLinearModel,ExponentialSmoothing,FFT,GlobalNaiveAggregate,KalmanForecaster,LightGBMModel,LinearRegressionModel,NBEATSModel,NHiTSModel,NLinearModel,Prophet,RandomForest,RNNModel,TransformerModel,AutoARIMA,AutoCES,AutoETS,AutoMFLES,AutoTBATS,Croston,StatsForecastModel,TBATS,TCNModel,TFTModel,FourTheta,TiDEModel,TSMixerModel,VARIMA,XGBModel,AutoTheta
# from darts import TimeSeries
# from darts.utils.utils import ModelMode, SeasonalityMode, generate_index
# from pytorch_lightning.callbacks.early_stopping import EarlyStopping
import numpy
from keras.src import backend

DART_MODEL_BLOCK_RNN = 'DART_MODEL_BLOCK_RNN' #skip
DART_MODEL_CAT_BOOST = 'DART_MODEL_CAT_BOOST'
DART_MODEL_DLINEAR = 'DART_MODEL_DLINEAR' #skip
DART_MODEL_EXP = 'DART_MODEL_EXP' #skip
DART_MODEL_FFT = 'DART_MODEL_FFT' #skip
DART_MODEL_GLOBAL_NATIVE = 'DART_MODEL_GLOBAL_NATIVE' #skip
DART_MODEL_KALMAN = 'DART_MODEL_KALMAN' #skip
DART_MODEL_LIGHT_GBM = 'DART_MODEL_LIGHT_GBM' #skip
DART_MODEL_LINEAR_REG = 'DART_MODEL_LINEAR_REG' #skip
DART_MODEL_N_BEATS = 'DART_MODEL_N_BEATS'
DART_MODEL_N_HITS = 'DART_MODEL_N_HITS'
DART_MODEL_N_LINEAR = 'DART_MODEL_N_LINEAR'
DART_MODEL_PROPHET = 'DART_MODEL_PROPHET' #skip
DART_MODEL_RANDOM_FOREST = 'DART_MODEL_RANDOM_FOREST'
DART_MODEL_RNN = 'DART_MODEL_RNN' #skip
DART_MODEL_TRANSFORMER = 'DART_MODEL_TRANSFORMER'
DART_MODEL_AUTO_ARIMA = 'DART_MODEL_AUTO_ARIMA' #skip
DART_MODEL_AUTO_CES = 'DART_MODEL_AUTO_CES' #skip
DART_MODEL_AUTO_ETS = 'DART_MODEL_AUTO_ETS' #skip
DART_MODEL_AUTO_MFLES = 'DART_MODEL_AUTO_MFLES' #skip
DART_MODEL_AUTO_TBATS = 'DART_MODEL_AUTO_TBATS' #skip
DART_MODEL_AUTO_THETA = 'DART_MODEL_AUTO_THETA' #skip
DART_MODEL_CROSTON = 'DART_MODEL_CROSTON' #skip
DART_MODEL_STATS_FORECAST = 'DART_MODEL_STATS_FORECAST' #skip
DART_MODEL_TBATS = 'DART_MODEL_TBATS' #skip
DART_MODEL_TCN = 'DART_MODEL_TCN' #skip
DART_MODEL_TFT = 'DART_MODEL_TFT' #skip
DART_MODEL_THETA = 'DART_MODEL_THETA' #skip
DART_MODEL_TIDE = 'DART_MODEL_TIDE' #skip
DART_MODEL_TSMIXER = 'DART_MODEL_TSMIXER' #skip
DART_MODEL_VRIMA = 'DART_MODEL_VRIMA' #skip
DART_MODEL_XGB = 'DART_MODEL_XGB' #skip


#early_stop_callback = EarlyStopping(monitor='loss', min_delta=5, patience=30, mode='min', verbose=1, restore_best_weights = True)

# test_ref_array = test['ref']
# train_ref_array = train['ref']
# del test['ref']
# del train['ref']
reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.1, patience=1, min_lr=1e-6)
def scheduler(epoch, lr):
    if epoch == 10:
        return lr * 10
    elif epoch == 20:
        return lr  * 10
    elif epoch == 30:
        return lr * 10
    elif epoch == 40:
        return lr / 10
    elif epoch == 50:
        return lr * 10
    elif epoch == 60:
        return lr / 10
    else:
        return lr
scheduler_lr = LearningRateScheduler(scheduler)



class CyclicLR(Callback):
    """This callback implements a cyclical learning rate policy (CLR).
    The method cycles the learning rate between two boundaries with
    some constant frequency, as detailed in this paper (https://arxiv.org/abs/1506.01186).
    The amplitude of the cycle can be scaled on a per-iteration or 
    per-cycle basis.
    This class has three built-in policies, as put forth in the paper.
    "triangular":
        A basic triangular cycle w/ no amplitude scaling.
    "triangular2":
        A basic triangular cycle that scales initial amplitude by half each cycle.
    "exp_range":
        A cycle that scales initial amplitude by gamma**(cycle iterations) at each 
        cycle iteration.
    For more detail, please see paper.
    
    # Example
        ```python
            clr = CyclicLR(base_lr=0.001, max_lr=0.006,
                                step_size=2000., mode='triangular')
            model.fit(X_train, Y_train, callbacks=[clr])
        ```
    
    Class also supports custom scaling functions:
        ```python
            clr_fn = lambda x: 0.5*(1+np.sin(x*np.pi/2.))
            clr = CyclicLR(base_lr=0.001, max_lr=0.006,
                                step_size=2000., scale_fn=clr_fn,
                                scale_mode='cycle')
            model.fit(X_train, Y_train, callbacks=[clr])
        ```    
    # Arguments
        base_lr: initial learning rate which is the
            lower boundary in the cycle.
        max_lr: upper boundary in the cycle. Functionally,
            it defines the cycle amplitude (max_lr - base_lr).
            The lr at any cycle is the sum of base_lr
            and some scaling of the amplitude; therefore 
            max_lr may not actually be reached depending on
            scaling function.
        step_size: number of training iterations per
            half cycle. Authors suggest setting step_size
            2-8 x training iterations in epoch.
        mode: one of {triangular, triangular2, exp_range}.
            Default 'triangular'.
            Values correspond to policies detailed above.
            If scale_fn is not None, this argument is ignored.
        gamma: constant in 'exp_range' scaling function:
            gamma**(cycle iterations)
        scale_fn: Custom scaling policy defined by a single
            argument lambda function, where 
            0 <= scale_fn(x) <= 1 for all x >= 0.
            mode paramater is ignored 
        scale_mode: {'cycle', 'iterations'}.
            Defines whether scale_fn is evaluated on 
            cycle number or cycle iterations (training
            iterations since start of cycle). Default is 'cycle'.
    """

    def __init__(self, base_lr=0.001, max_lr=0.006, step_size=2000., mode='triangular',
                 gamma=1., scale_fn=None, scale_mode='cycle'):
        super(CyclicLR, self).__init__()

        self.base_lr = base_lr
        self.max_lr = max_lr
        self.step_size = step_size
        self.mode = mode
        self.gamma = gamma
        if scale_fn == None:
            if self.mode == 'triangular':
                self.scale_fn = lambda x: 1.
                self.scale_mode = 'cycle'
            elif self.mode == 'triangular2':
                self.scale_fn = lambda x: 1/(2.**(x-1))
                self.scale_mode = 'cycle'
            elif self.mode == 'exp_range':
                self.scale_fn = lambda x: gamma**(x)
                self.scale_mode = 'iterations'
        else:
            self.scale_fn = scale_fn
            self.scale_mode = scale_mode
        self.clr_iterations = 0.
        self.trn_iterations = 0.
        self.history = {}

        self._reset()

    def _reset(self, new_base_lr=None, new_max_lr=None,
               new_step_size=None):
        """Resets cycle iterations.
        Optional boundary/step size adjustment.
        """
        if new_base_lr != None:
            self.base_lr = new_base_lr
        if new_max_lr != None:
            self.max_lr = new_max_lr
        if new_step_size != None:
            self.step_size = new_step_size
        self.clr_iterations = 0.
        
    def clr(self):
        cycle = np.floor(1+self.clr_iterations/(2*self.step_size))
        x = np.abs(self.clr_iterations/self.step_size - 2*cycle + 1)
        if self.scale_mode == 'cycle':
            return self.base_lr + (self.max_lr-self.base_lr)*np.maximum(0, (1-x))*self.scale_fn(cycle)
        else:
            return self.base_lr + (self.max_lr-self.base_lr)*np.maximum(0, (1-x))*self.scale_fn(self.clr_iterations)
        
    def on_train_begin(self, logs={}):
        logs = logs or {}
        if self.clr_iterations == 0:
            self.model.optimizer.learning_rate = self.base_lr
        else:
            self.model.optimizer.learning_rate = self.clr()     
            
    def on_batch_end(self, epoch, logs=None):
        logs = logs or {}
        self.trn_iterations += 1
        self.clr_iterations += 1
        self.history.setdefault('lr', []).append(K.get_value(self.model.optimizer.learning_rate))
        self.history.setdefault('iterations', []).append(self.trn_iterations)
        for k, v in logs.items():
            self.history.setdefault(k, []).append(v)
        self.model.optimizer.learning_rate = self.clr()
        logs["learning_rate"] = float(
            backend.convert_to_numpy(self.model.optimizer.learning_rate)
        )


# a
clr_fn = lambda x: 0.5*(1+np.sin(x*np.pi/2.))
cyclic_lr = CyclicLR(base_lr=0.00001, max_lr=0.0006,
                step_size=4000., scale_fn=clr_fn,
                scale_mode='cycle')
# b
# clr_fn = lambda x: 1/(5**(x*0.00001))
# cyclic_lr = CyclicLR(base_lr=0.00001, max_lr=0.0006,
#             step_size=2000., scale_fn=clr_fn,
#             scale_mode='iterations')


# def prepare_cnn_inner(raw, label_dim):
#     dim_size = 128
#     inputs = raw['x']
#     use1d = len(inputs.shape) < 4
#     outputs = Conv1D(filters=dim_size, kernel_size=1, activation=PReLU())(inputs) if use1d else Conv2D(filters=dim_size, kernel_size=(1,1),strides=(1,1), activation=PReLU())(inputs)
#     outputs = GroupNormalization(groups=64)(outputs)
#     outputs = Conv1D(filters=dim_size, kernel_size=1, activation=PReLU())(outputs) if use1d else Conv2D(filters=dim_size, kernel_size=(1,1),strides=(1,1), activation=PReLU())(outputs)
#     outputs = GroupNormalization(groups=64)(outputs)
#     outputs = MaxPooling1D(pool_size=1,strides=1)(outputs) if use1d else MaxPooling2D(pool_size=(1,1),strides=1)(outputs)
#     outputs = Flatten()(outputs)
#     outputs = Dropout(0.1)(outputs)
#     outputs = Dense(label_dim)(outputs)
#     outputs = Dropout(0.1)(outputs)
#     return outputs


def prepare_lstm_model(raw, label_dim):
    outputs = LSTM(units=64, return_sequences=True)(raw['x'])
    outputs = Dropout(0.1)(outputs)
    outputs = LSTM(units=32, return_sequences=False, activation='tanh')(outputs)
    outputs = Dropout(0.1)(outputs)
    outputs = Dense(label_dim, activation='tanh')(outputs)
    outputs = Dropout(0.1)(outputs)
    return outputs

def prepare_lstm_after_cnn_model(raw, label_dim):
    dim_size = 128
    inputs = raw['x']
    # inputs = (TokenEmbedding(dim_size)(inputs) + PositionalEmbedding(dim_size)(inputs))
    use1d = len(inputs.shape) < 4
    outputs = Conv1D(filters=dim_size, kernel_size=1, activation=PReLU())(inputs) if use1d else Conv2D(filters=dim_size, kernel_size=(1,1),strides=(1,1), activation=PReLU())(inputs)
    outputs = MaxPooling1D(pool_size=1,strides=1)(outputs) if use1d else MaxPooling2D(pool_size=(1,1),strides=1)(outputs)
    outputs = Flatten()(outputs)
    outputs = Dense(64, activation='relu')(outputs)
    outputs = Dropout(0.1)(outputs)
    outputs = LSTM(units=64, return_sequences=False)(outputs)
    outputs = Dropout(0.1)(outputs)
    outputs = LSTM(units=32, return_sequences=False, activation=PReLU())(outputs)
    outputs = Dropout(0.1)(outputs)
    outputs = Dense(label_dim, activation=PReLU())(outputs)
    outputs = Dropout(0.1)(outputs)
    return outputs

def prepare_cnn_after_lstm_model(raw, label_dim):
    outputs = LSTM(units=64, return_sequences=True)(raw['x'])
    outputs = Dropout(0.1)(outputs)
    outputs = LSTM(units=32, return_sequences=True, activation='tanh')(outputs)
    outputs = Dropout(0.1)(outputs)
    #outputs = Dense(label_dim, activation='tanh')(outputs)
    outputs = Dropout(0.1)(outputs)
    use1d = True
    dim_size = 128
    outputs = Conv1D(filters=dim_size, kernel_size=1, activation=PReLU())(outputs) if use1d else Conv2D(filters=dim_size, kernel_size=(1,1),strides=(1,1), activation=PReLU())(outputs)
    outputs = GroupNormalization(groups=64)(outputs)
    # outputs = Dropout(0.1)(outputs)
    outputs = Conv1D(filters=dim_size, kernel_size=1, activation=PReLU())(outputs) if use1d else Conv2D(filters=dim_size, kernel_size=(1,1),strides=(1,1), activation=PReLU())(outputs)
    outputs = GroupNormalization(groups=64)(outputs)
    # outputs = Dropout(0.1)(outputs)
    outputs = MaxPooling1D(pool_size=1,strides=1)(outputs) if use1d else MaxPooling2D(pool_size=(1,1),strides=1)(outputs)
    outputs = Flatten()(outputs)
    # outputs = Dense(dim_size, activation='tanh')(outputs)
    outputs = Dropout(0.1)(outputs)
    outputs = Dense(label_dim)(outputs)
    outputs = Dropout(0.1)(outputs)
    return outputs



# def dart_test(data, model_use=DART_MODEL_DLINEAR, input_chunk_length=42, output_chunk_length=2):
#     icl = input_chunk_length
#     ocl = output_chunk_length
#     ckpf = str(uuid.uuid1()).replace('-', '')
#     # model = NBEATSModel(
#     #         input_chunk_length=icl,
#     #         output_chunk_length=ocl,
#     #         n_epochs=50,
#     #         # activation='LeakyReLU',
#     #         batch_size = 1,
#     #         optimizer_kwargs = {'lr' : 0.001},
#     #         model_name=ckpf,
#     #         save_checkpoints=True,
#     #         force_reset=True
#     #     )
#     # model = NHiTSModel(
#     #     input_chunk_length=icl,
#     #     output_chunk_length=ocl,
#     #     num_blocks=2,
#     #     batch_size = 1,
#     #     optimizer_kwargs = {'lr' : 0.001},
#     #     n_epochs=50,
#     #     model_name=ckpf,
#     #     save_checkpoints=True,
#     #     force_reset=True
#     # )
#     # model.fit(series = data['train_series'], val_series=data['test_series'])
#     # model = NHiTSModel.load_from_checkpoint(model_name=ckpf, best=True)
#     if model_use == DART_MODEL_DLINEAR:
#         model = DLinearModel(
#             input_chunk_length=icl,
#             output_chunk_length=ocl,
#             batch_size = 1,
#             n_epochs=50,
#             optimizer_kwargs = {'lr' : 0.001},
#             model_name=ckpf,
#             save_checkpoints=True,
#             force_reset=True
#         )
#         model.fit(series = data['train_series'], val_series=data['test_series'])
#         model = DLinearModel.load_from_checkpoint(model_name=ckpf, best=True)
#     elif model_use == DART_MODEL_N_LINEAR:
#         model = NLinearModel(
#             input_chunk_length=icl,
#             output_chunk_length=ocl,
#             batch_size = 1,
#             optimizer_kwargs = {'lr' : 0.001},
#             n_epochs=50,
#             model_name=ckpf,
#             save_checkpoints=True,
#             force_reset=True
#         )
#         model.fit(series = data['train_series'], val_series=data['test_series'])
#         model = NLinearModel.load_from_checkpoint(model_name=ckpf, best=True)
#     pred_arr = []
#     y_arr = []
#     for val in data['val_series_arr']:
#         test = model.predict(output_chunk_length, series=val['train']).values()
#         for i in range(output_chunk_length):
#             pred_arr.append(test[i])
#             y_arr.append(val['val'][i])
#     try:
#         shutil.rmtree('darts_logs/' + ckpf)
#     except:
#         pass
#     return np.array(pred_arr),np.array(y_arr),np.array([model.predict(output_chunk_length, series=data['pred_series']).values()])

# https://github.com/mounalab/Multivariate-time-series-forecasting-keras/blob/main/Transformer.py
# https://github.com/keras-team/keras-io/blob/master/examples/timeseries/timeseries_classification_transformer.py
# 0.x 是因为他妈的超过1000次?放屁萝味



def cc_binary_crossentropy(
    y_true, y_pred, from_logits=False, label_smoothing=0.005, axis=-1
):
    """Computes the binary crossentropy loss.

    Args:
        y_true: Ground truth values. shape = `[batch_size, d0, .. dN]`.
        y_pred: The predicted values. shape = `[batch_size, d0, .. dN]`.
        from_logits: Whether `y_pred` is expected to be a logits tensor. By
            default, we assume that `y_pred` encodes a probability distribution.
        label_smoothing: Float in `[0, 1]`. If > `0` then smooth the labels by
            squeezing them towards 0.5, that is,
            using `1. - 0.5 * label_smoothing` for the target class
            and `0.5 * label_smoothing` for the non-target class.
        axis: The axis along which the mean is computed. Defaults to `-1`.

    Returns:
        Binary crossentropy loss value. shape = `[batch_size, d0, .. dN-1]`.

    Example:

    >>> y_true = [[0, 1], [0, 0]]
    >>> y_pred = [[0.6, 0.4], [0.4, 0.6]]
    >>> loss = keras.losses.binary_crossentropy(y_true, y_pred)
    >>> assert loss.shape == (2,)
    >>> loss
    array([0.916 , 0.714], dtype=float32)
    """
    y_pred = ops.convert_to_tensor(y_pred)
    y_true = ops.cast(y_true, y_pred.dtype)

    if label_smoothing:
        y_true = y_true * (1.0 - label_smoothing) + 0.5 * label_smoothing
    rst = ops.mean(
        ops.binary_crossentropy(y_true, y_pred, from_logits=from_logits),
        axis=axis,
    )
    return abs(rst - 0.68) + 0.68



def cc_binary_focal_crossentropy(
    y_true,
    y_pred,
    apply_class_balancing=False,
    alpha=1.7 / 1.8,
    gamma=1.1 / 1.8,
    from_logits=False,
    label_smoothing=0.005,
    axis=-1,
):
    """Computes the binary focal crossentropy loss.

    According to [Lin et al., 2018](https://arxiv.org/pdf/1708.02002.pdf), it
    helps to apply a focal factor to down-weight easy examples and focus more on
    hard examples. By default, the focal tensor is computed as follows:

    `focal_factor = (1 - output) ** gamma` for class 1
    `focal_factor = output ** gamma` for class 0
    where `gamma` is a focusing parameter. When `gamma` = 0, there is no focal
    effect on the binary crossentropy loss.

    If `apply_class_balancing == True`, this function also takes into account a
    weight balancing factor for the binary classes 0 and 1 as follows:

    `weight = alpha` for class 1 (`target == 1`)
    `weight = 1 - alpha` for class 0
    where `alpha` is a float in the range of `[0, 1]`.

    Args:
        y_true: Ground truth values, of shape `(batch_size, d0, .. dN)`.
        y_pred: The predicted values, of shape `(batch_size, d0, .. dN)`.
        apply_class_balancing: A bool, whether to apply weight balancing on the
            binary classes 0 and 1.
        alpha: A weight balancing factor for class 1, default is `0.25` as
            mentioned in the reference. The weight for class 0 is `1.0 - alpha`.
        gamma: A focusing parameter, default is `2.0` as mentioned in the
            reference.
        from_logits: Whether `y_pred` is expected to be a logits tensor. By
            default, we assume that `y_pred` encodes a probability distribution.
        label_smoothing: Float in `[0, 1]`. If > `0` then smooth the labels by
            squeezing them towards 0.5, that is,
            using `1. - 0.5 * label_smoothing` for the target class
            and `0.5 * label_smoothing` for the non-target class.
        axis: The axis along which the mean is computed. Defaults to `-1`.

    Returns:
        Binary focal crossentropy loss value
        with shape = `[batch_size, d0, .. dN-1]`.

    Example:

    >>> y_true = [[0, 1], [0, 0]]
    >>> y_pred = [[0.6, 0.4], [0.4, 0.6]]
    >>> loss = keras.losses.binary_focal_crossentropy(
    ...        y_true, y_pred, gamma=2)
    >>> assert loss.shape == (2,)
    >>> loss
    array([0.330, 0.206], dtype=float32)
    """
    y_pred = ops.convert_to_tensor(y_pred)
    y_true = ops.cast(y_true, y_pred.dtype)

    if label_smoothing:
        y_true = y_true * (1.0 - label_smoothing) + 0.5 * label_smoothing

    if from_logits:
        y_pred = ops.sigmoid(y_pred)

    bce = ops.binary_crossentropy(
        target=y_true,
        output=y_pred,
        from_logits=False,
    )

    # Calculate focal factor
    p_t = y_true * y_pred + (1 - y_true) * (1 - y_pred)
    focal_factor = ops.power(1.0 - p_t, gamma)

    focal_bce = focal_factor * bce

    if apply_class_balancing:
        weight = y_true * alpha + (1 - y_true) * (1 - alpha)
        focal_bce = weight * focal_bce
    rst = ops.mean(focal_bce, axis=axis)
    return abs(rst - 0.48) + 0.48

def custom_loss(y_true, y_pred):
    y_pred = ops.convert_to_tensor(y_pred)
    y_true = ops.convert_to_tensor(y_true, dtype=y_pred.dtype)
    y_true, y_pred = squeeze_or_expand_to_same_rank(y_true, y_pred)
    avg = ops.mean(ops.square(y_true - y_pred), axis=-1)
    std = ops.std(ops.square(y_true - y_pred), axis=-1)
    loss = std * 0.6 + avg * 0.4
    return loss


# scaler = MinMaxScaler()

# def custom_loss(y_true, y_pred):
#     y_true = (y_true - K.constant(scaler.min_)) / K.constant(scaler.scale_)
#     y_pred = (y_pred - K.constant(scaler.min_)) / K.constant(scaler.scale_)
#     return K.mean(K.abs(y_pred - y_true), axis=-1)


def cc_categorical_crossentropy(
    y_true, y_pred, from_logits=False, label_smoothing=0.01, axis=-1
):
    """Computes the categorical crossentropy loss.

    Args:
        y_true: Tensor of one-hot true targets.
        y_pred: Tensor of predicted targets.
        from_logits: Whether `y_pred` is expected to be a logits tensor. By
            default, we assume that `y_pred` encodes a probability distribution.
        label_smoothing: Float in [0, 1]. If > `0` then smooth the labels. For
            example, if `0.1`, use `0.1 / num_classes` for non-target labels
            and `0.9 + 0.1 / num_classes` for target labels.
        axis: Defaults to `-1`. The dimension along which the entropy is
            computed.

    Returns:
        Categorical crossentropy loss value.

    Example:

    >>> y_true = [[0, 1, 0], [0, 0, 1]]
    >>> y_pred = [[0.05, 0.95, 0], [0.1, 0.8, 0.1]]
    >>> loss = keras.losses.categorical_crossentropy(y_true, y_pred)
    >>> assert loss.shape == (2,)
    >>> loss
    array([0.0513, 2.303], dtype=float32)
    """
    if isinstance(axis, bool):
        raise ValueError(
            "`axis` must be of type `int`. "
            f"Received: axis={axis} of type {type(axis)}"
        )
    y_pred = ops.convert_to_tensor(y_pred)
    y_true = ops.cast(y_true, y_pred.dtype)

    if y_pred.shape[-1] == 1:
        warnings.warn(
            "In loss categorical_crossentropy, expected "
            "y_pred.shape to be (batch_size, num_classes) "
            f"with num_classes > 1. Received: y_pred.shape={y_pred.shape}. "
            "Consider using 'binary_crossentropy' if you only have 2 classes.",
            SyntaxWarning,
            stacklevel=2,
        )

    if label_smoothing:
        num_classes = ops.cast(ops.shape(y_true)[-1], y_pred.dtype)
        y_true = y_true * (1.0 - label_smoothing) + (
            label_smoothing / num_classes
        )

    rst = ops.categorical_crossentropy(
        y_true, y_pred, from_logits=from_logits, axis=axis
    )
    return rst#abs(rst - 0.58) + 0.58


def cc_categorical_focal_crossentropy(
    y_true,
    y_pred,
    alpha=1.7 / 1.8,
    gamma=1.1 / 1.8,
    from_logits=False,
    label_smoothing=0.01,
    axis=-1,
):
    if isinstance(axis, bool):
        raise ValueError(
            "`axis` must be of type `int`. "
            f"Received: axis={axis} of type {type(axis)}"
        )
    y_pred = ops.convert_to_tensor(y_pred)
    y_true = ops.cast(y_true, y_pred.dtype)

    if y_pred.shape[-1] == 1:
        warnings.warn(
            "In loss categorical_focal_crossentropy, expected "
            "y_pred.shape to be (batch_size, num_classes) "
            f"with num_classes > 1. Received: y_pred.shape={y_pred.shape}. "
            "Consider using 'binary_crossentropy' if you only have 2 classes.",
            SyntaxWarning,
            stacklevel=2,
        )

    if label_smoothing:
        num_classes = ops.cast(ops.shape(y_true)[-1], y_pred.dtype)
        y_true = y_true * (1.0 - label_smoothing) + (
            label_smoothing / num_classes
        )

    if from_logits:
        y_pred = ops.softmax(y_pred, axis=axis)

    # Adjust the predictions so that the probability of
    # each class for every sample adds up to 1
    # This is needed to ensure that the cross entropy is
    # computed correctly.
    output = y_pred / ops.sum(y_pred, axis=axis, keepdims=True)
    output = ops.clip(output, backend.epsilon(), 1.0 - backend.epsilon())

    # Calculate cross entropy
    cce = -y_true * ops.log(output)

    # Calculate factors
    modulating_factor = ops.power(1.0 - output, gamma)
    weighting_factor = ops.multiply(modulating_factor, alpha)

    # Apply weighting factor
    focal_cce = ops.multiply(weighting_factor, cce)
    focal_cce = ops.sum(focal_cce, axis=axis)
    focal_cce = abs(focal_cce - 0.48) + 0.48
    return focal_cce



class FNetEncoder(Layer):
    def __init__(self, embed_dim, dense_dim, **kwargs):
        super().__init__(**kwargs)
        self.embed_dim = embed_dim
        self.dense_dim = dense_dim
        self.dense_proj = keras.Sequential(
            [
                layers.Dense(dense_dim, activation="relu"),
                layers.Dense(embed_dim),
            ]
        )
        self.layernorm_1 = layers.LayerNormalization()
        self.layernorm_2 = layers.LayerNormalization()

    def call(self, inputs):
        # Casting the inputs to complex64
        inp_complex = tf.cast(inputs, tf.complex64)
        # Projecting the inputs to the frequency domain using FFT2D and
        # extracting the real part of the output
        fft = tf.math.real(tf.signal.fft2d(inp_complex))
        proj_input = self.layernorm_1(inputs + fft)
        proj_output = self.dense_proj(proj_input)
        return self.layernorm_2(proj_input + proj_output)


class PositionEncoding(Layer): 
    def __init__(self, model_dim, **kwargs):
        self._model_dim = model_dim
        super(PositionEncoding, self).__init__(**kwargs)
 
    def call(self, inputs):
        seq_length = inputs.shape[1]
        position_encodings = np.zeros((seq_length, self._model_dim))
        for pos in range(seq_length):
            for i in range(self._model_dim):
                position_encodings[pos, i] = pos / np.power(10000, (i-i%2) / self._model_dim)
        position_encodings[:, 0::2] = np.sin(position_encodings[:, 0::2]) # 2i
        position_encodings[:, 1::2] = np.cos(position_encodings[:, 1::2]) # 2i+1
        position_encodings = K.cast(position_encodings, 'float32')
        print('看pos', position_encodings.shape)
        return position_encodings
 
    def compute_output_shape(self, input_shape):
        return input_shape



class PositionalEmbedding(Layer):
    def __init__(self, embedding_dim, max_seq_len=5000, **kwargs):
        super(PositionalEmbedding, self).__init__()
        self.max_seq_len = max_seq_len
        self.embedding_dim = embedding_dim
        if self.embedding_dim % 2 == 1 : self.embedding_dim += 1
        gX, gY = np.meshgrid(np.arange(self.max_seq_len), np.arange(self.embedding_dim // 2)) #50, 256
        pE = np.empty((1, self.max_seq_len, self.embedding_dim)) # 50, 512
        print(pE[0, :, ::2].shape)
        print(np.sin(gX / 10000**(2 * gY / self.embedding_dim)).shape)
        pE[0, :, ::2] = np.sin(gX / 10000**(2 * gY / self.embedding_dim)).T
        pE[0, :, 1::2] = np.cos(gX / 10000**(2 * gY / self.embedding_dim)).T
        self.pE = tf.constant(pE, dtype=tf.float32)

    def call(self, x):
        x_shape = tf.shape(x)
        result = tf.tile(self.pE[:, :x_shape[-2], :], [x_shape[0], 1, 1])
        return result


class TokenEmbedding(Layer):
    def __init__(self, dim_model, **kwargs):
        super(TokenEmbedding, self).__init__()
        self.dim_model = dim_model
        self.token_conv = Conv1D(dim_model, 3, padding='causal', activation= LeakyReLU())
  
    def call(self, x):
        x = self.token_conv(x)
        return x
  
    def get_config(self):
        config = super(TokenEmbedding, self).get_config()
        config.update({ "dim_model": self.dim_model })
        return config

class FixedEmbedding(Layer):
    def __init__(self, input_size, dim_model, **kwargs):
        super(FixedEmbedding, self).__init__()
        self.input_size = input_size
        self.dim_model = dim_model
        if self.dim_model % 2 == 1 : self.dim_model += 1
        gX, gY = np.meshgrid(np.arange(self.input_size), np.arange(self.dim_model // 2)) #50, 256
        W = np.empty((1, self.input_size, self.dim_model)) # 50, 512
        W[0, :, ::2] = np.sin(gX / 10000**(2 * gY / self.dim_model)).T
        W[0, :, 1::2] = np.cos(gX / 10000**(2 * gY / self.dim_model)).T
        W = tf.constant(W, dtype=tf.float32)
        tf.stop_gradient(W)
        W = Constant(W)
        self.E = Embedding(self.input_size, self.dim_model, embeddings_initializer=W, trainable=False)

    def call(self, x):
        return self.E(x)

    def get_config(self):
        config = super(FixedEmbedding, self).get_config()
        config.update({ "input_size": self.input_size, "dim_model": self.dim_model })
        return config

class TemporalEmbedding(Layer):
    def __init__(self, dim_model=512, embed_type="fixed", frequency="h", **kwargs):
        super(TemporalEmbedding, self).__init__()
        self.embed_type = embed_type
        self.frequency = frequency
        min = 4
        hr = 24
        wk = 7
        dy = 32
        mon = 13
        Embed = FixedEmbedding if self.embed_type == 'fixed' else Embedding
        if self.frequency == "m":
            self.minute_embed = Embed(min, dim_model)
        self.hour_embed = Embed(hr, dim_model)
        self.weekday_embed = Embed(wk, dim_model)
        self.day_embed = Embed(dy, dim_model)
        self.month_embed = Embed(mon, dim_model)

    def call(self, x):
        min_x = self.minute_embed(x[:, :, 4]) if hasattr(self, 'minute_embed') else 0.
        hour_x = self.hour_embed(x[:, :, 3])
        weekday_x = self.weekday_embed(x[:, :, 2])
        day_x = self.day_embed(x[:, :, 1])
        month_x = self.month_embed(x[:, :, 0])
        return hour_x + weekday_x + day_x + month_x + min_x

    def get_config(self):
        config = super(TemporalEmbedding, self).get_config()
        config.update({ "embed_type": self.embed_type, "frequency": self.frequency })
        return config

