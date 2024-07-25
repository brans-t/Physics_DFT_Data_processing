# -*- coding: utf-8 -*-

# 导入 matplotlib.pyplot 用于绘图，以及 matplotlib 用于设置
import matplotlib.pyplot as plt
import matplotlib as mpl
# 设置 matplotlib 的后端为 'TKAgg'，适用于非交互式环境
mpl.use('TKAgg')

# 从 pymatgen 库中导入 Vasprun 类用于读取 VASP 输出文件
from pymatgen.io.vasp.outputs import Vasprun
# 从 pymatgen 库中导入电子结构绘图相关的类
from pymatgen.electronic_structure.plotter import BSDOSPlotter, BSPlotter, BSPlotterProjected, DosPlotter

# 读取 'vasprun.xml' 文件，同时解析能带结构中的投影态
bs_vasprun = Vasprun("vasprun.xml", parse_projected_eigen=True)
# 从 Vasprun 对象中获取能带结构数据
bs_data = bs_vasprun.get_band_structure(line_mode=True)

# 再次读取 'vasprun.xml' 文件，这次用于获取态密度数据
dos_vasprun = Vasprun("vasprun1.xml")
# 获取完整的态密度数据
dos_data = dos_vasprun.complete_dos

# 创建 BSDOSPlotter 对象，用于绘制能带结构和态密度图
# bs_projection 和 dos_projection 参数指定投影类型为 'elements'，即按元素投影
# vb_energy_range 和 cb_energy_range 分别指定价带和导带的能量范围
# fixed_cb_energy 指定固定导带能量范围
banddos_fig = BSDOSPlotter(bs_projection='elements', dos_projection='elements',
                            vb_energy_range=3, cb_energy_range=3, fixed_cb_energy=3)
# 使用 BSDOSPlotter 对象绘制能带结构和态密度图
banddos_fig.get_plot(bs=bs_data, dos=dos_data)

# 将绘制的能带-态密度图保存为 'banddos_fig.png'
plt.savefig('banddos_fig.png')

# 创建 BSPlotter 对象，用于绘制布里渊区图
band_fig = BSPlotter(bs=bs_data)
# 使用 BSPlotter 对象绘制布里渊区图
band_fig.plot_brillouin()

# 将绘制的布里渊区图保存为 'brillouin_fig.png'
plt.savefig('brillouin_fig.png')

# 显示所有绘制的图形
plt.show()