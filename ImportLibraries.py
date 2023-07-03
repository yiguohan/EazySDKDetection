import csv
import os
import uuid
import ast

csv_file_path = os.path.join("data", "sdk_libraries.csv")
sdk_references_file = os.path.join("data", "sdk_references.csv")

def initialize_csv_file():
    if not os.path.isfile(csv_file_path):
        with open(csv_file_path, 'w', newline='') as csv_file:
            fieldnames = ['id', 'title', 'description', 'package_names']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()

def update_library(library_rows):
    with open(csv_file_path, 'w', newline='') as csv_file:
        fieldnames = ['id', 'title', 'description', 'package_names']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(library_rows)

def generate_library_id():
    return str(uuid.uuid4())

# 初始化CSV文件
initialize_csv_file()

# 读取sdk_libraries文件中的数据
sdk_libraries_rows = []
with open(csv_file_path, 'r') as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        sdk_libraries_rows.append(row)

# 引导用户选择修复方式
while True:
    input_option = input("请选择修复方式（1 - 手动修复，2 - 自动修复）：")
    if input_option == "2":
        # 自动修复库信息
        if not os.path.isfile(sdk_references_file):
            print("找不到 sdk_references.csv 文件，请先生成该文件。")
            continue

        with open(sdk_references_file, 'r') as references_csv_file:
            references_reader = csv.DictReader(references_csv_file)
            for reference_row in references_reader:
                package_name = reference_row['Package Name']

                package_name_exist = False
                for library_row in sdk_libraries_rows:
                    if package_name in library_row['package_names']:
                        package_name_exist = True
                        break

                if package_name_exist:
                    print(f"包名：{package_name} 的库信息已存在，跳过。")
                    continue

                print(f"包名：{package_name} 不存在，请补全。")
                user_input_title = input(f"请输入库名称（{package_name}），如需退出请输入q：")

                if user_input_title == 'q':
                   break

                is_title_exist = False
                for library_row in sdk_libraries_rows:
                    if user_input_title == library_row['title']:
                        is_title_exist = True
                        existing_package_names =ast.literal_eval(library_row['package_names'])
                        if package_name not in existing_package_names:
                            existing_package_names.append(package_name)
                            sdk_libraries_rows[sdk_libraries_rows.index(library_row)]['package_names'] = str(existing_package_names)
                            update_library(sdk_libraries_rows)
                            print(f"包名：{package_name} 的库信息已存在，添加包名，已保存。")
                        break

                if is_title_exist:
                    continue

                library_data = {}
                library_data['id'] = generate_library_id()
                library_data['title'] = user_input_title
                library_data['description'] = input(f"请输入库描述（{package_name}）：")
                library_data['package_names'] = [package_name]
                # 将库信息添加到数组中
                sdk_libraries_rows.append(library_data)
            else:
                print("现有数据修复完成。")
        break
    else:
        print("无效的选项，请重新选择。")
