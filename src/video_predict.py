import os
import cv2
import torch
from torchvision import models, transforms
from PIL import Image
import pandas as pd

# 配置
VIDEO_DIR = 'testvideo'
RESULT_DIR = 'predict_result'
FRAME_DIR = os.path.join(RESULT_DIR, 'frames')
CSV_PATH = os.path.join(RESULT_DIR, 'result.csv')
MODEL_PATH = 'fight_detection_resnet18.pth'
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# 创建结果目录
os.makedirs(FRAME_DIR, exist_ok=True)

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
    base_name = os.path.splitext(os.path.basename(video_path))[0]
    frame_paths = []
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_name = f"{base_name}_{frame_count:05d}.jpg"
        frame_path = os.path.join(save_dir, frame_name)
        cv2.imwrite(frame_path, frame)
        frame_paths.append(frame_path)
        frame_count += 1
    cap.release()
    print(f"{video_path} 提取 {frame_count} 帧")
    return frame_paths

def predict_frames(frame_paths):
    results = []
    with torch.no_grad():
        for frame_path in frame_paths:
            image = Image.open(frame_path).convert('RGB')
            input_tensor = transform(image).unsqueeze(0).to(DEVICE)
            output = model(input_tensor)
            prob = torch.softmax(output, dim=1)[0]
            pred = torch.argmax(prob, dim=1).item()
            fight_prob = float(prob[1])  # 打架类别的概率
            results.append({'frame_name': os.path.basename(frame_path), 'fight_prob': fight_prob, 'pred_label': pred})
    return results

def main():
    all_frame_paths = []
    for file in os.listdir(VIDEO_DIR):
        if file.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
            video_path = os.path.join(VIDEO_DIR, file)
            frame_paths = extract_frames(video_path, FRAME_DIR)
            all_frame_paths.extend(frame_paths)
    # 预测
    results = predict_frames(all_frame_paths)
    # 保存csv
    pd.DataFrame(results).to_csv(CSV_PATH, index=False)
    print(f"预测结果已保存到 {CSV_PATH}")

if __name__ == '__main__':
    main() 