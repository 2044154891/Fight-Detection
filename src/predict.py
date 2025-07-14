import os
import torch
from torchvision import models, transforms
from PIL import Image
import pandas as pd

MODEL_PATH = 'fight_detection_resnet18.pth'
EVAL_DIR = os.path.join('data', 'eval_frames')
OUTPUT_CSV = os.path.join('data', 'labels', 'result.csv')
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# 加载模型
model = models.resnet18(weights=None)
model.fc = torch.nn.Linear(model.fc.in_features, 2)
model.load_state_dict(torch.load(MODEL_PATH, map_location=DEVICE))
model = model.to(DEVICE)
model.eval()

results = []
with torch.no_grad():
    for fname in sorted(os.listdir(EVAL_DIR)):
        if not fname.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue
        img_path = os.path.join(EVAL_DIR, fname)
        image = Image.open(img_path).convert('RGB')
        input_tensor = transform(image).unsqueeze(0).to(DEVICE)  # 先transform再unsqueeze
        output = model(input_tensor)
        prob = torch.softmax(output, dim=1)[0]
        pred = torch.argmax(prob).item()
        results.append({'frame_name': fname, 'fight_prob': float(prob[1]), 'pred_label': pred})  # 概率为打架类别的概率

# 保存结果
pd.DataFrame(results).to_csv(OUTPUT_CSV, index=False)
print(f"推理结果已保存到 {OUTPUT_CSV}") 