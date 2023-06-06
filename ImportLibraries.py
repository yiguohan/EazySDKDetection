import csv
import os
import uuid

# 获取当前脚本所在的路径
script_path = os.path.dirname(os.path.abspath(__file__))

# 创建 data 文件夹
csv_folder_path = os.path.join(script_path, "data")
os.makedirs(csv_folder_path, exist_ok=True)

# CSV 文件路径
csv_file_path = os.path.join(csv_folder_path, "sdk_libraries.csv")

def initialize_csv_file():
    if not os.path.isfile(csv_file_path):
        with open(csv_file_path, 'w', newline='') as csv_file:
            fieldnames = ['id', 'title', 'description', 'package_name']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()

def add_library(title, description, package_names):
    library_id = str(uuid.uuid4())  # 生成唯一的库ID
    with open(csv_file_path, 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([library_id, title, description, ','.join(package_names)])

# 初始化CSV文件
initialize_csv_file()

# 引导用户录入三方库信息
title = input("请输入库名称：")
description = input("请输入库描述：")
package_names = input("请输入库包名（以逗号分隔）：").split(',')

# 添加库信息到CSV文件
add_library(title, description, package_names)

print("库信息已保存到 sdk_libraries.csv 文件中。")
