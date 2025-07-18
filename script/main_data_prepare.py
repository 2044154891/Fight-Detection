import subprocess
import sys
import os

# 保证脚本路径正确
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

print('1. 批量重命名视频...')
subprocess.run([sys.executable, os.path.join(SCRIPT_DIR, 'rename_videos.py')], check=True)

print('2. 清空并重新提取所有帧...')
subprocess.run([sys.executable, os.path.join(SCRIPT_DIR, 'extract_frames.py')], check=True)

print('3. 删除并重新生成标签文件...')
subprocess.run([sys.executable, os.path.join(SCRIPT_DIR, 'generate_labels.py')], check=True)

print('数据准备流程已全部完成！') 