import os
import re

# 定义正则表达式模式
filename_pattern = r'^vaspjob\.o\d+$'

# 检查文件名是否符合格式
def check_filename(filename):
    return re.match(filename_pattern, filename) is not None

# 检查文件内容是否表示结构优化收敛
def check_convergence(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            if len(lines) < 3:
                print(f"文件 {file_path} 内容不足，无法检查倒数第三行。")
                return False

            third_last_line = lines[-3].strip()
            if third_last_line == "reached required accuracy - stopping structural energy minimisation":
                return True
            else:
                return False
    except FileNotFoundError:
        print(f"文件 {file_path} 未找到。")
        return False
    except UnicodeDecodeError as e:
        print(f"解码错误：{e}。请检查文件 {file_path} 的编码格式是否正确。")
        return False
    except Exception as e:
        print(f"读取文件 {file_path} 时发生错误：{e}")
        return False

# 主程序：检查指定目录下的所有文件
def check_files_in_directory(directory):
    if not os.path.exists(directory):
        print(f"目录 {directory} 不存在。")
        return None

    converged = False

    for filename in os.listdir(directory):
        if check_filename(filename):  # 检查文件名是否符合格式
            file_path = os.path.join(directory, filename)
            if check_convergence(file_path):  # 检查文件内容是否表示结构优化收敛
                converged = True
                break  # 只要有一个文件收敛，就认为该目录收敛

    return converged

# 获取当前脚本的绝对路径
script_path = os.path.abspath(__file__)
# 获取当前脚本所在的目录
script_dir = os.path.dirname(script_path)

# 获取当前工作目录
current_directory = os.getcwd()
# 构造元素文件的路径（假设它位于当前目录的 'output' 子目录中）
elements_file = os.path.join(current_directory, "output", "atom_elements.txt")

# 读取元素文件并处理
try:
    summary = []

    with open(elements_file, 'r') as file:
        for line in file:
            # 去除首尾空白字符和括号
            line = line.strip().strip('[]')
            # 分割元素符号
            elements = [element.strip("'") for element in line.split(', ')]
            # 去除每个元素首尾的空白字符
            cleaned_elements = [element.strip() for element in elements]
            # 根据元素生成目标文件夹名称
            subfolder_name = '_'.join(cleaned_elements)
            # 构造目标目录路径（指向 'Tot_Band' 子目录中的 'opt' 文件夹）
            target_directory = os.path.join(script_dir, "Tot_Band", subfolder_name, "opt")
            # 检查目标目录下的文件
            converged = check_files_in_directory(target_directory)
            if converged is not None:
                summary.append((subfolder_name, converged))

    # 输出汇总信息
    print("\n汇总结果：")
    for subfolder, converged in summary:
        if converged:
            print(f"{subfolder} 结构优化收敛。")
        else:
            print(f"{subfolder} 结构优化不收敛。")

except FileNotFoundError:
    print(f"文件 {elements_file} 未找到。")
except Exception as e:
    print(f"读取文件 {elements_file} 时发生错误：{e}")