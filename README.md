# Fight Detection

基于深度学习的打架/斗殴行为识别项目。
本项目可自动从视频中提取帧图片，利用ResNet18模型对每一帧是否为打架行为进行分类，并输出每帧的预测标签和概率。

---

## 目录结构

```
Fight_Detection/
├── data/
│   ├── frames/           # 提取的训练帧图片（fight, non_fight）
│   ├── labels/           # 标签文件（labels.csv等）
│   ├── eval_frames/      # 评估采样帧
│   ├── videos/           # 原始训练视频（fight, non_fight）
├── testvideo/            # 待判定视频（用户推理用）
├── predict_result/       # 推理结果（自动生成）
│   ├── frames/           # 推理时提取的帧
│   └── result.csv        # 推理结果
├── src/                  # 主要代码
│   ├── train.py          # 训练脚本
│   ├── predict.py        # 单帧推理脚本
│   ├── video_predict.py  # 视频推理脚本
│   └── dataset.py        # 数据集定义
├── requirements.txt      # 依赖包
├── fight_detection_resnet18.pth # 训练好的模型权重
```

---

## 环境依赖

建议使用 Python 3.8+，推荐使用 Anaconda/Miniconda 管理环境。

安装依赖：
```bash
pip install -r requirements.txt
```

requirements.txt 内容示例：
```
torch
torchvision
pandas
opencv-python
numpy
```

---

## 数据准备

1. **训练数据**  
   - 将打架视频放入 `data/videos/fight/`，非打架视频放入 `data/videos/non_fight/`。
   - 运行脚本自动提取帧、生成标签（见 `script/` 或 `src/` 目录下相关脚本）。

2. **推理数据**  
   - 将待判定视频放入 `testvideo/` 目录。

---

## 训练模型

```bash
python src/train.py
```
- 训练完成后会在根目录生成 `fight_detection_resnet18.pth`。

---

## 单帧推理

对 `data/eval_frames/` 下的图片进行推理，输出到 `data/labels/result.csv`：

```bash
python src/predict.py
```

---

## 视频推理

自动提取 `testvideo/` 下所有视频的帧，利用模型进行分类，输出到 `predict_result/result.csv`：

```bash
python src/video_predict.py
```
- 结果文件包含每帧的文件名、打架概率、预测标签。

---

## 结果说明

- `result.csv` 文件格式：
  ```
  frame_name,fight_prob,pred_label
  test_0001_00001.jpg,0.87,1
  test_0001_00002.jpg,0.12,0
  ```
  - fight_prob：该帧为打架的概率（0~1）
  - pred_label：预测标签（1=打架，0=非打架）

---

## 其他说明

- 支持自定义模型、数据增强、评估采样等功能。
- 如需扩展为视频级别识别，可对帧结果做后处理（如多数投票等）。

---

## 致谢

本项目为《深度学习综合实践》课程期末综合实践项目。
如有问题欢迎提issue或联系作者。 