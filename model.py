import torch
import torch.nn as nn
import os

class Linear_QNet(nn.Module):
    def __init__(self, input_size=11, hidden_size=128, output_size=3):
        super().__init__()
        self.linear1 = nn.Linear(input_size, hidden_size)
        self.linear2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = torch.relu(self.linear1(x))
        return self.linear2(x)

    def save(self, file_name="model.pth"):
        torch.save(self.state_dict(), file_name)

    def load(self, file_name="model.pth"):
        self.load_state_dict(torch.load(file_name))
        self.eval()