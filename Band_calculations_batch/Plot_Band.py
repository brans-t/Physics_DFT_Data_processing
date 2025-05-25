# -*- coding: utf-8 -*-

# 导入必要的模块
import os
import matplotlib.pyplot as plt
import matplotlib as mpl
from pymatgen.io.vasp.outputs import Vasprun
from pymatgen.electronic_structure.plotter import BSDOSPlotter

# 设置 matplotlib 的后端为 'TKAgg'，适用于非交互式环境
mpl.use('TKAgg')

def plot_band_structure(input_dir, subfolder_name):
    """
    绘制能带结构和态密度图。

    参数:
        input_dir (str): 包含 vasprun.xml 文件的目录路径。
        subfolder_name (str): 子文件夹名称，用于生成图像文件名。
    """
    # 检查输入目录是否存在
    if not os.path.exists(input_dir):
        raise FileNotFoundError(f"Directory not found: {input_dir}")
    print(f"Using input directory: {input_dir}")

    # 构建 vasprun.xml 文件的完整路径
    vasprun_path = os.path.join(input_dir, "vasprun.xml")
    if not os.path.exists(vasprun_path):
        raise FileNotFoundError(f"File not found: {vasprun_path}")
    print(f"Using vasprun.xml file at: {vasprun_path}")

    # 读取 'vasprun.xml' 文件，同时解析能带结构中的投影态
    bs_vasprun = Vasprun(vasprun_path, parse_projected_eigen=True)
    # 从 Vasprun 对象中获取能带结构数据
    bs_data = bs_vasprun.get_band_structure(line_mode=True)

    # 创建 BSDOSPlotter 对象，用于绘制能带结构和态密度图
    banddos_fig = BSDOSPlotter(bs_projection=None,
                               vb_energy_range=2, cb_energy_range=2, fixed_cb_energy=2)

    # 使用 BSDOSPlotter 对象绘制能带结构和态密度图
    ax = banddos_fig.get_plot(bs=bs_data)

    # 获取 ax 所属的 Figure 对象
    fig = ax.figure

    # 构建输出文件路径，文件名为 subfolder_name + "_Band.png"
    output_path = os.path.join(input_dir, f"{subfolder_name}_Band.png")
    # 将绘制的能带-态密度图保存为 'subfolder_name_Band.png'
    fig.savefig(output_path)
    print(f"Saved band structure and DOS plot to: {output_path}")

    # 显示所有绘制的图形
    # plt.show()

# 示例：调用函数
if __name__ == "__main__":
    # 获取当前脚本的绝对路径
    script_path = os.path.abspath(__file__)
    # 获取当前脚本所在的目录
    script_dir = os.path.dirname(script_path)

    # 获取当前工作目录
    current_directory = os.getcwd()
    # 构建目标目录路径（假设目标目录位于当前脚本目录的 "Tot_Band" 子目录中）
    target_base_directory = os.path.join(script_dir, "Tot_Band")

    # 检查目标基目录是否存在
    if not os.path.exists(target_base_directory):
        raise FileNotFoundError(f"Base directory not found: {target_base_directory}")

    # 遍历目标基目录中的所有子文件夹
    for root, dirs, files in os.walk(target_base_directory):
        for dir_name in dirs:
            # 构建目标子文件夹路径
            target_directory = os.path.join(root, dir_name, "con")
            if os.path.exists(target_directory):
                # 获取子文件夹名称
                subfolder_name = os.path.basename(os.path.dirname(target_directory))
                print(f"Processing directory: {target_directory}")
                # 调用绘图函数
                plot_band_structure(target_directory, subfolder_name)
            else:
                print(f"Skipping non-existent directory: {target_directory}")