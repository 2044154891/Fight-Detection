import os
import random
import shutil
import csv

FRAME_DIR = os.path.join('data', 'frames')
EVAL_DIR = os.path.join('data', 'eval_frames')
LABELS_CSV = os.path.join('data', 'labels', 'eval_sample.csv')
SAMPLE_NUM = 200
CATEGORIES = {'fight': 1, 'non_fight': 0}

os.makedirs(EVAL_DIR, exist_ok=True)
os.makedirs(os.path.dirname(LABELS_CSV), exist_ok=True)

def get_all_frames():
    all_frames = []
    for category, label in CATEGORIES.items():
        frame_folder = os.path.join(FRAME_DIR, category)
        for fname in os.listdir(frame_folder):
            if fname.lower().endswith(('.jpg', '.jpeg', '.png')):
                full_path = os.path.join(frame_folder, fname)
                all_frames.append((full_path, fname, label))
    return all_frames

def main():
    all_frames = get_all_frames()
    if len(all_frames) < SAMPLE_NUM:
        raise ValueError(f"总帧数不足 {SAMPLE_NUM}，当前仅有 {len(all_frames)}")
    sampled = random.sample(all_frames, SAMPLE_NUM)
    # 复制帧到EVAL_DIR，并记录标签
    rows = []
    for src_path, fname, label in sampled:
        dst_path = os.path.join(EVAL_DIR, fname)
        shutil.copy2(src_path, dst_path)
        rows.append([fname, label])
    # 写入CSV
    with open(LABELS_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['frame_name', 'label'])
        writer.writerows(rows)
    print(f"已随机采样并复制 {SAMPLE_NUM} 帧到 {EVAL_DIR}，标签写入 {LABELS_CSV}")

if __name__ == '__main__':
    main() 