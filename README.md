# Fight Detection 项目说明

本项目实现了基于深度学习的打架斗殴行为自动识别，支持从原始视频到模型训练、推理、结果输出的全流程自动化。项目结构清晰，脚本规范，便于复现和扩展。

---

## 目录结构与文件说明

```
Fight_Detection/
├── data/                    # 数据相关目录
│   ├── videos/              # 原始视频（fight/non_fight）
│   ├── frames/              # 提取的帧图片（fight/non_fight）
│   └── labels/              # 标签文件（labels.csv）
├── script/                  # 数据处理与自动化脚本
│   ├── main_data_prepare.py # 一键数据准备主脚本
│   ├── rename_videos.py     # 视频批量重命名脚本
│   ├── extract_frames.py    # 视频帧提取与清理脚本
│   └── generate_labels.py   # 标签生成与清理脚本
├── src/                     # 模型训练与推理核心代码
│   ├── train.py             # 模型训练脚本
│   ├── predict.py           # 单帧推理脚本
│   ├── video_predict.py     # 批量视频推理脚本
│   └── dataset.py           # 数据集定义
├── result/                  # 推理结果输出目录
│   └── *.csv                # 每个测试视频的推理结果
├── ans/                     # 测试集真实标签（如anslabels.csv）
├── testvideo/               # 待推理视频目录
├── fight_detection_resnet18.pth # 训练好的模型权重
├── requirements.txt         # 依赖包列表
├── calculate.py             # 预测与真实标签准确率计算脚本
├── README.md                # 项目说明
└── .gitignore               # git忽略文件
```

---

# 一、模型训练流程

## 1. 数据准备

- 将打架视频放入`data/videos/fight/`，非打架视频放入`data/videos/non_fight/`。
- 运行一键数据准备脚本，自动完成视频重命名、帧清空与提取、标签清空与生成：

```bash
python script/main_data_prepare.py
```
- 该脚本会依次调用：
  - `rename_videos.py`：将所有视频重命名为`fight_0001.mp4`、`non_fight_0001.mp4`等规范格式。
  - `extract_frames.py`：清空所有帧图片，重新提取所有视频帧到`data/frames/`。
  - `generate_labels.py`：删除旧标签，重新生成`data/labels/labels.csv`。

## 2. 模型训练

- 运行训练脚本：

```bash
python src/train.py
```
- 训练参数（可在脚本内修改）：
  - batch size：32
  - epoch：10
  - 学习率：0.0001
  - 优化器：Adam
- 训练完成后，模型权重保存在根目录`fight_detection_resnet18.pth`。

---

# 二、模型预测与结果输出

## 1. 视频推理

- 将待推理视频放入`testvideo/`目录。
- 运行批量推理脚本：

```bash
python src/video_predict.py
```
- 脚本会自动：
  - 清空`result/frames/`和`result/`下所有历史推理结果
  - 对`testvideo/`下每个视频逐帧推理，输出每帧的概率和标签
  - 每个视频的推理结果保存为`result/视频名.csv`，帧图片保存为`result/frames/视频名/`

## 2. 结果评估

- 若有真实标签（如`ans/anslabels.csv`），可用`calculate.py`计算准确率：

```bash
python calculate.py
```
- 该脚本会自动对齐预测结果和真实标签，输出总数、正确数和准确率。

## 3. 结果文件命名规范

- 推理结果文件：`result/视频名.csv`，如`result/mytest.csv`
- 真实标签文件：`ans/anslabels.csv`
- 预测与真实标签对比脚本：`calculate.py`

---

# 依赖安装

建议使用Python 3.8+，推荐Anaconda/Miniconda环境。

```bash
pip install -r requirements.txt
```

---

# 其他说明

- 所有脚本均有详细注释，便于二次开发。
- .gitignore已配置，避免上传大文件和中间结果。
- 如需增量数据处理、参数自定义、结果可视化等高级功能，可在脚本内调整参数或联系开发者。

---

如有问题欢迎提issue或联系作者。 