import os

VIDEO_DIR = os.path.join('data', 'videos', 'fight')

# 支持的视频格式
VIDEO_EXTS = ['.mp4', '.avi', '.mov', '.mkv']

def main():
    files = [f for f in os.listdir(VIDEO_DIR) if os.path.isfile(os.path.join(VIDEO_DIR, f)) and os.path.splitext(f)[1].lower() in VIDEO_EXTS]
    files.sort()  # 按文件名排序
    for idx, file in enumerate(files, 1):
        ext = os.path.splitext(file)[1].lower()
        new_name = f"fight_{idx:04d}{ext}"
        src = os.path.join(VIDEO_DIR, file)
        dst = os.path.join(VIDEO_DIR, new_name)
        os.rename(src, dst)
        print(f"{file} -> {new_name}")
    print(f"共重命名 {len(files)} 个视频文件。")

if __name__ == '__main__':
    main() 