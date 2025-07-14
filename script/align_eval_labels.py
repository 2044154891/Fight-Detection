import os
import csv

EVAL_DIR = os.path.join('data', 'eval_frames')
LABELS_CSV = os.path.join('data', 'labels', 'eval_sample.csv')
OUTPUT_CSV = os.path.join('data', 'labels', 'eval_sample_aligned.csv')

# 读取标签
label_dict = {}
with open(LABELS_CSV, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        label_dict[row['frame_name']] = row['label']

# 获取eval_frames下所有图片，按文件名排序
frame_files = [f for f in os.listdir(EVAL_DIR) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
frame_files.sort()

# 生成对齐后的标签列表
aligned_rows = []
for fname in frame_files:
    label = label_dict.get(fname, None)
    if label is not None:
        aligned_rows.append([fname, label])
    else:
        print(f"警告: {fname} 未在标签文件中找到，将跳过")

# 写入新csv
with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['frame_name', 'label'])
    writer.writerows(aligned_rows)

print(f"已生成顺序对齐的标签文件: {OUTPUT_CSV}，共 {len(aligned_rows)} 条") 