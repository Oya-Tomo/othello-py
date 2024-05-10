import time
import torch
from torch import nn, optim, utils

from model import FNN
from dataloader import BATCH_SIZE, train_dataloader, test_dataloader
from env import MODEL_PATH
from utils import ProgressManager

RETRAIN_FLAG = True

fnn = FNN()

device = torch.device("cuda:0")

net = fnn.to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(
    net.parameters(), lr=0.03, momentum=0.0, weight_decay=0.000, nesterov=False
)

if RETRAIN_FLAG:
    model_state_dict = torch.load(MODEL_PATH)["model_state_dict"]
    optimizer_state_dict = torch.load(MODEL_PATH)["optimizer_state_dict"]
    net.load_state_dict(model_state_dict)
    optimizer.load_state_dict(optimizer_state_dict)
    print("trained state loaded")

pm = ProgressManager(
    batch=BATCH_SIZE,
    train_data_count=len(train_dataloader),
    test_data_count=len(test_dataloader),
)

for epoch in range(5):
    print(f"Epoch {epoch + 1} start")

    pm.reset()

    for x, y in train_dataloader:
        x, y = x.to(device), y.to(device)
        optimizer.zero_grad()
        outputs = net(x)
        loss = criterion(outputs, y)
        loss.backward()
        optimizer.step()
        pm.count_up_train_progress()
    pm.finish_progress()
    pm.reset()

    for x, y in train_dataloader:
        x, y = x.to(device), y.to(device)
        optimizer.zero_grad()
        outputs = net(x)
        loss = criterion(outputs, y)
        _, answer = y.max(1)
        _, predicted = outputs.max(1)
        pm.sum_train_loss(loss.item())
        pm.count_train_correct((predicted == answer).long().sum().item(), y.size(0))
        pm.count_up_train_progress()
    pm.finish_progress()
    pm.show_train_loss_accuracy()
    pm.reset()

    for x, y in test_dataloader:
        x, y = x.to(device), y.to(device)
        optimizer.zero_grad()
        outputs = net(x)
        loss = criterion(outputs, y)
        _, answer = y.max(1)
        _, predicted = outputs.max(1)
        pm.sum_test_loss(loss.item())
        pm.count_test_correct((predicted == answer).long().sum().item(), y.size(0))
        pm.count_up_test_progress()
    pm.finish_progress()
    pm.show_test_loss_accuracy()
    pm.reset()


torch.save(
    {
        "model_state_dict": net.to("cpu").state_dict(),
        "optimizer_state_dict": optimizer.state_dict(),
    },
    MODEL_PATH,
)
