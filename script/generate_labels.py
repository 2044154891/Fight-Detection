import os
import csv

FRAME_DIR = os.path.join('data', 'frames')
LABELS_FILE = os.path.join('data', 'labels', 'labels.csv')
CATEGORIES = {'fight': 1, 'non_fight': 0}

# 自动创建labels目录
os.makedirs(os.path.dirname(LABELS_FILE), exist_ok=True)

def main():
    rows = []
    for category, label in CATEGORIES.items():
        frame_folder = os.path.join(FRAME_DIR, category)
        for file in os.listdir(frame_folder):
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                frame_path = os.path.join('frames', category, file)  # 相对路径
                rows.append([frame_path, label])
    # 写入CSV
    with open(LABELS_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['frame_path', 'label'])
        writer.writerows(rows)
    print(f"标签文件已生成: {LABELS_FILE}，共 {len(rows)} 条")

if __name__ == '__main__':
    main() 