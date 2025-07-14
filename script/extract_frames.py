import os
import cv2

# 配置路径
VIDEO_DIR = os.path.join('data', 'videos')
FRAME_DIR = os.path.join('data', 'frames')
CATEGORIES = ['fight']  # 只处理fight

# 每隔多少帧提取一帧（1为每帧都提取）
EXTRACT_EVERY = 1
# 最大帧数
MAX_TOTAL_FRAMES = 10000

def get_total_frames():
    total = 0
    for category in CATEGORIES:
        frame_folder = os.path.join(FRAME_DIR, category)
        if os.path.exists(frame_folder):
            total += len([f for f in os.listdir(frame_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
    return total

# 自动创建目录
for category in CATEGORIES:
    os.makedirs(os.path.join(VIDEO_DIR, category), exist_ok=True)
    os.makedirs(os.path.join(FRAME_DIR, category), exist_ok=True)

def extract_frames_from_video(video_path, save_dir, extract_every=1, max_total_frames=10000):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"无法打开视频: {video_path}")
        return 0
    base_name = os.path.splitext(os.path.basename(video_path))[0]
    frame_count = 0
    saved_count = 0
    while True:
        if get_total_frames() >= max_total_frames:
            print(f"已达到最大帧数 {max_total_frames}，停止提取。")
            break
        ret, frame = cap.read()
        if not ret:
            break
        if frame_count % extract_every == 0:
            frame_name = f"{base_name}_{frame_count:05d}.jpg"
            frame_path = os.path.join(save_dir, frame_name)
            cv2.imwrite(frame_path, frame)
            saved_count += 1
        frame_count += 1
    cap.release()
    print(f"{video_path} 提取 {saved_count} 帧到 {save_dir}")
    return saved_count

def main():
    for category in CATEGORIES:
        video_folder = os.path.join(VIDEO_DIR, category)
        frame_folder = os.path.join(FRAME_DIR, category)
        for file in os.listdir(video_folder):
            if get_total_frames() >= MAX_TOTAL_FRAMES:
                print(f"总帧数已达 {MAX_TOTAL_FRAMES}，提前终止所有提取。")
                return
            if file.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
                video_path = os.path.join(video_folder, file)
                extract_frames_from_video(video_path, frame_folder, EXTRACT_EVERY, MAX_TOTAL_FRAMES)

if __name__ == '__main__':
    main() 