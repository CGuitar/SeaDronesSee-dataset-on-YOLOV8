import os
from tqdm import tqdm
from PIL import Image
import json

def generate_txt_file(folder_path, txt_file_path):
    print("正在处理文件夹:", folder_path)
    with open(txt_file_path, 'w') as txt_file:
        file_list = os.listdir(folder_path)
        for file_name in file_list:
            if file_name.endswith('.jpg') or file_name.endswith('.png'):
                txt_file.write('data/images/' + file_name + '\n')
    print("已生成文件:", txt_file_path)


def JSONtoTXT(mode,datapath):
    # 若没有，创建labels文件夹
    if not os.path.exists('labels'):
        os.mkdir('labels')
    with open(datapath, 'r') as file:
        data = json.load(file)
    print("正在处理：" + datapath)
    annotations = data['annotations']
    for annotation in tqdm(annotations):
        category_id = annotation['category_id']

        if category_id == 0:  # 如果category_id为ignore，则跳过当前注释信息
            print(str(annotation['image_id']) + ".jpg的标签为ignore")
            continue

        image_id = annotation['image_id']
        file_path = os.path.join('images/', mode + '/' + str(image_id) + '.jpg')
        with Image.open(file_path) as img:
            width, height = img.size
        bbox = annotation['bbox']
        # 目标框中心点x轴相对于图片x轴的比例 = (目标框x位置 + 目标框宽度 / 2) / 图片宽度
        x = (int(bbox[0]) + int(bbox[2]) / 2) / int(width)
        # 目标框中心点y轴相对于图片y轴的比例 = (目标框y位置 + 目标框高度 / 2) / 图片高度
        y = (int(bbox[1]) + int(bbox[3]) / 2) / int(height)
        # 目标框宽度相对于图片宽度的比例 = 目标框宽度 / 图片宽度
        w = int(bbox[2]) / int(width)
        # 目标框高度相对于图片高度的比例 = 目标框高度 / 图片高度
        h = int(bbox[3]) / int(height)

        content = f"{category_id} {x} {y} {w} {h}"
        file_name = image_id
        file_path = f'labels/{file_name}.txt'

        if os.path.exists(file_path):
            with open(file_path, 'a') as file:
                file.write('\n' + content)
        else:
            with open(file_path, 'w') as file:
                file.write(content)


"""
一：根据images下的三个文件夹，生成对应的txt。内容为各图片路径========================
"""
# 文件夹路径
train_folder = 'images/train'
val_folder = 'images/val'
test_folder = 'images/test'
# 生成txt文件
generate_txt_file(train_folder, 'train2.txt')
generate_txt_file(val_folder, 'val2.txt')
generate_txt_file(test_folder, 'test2.txt')
print("文件处理完成。")

"""
二：根据JSON转txt=============================================================
"""
# JSON文件数据清洗转TXT
JSONtoTXT('train', 'annotations/instances_train.json')
JSONtoTXT('val', 'annotations/instances_val.json')
print("处理完成")
