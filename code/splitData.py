import os
import shutil
import random

# 定義路徑
source_dir = "/home/user/Downloads/trainData"  # 原始照片資料夾
train_dir = "/home/user/Downloads/train"    # 訓練集目標資料夾
test_dir = "/home/user/Downloads/test"      # 測試集目標資料夾

# 設定訓練集與測試集比例
train_ratio = 0.8  # 80% 用於訓練，20% 用於測試

# 創建目標資料夾（如果不存在）
os.makedirs(train_dir, exist_ok=True)
os.makedirs(test_dir, exist_ok=True)

# 獲取所有照片檔案
all_photos = [f for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f))]

# 隨機打亂照片順序
random.shuffle(all_photos)

# 計算訓練集大小
train_size = int(len(all_photos) * train_ratio)

# 分割照片
train_photos = all_photos[:train_size]
test_photos = all_photos[train_size:]

# 複製照片到訓練集和測試集
for photo in train_photos:
    shutil.copy(os.path.join(source_dir, photo), os.path.join(train_dir, photo))

for photo in test_photos:
    shutil.copy(os.path.join(source_dir, photo), os.path.join(test_dir, photo))

print(f"已成功分割：{len(train_photos)} 張訓練集，{len(test_photos)} 張測試集")
