import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.optim.lr_scheduler import ReduceLROnPlateau
from torch.utils.data import DataLoader, TensorDataset
import numpy as np
import uuid
import os
from base import *

class GroupNormalization(nn.Module):
    def __init__(self, num_groups, num_channels, eps=1e-5, affine=True):
        super(GroupNormalization, self).__init__()
        self.gn = nn.GroupNorm(num_groups, num_channels, eps, affine)
    def forward(self, x):
        return self.gn(x)

class CNNModel1D(nn.Module):
    def __init__(self, input_shape, dim):
        super(CNNModel1D, self).__init__()
        self.conv1 = nn.Conv1d(input_shape[0], dim, kernel_size=1)
        self.prelu1 = nn.PReLU()
        #self.gn1 = GroupNormalization(64, dim)
        #self.dropout1 = nn.Dropout(0.1)
        self.conv2 = nn.Conv1d(dim, dim, kernel_size=1)
        self.prelu2 = nn.PReLU()
        #self.gn2 = GroupNormalization(64, dim)
        #self.dropout2 = nn.Dropout(0.1)
        self.pool = nn.MaxPool1d(kernel_size=1, stride=1)
        self.flatten = nn.Flatten()
        self.fc = nn.Linear(dim * input_shape[1], dim)
        self.dropout3 = nn.Dropout(0.001)
        self.prelu3 = nn.PReLU()

    def forward(self, x):
        x = self.conv1(x)
        x = self.prelu1(x)
        #x = self.gn1(x)
        #x = self.dropout1(x)
        x = self.conv2(x)
        x = self.prelu2(x)
        #x = self.gn2(x)
        #x = self.dropout2(x)
        x = self.pool(x)
        x = self.flatten(x)
        x = self.fc(x)
        x = self.dropout3(x)
        x = self.prelu3(x)
        return x

class CNNModel2D(nn.Module):
    def __init__(self, input_shape, dim):
        super(CNNModel2D, self).__init__()
        self.conv1 = nn.Conv2d(input_shape[0], dim, kernel_size=(1,1), stride=(1,1))
        self.prelu1 = nn.PReLU()
        #self.gn1 = GroupNormalization(64, dim)
        #self.dropout1 = nn.Dropout(0.1)
        self.conv2 = nn.Conv2d(dim, dim, kernel_size=(1,1), stride=(1,1))
        self.prelu2 = nn.PReLU()
        #self.gn2 = GroupNormalization(64, dim)
        #self.dropout2 = nn.Dropout(0.1)
        self.pool = nn.MaxPool2d(kernel_size=(1,1), stride=1)
        self.flatten = nn.Flatten()
        self.fc = nn.Linear(dim * input_shape[1] * input_shape[2], dim)
        self.dropout3 = nn.Dropout(0.001)
        self.prelu3 = nn.PReLU()

    def forward(self, x):
        x = self.conv1(x)
        x = self.prelu1(x)
        #x = self.gn1(x)
        #x = self.dropout1(x)
        x = self.conv2(x)
        x = self.prelu2(x)
        #x = self.gn2(x)
        #x = self.dropout2(x)
        x = self.pool(x)
        x = self.flatten(x)
        x = self.fc(x)
        x = self.dropout3(x)
        x = self.prelu3(x)
        return x

def log_cosh_loss(y_pred, y_true):
    return torch.mean(torch.log(torch.cosh(y_pred - y_true)))

def CNN(trainX=None, testX=None, predX=None, trainY=None, testY=None):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    dim = trainY.shape[1]
    input_shape = trainX.shape[1:]
    use1d = len(input_shape) < 2 or (len(input_shape) == 2 and input_shape[-1] == 1)
    if use1d:
        model = CNNModel1D(input_shape, dim)
        trainX = np.transpose(trainX, (0,2,1)) if trainX.shape[2] == input_shape[0] else trainX
        testX = np.transpose(testX, (0,2,1)) if testX.shape[2] == input_shape[0] else testX
        predX = np.transpose(predX, (0,2,1)) if predX.shape[2] == input_shape[0] else predX
    else:
        model = CNNModel2D(input_shape, dim)
    model.to(device)

    train_dataset = TensorDataset(torch.tensor(trainX, dtype=torch.float32), torch.tensor(trainY, dtype=torch.float32))
    test_dataset = TensorDataset(torch.tensor(testX, dtype=torch.float32), torch.tensor(testY, dtype=torch.float32))
    train_loader = DataLoader(train_dataset, batch_size=1, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=1, shuffle=False)

    optimizer = optim.AdamW(model.parameters(), lr=0.0001)
    scheduler = ReduceLROnPlateau(optimizer, 'min', patience=10, verbose=True)
    best_loss = float('inf')
    checkpoint_filepath = str(uuid.uuid1()).replace('-', '') + '.weights.pt'

    for epoch in range(100):
        model.train()
        for x_batch, y_batch in train_loader:
            x_batch, y_batch = x_batch.to(device), y_batch.to(device)
            optimizer.zero_grad()
            outputs = model(x_batch)
            loss = log_cosh_loss(outputs, y_batch)
            loss.backward()
            optimizer.step()
        model.eval()
        val_losses = []
        with torch.no_grad():
            for x_batch, y_batch in test_loader:
                x_batch, y_batch = x_batch.to(device), y_batch.to(device)
                outputs = model(x_batch)
                val_loss = log_cosh_loss(outputs, y_batch)
                val_losses.append(val_loss.item())
        avg_val_loss = np.mean(val_losses)
        scheduler.step(avg_val_loss)
        if avg_val_loss < best_loss:
            best_loss = avg_val_loss
            torch.save(model.state_dict(), checkpoint_filepath)
        print(f"Epoch {epoch+1}/100, val_loss: {avg_val_loss:.6f}")

    model.load_state_dict(torch.load(checkpoint_filepath))
    model.eval()
    predX_tensor = torch.tensor(predX, dtype=torch.float32).to(device)
    with torch.no_grad():
        predY = model(predX_tensor).cpu().numpy()
    return predY

#detach


if __name__ == '__main__':
    data,show = loadProbRaw(500, [500,500], None, 'qxc_raw_txt', 3, 42, 14, mode='PROB_TIME_SERIES', enrich=None, reverse=False, sample_mode='random', debug=False, shrink=True, test_len=180, pred_len=14, output_chunk_length=2)
    CNN(data['train']['x'], data['test']['x'], data['pred']['x'], data['train']['y'], data['test']['y'])




