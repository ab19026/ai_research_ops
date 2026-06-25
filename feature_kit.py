import matplotlib.pyplot as plt
from pykalman import KalmanFilter, UnscentedKalmanFilter
from statsmodels.tsa.stattools import adfuller
from statsmodels.stats.diagnostic import acorr_ljungbox as lb_test
import statsmodels.tsa.stattools as stattools
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from scipy.signal import butter, lfilter
from scipy.signal import savgol_filter
# from darts.timeseries import TimeSeries
import statsmodels.api as sm
from scipy.interpolate import make_interp_spline
import pywt
from PyEMD import EMD, EEMD, CEEMDAN
from vmdpy import VMD
from PyLMD import LMD
import scipy.linalg as lg
from scipy.signal import hilbert, firwin
from scipy.linalg import inv
from scipy.fft import fft
#from imblearn.over_sampling import SMOTE, BorderlineSMOTE, ADASYN, KMeansSMOTE, SVMSMOTE, SMOTEN, SMOTENC, RandomOverSampler
#from imblearn.combine import SMOTEENN, SMOTETomek
import numpy as np
import math


class SGMD:
    def __init__(self,sig,fs,mode='eig',delay_time=1,nfft=256,is_plot=False,threshold_corr=0.95,threshold_nmse=0.25, end_indicator='nmse') -> None:
        """ 
        Basic parameters: 
            sig: ndarry, the target signal,
            fs: int, sample frequency of sig,
            threshold_corr: float, the threshold of the corr (optional, default 0.95),
            threshold_nmse: float, the threshold of the nmse (optional, default 0.5).
        Advanced parameters: 
            mode: str, 'eig', 'schur' or 'qr' (optional, default eig),
            delay_time: int, one parameter for SGMD.trajectory_matrix (optional, default 1),
            nfft: int, window length for SGMD.trajectory_matrix (optional, default 256),
            is_plot: bool, whether to plot the PSD figure (optional, default False),
            end_indicator: str, metrics for deciding whether to stop iterating, 'nmse', 'std' or 'var' (optional, default nmse).
        """
        self.sig = sig
        self.n = len(sig)
        self.fs = fs
        self.nfft = nfft
        self.threshold_corr = threshold_corr
        self.threshold_nmse = threshold_nmse
        self.mode = mode
        self.end_indicator = end_indicator
        self.trajectory_matrix(is_plot=is_plot,delay_time=delay_time)

    def trajectory_matrix(self,is_plot=False,delay_time=1):
        if 'X' in dir(self):
            if is_plot:
                plt.plot(self.f1,self.psd)
                plt.xscale('log')
                plt.yscale('log')
                plt.xlabel('f/Hz',fontsize=12)
                plt.ylabel('PSD', fontsize=12)
                plt.grid(False)
                plt.plot(self.f1[self.max_index[0]],self.psd[self.max_index[0]],'*r')
                plt.show()
            return self.X
        else:
            psd,f1 = plt.psd(self.sig,
                                NFFT=self.nfft,
                                Fs=self.fs,
                                detrend='mean',
                                window=np.hanning(self.nfft),
                                noverlap=int(self.nfft*3/4),
                                sides='twosided')
            plt.close()
            self.f1 = f1[self.nfft//2:]
            self.psd = psd[self.nfft//2:]
            self.max_index = np.where(self.psd[:]==np.max(self.psd))
            f_max = self.f1[self.max_index[0]][0]
            norm_val = f_max / self.fs
            self.d = 1.2*(self.fs/f_max) if norm_val >= 1e-3 else self.n/3
            self.d = np.int16(np.round(self.d))
            self.m = int(self.n - (self.d-1)*delay_time)
            self.X = np.zeros((self.m,int(1+(self.d-1)*delay_time)))
            if self.d > self.m:
                for i in range(self.m):
                    self.X[i,:] = self.sig[i:i+(self.d-1)*delay_time+1]
            else:
                for i in range(self.d):
                    self.X[:,i] = self.sig[i*delay_time:self.m+i*delay_time]

    def sgmd(self):
        matrix_A = np.dot(self.X.T,self.X)
        if self.mode == 'eig':
            _, matrix_Q = lg.eig(np.dot(matrix_A,matrix_A))
        elif self.mode == 'schur':
            _, matrix_Q = lg.schur(np.dot(matrix_A,matrix_A),'complex')
        elif self.mode == 'qr':
            matrix_Q, _ = lg.qr(np.dot(matrix_A,matrix_A))
        matrix_Q = np.real(matrix_Q)
        matrix_Y = np.zeros((self.d,self.n))
        self.d, self.m = min(self.d,self.m), max(self.d,self.m)
        for i in range(self.d):
            matrix_Z = np.dot(np.dot(np.expand_dims(matrix_Q[:,i],-1),np.expand_dims(matrix_Q[:,i],-1).T),self.X.T)
            matrix_Z = matrix_Z.T if self.m < self.d else matrix_Z
            matrix_Y[i,:self.d] = [np.mean(np.diag(np.flip(matrix_Z[:j+1,:j+1],axis=1))) for j in range(self.d)]
            matrix_Y[i,self.d:self.m] = [np.mean(np.diag(np.flip(matrix_Z[:,j+1-self.d:j+1],axis=1))) for j in range(self.d,self.m)]
            matrix_Y[i,self.m:] = [np.mean(np.diag(np.flip(matrix_Z[j+1-self.m:,j+1-self.d:],axis=1))) for j in range(self.m,self.n)]
                
        index = np.arange(self.d)
        flags = np.array([True]*(self.d))

        if self.end_indicator == 'nmse':
            x_e = np.sum((self.sig-np.mean(self.sig))**2)
        else: 
            x_e = np.std(self.sig) if self.end_indicator == 'std' else np.var(self.sig)
        while len(index[flags]):
            source = matrix_Y[index[flags][0]]
            flags[index[flags][0]] = False
            tmp_flag = [i for i in index[flags] if np.corrcoef(source,matrix_Y[i])[0,1] >= self.threshold_corr]
            flags[tmp_flag] = False
            SGCs = np.vstack((SGCs,source+np.sum(matrix_Y[tmp_flag],axis=0))) if 'SGCs' in dir() else source+np.sum(matrix_Y[tmp_flag],axis=0)
            if self.end_indicator == 'nmse':
                g_h = np.sum(SGCs,axis=0)
                g_h_e = np.sum((self.sig-g_h)**2)
            else: 
                g_h = np.sum(matrix_Y[index[flags]],axis=0)
                g_h_e = np.std(g_h) if self.end_indicator == 'std' else np.var(g_h)
            if g_h_e / x_e < self.threshold_nmse:
                break
        if self.end_indicator == 'nmse':
            SGCs = np.vstack((SGCs,self.sig-g_h))
        else:
            SGCs = np.vstack((SGCs,g_h))
        return SGCs

def exp_avg(arr, alpha):
    rst = None
    for v in arr:
        if rst is None:
            rst = v
        else:
            rst = rst * (1 - alpha) + v * alpha
    return rst

def smooth_reverse(raw=None, dim=None, _type='LOG', debug=False):
    window_size = 2
    alpha = [0.01,0.1,0.01,0.1,0.01,0.1,0.01]
    rst = []
    cand = []
    if _type == 'EXP':
        for i in range(dim):
            observations = []
            for j in range(len(raw) - 1, 0, -1):
                observations.insert(0, (raw[j][i] - raw[j - 1][i] * (1 - alpha[i])) / alpha[i])
            observations.insert(0, raw[0][i])
            cand.append(observations)
        rst = [[cand[k][i] for k in range(dim)] for i in range(len(raw))]
    elif _type == 'EXP_SQRT':
        for i in range(dim):
            observations = []
            for j in range(len(raw) - 1, 0, -1):
                observations.insert(0, ( math.sqrt(math.pow(raw[j][i], 2) - math.pow(raw[j - 1][i] * (1 - alpha[i]), 2)) ) / alpha[i] )
            observations.insert(0, raw[0][i])
            cand.append(observations)
        rst = [[cand[k][i] for k in range(dim)] for i in range(len(raw))]
    return rst



def smooth_avg(observations):
    observations = np.convolve(observations, np.ones(2) / 2, mode='valid')
    observations = np.concatenate(([observations[0] / 2.0], observations))
    return observations


def wave(observations, level=1, wavelet='bior6.8'):
    # 执行小波变换
    wavelet = wavelet  # 选择小波基函数
    level = level  # 分解的级数
    coeffs = pywt.wavedec(observations, wavelet, level=level)
    # 将高频部分系数置零，以实现平滑
    coeffs_smoothed = [coeffs[0]] + [np.zeros_like(coeffs[i]) for i in range(1, len(coeffs))]
    # 重构平滑后的信号
    observations = pywt.waverec(coeffs_smoothed, wavelet)
    return observations


def smooth(raw=None, _type='AVG', debug=False, param=None):
    result = None
    if _type == 'AVG':
        result = np.convolve(raw, np.ones(2) / 2, mode='valid')
        result = np.concatenate(([result[0] / 2.0], result))
        result = [[v for v in result]]
    elif _type == 'KALMAN':
        # To return the smoothed time series data
        observation_covariance = 0.1
        initial_state_covariance = 0.4
        initial_value_guess = raw[0]
        transition_matrix = 0.5
        transition_covariance = 0.8
        kf = KalmanFilter(
                initial_state_mean=initial_value_guess,
                initial_state_covariance=initial_state_covariance,
                observation_covariance=observation_covariance,
                transition_covariance=transition_covariance,
                transition_matrices=transition_matrix
            )
        pred_state, state_cov = kf.filter(raw)
        result = [v[0] for v in pred_state]
        result = [[v for v in result]]
    elif _type == 'EXP':
        result = [raw[0]]
        for i in range(1, len(raw)):
            result.append(raw[i] * param['alpha'] + result[-1] * (1 - param['alpha']))
        result = [[v for v in result]]
        return result
    elif _type == 'EXP_SQRT':
        result = [raw[0]]
        for i in range(1, len(raw)):
            result.append( math.sqrt( math.pow(raw[i] * param['alpha'], 2) + math.pow(result[-1] * (1 - param['alpha']) , 2)))
        result = [[v for v in result]]
        return result
    elif _type == 'LOG':
        result = [(math.log(v) if v != 0 else 0) * 10.0 for v in raw]
        result = [[v for v in result]]
    elif _type == 'FFT':
        raw_corr = np.correlate(raw, raw, 'same')
        a = np.fft.fft(raw)
        b = [v for v in np.fft.ifft(np.log(a)).real]
        c = np.fft.fft(raw_corr)
        d = [v for v in np.fft.ifft(np.log(c)).real]
        result = [a,b,c,d]
    elif _type == 'ORIGIN':
        return [raw]
    elif _type == 'EXP_SMOOTH':
        result = ExponentialSmoothing(raw, trend='add', seasonal='add', seasonal_periods=param['period']).fit().fittedvalues
        result = [[v for v in result]]
    elif _type == 'BUTTER':
        fs = 20
        cutoff_freq = 5
        nyquist_freq = 0.5 * fs
        normal_cutoff = cutoff_freq / nyquist_freq
        b, a = butter(3, normal_cutoff, btype='low', analog=False)
        result = [[v for v in lfilter(b, a, raw)]]
    elif _type == 'SAVGOL':
        # 执行Savitzky-Golay滤波
        window_length = 3  # 窗口长度（奇数）
        polyorder = 2  # 多项式阶数
        result = [[v for v in savgol_filter(raw, window_length, polyorder)]]
    elif _type == 'WAVE':
        # 执行小波变换
        if param is not None and 'wavelet' in param and 'level' in param:
            wavelet = param['wavelet']  # 选择小波基函数
            level = param['level']  # 分解的级数
        else:
            wavelet = 'bior6.8'  # 选择小波基函数
            level = 10  # 分解的级数
        coeffs = pywt.wavedec(raw, wavelet, level=level)
        result = []
        # 将高频部分系数置零，以实现平滑
        for i in range(len(coeffs)):
            coeffs_smoothed = []
            for j in range(len(coeffs)):
                if j == i:
                    coeffs_smoothed.append(np.zeros_like(coeffs[j]))
                else:
                    coeffs_smoothed.append(coeffs[j])
            # 重构平滑后的信号
            result.append([v for v in pywt.waverec(coeffs_smoothed, wavelet)])
        return result
    elif _type == 'LOESS':
        x = np.linspace(0, len(raw) / 2, len(raw))
        # 执行Loess平滑
        lowess = sm.nonparametric.lowess(raw, x, frac=0.3)  # frac参数控制平滑带宽，可以调整以获得不同的平滑度
        # 获取平滑后的数据
        x_smooth, result = lowess.T
        return [[v for v in result]]
    elif _type == 'BESEL':
        x = np.linspace(0, len(raw), len(raw))
        tck = make_interp_spline(x, raw, k=5)
        x_new = np.linspace(0, int(len(raw) * 0.9), len(raw))  # 新的X坐标范围
        result = [[v for v in tck(x_new)]]
    elif _type == 'POLY':
        x = np.linspace(0, len(raw), len(raw))
        # 三阶多项式拟合
        degree = 3
        coefficients = np.polyfit(x, raw, degree)
        # 构建多项式函数
        poly = np.poly1d(coefficients)
        # 生成用于绘图的新X值
        x_new = np.linspace(min(x), max(x), len(raw))
        # 计算拟合后的Y值
        result = [[v for v in poly(x_new)]]
    elif _type == 'EMD':
        imfs = EMD().emd(np.array(raw), np.linspace(0, len(raw), len(raw)))
        result = [[vv for vv in v ] for v in imfs]
    elif _type == 'EEMD':
        imfs = EEMD().eemd(np.array(raw), np.linspace(0, len(raw), len(raw)))
        result = [[vv for vv in v ] for v in imfs]
    elif _type == 'CEEMDAN':
        imfs = CEEMDAN().ceemdan(np.array(raw), np.linspace(0, len(raw), len(raw)))
        result = [[vv for vv in v ] for v in imfs]
    elif _type == 'VMD':
        imfs, u_hat, omega = VMD(raw, alpha=1500, tau=0.0, K=6, DC=0, init=1, tol=1e-7)
        result = [[vv for vv in v ][:-1] if 'vmd_cut' in param and param['vmd_cut'] else [vv for vv in v ] for v in imfs]
    elif _type == 'SGMD':
        sgmd = SGMD(raw,len(raw),nfft=len(raw),threshold_corr=0.8,threshold_nmse=0.0001,mode='eig')
        imfs = sgmd.sgmd()
        result = [[vv for vv in v ] for v in imfs]
    elif _type == 'LMD':
        imfs, res = LMD().lmd(np.array(raw))
        result = imfs.tolist() + [res.tolist()]
        # result = imfs.tolist()
        result = [[vv for vv in v ] for v in result]
    if debug:
        plt.figure('a')
        plt.plot(raw)
        plt.figure('b')
        plt.plot(result)
        plt.show()
    return result


def adf_check(raw):
    return adfuller(raw)

def lb_check(raw, lg):
    re = lb_test(raw, lags=lg)
    return re.to_numpy()

def acf_check(raw, lg):
    return stattools.acf(raw, nlags=lg)

def pacf_check(raw, lg):
    return stattools.pacf(raw, nlags=lg)


def norm_min_max(data_array):
    shape = np.array(data_array[0][0]).shape
    if len(shape) == 3:
        max_arr = [[[0 for j in range(shape[2])] for i in range(shape[1])] for k in range(shape[0])]
        min_arr = [[[0 for j in range(shape[2])] for i in range(shape[1])] for k in range(shape[0])]
        for data in data_array:
            for i in range(len(data)):
                for j in range(len(max_arr)):
                    for k in range(len(max_arr[0])):
                        for l in range(len(max_arr[0][0])):
                            max_arr[j][k][l] = max(max_arr[j][k][l], data[i][j][k][l])
                            min_arr[j][k][l] = min(min_arr[j][k][l], data[i][j][k][l])
        for data in data_array:
            for i in range(len(data)):
                for j in range(len(max_arr)):
                    for k in range(len(max_arr[0])):
                        for l in range(len(max_arr[0][0])):
                            data[i][j][k][l] = (data[i][j][k][l] - min_arr[j][k][l]) / ((max_arr[j][k][l] - min_arr[j][k][l]) if (max_arr[j][k][l] - min_arr[j][k][l]) != 0 else 1)
    else:
        max_arr = [[0 for j in range(shape[1])] for i in range(shape[0])]
        min_arr = [[0 for j in range(shape[1])] for i in range(shape[0])]
        for data in data_array:
            for i in range(len(data)):
                for j in range(len(max_arr)):
                    for k in range(len(max_arr[0])):
                        max_arr[j][k] = max(max_arr[j][k], data[i][j][k])
                        min_arr[j][k] = min(min_arr[j][k], data[i][j][k])
        for data in data_array:
            for i in range(len(data)):
                for j in range(len(max_arr)):
                    for k in range(len(max_arr[0])):
                        data[i][j][k] = (data[i][j][k] - min_arr[j][k]) / ((max_arr[j][k] - min_arr[j][k]) if (max_arr[j][k] - min_arr[j][k]) != 0 else 1)


def norm_z_score(data_array):
    shape = np.array(data_array[0][0]).shape
    if len(shape) == 3:
        avg_arr = [[[0 for j in range(shape[2])] for i in range(shape[1])] for k in range(shape[0])]
        std_arr = [[[0 for j in range(shape[2])] for i in range(shape[1])] for k in range(shape[0])]
        for data in data_array:
            for i in range(len(data)):
                for j in range(len(avg_arr)):
                    for k in range(len(avg_arr[0])):
                        for l in range(len(avg_arr[0][0])):
                            avg_arr[j][k][l] += data[i][j][k][l]
        for j in range(len(avg_arr)):
            for k in range(len(avg_arr[0])):
                for l in range(len(avg_arr[0][0])):
                    avg_arr[j][k][l] /= sum([len(arr) for arr in data])
        for data in data_array:
            for i in range(len(data)):
                for j in range(len(std_arr)):
                    for k in range(len(std_arr[0])):
                        for l in range(len(std_arr[0][0])):
                            std_arr[j][k][l] += (data[i][j][k][l] - avg_arr[j][k][l]) * (data[i][j][k][l] - avg_arr[j][k][l])
        for j in range(len(std_arr)):
            for k in range(len(std_arr[0])):
                for l in range(len(std_arr[0][0])):
                    std_arr[j][k][l] /= (sum([len(arr) for arr in data]) - 1)
                    std_arr[j][k][l] = math.sqrt(std_arr[j][k][l])
        for data in data_array:
            for i in range(len(data)):
                for j in range(len(std_arr)):
                    for k in range(len(std_arr[0])):
                        for l in range(len(std_arr[0][0])):
                            data[i][j][k][l] = (data[i][j][k][l] - avg_arr[j][k][l]) / (std_arr[j][k][l] if std_arr[j][k][l] != 0 else 1)
    else:
        avg_arr = [[0 for j in range(shape[1])] for i in range(shape[0])]
        std_arr = [[0 for j in range(shape[1])] for i in range(shape[0])]
        for data in data_array:
            for i in range(len(data)):
                for j in range(len(avg_arr)):
                    for k in range(len(avg_arr[0])):
                        avg_arr[j][k] += data[i][j][k]
        for j in range(len(avg_arr)):
            for k in range(len(avg_arr[0])):
                avg_arr[j][k] /= sum([len(arr) for arr in data])
        for data in data_array:
            for i in range(len(data)):
                for j in range(len(std_arr)):
                    for k in range(len(std_arr[0])):
                        std_arr[j][k] += (data[i][j][k] - avg_arr[j][k]) * (data[i][j][k] - avg_arr[j][k])
        for j in range(len(std_arr)):
            for k in range(len(std_arr[0])):
                    std_arr[j][k] /= (sum([len(arr) for arr in data]) - 1)
                    std_arr[j][k] = math.sqrt(std_arr[j][k])
        for data in data_array:
            for i in range(len(data)):
                for j in range(len(std_arr)):
                    for k in range(len(std_arr[0])):
                        data[i][j][k] = (data[i][j][k] - avg_arr[j][k]) / (std_arr[j][k] if std_arr[j][k] != 0 else 1)


