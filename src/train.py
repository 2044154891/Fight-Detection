import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import models, transforms
from dataset import FrameDataset
from PIL import Image  # 确保PIL已导入
import pandas as pd    # 确保pandas已导入
import numpy as np     # 确保numpy已导入

def main():
    # 配置
    CSV_PATH = os.path.join('data', 'labels', 'labels.csv')
    FRAME_ROOT = 'data'  # dataset.py中拼接的是root_dir+csv内路径
    MODEL_PATH = 'fight_detection_resnet18.pth'
    BATCH_SIZE = 32
    EPOCHS = 10
    LR = 1e-4
    DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    # 数据增强与预处理
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    dataset = FrameDataset(CSV_PATH, FRAME_ROOT, transform=transform)
    dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True, num_workers=2)

    # 模型
    model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
    model.fc = nn.Linear(model.fc.in_features, 2)
    model = model.to(DEVICE)

    # 损失与优化器
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=LR)

    # 训练
    for epoch in range(EPOCHS):
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0
        for images, labels in dataloader:
            images, labels = images.to(DEVICE), labels.to(DEVICE)
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item() * images.size(0)
            _, predicted = torch.max(outputs, 1)
            correct += (predicted == labels).sum().item()
            total += labels.size(0)
        epoch_loss = running_loss / total
        epoch_acc = correct / total
        print(f"Epoch {epoch+1}/{EPOCHS} Loss: {epoch_loss:.4f} Acc: {epoch_acc:.4f}")

    # 保存模型
    torch.save(model.state_dict(), MODEL_PATH)
    print(f"模型已保存到 {MODEL_PATH}")

if __name__ == "__main__":
    main() 