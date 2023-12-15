import gin
import os
import cv2
import torch

import numpy as np

from loguru import logger
from rich.progress import track
from torch.utils.data import Dataset
from torchvision import transforms
from utils import check_and_retrieveVocabulary

data = np.load('vocab/GrandStaff_bekrnw2i.npy', allow_pickle=True)

print((data.item()))
print(len(data.item()))