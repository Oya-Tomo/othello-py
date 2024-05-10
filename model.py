from torch import nn
import torch.nn.functional as F
import torch

ki = 2
k1 = 512
k2 = 256
k3 = 128
k4 = 64
ko = 1


# class Bias(torch.nn.Module):
#     def __init__(self, in_ftr) -> None:
#         super().__init__()
#         bias_value = torch.randn((in_ftr))
#         self.bias_layer = torch.nn.Parameter(bias_value)

#     def forward(self, x):
#         return x + self.bias_layer


class FNN(nn.Module):
    def __init__(self) -> None:
        super(FNN, self).__init__()

        self.layer1 = nn.Sequential(
            nn.Conv2d(ki, k1, kernel_size=3, padding=1),
            nn.BatchNorm2d(k1),
            nn.ReLU(),
        )
        self.layer2 = nn.Sequential(
            nn.Conv2d(k1, k1, kernel_size=3, padding=1),
            nn.BatchNorm2d(k1),
            nn.ReLU(),
        )
        self.layer3 = nn.Sequential(
            nn.Conv2d(k1, k2, kernel_size=3, padding=1),
            nn.BatchNorm2d(k2),
            nn.ReLU(),
        )
        self.layer4 = nn.Sequential(
            nn.Conv2d(k2, k2, kernel_size=3, padding=1),
            nn.BatchNorm2d(k2),
            nn.ReLU(),
        )
        self.layer5 = nn.Sequential(
            nn.Conv2d(k2, k3, kernel_size=3, padding=1),
            nn.BatchNorm2d(k3),
            nn.ReLU(),
        )
        self.layer6 = nn.Sequential(
            nn.Conv2d(k3, k3, kernel_size=3, padding=1),
            nn.BatchNorm2d(k3),
            nn.ReLU(),
        )
        self.layer7 = nn.Sequential(
            nn.Conv2d(k3, k4, kernel_size=3, padding=1),
            nn.BatchNorm2d(k4),
            nn.ReLU(),
        )
        self.layer8 = nn.Sequential(
            nn.Conv2d(k4, k4, kernel_size=3, padding=1),
            nn.BatchNorm2d(k4),
            nn.ReLU(),
        )
        self.layer9 = nn.Sequential(
            nn.Conv2d(k4, ko, kernel_size=1),
            nn.BatchNorm2d(ko),
            nn.Flatten(),
            nn.Softmax(dim=1),
        )

    def forward(self, x):
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)
        x = self.layer5(x)
        x = self.layer6(x)
        x = self.layer7(x)
        x = self.layer8(x)
        x = self.layer9(x)

        return x
