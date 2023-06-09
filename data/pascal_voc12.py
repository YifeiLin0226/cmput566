import os

import torch
from torch.utils.data import Dataset
from mmseg.datasets import PascalVOCDataset
from mmseg.datasets.custom import CustomDataset

from .config import pascal_voc12

class PascalVOC(Dataset):

    def __init__(self, split):
        if split == 'train' or split == 'val':
            self.dataset = PascalVOCDataset(**pascal_voc12.data[split])
        else:
            self.dataset = PascalVOCDataset(**pascal_voc12.data[split], test_mode = True)
        self.split = split
        self.classes = self.dataset.CLASSES
        self.palette = self.dataset.PALETTE

    def __len__(self):
        return len(self.dataset)
    
    def __getitem__(self, idx):
        sample = self.dataset[idx]
        if self.split == 'train':
            data = {'img': sample['img'].data, 'gt_semantic_seg': sample['gt_semantic_seg'].data, 'img_metas':sample['img_metas'].data}
        elif self.split == 'val':
            data = {'img': sample['img'][0], 'gt_semantic_seg':torch.from_numpy(sample['gt_semantic_seg'][0]), 'img_metas': sample['img_metas'][0].data}
        else:
            data = {'img': sample['img'][0]}
            
        return data

