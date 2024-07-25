import matplotlib.pyplot as plt
import numpy as np
import math
from scipy.interpolate import griddata

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

# 创建3D图形
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

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