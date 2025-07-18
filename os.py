import matplotlib.pyplot as plt

# 伪造10个epoch的数据
epochs = list(range(1, 11))
train_losses = [1.0, 0.85, 0.72, 0.60, 0.52, 0.45, 0.40, 0.36, 0.33, 0.30]
val_losses   = [1.05, 0.90, 0.80, 0.70, 0.62, 0.58, 0.55, 0.53, 0.52, 0.51]
train_accuracies = [0.55, 0.62, 0.68, 0.74, 0.79, 0.83, 0.86, 0.88, 0.90, 0.92]
val_accuracies   = [0.52, 0.60, 0.65, 0.70, 0.74, 0.77, 0.79, 0.80, 0.81, 0.82]

plt.figure(figsize=(12,5))

# 损失曲线
plt.subplot(1,2,1)
plt.plot(epochs, train_losses, marker='o', label='训练损失')
plt.plot(epochs, val_losses, marker='s', label='验证损失')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('训练/验证损失曲线')
plt.legend()
plt.grid(True)

# 准确率曲线
plt.subplot(1,2,2)
plt.plot(epochs, train_accuracies, marker='o', label='训练准确率')
plt.plot(epochs, val_accuracies, marker='s', label='验证准确率')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.title('训练/验证准确率曲线')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()
