import math
import torch
import torch.nn as nn
import torch.nn.functional as F
from model.sync_batchnorm.batchnorm import SynchronizedBatchNorm2d
#from sync_batchnorm.batchnorm import SynchronizedBatchNorm2d
class ASPP_Module(nn.Module):
    def __init__(self, inplanes, planes, dilation, BatchNorm=nn.BatchNorm2d):
        super(ASPP_Module, self).__init__()
        if dilation == 1:
            kernel_size = 1
            padding = 0
        else:
            kernel_size = 3
            padding = dilation
        self.atrous_convolution = nn.Conv2d(inplanes, planes, kernel_size=kernel_size,
                                            stride=1, padding=padding, dilation=dilation, bias=False)
        self.bn = BatchNorm(planes)
        self.relu = nn.ReLU()

        self._init_weight()

    def forward(self, x):
        x = self.atrous_convolution(x)
        x = self.bn(x)

        return self.relu(x)
    
    def _init_weight(self):
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                torch.nn.init.kaiming_normal_(m.weight)
            elif isinstance(m, nn.BatchNorm2d):
                m.weight.data.fill_(1)
                m.bias.data.zero_()
            elif isinstance(m, SynchronizedBatchNorm2d):
                m.weight.data.fill_(1)
                m.bias.data.zero_()

class ASPP(nn.Module):
    def __init__(self, output_stride, BatchNorm=nn.BatchNorm2d, inplanes=2048):
        super(ASPP, self).__init__()
        if output_stride == 16:
            dilations = [1, 6, 12, 18]
        elif output_stride == 8:
            dilations = [1, 12, 24, 36]
        else:
            raise NotImplementedError

        self.aspp1 = ASPP_Module(inplanes, 256, dilation=dilations[0], BatchNorm=BatchNorm)
        self.aspp2 = ASPP_Module(inplanes, 256, dilation=dilations[1], BatchNorm=BatchNorm)
        self.aspp3 = ASPP_Module(inplanes, 256, dilation=dilations[2], BatchNorm=BatchNorm)
        self.aspp4 = ASPP_Module(inplanes, 256, dilation=dilations[3], BatchNorm=BatchNorm)

        self.global_avg_pool = nn.Sequential(nn.AdaptiveAvgPool2d((1, 1)),
                                             nn.Conv2d(inplanes, 256, 1, stride=1, bias=False),
                                             BatchNorm(256),
                                             nn.ReLU())
        self.conv1 = nn.Conv2d(1280, 256, 1, bias=False)
        self.bn1 = BatchNorm(256)
        self.relu = nn.ReLU()
        #self.dropout = nn.Dropout(0.5)
        self._init_weight()

    def forward(self, x):
        x1 = self.aspp1(x)
        x2 = self.aspp2(x)
        x3 = self.aspp3(x)
        x4 = self.aspp4(x)
        x5 = self.global_avg_pool(x)
        x5 = F.interpolate(x5, size=x4.size()[2:], mode='bilinear', align_corners=True)
        x = torch.cat((x1, x2, x3, x4, x5), dim=1)
        # below structure not show in orginal paper
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)
        # x = self.dropout(x)
        return x

    def _init_weight(self):
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                torch.nn.init.kaiming_normal_(m.weight)
            elif isinstance(m, nn.BatchNorm2d):
                m.weight.data.fill_(1)
                m.bias.data.zero_()
            elif isinstance(m,  SynchronizedBatchNorm2d):
                m.weight.data.fill_(1)
                m.bias.data.zero_()

def build_aspp(output_stride, BatchNorm):
    return ASPP(output_stride, BatchNorm)
