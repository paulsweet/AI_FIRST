####

import os
import shutil
from datetime import datetime

def organize_folder(folder_path):
    """
    Organizes files in a folder by type and modification date.

    Args:
        folder_path (str): The path to the folder to organize.
    """
    if not os.path.isdir(folder_path):
        print(f"错误：文件夹 '{folder_path}' 不存在。")
        return

    print(f"开始整理文件夹: {folder_path}")

    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)

        if os.path.isfile(item_path):
            try:
                # 获取文件扩展名作为类型
                file_extension = os.path.splitext(item)[1].lower()
                if not file_extension: #跳过没有扩展名的文件
                    print(f"跳过文件 (无扩展名): {item}")
                    continue
                file_type = file_extension[1:] # 去掉点号

                # 获取文件修改时间
                modification_time = os.path.getmtime(item_path)
                date_obj = datetime.fromtimestamp(modification_time)
                year = str(date_obj.year)
                month = date_obj.strftime('%m') # 格式化为两位数月份，例如 01, 02, ..., 12

                # 创建目标文件夹路径
                type_folder = os.path.join(folder_path, file_type)
                year_folder = os.path.join(type_folder, year)
                month_folder = os.path.join(year_folder, month)

                # 创建文件夹 (如果不存在)
                os.makedirs(month_folder, exist_ok=True)

                # 移动文件
                destination_path = os.path.join(month_folder, item)
                
                # 检查目标文件是否已存在
                if os.path.exists(destination_path):
                    # 如果文件已存在，可以添加一个后缀来避免覆盖
                    base, ext = os.path.splitext(item)
                    counter = 1
                    new_item_name = f"{base}_{counter}{ext}"
                    destination_path = os.path.join(month_folder, new_item_name)
                    while os.path.exists(destination_path):
                        counter += 1
                        new_item_name = f"{base}_{counter}{ext}"
                        destination_path = os.path.join(month_folder, new_item_name)
                    print(f"目标文件已存在，重命名为: {new_item_name}")

                shutil.move(item_path, destination_path)
                print(f"已移动: {item} -> {os.path.relpath(destination_path, folder_path)}")

            except Exception as e:
                print(f"处理文件 '{item}' 时发生错误: {e}")
        elif item == os.path.basename(__file__):
             # 跳过脚本文件本身
            print(f"跳过脚本文件: {item}")
            continue
        elif os.path.isdir(item_path):
            # 可选：递归整理子文件夹
            # print(f"发现子文件夹: {item} (当前版本不处理子文件夹)")
            pass # 当前版本不递归处理子文件夹，避免复杂性

    print("文件夹整理完成。")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        target_directory = sys.argv[1]
        if not os.path.isabs(target_directory):
            print(f"错误：提供的路径 '{target_directory}' 不是一个绝对路径。请提供绝对路径。")
            sys.exit(1)
        organize_folder(target_directory)
    else:
        print("错误：请提供要整理的文件夹路径作为命令行参数。")
        print("用法: python3 organize_files.py /path/to/your/folder")
        sys.exit(1)
