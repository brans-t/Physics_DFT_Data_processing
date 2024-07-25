import matplotlib.pyplot as plt
import numpy as np
import math
from scipy.interpolate import griddata
from scipy.spatial import Delaunay
from mpl_toolkits.mplot3d import Axes3D

# 定义倒空间基矢量数组
vector_b = np.array([
    [4.2367255088335174, 0.0000000000000000],
    [0.0000000000000000, 4.2367255088335174]
])

# 定义读取EIGENVAL文件的函数
def read_values_from_EIGENVAL(filename):
    with open(filename, "r") as file:
        kx_rac = []
        ky_rac = []
        E_up = []
        E_down = []
        lines = file.readlines()
        num_kpoints = int(lines[5].split()[1])
        num_energy_levels = int(lines[5].split()[2])
        for j in range(num_kpoints):
            k_direct = list(map(float, lines[7 + (num_energy_levels + 2) * j].split()[0:2]))
            k_rac = np.dot(k_direct, vector_b) * 2 * math.pi
            energy_positions = [29]  # 这里假设只有一个能级位置，根据实际文件调整
            energies_up = []
            energies_down = []
            for energy_position in energy_positions:
                energy_up = float(lines[energy_position + num_energy_levels * j + 2 * j].split()[1]) + 2.45707247
                energy_down = float(lines[energy_position + num_energy_levels * j + 2 * j].split()[2]) + 2.45707247
                energies_up.append(energy_up)
                energies_down.append(energy_down)
            E_up.append(energies_up[0])
            E_down.append(energies_down[0])
            kx_rac.append(k_rac[0])
            ky_rac.append(k_rac[1])
    return kx_rac, ky_rac, E_up, E_down, num_kpoints

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