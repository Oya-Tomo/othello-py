import torch
import numpy as np

from model import FNN
from env import MODEL_PATH

import dataloader

fnn = FNN()
fnn.load_state_dict(torch.load(MODEL_PATH)["model_state_dict"])
print("loaded ...")

B = (1, 0)
W = (0, 1)
E = (0, 0)

test_data = [
    [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)],
    [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)],
    [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)],
    [(0, 0), (0, 0), (0, 0), (0, 1), (1, 0), (0, 0), (0, 0), (0, 0)],
    [(0, 0), (0, 0), (0, 0), (1, 0), (0, 1), (0, 0), (0, 0), (0, 0)],
    [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)],
    [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)],
    [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)],
]


test_data_np = np.array(test_data, dtype=np.float32).transpose()
test_data_pt = torch.Tensor([test_data_np])

fnn.eval()
res = fnn(test_data_pt)

print(res[0].reshape((8, 8)))
