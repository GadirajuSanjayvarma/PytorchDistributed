from __future__ import print_function
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms


class Net1(nn.Module):
    def __init__(self):
        super(Net1, self).__init__()
        self.conv1 = nn.Conv2d(3, 32, 3, padding=1,bias=False)
        self.conv2 = nn.Conv2d(32, 64, 3, padding=1,bias=False)
        self.pool1 = nn.MaxPool2d(2, 2)
        self.conv3 = nn.Conv2d(64, 128, 3, padding=1,bias=False)
        self.conv4 = nn.Conv2d(128, 256, 3, padding=1,bias=False)
        self.pool2 = nn.MaxPool2d(2, 2)
        self.conv5 = nn.Conv2d(256, 512, 3,bias=False)
        self.conv6 = nn.Conv2d(512, 1024, 3,bias=False)
        self.conv7 = nn.Conv2d(1024, 100, 3,bias=False)
        self.gap=nn.AdaptiveAvgPool2d((1,1))
        self.params=[self.conv1,self.conv2,self.conv3,self.conv4,self.conv5,self.conv6,self.conv7]
    def forward(self, x):
        x = self.pool1(F.relu(self.conv2(F.relu(self.conv1(x)))))
        x = self.pool2(F.relu(self.conv4(F.relu(self.conv3(x)))))
        x = F.relu(self.conv6(F.relu(self.conv5(x))))
        x = F.relu(self.conv7(x))
        x=self.gap(x)
        x = x.view(-1, 100)
        return F.log_softmax(x)
