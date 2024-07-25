import matplotlib.pyplot as plt
import numpy as np
import math
from scipy.interpolate import griddata
from scipy.spatial import Delaunay
from mpl_toolkits.mplot3d import Axes3D
import xml.etree.ElementTree as ET

band_sel = input("Do you want to draw the conduction band or the valence band? Enter 'conduction' or 'valence':")
# 定义变量Iq
Iq = input("Please enter the value of Iq (h for high, l for low, or sc for Scatter):")

########################################################################################################################
########################################################################################################################
########################################################################################################################

# 定义读取POSCAR的文件，并获取二维基矢 
def extract_vectors_from_poscar(poscar_filename):
    try:
        with open(poscar_filename, 'r') as file:
            # 跳过前两行，从第三行开始读取
            for _ in range(2):  # 跳过前两行
                next(file)
            
            # 读取基矢量
            vectors = []
            for _ in range(2):  # 读取三行，每行代表一个基矢量
                line = next(file).strip()
                parts = line.split()
                if len(parts) > 1:  # 确保行中至少有两个元素
                    vectors.append((float(parts[0]), float(parts[1])))
            
            return vectors
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
########################################################################################################################
########################################################################################################################
########################################################################################################################
    
#读取费米能级
def extract_efermi_value(xml_file):
    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Find all <i name="efermi"> tags
    efermi_tags = root.findall('.//i[@name="efermi"]')

    # Check if any tag is found
    if efermi_tags:
        # Get the text content of the first tag
        fermi_value = efermi_tags[0].text
        # Convert the text to a floating-point number
        Ferm = float(fermi_value)
        return Ferm
    else:
        raise ValueError("efermi tag not found")

#费米能级赋值
Ferm = extract_efermi_value('vasprun.xml')
print(Ferm)

########################################################################################################################
########################################################################################################################
########################################################################################################################

# 读取POSCAR文件   
poscar_filename = 'POSCAR'
vectors = extract_vectors_from_poscar(poscar_filename)
vector_b = np.array(vectors)

# 读取Spin开关是否打开
def read_spinvalues_from_EIGENVAL(filename):
    with open(filename, "r") as file:
        lines = file.readlines()
        spin_oc = int(lines[0].split()[3])                     #spin open or close
    return spin_oc 

########################################################################################################################
########################################################################################################################
########################################################################################################################

# 寻找导带和价带函数
def find_energy_extremes(energy_levels):
    lab_energy = []
    
    # 计算每个能量级别的负数最大值或正数最小值
    for energy_level_values in energy_levels.values():
        # 找到负数中的最大值
        max_negative = max((v for v in energy_level_values if v < 0), default=None)
        # 找到正数中的最小值
        min_positive = min((v for v in energy_level_values if v > 0), default=None)
        
        # 选择负数最大值或正数最小值
        if max_negative is not None and min_positive is not None:
            lab_energy_value = max(max_negative, min_positive)
        elif max_negative is not None:
            lab_energy_value = max_negative
        else:
            lab_energy_value = min_positive
        lab_energy.append(lab_energy_value)
    
    # 初始化变量
    min_positive = None
    max_negative = None
    
    # 遍历 lab_energy 列表，找到正数的最小值和负数的最大值
    for index, value in enumerate(lab_energy):
        if value > 0 and (min_positive is None or value < min_positive):
            min_positive = value
        if value < 0 and (max_negative is None or value > max_negative):
            max_negative = value
    
    # 找到正数最小值和负数最大值的索引
    min_positive_index = lab_energy.index(min_positive) if min_positive is not None else None
    max_negative_index = lab_energy.index(max_negative) if max_negative is not None else None

    return max_negative_index, min_positive_index
##################################################################################Spin_oc=1###########################################################
##################################################################################Spin_oc=1###########################################################

spin_oc = read_spinvalues_from_EIGENVAL("EIGENVAL")
# print(spin_oc)

if spin_oc == 1:
    with open('EIGENVAL', 'r') as file:
        # 读取第六行，并分别获取num_kpoints和num_energy_levels
        lines = file.readlines()
        num_kpoints = int(lines[5].split()[1])
        num_energy_levels = int(lines[5].split()[2])

        # 创建num_energy_levels数量的列表
        energy_levels_lists = {f'E_{i}': [] for i in range(1, num_energy_levels + 1)}
        # lines = [next(file) for _ in range(num_kpoints * num_energy_levels)]
        
        # 读取每个k-point的能量值
        for energy_level in range(num_energy_levels):

            # 假设每行的前两个数是k-point索引和无关的计数，实际能量值从第三个开始
            energy_positions = 8 + energy_level
            for kpoint in range(num_kpoints):
                # 从索引2开始读取，索引0和1被跳过
                energy_value = float(lines[energy_positions + num_energy_levels * kpoint + 2 * kpoint].split()[1]) -  Ferm
                energy_levels_lists[f'E_{energy_level + 1}'].append(energy_value)
    
    max_negative_index, min_positive_index = find_energy_extremes(energy_levels_lists)
    # print(f"The serial number of the valence band is: {max_negative_index + 1}")
    # print(f"The serial number of the conduction band is: {min_positive_index + 1}")
    if band_sel == 'co':
        band_label = min_positive_index + 8
    else:
        band_label = max_negative_index + 8

##################################################################################Spin_oc=2###########################################################
##################################################################################Spin_oc=2###########################################################

else:    
    # 首先，打开EIGENVAL文件
    with open('EIGENVAL', 'r') as file:
        # 读取第六行，并分别获取num_kpoints和num_energy_levels
        lines = file.readlines()
        num_kpoints = int(lines[5].split()[1])
        num_energy_levels = int(lines[5].split()[2])

        # 创建num_energy_levels数量的列表
        energy_up_levels_lists = {f'Eup_{i}': [] for i in range(1, num_energy_levels + 1)}
        energy_dn_levels_lists = {f'Edn_{i}': [] for i in range(1, num_energy_levels + 1)}
        
        # 读取每个k-point的能量值
        for energy_level in range(num_energy_levels):

            # 实际能量值从第9行开始
            energy_positions = 8 + energy_level
            for kpoint in range(num_kpoints):
                # 从索引2开始读取，索引0和1被跳过
                energy_up_value = float(lines[energy_positions + num_energy_levels * kpoint + 2 * kpoint].split()[1]) -  Ferm
                energy_dn_value = float(lines[energy_positions + num_energy_levels * kpoint + 2 * kpoint].split()[2]) -  Ferm
                energy_up_levels_lists[f'Eup_{energy_level + 1}'].append(energy_up_value)
                energy_dn_levels_lists[f'Edn_{energy_level + 1}'].append(energy_dn_value)

    # 调用函数
    max_up_negative_index, min_up_positive_index = find_energy_extremes(energy_up_levels_lists)
    # print(f"The serial number of the valence band(Spin-up) is: {max_up_negative_index + 1}")
    # print(f"The serial number of the conduction band(Spin-up) is: {min_up_positive_index + 1}")
    band_label_up = max_up_negative_index + 8


    max_dn_negative_index, min_dn_positive_index = find_energy_extremes(energy_dn_levels_lists)
    # print(f"The serial number of the valence band(Spin-dn) is: {max_dn_negative_index + 1}")
    # print(f"The serial number of the conduction band(Spin-dn) is: {min_dn_positive_index + 1}")
    band_label_dn = max_dn_negative_index + 8

    if band_sel == 'co':
        band_label = min_up_positive_index + 8
    else:
        band_label = max_up_negative_index + 8

########################################################################################################################
########################################################################################################################
########################################################################################################################

# 定义读取EIGENVAL文件的函数
def read_values_from_EIGENVAL(filename):
    with open(filename, "r") as file:
        kx_rac = []
        ky_rac = []
        E_only =[]
        E_up = []
        E_down = []
        lines = file.readlines()
        
        num_kpoints = int(lines[5].split()[1])
        num_energy_levels = int(lines[5].split()[2])
        spin_oc = int(lines[0].split()[3])                     #spin open or close
        
        if spin_oc == 1:                                       #no spin
            for j in range(num_kpoints):
                k_direct = list(map(float, lines[7 + (num_energy_levels + 2) * j].split()[0:2]))
                k_rac = np.dot(k_direct, vector_b) * 2 * math.pi
                energy_positions = [band_label]  
                energies_only = []
                for energy_position in energy_positions:
                    energy_only = float(lines[energy_position + num_energy_levels * j + 2 * j].split()[1]) - Ferm
                    energies_only.append(energy_only)
                E_only.append(energies_only[0])
                kx_rac.append(k_rac[0])
                ky_rac.append(k_rac[1])
        
        else:                                                  #with spin 
         for j in range(num_kpoints):
             k_direct = list(map(float, lines[7 + (num_energy_levels + 2) * j].split()[0:2]))
             k_rac = np.dot(k_direct, vector_b) * 2 * math.pi
             energy_positions = [band_label]  
             energies_up = []
             energies_down = []
             for energy_position in energy_positions:
                 energy_up = float(lines[energy_position + num_energy_levels * j + 2 * j].split()[1]) - Ferm
                 energy_down = float(lines[energy_position + num_energy_levels * j + 2 * j].split()[2]) - Ferm
                 energies_up.append(energy_up)
                 energies_down.append(energy_down)
             E_up.append(energies_up[0])
             E_down.append(energies_down[0])
             kx_rac.append(k_rac[0])
             ky_rac.append(k_rac[1])
        

    if spin_oc == 1:
        return kx_rac, ky_rac, E_only, num_kpoints 
    else:
        return kx_rac, ky_rac, E_up, E_down, num_kpoints
    
spin_oc = read_spinvalues_from_EIGENVAL("EIGENVAL")

################################################################Spin_oc=1#############################################################################
################################################################Spin_oc=1#############################################################################   
 
if spin_oc == 1:
    # 调用函数读取EIGENVAL文件
    E0_kx, E0_ky, Eon, num_kpoints = read_values_from_EIGENVAL("EIGENVAL")
    # 将读取的数据转换为numpy数组
    kx = np.array(E0_kx)
    ky = np.array(E0_ky)
    E_onn = np.array(Eon)

    # 创建kx和ky的网格
    kx_grid, ky_grid = np.meshgrid(
        np.linspace(min(kx), max(kx), num=num_kpoints),
        np.linspace(min(ky), max(ky), num=num_kpoints)
    )

    # 使用griddata函数对能量数据进行插值
    E_onn_grid = griddata((kx, ky), E_onn, (kx_grid, ky_grid), method='cubic')

    # 反转颜色映射表以实现能量越低颜色越深
    cmap_blue_reversed = plt.get_cmap('Blues').reversed()

    # 创建图形和3D坐标轴
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # 根据变量Iq的值执行相应的条件

    #############################################high_picture#############################################################
    if Iq == 'h':
        # 设置视角
        ax.view_init(elev=5, azim=180)

        # 绘制E_upp能量的3D表面图，使用反转后的红色映射表
        surf1 = ax.plot_surface(kx_grid, ky_grid, E_onn_grid, cmap=cmap_blue_reversed, alpha=0.6, rstride=1, cstride=1)

        # 添加颜色条，将值映射到颜色
        cbar1 = fig.colorbar(surf1, ax=ax, pad=0.1, label='E (eV)')

        # 设置坐标轴标签
        ax.set_xlabel('$k_x$ ($1/\\AA$)')
        ax.set_ylabel('$k_y$ ($1/\\AA$)')
        ax.set_zlabel('Energy (eV)')

        # 绘制投影到xy平面
        # 找到E_upp_grid和E_dnn_grid的最大和最小值作为投影的参考高度
        z_max = np.max(E_onn_grid)
        z_min = np.min(E_onn_grid)

        # 绘制E_upp的投影，使用反转后的红色映射表
        ax.contourf(kx_grid, ky_grid, E_onn_grid, zdir='z', offset=z_min, cmap=cmap_blue_reversed, alpha=0.8)

        # 显示3D图形
        plt.show()
    #############################################low_picture#############################################################    
    elif Iq == 'l':
        # 进行三角化
        tri = Delaunay(np.column_stack((kx, ky)))

        # 绘制E_upp能量的3D曲面图
        ax.plot_trisurf(kx, ky, E_onn, triangles=tri.simplices, cmap=cmap_blue_reversed, alpha=0.8)
        ax.set_xlabel('$k_x$ ($1/\\AA$)')
        ax.set_ylabel('$k_y$ ($1/\\AA$)')
        ax.set_zlabel('Energy (eV)')

        # 添加颜色条
        cbar1 = fig.colorbar(ax.collections[0], ax=ax, pad=0.1, label='E (eV)')

        # 显示3D图形
        plt.show()
    #############################################Scatter_picture#############################################################    
    elif Iq == 'sc':
        # 绘制E_upp能量的3D散点图
        scatter1 = ax.scatter(kx, ky, E_onn, c=E_onn, cmap=cmap_blue_reversed, alpha=0.8, edgecolors='none')

        # 添加颜色条
        cbar1 = fig.colorbar(scatter1, ax=ax, pad=0.1, label='E (eV)')

        # 设置坐标轴标签
        ax.set_xlabel('$k_x$ ($1/\\AA$)')
        ax.set_ylabel('$k_y$ ($1/\\AA$)')
        ax.set_zlabel('Energy (eV)')

        # 绘制E_upp能量的等高线图到xy平面
        contour1 = ax.contour(kx_grid, ky_grid, E_onn_grid, levels=14, cmap=cmap_blue_reversed, zdim='z')
        ax.clabel(contour1, inline=True, fontsize=10)

        # 显示3D图形
        plt.show()

    else:
        print("Please enter 'h' for high, 'l' for low, or 'sc' for Scatter.")    

################################################################Spin_oc=2#############################################################################
################################################################Spin_oc=2#############################################################################

else:
    # 调用函数读取EIGENVAL文件
    E0_kx, E0_ky, Eup, Edn, num_kpoints = read_values_from_EIGENVAL("EIGENVAL")

    # 将读取的数据转换为numpy数组
    kx = np.array(E0_kx)
    ky = np.array(E0_ky)
    E_upp = np.array(Eup)
    E_dnn = np.array(Edn)

    # 创建kx和ky的网格
    kx_grid, ky_grid = np.meshgrid(
        np.linspace(min(kx), max(kx), num=num_kpoints),
        np.linspace(min(ky), max(ky), num=num_kpoints)
    )

    # 使用griddata函数对能量数据进行插值
    E_upp_grid = griddata((kx, ky), E_upp, (kx_grid, ky_grid), method='cubic')
    E_dnn_grid = griddata((kx, ky), E_dnn, (kx_grid, ky_grid), method='cubic')

    # 反转颜色映射表以实现能量越低颜色越深
    cmap_red_reversed = plt.get_cmap('Reds').reversed()
    cmap_blue_reversed = plt.get_cmap('Blues').reversed()

    # 创建图形和3D坐标轴
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # 根据变量Iq的值执行相应的条件

    #############################################high_picture#############################################################
    
    if Iq == 'h':
        # 设置视角
        ax.view_init(elev=5, azim=180)

        # 绘制E_upp能量的3D表面图，使用反转后的红色映射表
        surf1 = ax.plot_surface(kx_grid, ky_grid, E_upp_grid, cmap=cmap_red_reversed, alpha=0.6, rstride=1, cstride=1)

        # 绘制E_dnn能量的3D表面图，使用反转后的蓝色映射表
        surf2 = ax.plot_surface(kx_grid, ky_grid, E_dnn_grid, cmap=cmap_blue_reversed, alpha=0.6, rstride=1, cstride=1)

        # 添加颜色条，将值映射到颜色
        cbar1 = fig.colorbar(surf1, ax=ax, pad=0.1, label='E_up (eV)')
        cbar2 = fig.colorbar(surf2, ax=ax, pad=0.1, label='E_down (eV)')

        # 设置坐标轴标签
        ax.set_xlabel('$k_x$ ($1/\\AA$)')
        ax.set_ylabel('$k_y$ ($1/\\AA$)')
        ax.set_zlabel('Energy (eV)')

        # 绘制投影到xy平面
        # 找到E_upp_grid和E_dnn_grid的最大和最小值作为投影的参考高度
        z_max = max(np.max(E_upp_grid), np.max(E_dnn_grid))
        z_min = min(np.min(E_upp_grid), np.min(E_dnn_grid))

        # 绘制E_upp的投影，使用反转后的红色映射表
        ax.contourf(kx_grid, ky_grid, E_upp_grid, zdir='z', offset=z_min, cmap=cmap_red_reversed, alpha=0.8)

        # 绘制E_dnn的投影，使用反转后的蓝色映射表
        ax.contourf(kx_grid, ky_grid, E_dnn_grid, zdir='z', offset=z_min, cmap=cmap_blue_reversed, alpha=0.8)

        # 显示3D图形
        plt.show()

    #############################################low_picture#############################################################    
    
    elif Iq == 'l':
        # 进行三角化
        tri = Delaunay(np.column_stack((kx, ky)))

        # 绘制E_upp能量的3D曲面图
        ax.plot_trisurf(kx, ky, E_upp, triangles=tri.simplices, cmap=cmap_red_reversed, alpha=0.8)
        ax.set_xlabel('$k_x$ ($1/\\AA$)')
        ax.set_ylabel('$k_y$ ($1/\\AA$)')
        ax.set_zlabel('Energy (eV)')

        # 添加颜色条
        cbar1 = fig.colorbar(ax.collections[0], ax=ax, pad=0.1, label='E_up (eV)')

        # 绘制E_dnn能量的3D曲面图
        ax.plot_trisurf(kx, ky, E_dnn, triangles=tri.simplices, cmap=cmap_blue_reversed, alpha=0.8)

        # 添加颜色条
        cbar2 = fig.colorbar(ax.collections[1], ax=ax, pad=0.1, label='E_down (eV)')

        # 显示3D图形
        plt.show()

    #############################################Scatter_picture#############################################################    
    
    elif Iq == 'sc':
        # 绘制E_upp能量的3D散点图
        scatter1 = ax.scatter(kx, ky, E_upp, c=E_upp, cmap=cmap_red_reversed, alpha=0.8, edgecolors='none')

        # 绘制E_dnn能量的3D散点图
        scatter2 = ax.scatter(kx, ky, E_dnn, c=E_dnn, cmap=cmap_blue_reversed, alpha=0.8, edgecolors='none')

        # 添加颜色条
        cbar1 = fig.colorbar(scatter1, ax=ax, pad=0.1, label='E_up (eV)')
        cbar2 = fig.colorbar(scatter2, ax=ax, pad=0.1, label='E_down (eV)')

        # 设置坐标轴标签
        ax.set_xlabel('$k_x$ ($1/\\AA$)')
        ax.set_ylabel('$k_y$ ($1/\\AA$)')
        ax.set_zlabel('Energy (eV)')

        # 绘制E_upp能量的等高线图到xy平面
        contour1 = ax.contour(kx_grid, ky_grid, E_upp_grid, levels=14, cmap=cmap_red_reversed, zdim='z')
        ax.clabel(contour1, inline=True, fontsize=10)

        # 绘制E_dnn能量的等高线图到xy平面
        contour2 = ax.contour(kx_grid, ky_grid, E_dnn_grid, levels=14, cmap=cmap_blue_reversed, zdim='z')
        ax.clabel(contour2, inline=True, fontsize=10)

        # 显示3D图形
        plt.show()

    else:
        print("Please enter 'h' for high, 'l' for low, or 'sc' for Scatter.")   

# print("Spin",spin_oc)
# print("fermi",Ferm)
# print("energy",band_label_up)
# print("enenrgyband",max_up_negative_index)