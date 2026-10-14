# -*- coding: utf-8 -*-
"""
生成月度报告配图（控制算法方向）
输出：PNG，供 LaTeX 用 \includegraphics 引入
"""
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 150
plt.rcParams['savefig.dpi'] = 150
plt.rcParams['axes.edgecolor'] = '#888888'
plt.rcParams['axes.linewidth'] = 0.9
plt.rcParams['grid.color'] = '#DDDDDD'
plt.rcParams['grid.linewidth'] = 0.7

OUT = r'D:\work\chipdisheat\dachuang-monthly-report\reports\figs'
os.makedirs(OUT, exist_ok=True)

C1 = '#1868A8'   # 主色（与文档配色一致）
C2 = '#E6A23C'
C3 = '#2E7D32'
CR = '#C62828'
GREY = '#666666'


def save(fig, name):
    p = os.path.join(OUT, name)
    fig.savefig(p, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print('  已保存', name, '%.0f KB' % (os.path.getsize(p) / 1024))


# ======================================================================
# 图 1：二阶系统阶跃响应（不同阻尼比）—— 阶段一复现结果
# ======================================================================
zeta_list = [0.0, 0.3, 0.5, 0.707, 1.0, 1.5]
colors = ['#9E9E9E', CR, C2, C3, C1, '#6A1B9A']
labels = [r'$\zeta=0$ (无阻尼)', r'$\zeta=0.3$', r'$\zeta=0.5$',
          r'$\zeta=0.707$ (最佳)', r'$\zeta=1.0$ (临界)', r'$\zeta=1.5$ (过阻尼)']

wn = 1.0
t = np.linspace(0, 16, 2000)


def step2(z, wn, t):
    """二阶系统单位阶跃响应解析解"""
    if z < 1:
        wd = wn * np.sqrt(1 - z**2)
        return 1 - np.exp(-z*wn*t) * (np.cos(wd*t) + z/np.sqrt(1-z**2)*np.sin(wd*t))
    elif abs(z - 1) < 1e-9:
        return 1 - np.exp(-wn*t) * (1 + wn*t)
    else:
        s = np.sqrt(z**2 - 1)
        r1 = -wn*(z - s); r2 = -wn*(z + s)
        return 1 + (r2*np.exp(r1*t) - r1*np.exp(r2*t))/(r1 - r2)


fig, ax = plt.subplots(figsize=(9, 5.2))
for z, c, lb in zip(zeta_list, colors, labels):
    y = step2(z, wn, t)
    lw = 2.8 if abs(z-0.707) < 1e-6 else 2.0
    ax.plot(t, y, color=c, lw=lw, label=lb)

ax.axhline(1.0, color='#333333', ls=':', lw=1.4, label='目标值 1')
ax.axhspan(0.98, 1.02, color=C3, alpha=0.10)
ax.text(13.6, 1.045, '±2% 误差带', fontsize=9, color=C3)

# 标注 ζ=0.707 的峰值
y_best = step2(0.707, wn, t)
i_pk = int(np.argmax(y_best))
ax.annotate('超调 4.33%\n峰值时间 4.44 s',
            xy=(t[i_pk], y_best[i_pk]), xytext=(6.2, 1.30),
            fontsize=9.5, color=C3,
            arrowprops=dict(arrowstyle='->', color=C3, lw=1.3))

ax.set_xlabel(r'时间 $t$ / s', fontsize=11)
ax.set_ylabel(r'输出 $y(t)$', fontsize=11)
ax.set_title(r'二阶系统单位阶跃响应：不同阻尼比对比（$\omega_n=1$ rad/s）',
             fontsize=12.5, fontweight='bold', color='#1a1a1a')
ax.set_xlim(0, 16); ax.set_ylim(-0.05, 1.95)
ax.legend(fontsize=9, loc='lower right', framealpha=0.95)
ax.grid(alpha=0.5); ax.set_axisbelow(True)
save(fig, 'fig_step_response.png')


# ======================================================================
# 图 2：性能指标随阻尼比变化 —— 阶段一复现结果（第二张）
# ======================================================================
zs = np.linspace(0.05, 1.6, 400)
Mp = np.where(zs < 1, np.exp(-np.pi*zs/np.sqrt(np.abs(1-zs**2)))*100, 0)
ts = 4/(zs*wn)

fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.2))

a1.plot(zs, Mp, color=CR, lw=2.6)
for z0 in [0.3, 0.5, 0.707]:
    m0 = np.exp(-np.pi*z0/np.sqrt(1-z0**2))*100
    a1.plot([z0], [m0], 'o', color=CR, ms=7, zorder=5)
    a1.annotate('%.2f%%' % m0, xy=(z0, m0), xytext=(z0+0.06, m0+2.5),
                fontsize=9.5, color=CR)
a1.axvline(0.707, color=C3, ls='--', lw=1.4)
a1.text(0.72, 30, r'$\zeta=0.707$' + '\n超调 4.33%', fontsize=9.5, color=C3)
a1.set_xlabel(r'阻尼比 $\zeta$', fontsize=11)
a1.set_ylabel(r'超调量 $M_p$ / \%', fontsize=11)
a1.set_title('超调量随阻尼比的变化', fontsize=11.5, fontweight='bold')
a1.grid(alpha=0.5); a1.set_axisbelow(True)
a1.set_xlim(0.05, 1.6)

a2.plot(zs, ts, color=C1, lw=2.6, label=r'理论式 $t_s=4/(\zeta\omega_n)$')
# 仿真量取值（本项目复现所得）
z_sim = np.array([0.3, 0.5, 0.707, 1.0])
ts_sim = np.array([11.8, 7.6, 5.7, 4.0])
a2.plot(z_sim, ts_sim, 's--', color=C2, lw=2.0, ms=7,
        label='仿真量取值')
a2.annotate('理论式偏保守\n约 11%', xy=(0.3, 13.33), xytext=(0.45, 12.4),
            fontsize=9.5, color=CR,
            arrowprops=dict(arrowstyle='->', color=CR, lw=1.3))
a2.set_xlabel(r'阻尼比 $\zeta$', fontsize=11)
a2.set_ylabel(r'调节时间 $t_s$ / s', fontsize=11)
a2.set_title('调节时间：理论式与仿真量取的差异', fontsize=11.5, fontweight='bold')
a2.legend(fontsize=9); a2.grid(alpha=0.5); a2.set_axisbelow(True)
a2.set_xlim(0.05, 1.6)

plt.tight_layout()
save(fig, 'fig_metrics.png')


# ======================================================================
# 图 3：控制系统结构图 —— 贯穿两份报告
# ======================================================================
fig, ax = plt.subplots(figsize=(10.5, 4.4))
ax.set_xlim(0, 10.5); ax.set_ylim(0, 4.4)
ax.axis('off')


def box(x, y, w, h, text, fc='#EAF3FA', ec=C1, fs=10, bold=False, tc='black'):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                 boxstyle='round,pad=0.02,rounding_size=0.10',
                 facecolor=fc, edgecolor=ec, lw=1.5, zorder=3))
    ax.text(x + w/2, y + h/2, text, ha='center', va='center',
            fontsize=fs, zorder=4, color=tc,
            fontweight='bold' if bold else 'normal')


def arrow(x1, y1, x2, y2, color='#333333', lw=1.6, style='-|>'):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2),
                 arrowstyle=style, mutation_scale=14,
                 color=color, lw=lw, zorder=2,
                 shrinkA=0, shrinkB=0))


def label(x, y, s, fs=9, color=GREY, ha='center'):
    ax.text(x, y, s, fontsize=fs, color=color, ha=ha, va='center', zorder=5)


# 求和点
ax.add_patch(plt.Circle((1.15, 2.6), 0.22, facecolor='white',
                        edgecolor='#333333', lw=1.5, zorder=4))
ax.text(1.15, 2.6, r'$-$', fontsize=16, ha='center', va='center', zorder=5)
ax.text(1.15, 2.98, r'$+$', fontsize=13, ha='center', va='center', zorder=5)

# 主链
box(0.05, 2.38, 0.75, 0.45, r'$T_{set}$', fc='#F5F5F5', ec=GREY, fs=11)
arrow(0.80, 2.60, 0.93, 2.60)
box(1.60, 2.30, 1.35, 0.60, '控制算法\nPID', fc='#FFF3E0', ec=C2, fs=10, bold=True)
arrow(1.37, 2.60, 1.60, 2.60)
box(3.25, 2.30, 1.30, 0.60, '执行器\n泵（阀）', fc='#EAF3FA', ec=C1, fs=10)
arrow(2.95, 2.60, 3.25, 2.60)
box(4.85, 2.30, 1.20, 0.60, '流速\n' + r'$Q$', fc='#E8F5E9', ec=C3, fs=10, bold=True)
arrow(4.55, 2.60, 4.85, 2.60)
box(6.35, 2.30, 1.45, 0.60, '散热片\n（热流耦合）', fc='#EAF3FA', ec=C1, fs=10)
arrow(6.05, 2.60, 6.35, 2.60)
box(8.10, 2.30, 0.95, 0.60, '芯片\n' + r'$T_c$', fc='#FCE4EC', ec=CR, fs=10, bold=True)
arrow(7.80, 2.60, 8.10, 2.60)
arrow(9.05, 2.60, 9.85, 2.60)
label(10.10, 2.60, r'$T_c$', fs=12, ha='left')

# 反馈
arrow(9.60, 2.30, 9.60, 1.35, color=GREY, lw=1.4)
arrow(9.60, 1.35, 1.15, 1.35, color=GREY, lw=1.4)
arrow(1.15, 1.35, 1.15, 2.38, color=GREY, lw=1.4)
label(5.4, 1.10, '反馈：温度传感器（离散测点）', fs=9.5, color=GREY)

# 两根待辨识函数的标注
ax.annotate('', xy=(4.75, 3.35), xytext=(3.35, 3.35),
            arrowprops=dict(arrowstyle='<|-|>', color=C2, lw=1.6))
label(4.05, 3.55, '待辨识函数 f', fs=10, color=C2)
ax.annotate('', xy=(7.75, 3.35), xytext=(6.45, 3.35),
            arrowprops=dict(arrowstyle='<|-|>', color=C2, lw=1.6))
label(7.10, 3.55, '待辨识函数 g', fs=10, color=C2)

# 扰动
arrow(6.35, 4.05, 6.60, 2.90, color=CR, lw=1.6, style='-|>')
label(6.05, 4.15, '不可控扰动：热流密度 ' + r'$q$', fs=9.5, color=CR)

# 图例
label(0.05, 0.55,
      '待辨识：f = 执行器→流速，g = 流速/水温→芯片温度',
      fs=10, color=C2, ha='left')
label(0.05, 0.20,
      '自变量：泵转速、阀开度、入口水温    因变量：芯片温度    目标：稳定 $T_c$',
      fs=9.5, color=GREY, ha='left')

save(fig, 'fig_block.png')


# ======================================================================
# 图 4：PID 温控仿真时程（数据来自 _sim_pid.py）
# ======================================================================
d = np.load(r'D:\work\chipdisheat\dachuang-monthly-report\reports\figs\pid_sim.npz')
t_sim, heat, hT, hU, hE, hI = d['t'], d['heat'], d['T'], d['U'], d['E'], d['I']
TARGET = 68.0

fig, (a1, a2, a3) = plt.subplots(3, 1, figsize=(9.5, 8.4), sharex=True)

a1.plot(t_sim, heat, color=GREY, lw=1.5, ls='--', label='热源温度（不可控扰动）')
a1.plot(t_sim, hT, color=CR, lw=2.6, label='芯片温度（被控量）')
a1.axhline(TARGET, color=C1, lw=1.8, ls=':', label='目标温度 68 ' + r'\\circ\$' + 'C')
a1.fill_between(t_sim, TARGET, hT, where=(hT > TARGET), color=CR, alpha=0.13)
a1.set_ylabel('温度 / ' + r'\\circ\$' + 'C', fontsize=11)
a1.set_title('增量式 PID 温控仿真（热源 82' + r'\$\pm\$' + '12 ' + r'\\circ\$' + 'C，周期 15 s）',
             fontsize=12.5, fontweight='bold', color='#1a1a1a')
a1.legend(fontsize=9, loc='upper right')
a1.grid(alpha=0.45); a1.set_axisbelow(True)
a1.annotate('峰值超调 3.89 ' + r'\\circ\$' + 'C', xy=(t_sim[np.argmax(hT)], hT.max()),
            xytext=(t_sim[np.argmax(hT)]+6, hT.max()+1.6), fontsize=9.5, color=CR,
            arrowprops=dict(arrowstyle='->', color=CR, lw=1.3))

a2.plot(t_sim, hU, color=C1, lw=2.2)
a2.axhline(100, color=CR, lw=1.8, ls='--')
a2.axhline(0, color=CR, lw=1.8, ls='--')
a2.fill_between(t_sim, 100, 104, color=CR, alpha=0.13)
sat = (hU >= 99.9).mean()*100
a2.text(1.0, 87, '执行器上行程 100%（物理上限）', fontsize=9, color=CR)
a2.text(1.0, 5, '执行器下行程 0%', fontsize=9, color=CR)
a2.text(46, 62, '峰值段有 %.1f%% 时间处于饱和' % sat, fontsize=9.5, color=CR,
        bbox=dict(boxstyle='round', fc='#FFEBEE', ec=CR, alpha=0.9))
a2.set_ylabel('阀开度 / %', fontsize=11)
a2.set_ylim(-8, 112)
a2.grid(alpha=0.45); a2.set_axisbelow(True)

a3.plot(t_sim, hE, color=CR, lw=2.0, label='温度误差 ' + r'\$')
a3.plot(t_sim, hI/10, color=C2, lw=2.0, label='积分项 / 10（限幅 ' + r'\$\pm\$' + '100）')
a3.axhline(0, color='#333333', lw=1.0, ls=':')
a3.set_ylabel('误差 / 积分项', fontsize=11)
a3.set_xlabel('时间 / s', fontsize=11)
a3.legend(fontsize=9); a3.grid(alpha=0.45); a3.set_axisbelow(True)

plt.tight_layout()
save(fig, 'fig_pid_sim.png')

print('\n配图完成 ->', OUT)
