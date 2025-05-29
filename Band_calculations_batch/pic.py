import os
import shutil

def extract_png_files(source_folder, target_folder):
    """
    从指定文件夹中提取所有.png文件，并将它们复制到目标文件夹中。

    参数:
    source_folder (str): 源文件夹路径，包含要提取的.png文件。
    target_folder (str): 目标文件夹路径，用于存放提取的.png文件。
    """
    # 确保目标文件夹存在，如果不存在则创建
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
        print(f"创建目标文件夹: {target_folder}")

    # 遍历源文件夹中的所有文件和子文件夹
    for root, dirs, files in os.walk(source_folder):
        for file in files:
            # 检查文件扩展名是否为.png
            if file.lower().endswith('.png'):
                # 构造完整的文件路径
                file_path = os.path.join(root, file)
                # 构造目标文件夹中的目标路径
                target_path = os.path.join(target_folder, file)
                # 复制文件到目标文件夹
                shutil.copy(file_path, target_path)
                print(f"复制文件: {file_path} -> {target_path}")

    print("所有.png文件已提取完成！")


# 示例：调用函数
if __name__ == "__main__":
    # 获取当前工作目录
    current_directory = os.getcwd()
    # 目标文件夹路径，所有提取的.png文件将存放在这个文件夹中
    target_folder = os.path.join(current_directory, "Tot_pice")

    # 检查目标文件夹是否存在，如果不存在则创建
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
        print(f"创建目标文件夹: {target_folder}")

    # 构建源目录路径（假设源目录位于当前工作目录的 "Tot_Band" 子目录中）
    source_directory = os.path.join(current_directory, "Tot_Band")

    # 检查源目录是否存在
    if not os.path.exists(source_directory):
        raise FileNotFoundError(f"Source directory not found: {source_directory}")

    # 遍历源目录中的所有文件和子文件夹
    for root, dirs, files in os.walk(source_directory):
        for dir_name in dirs:
            # 构建源子文件夹路径
            source_subfolder = os.path.join(root, dir_name, "con")
            if os.path.exists(source_subfolder):
                print(f"Processing directory: {source_subfolder}")
                # 调用函数，将子文件夹中的.png文件复制到目标文件夹
                extract_png_files(source_subfolder, target_folder)
            else:
                print(f"Skipping non-existent directory: {source_subfolder}")