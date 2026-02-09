import os
from PIL import Image

source_dir = "/Users/frank/Desktop/产品截图"
target_dir = os.path.join(source_dir, "cropped_1x1")

if not os.path.exists(target_dir):
    os.makedirs(target_dir)

files = ["1.png", "2.png", "3.png", "4.png"]

print(f"开始处理图片，源目录: {source_dir}")
print(f"输出目录: {target_dir}")

for filename in files:
    file_path = os.path.join(source_dir, filename)
    if os.path.exists(file_path):
        try:
            img = Image.open(file_path)
            width, height = img.size
            
            # 计算裁剪区域 (居中裁剪)
            min_dim = min(width, height)
            left = (width - min_dim) / 2
            top = (height - min_dim) / 2
            right = (width + min_dim) / 2
            bottom = (height + min_dim) / 2
            
            img_cropped = img.crop((left, top, right, bottom))
            
            # 保存到输出目录
            save_path = os.path.join(target_dir, filename)
            img_cropped.save(save_path)
            print(f"✅ 已裁剪: {filename} -> {save_path} ({min_dim}x{min_dim})")
            
        except Exception as e:
            print(f"❌ 处理失败 {filename}: {e}")
    else:
        print(f"⚠️ 文件不存在: {filename}")

print("所有图片处理完成！")
