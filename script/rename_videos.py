import os

VIDEO_ROOT = os.path.join('data', 'videos')
CATEGORIES = ['fight', 'non_fight']

for category in CATEGORIES:
    folder = os.path.join(VIDEO_ROOT, category)
    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f)) and os.path.splitext(f)[1].lower() in ['.mp4', '.avi', '.mov', '.mkv']]
    files.sort()
    for idx, file in enumerate(files, 1):
        ext = os.path.splitext(file)[1].lower()
        new_name = f"{category}_{idx:04d}{ext}"
        src = os.path.join(folder, file)
        dst = os.path.join(folder, new_name)
        if src != dst:
            os.rename(src, dst)
            print(f"{file} -> {new_name}")
    print(f"{category} 类别共重命名 {len(files)} 个视频文件。") 