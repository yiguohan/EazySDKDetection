import os
import re
import subprocess
import zipfile
import time
import shutil
import csv

# 获取当前脚本所在的路径
script_path = os.path.dirname(os.path.abspath(__file__))

# 获取APK文件夹路径
apk_folder_path = os.path.join(script_path, "APKToDetect")
if not os.path.exists(apk_folder_path):
    raise FileNotFoundError("APKToDetect文件夹不存在，请在脚本所在路径下创建APKToDetect文件夹并放置APK文件")

# 获取APK文件列表
apk_files = [f for f in os.listdir(apk_folder_path) if f.endswith(".apk")]

if not apk_files:
    raise FileNotFoundError("APKToDetect文件夹中没有找到APK文件")

print("找到以下APK文件：")
for i, apk_file in enumerate(apk_files):
    print(f"{i+1}. {apk_file}")

# 让用户选择要检测的APK文件
selected_index = input("请选择要检测的APK文件的编号：")
try:
    selected_index = int(selected_index) - 1
    apk_file_path = os.path.join(apk_folder_path, apk_files[selected_index])
except (ValueError, IndexError):
    raise ValueError("请输入有效的APK文件编号")

# 获取输出文件夹路径
output_folder_path = os.path.join(script_path, "SDKOutput")
if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)

# 生成以时间戳为名称的新文件夹
new_folder_name = time.strftime("%Y%m%d_%H%M%S")
new_folder_path = os.path.join(output_folder_path, new_folder_name)
os.makedirs(new_folder_path)

try:
    # 解压APK文件
    with zipfile.ZipFile(apk_file_path, 'r') as zip_ref:
        zip_ref.extractall(new_folder_path)

    # 反编译APK文件
    jadx_output_path = os.path.join(new_folder_path, "jadx_output")
    os.makedirs(jadx_output_path)

    jadx_command = ["jadx", apk_file_path, "-d", jadx_output_path]
    subprocess.call(jadx_command)

    # 查找并提取所有的包名
    package_names = set()  # 使用集合来存储去重后的包名

    for root, dirs, files in os.walk(jadx_output_path):
        for file in files:
            if file.endswith(".java"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    content = f.read()
                    # 提取import语句中的包名
                    matches = re.findall(r"import\s+([\w.]+)\s*;", content)
                    for match in matches:
                        # 过滤条件：不包含以java、javax、kotlin开头的包名，并去除类名后的部分
                        if not match.startswith(("java.", "javax.", "kotlin.")):
                            package_name = match.split(".")[:-1]  # 去除类名部分
                            package_names.add(".".join(package_name))

    # 输出结果
    if package_names:
        print("Found the following package names:")
        for package_name in sorted(package_names):
            print(package_name)
    else:
        print("No package names found.")

    # 保存结果到CSV文件
    csv_file_path = os.path.join(output_folder_path, "sdk_references.csv")
    fieldnames = ['Timestamp', 'APK Package Name', 'Package Name']
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    apk_package_name = os.path.basename(apk_file_path)
    with open(csv_file_path, 'a', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        if os.stat(csv_file_path).st_size == 0:
            writer.writeheader()
        for package_name in sorted(package_names):
            writer.writerow({
                'Timestamp': timestamp,
                'APK Package Name': apk_package_name,
                'Package Name': package_name
            })

except Exception as e:
    print("An error occurred during the detection process:", str(e))

finally:
    print("Files cleaned up.")
    # 删除临时文件夹中的除CSV文件外的所有文件
    for root, dirs, files in os.walk(new_folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            if file_path != csv_file_path:
                os.remove(file_path)
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if dir_path != new_folder_path:
                shutil.rmtree(dir_path)