import pandas as pd

# 读取预测结果和真实标签
pred_df = pd.read_csv('result/labels/mytest.csv')
gt_df = pd.read_csv('ans/anslabels.csv')

# 对齐frame_name，确保顺序一致
merged = pd.merge(pred_df, gt_df, on='frame_name', suffixes=('_pred', '_gt'))

# 计算准确率
correct = (merged['pred_label_pred'] == merged['pred_label_gt']).sum()
total = len(merged)
accuracy = correct / total if total > 0 else 0

print(f'预测帧总数: {total}')
print(f'预测正确帧数: {correct}')
print(f'准确率: {accuracy:.4f}') 