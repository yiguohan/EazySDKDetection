import csv
import os
import uuid

csv_file_path = os.path.join("data", "sdk_libraries.csv")

def initialize_csv_file():
    if not os.path.isfile(csv_file_path):
        with open(csv_file_path, 'w', newline='') as csv_file:
            fieldnames = ['id', 'title', 'description', 'package_names']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()

def add_library(library_data):
    with open(csv_file_path, 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(library_data)

def generate_library_id():
    return str(uuid.uuid4())

# 初始化CSV文件
initialize_csv_file()

# 引导用户选择修复方式
while True:
    input_option = input("请选择修复方式（1 - 手动修复，2 - 自动修复）：")
    if input_option == "1":
        while True:
            # 手动修复库信息
            library_data = {}

            library_data['id'] = generate_library_id()
            library_data['title'] = input("请输入库名称：")
            library_data['description'] = input("请输入库描述：")
            package_names_input = input("请输入库包名（以逗号分隔）：")
            library_data['package_names'] = package_names_input.split(',')

            # 添加库信息到CSV文件
            add_library(library_data)

            continue_input = input("继续修复下一个库信息？（输入 q 停止修复）：")
            if continue_input.lower() == "q":
                break

        print("库信息已修复完成并保存到 sdk_libraries.csv 文件中。")
        break

    elif input_option == "2":
        # 自动修复库信息
        existing_libraries = {}
        with open(csv_file_path, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                package_names = row['package_names'].split(',')
                existing_libraries[package_names[0]] = {
                    'id': row['id'],
                    'title': row['title'],
                    'description': row['description'],
                    'package_names': package_names
                }

        sdk_references_file = os.path.join("data", "sdk_references.csv")
        if not os.path.isfile(sdk_references_file):
            print("找不到 sdk_references.csv 文件，请先生成该文件。")
            continue

        with open(sdk_references_file, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                package_name = row['Package Name']
                if package_name not in existing_libraries:
                    print(f"包名：{package_name} 缺少字段信息，请修复。")

                    library_data = {}
                    library_data['id'] = generate_library_id()
                    library_data['title'] = input(f"请输入库名称（{package_name}）：")
                    library_data['description'] = input(f"请输入库描述（{package_name}）：")
                    library_data['package_names'] = [package_name]

                    # 添加库信息到CSV文件
                    add_library(library_data)

                else:
                    existing_library = existing_libraries[package_name]
                    missing_fields = []
                    for field in ['title', 'description', 'package_names']:
                        if field not in existing_library or not existing_library[field]:
                            missing_fields.append(field)

                    if missing_fields:
                        print(f"包名：{package_name} 缺少字段信息，请修复。")

                        for field in missing_fields:
                            if field == 'title':
                                existing_library['title'] = input(f"请输入库名称（{package_name}）：")
                            elif field == 'description':
                                existing_library['description'] = input(f"请输入库描述（{package_name}）：")
                            elif field == 'package_names':
                                package_names_input = input(f"请输入库包名（{package_name}）（以逗号分隔）：")
                                existing_library['package_names'] = package_names_input.split(',')

                        # 更新库信息到CSV文件
                        add_library(existing_library)

        print("现有数据修复完成并保存到 sdk_libraries.csv 文件中。")
        break

    elif input_option.lower() == "q":
        print("程序结束。")
        break
