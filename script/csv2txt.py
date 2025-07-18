import os
import pandas as pd

LABELS_DIR = os.path.join('result', 'labels')
TXT_DIR = os.path.join('resulttxt')
os.makedirs(TXT_DIR, exist_ok=True)

for csv_file in os.listdir(LABELS_DIR):
    if not csv_file.endswith('.csv'):
        continue
    csv_path = os.path.join(LABELS_DIR, csv_file)
    df = pd.read_csv(csv_path)
    # 按frame_name排序
    df = df.sort_values('frame_name')
    txt_name = os.path.splitext(csv_file)[0] + '.txt'
    txt_path = os.path.join(TXT_DIR, txt_name)
    with open(txt_path, 'w') as f:
        for label in df['pred_label']:
            f.write(f'{label}\n')
    print(f'{csv_file} -> {txt_name}') 