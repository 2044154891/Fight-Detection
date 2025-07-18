import os
import csv

FRAME_ROOT = os.path.join('data', 'frames')
LABELS_FILE = os.path.join('data', 'labels', 'labels.csv')
CATEGORIES = {'fight': 1, 'non_fight': 0}

# 删除旧标签文件
if os.path.exists(LABELS_FILE):
    os.remove(LABELS_FILE)
    print('已删除旧标签文件。')

# 自动创建labels目录
os.makedirs(os.path.dirname(LABELS_FILE), exist_ok=True)

rows = []
for category, label in CATEGORIES.items():
    frame_folder = os.path.join(FRAME_ROOT, category)
    for file in os.listdir(frame_folder):
        if file.lower().endswith(('.jpg', '.jpeg', '.png')):
            frame_path = os.path.join('frames', category, file)
            rows.append([frame_path, label])

with open(LABELS_FILE, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['frame_path', 'label'])
    writer.writerows(rows)
print(f"标签文件已生成: {LABELS_FILE}，共 {len(rows)} 条") 