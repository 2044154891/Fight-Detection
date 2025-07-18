import os
import shutil
import cv2
import torch
from torchvision import models, transforms
from PIL import Image
import pandas as pd

# 配置
VIDEO_DIR = 'testvideo'
RESULT_DIR = 'result'
FRAMES_ROOT = os.path.join(RESULT_DIR, 'frames')
MODEL_PATH = 'fight_detection_resnet18.pth'
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# 清空结果目录
if os.path.exists(FRAMES_ROOT):
    shutil.rmtree(FRAMES_ROOT)
os.makedirs(FRAMES_ROOT, exist_ok=True)
# 清空result目录下所有csv文件
for f in os.listdir(RESULT_DIR):
    if f.endswith('.csv'):
        os.remove(os.path.join(RESULT_DIR, f))

# 加载模型
model = models.resnet18(weights=None)
model.fc = torch.nn.Linear(model.fc.in_features, 2)
model.load_state_dict(torch.load(MODEL_PATH, map_location=DEVICE))
model = model.to(DEVICE)
model.eval()

# 预处理
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

def extract_frames(video_path, save_dir):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"无法打开视频: {video_path}")
        return []
    frame_paths = []
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_name = f"{frame_count:05d}.jpg"
        frame_path = os.path.join(save_dir, frame_name)
        cv2.imwrite(frame_path, frame)
        frame_paths.append(frame_path)
        frame_count += 1
    cap.release()
    print(f"{os.path.basename(video_path)} 提取 {frame_count} 帧")
    return frame_paths

def predict_frames(frame_paths):
    results = []
    with torch.no_grad():
        for frame_path in frame_paths:
            try:
                image = Image.open(frame_path).convert('RGB')
            except Exception as e:
                print(f"读取图片失败: {frame_path}, 错误: {e}")
                continue
            input_tensor = transform(image).unsqueeze(0).to(DEVICE)
            output = model(input_tensor)
            prob = torch.softmax(output, dim=1)[0]
            pred = torch.argmax(prob).item()  # 修正此处
            fight_prob = float(prob[1])
            results.append({'frame_name': os.path.basename(frame_path), 'fight_prob': fight_prob, 'pred_label': pred})
    return results

def main():
    for file in os.listdir(VIDEO_DIR):
        if not file.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
            continue
        video_name = os.path.splitext(file)[0]
        frame_dir = os.path.join(FRAMES_ROOT, video_name)
        csv_path = os.path.join(RESULT_DIR, f'{video_name}.csv')
        # 不再检查是否已预测过，全部重新预测
        os.makedirs(frame_dir, exist_ok=True)
        video_path = os.path.join(VIDEO_DIR, file)
        frame_paths = extract_frames(video_path, frame_dir)
        if not frame_paths:
            print(f"{file} 无帧可预测，跳过。")
            continue
        results = predict_frames(frame_paths)
        pd.DataFrame(results).to_csv(csv_path, index=False)
        print(f"{file} 预测完成，结果已保存到 {csv_path}")

if __name__ == '__main__':
    main() 