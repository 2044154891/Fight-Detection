import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

# 读取真实标签和预测结果
gt = pd.read_csv('ans/anslabels.csv')  # 真实标签
pred = pd.read_csv('result/labels/mytest.csv')  # 模型预测

# 对齐（假设frame_name完全一致且顺序一致，否则需merge）
y_true = gt['pred_label']
y_pred = pred['pred_label']

# 计算指标
acc = accuracy_score(y_true, y_pred)
prec = precision_score(y_true, y_pred)
rec = recall_score(y_true, y_pred)
f1 = f1_score(y_true, y_pred)
cm = confusion_matrix(y_true, y_pred)

print(f'准确率: {acc:.3f}')
print(f'精确率: {prec:.3f}')
print(f'召回率: {rec:.3f}')
print(f'F1分数: {f1:.3f}')
print('混淆矩阵:')
print(cm)