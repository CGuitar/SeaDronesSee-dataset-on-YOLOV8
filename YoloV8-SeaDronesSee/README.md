# SeaDronesSee数据集在YOLOV8上的部署



## 一、数据预处理

1. 将Compressed Version中的images和annotations粘贴到data中
2. 运行data_process.py。将会生成三个txt文件和一个labels文件夹
5. 把images/test、train、val中的所有图片移动到images下

+ 注意！   在autodl上，SeaDronesSee.yaml中的txt路径要这样写才能找到，如果不行的话需要再调试一下

  > train: ../../data/train.txt
  > val: ../../data/val.txt
  > test: ../../data/test.txt

+ yolov8最终会读取的东西：images下的所有jpg、labels下的所有txt、SeaDronesSee.yaml、train.txt、val.txt、test.txt

> 训练开始前所必须的目录结构（能多不能少）：
>
> .
> ├── ./data
> │   ├── ./data/images
> │   │   ├── ./data/images/1.jpg
> │   │   ├── ./data/images/2.jpg
> │   │   ├── ./data/images/3.jpg
> │   │   ├── ...
> │   ├── ./data/labels
> │   │   ├── ./data/labels/1.txt
> │   │   ├── ./data/labels/2.txt
> │   │   ├── ./data/labels/3.txt
> │   │   ├── ...
> │   ├── ./data/SeaDronesSee.yaml
> │   ├── ./data/train.txt
> │   ├── ./data/val.txt
> │   └── ./data/test.txt
> ————————————————



## 二、快速开始

6. 模型训练（只进行了快速试验，若换成yolov8s.pt   epochs=100，效果会更好些）

``` Terminal
yolo task=detect mode=train model=yolov8n.pt data=data/SeaDronesSee.yaml batch=32 epochs=20 imgsz=640 workers=16 device=0
```

7. 模型验证（注意！运行前请查看并替换上面train生成的文件夹名称‘runs/detect/train1’）

```Terminal
yolo task=detect mode=val model=runs/detect/train1/weights/best.pt data=data/SeaDronesSee.yaml device=0
```

8. 模型预测（source换为需要预测的文件目录）

```Terminal
yolo task=detect mode=predict model=runs/detect/train1/weights/best.pt source=data/images device=0
```

+ 所有的运行结果会保存在/runs/detect/目录下



## 二、文件解释

最终目标：实现yaml对三个txt的读取。实现labels与images的所需格式

1. data_process.py：

   > + 根据images中不同文件夹和图片名称，生成对应的train、val、test.txt三个文件。内容为图片路径
   > + 清洗两个JSON文件中的必要性数据，并进行归一化处理（输出格式为：目标框类别 目标框中心点x轴相对于图片x轴的比例 目标框...y轴的比例 目标框宽度相对于图片宽度的比例 目标框长度...的比例）
   > + 生成（图片id.txt）到labels文件夹中

2. SeaDronesSee.yaml：让yolo命令读取到必要信息

```python
# 图片名称信息路径
train: ../../data/train.txt
val: ../../data/val.txt
test: ../../data/test.txt

# 类别数量
nc: 6

# 类别名称
names: ['ignored', 'swimmer', 'boat', 'jetski', 'life_saving_appliances', 'buoy']
```

3. 注意：'ignored'标签在标注图片中没有出现



## 四、致谢

感谢 [YOLOv8教程系列](https://blog.csdn.net/weixin_45921929/article/details/128673338?ops_request_misc=%7B%22request%5Fid%22%3A%22170037567616800192218540%22%2C%22scm%22%3A%2220140713.130102334..%22%7D&request_id=170037567616800192218540&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~top_positive~default-1-128673338-null-null.142^v96^pc_search_result_base5&utm_term=yolov8&spm=1018.2226.3001.4187) 的方法指导

感谢超级好用的GPT3.5的超级好用的回答