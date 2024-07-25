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
        lines = file.readlines()
        num_kpoints = int(lines[5].split()[1]) 
        num_energy_levels = int(lines[5].split()[2])
        for j in range(num_kpoints):
            k_direct = list(map(float, lines[7 + (num_energy_levels + 2) * j].split()[0:2]))
            k_rac = np.dot(k_direct, vector_b) * 2 * math.pi
            energy_positions = [12]  # 这里假设只有一个能级位置，根据实际文件调整
            energies_up = []
            for energy_position in energy_positions:
                energy_up = float(lines[energy_position + num_energy_levels * j + 2 * j].split()[1]) + 0
                energies_up.append(energy_up)
            E_up.append(energies_up[0])
            kx_rac.append(k_rac[0])
            ky_rac.append(k_rac[1])
    return kx_rac, ky_rac, E_up, num_kpoints

# 调用函数读取EIGENVAL文件
E0_kx, E0_ky, Eup, num_kpoints = read_values_from_EIGENVAL("EIGENVAL")

print(num_kpoints)
print(Eup)
# 将读取的数据转换为numpy数组
kx = np.array(E0_kx)
ky = np.array(E0_ky)
E_upp = np.array(Eup)

# 创建kx和ky的网格
kx_grid, ky_grid = np.meshgrid(
    np.linspace(min(kx), max(kx), num=num_kpoints),
    np.linspace(min(ky), max(ky), num=num_kpoints)
)

# 使用griddata函数对能量数据进行插值
E_upp_grid = griddata((kx, ky), E_upp, (kx_grid, ky_grid), method='cubic')

# 反转颜色映射表以实现能量越低颜色越深
cmap_red_reversed = plt.get_cmap('Reds')

# 创建图形
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# 设置视角
ax.view_init(elev=5, azim=180)

# 绘制散点图，其中kx, ky是散点的坐标，E_upp是颜色映射的依据
sc1 = ax.scatter(kx, ky, E_upp, c=E_upp, cmap=cmap_red_reversed)

# 添加颜色条，将值映射到颜色
cbar1 = fig.colorbar(sc1, ax=ax, pad=0.1, label='E_up (eV)')

# 设置坐标轴标签
ax.set_xlabel('$k_x$ ($1/\\AA$)')
ax.set_ylabel('$k_y$ ($1/\\AA$)')
ax.set_zlabel('Energy (eV)')

# 显示图形
plt.show()