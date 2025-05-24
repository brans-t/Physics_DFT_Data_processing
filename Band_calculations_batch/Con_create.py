import os
import shutil

def create_con(directory, elements):
    """
    创建一个子文件夹，并返回该子文件夹的路径。

    :param directory: 包含 INCAR 和 KPOINTS 文件的目录。
    :param elements: 用于生成子文件夹名称的元素列表。
    :return: 创建的子文件夹路径。
    """
    if not os.path.isdir(directory):
        print(f"Error: The path '{directory}' is not a valid directory.")
        return None

    # 去除每个元素的首尾空格
    cleaned_elements = [element.strip() for element in elements]
    # 根据元素生成目标文件夹名称
    subfolder_name = '_'.join(cleaned_elements)
    # 生成子文件夹路径（使用当前工作目录）
    subfolder_path = os.path.join(os.getcwd(), "Tot Band", subfolder_name, "con")

    # 确保子文件夹存在
    if not os.path.exists(subfolder_path):
        os.makedirs(subfolder_path)
        print(f"Created subfolder: {subfolder_path}")
    return subfolder_path


def move_input(con_directory, elements):
    """
    将指定目录中的文件复制到生成的子文件夹中。

    :param con_directory: 包含输入文件的目录。
    :param elements: 用于生成子文件夹名称的元素列表。
    """
    if not os.path.isdir(con_directory):
        print(f"Error: The path '{con_directory}' is not a valid directory.")
        return

    # 去除每个元素的首尾空格
    cleaned_elements = [element.strip() for element in elements]
    # 根据元素生成目标文件夹名称
    subfolder_name = '_'.join(cleaned_elements)
    # 输入文件的源路径
    input_path = os.path.join(os.getcwd(), "Con_source")

    # 创建目标子文件夹路径
    output_path = create_con(con_directory, elements)
    if output_path is None:
        return

    # 复制 INCAR、KPOINTS 和 vasp.pbs 文件
    for filename in os.listdir(input_path):
        if filename.startswith(("INCAR", "KPOINTS", "vasp.pbs")):
            # 构造输入文件路径
            input_file = os.path.join(input_path, filename)
            # 构造输出文件路径
            output_file = os.path.join(output_path, filename)
            # 复制文件
            shutil.copy(input_file, output_file)
            print(f"Copied {input_file} to {output_file}")

    # 获取上一级目录路径
    parent_path = os.path.dirname(output_path)
    # CONTCAR 和 POTCAR 文件所在的路径
    optfile_path = os.path.join(parent_path, "opt")

    # 确保 opt 文件夹存在
    if not os.path.exists(optfile_path):
        print(f"Error: The path '{optfile_path}' does not exist.")
        return

    # 复制 CONTCAR 和 POTCAR 文件
    for filename in os.listdir(optfile_path):
        if filename.startswith("CONTCAR"):
            # 构造输入文件路径
            input_file = os.path.join(optfile_path, filename)
            # 构造输出文件路径（将 CONTCAR 重命名为 POSCAR）
            output_file = os.path.join(output_path, "POSCAR")
            # 复制文件
            shutil.copy(input_file, output_file)
            print(f"Copied {input_file} to {output_file}")
        elif filename.startswith("POTCAR"):
            # 构造输入文件路径
            input_file = os.path.join(optfile_path, filename)
            # 构造输出文件路径
            output_file = os.path.join(output_path, filename)
            # 复制文件
            shutil.copy(input_file, output_file)
            print(f"Copied {input_file} to {output_file}")


# 获取当前工作目录
current_directory = os.getcwd()

# 构造元素文件的路径（假设它位于当前目录的 'output' 子目录中）
elements_file = os.path.join(current_directory, "output", "atom_elements.txt")

# 构造包含 INCAR 和 KPOINTS 文件的目录路径（假设它位于当前目录的 'Con_source' 子目录中）
source_directory = os.path.join(current_directory, "Con_source")

# 打开元素文件并逐行读取
with open(elements_file, 'r') as file:
    for line in file:
        # 去除首尾空格和括号
        line = line.strip().strip('[]')
        # 分割元素符号
        elements = [element.strip("'") for element in line.split(', ')]
        # 调用函数处理 INCAR 和 KPOINTS 文件
        move_input(source_directory, elements)