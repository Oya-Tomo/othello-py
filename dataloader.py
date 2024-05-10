import torch
from torch.utils.data import Dataset, DataLoader, random_split
import numpy as np

from env import BATCH_SIZE, SPLIT_RATIO

board_data = np.load(f"data/wthor-5.npz")["arr_0"]
moves_data = np.load(f"data/wthor-5.npz")["arr_1"]

for i in range(6, 10):
    npz_file = np.load(f"data/wthor-{i}.npz")
    board_data = np.concatenate([board_data, npz_file["arr_0"]], 0)
    moves_data = np.concatenate([moves_data, npz_file["arr_1"]], 0)


x_data: np.ndarray = board_data
y_data: np.ndarray = moves_data.reshape((-1, 64))

x_data = x_data.astype(np.float32)
y_data = y_data.astype(np.float32)

TRAIN_SPLIT_COUNT = int(len(x_data) * SPLIT_RATIO)
TEST_SPLIT_COUNT = len(x_data) - TRAIN_SPLIT_COUNT


class OthelloDataset(Dataset):
    def __init__(self, x, y, transform=None) -> None:
        self.x = x
        self.y = y
        self.transform = transform

    def __getitem__(self, index):
        return self.x[index].transpose(), self.y[index]

    def __len__(self):
        return len(self.x)


dataset = OthelloDataset(x_data, y_data)

train_data, test_data = random_split(dataset, [TRAIN_SPLIT_COUNT, TEST_SPLIT_COUNT])

train_dataloader = DataLoader(train_data, batch_size=BATCH_SIZE)
test_dataloader = DataLoader(test_data, batch_size=BATCH_SIZE)

if __name__ == "__main__":
    print(train_data[0])
    print(test_data[0])
