# -*- coding: utf-8 -*-
"""PID 温控仿真：确定可用参数并输出时程数据（供绘图）"""
import numpy as np

TARGET = 68.0
T_AMB = 25.0
HEAT_BASE, HEAT_AMP, HEAT_T = 82.0, 12.0, 15.0
A_HEAT = 0.45
K_MIN, K_MAX = 0.03, 0.20
B_NAT = 0.005
DT = 0.05
T_END = 90.0

# PID 参数（沿用项目里的设定）
KP, KI, KD = 8.0, 0.5, 2.0

t = np.arange(0, T_END, DT)
n = len(t)
heat = HEAT_BASE + HEAT_AMP * np.sin(2 * np.pi * t / HEAT_T)


def simulate(kp, ki, kd, clamp=True, T0=50.0):
    T = T0
    u = 50.0
    le = le2 = 0.0
    integ = 0.0
    hT = np.zeros(n); hU = np.zeros(n); hE = np.zeros(n); hI = np.zeros(n)
    sat_hi = sat_lo = 0
    for k in range(n):
        e = T - TARGET
        integ += e
        if clamp:
            integ = min(max(integ, -100.0), 100.0)
        d = kp * (e - le) + ki * e + kd * (e - 2 * le + le2)
        u += d
        ur = u
        u = min(max(u, 0.0), 100.0)
        if u != ur:
            if ur > 100: sat_hi += 1
            else: sat_lo += 1
        le2, le = le, e
        kk = K_MIN + (K_MAX - K_MIN) * (u / 100.0) ** 0.8
        heating = A_HEAT * (heat[k] - T)
        cooling = kk * (T - T_AMB)
        natural = B_NAT * (T - T_AMB)
        T = min(max(T + (heating - cooling - natural) * DT, 20.0), 120.0)
        hT[k] = T; hU[k] = u; hE[k] = e; hI[k] = integ
    return hT, hU, hE, hI, sat_hi, sat_lo


hT, hU, hE, hI, sh, sl = simulate(KP, KI, KD, clamp=True)

print('=' * 70)
print('PID 温控仿真（a=%.2f, k=%.2f~%.2f, 热源 %.0f±%.0f°C, 目标 %.0f°C）'
      % (A_HEAT, K_MIN, K_MAX, HEAT_BASE, HEAT_AMP, TARGET))
print('=' * 70)
print('  芯片温度   范围 %.2f ~ %.2f °C   末值 %.2f   稳态均值 %.2f'
      % (hT.min(), hT.max(), hT[-1], hT[n//2:].mean()))
print('  阀开度     范围 %.1f ~ %.1f %%     均值 %.1f'
      % (hU.min(), hU.max(), hU.mean()))
print('  最大误差   %+.2f °C' % hE[n//2:].max())
print('  上行程饱和 %d 步（%.1f%%）  下行程饱和 %d 步（%.1f%%）'
      % (sh, sh/n*100, sl, sl/n*100))

# 超调量
steady = hT[n//2:].mean()
overshoot = (hT[n//2:].max() - TARGET) / TARGET * 100
print('  相对目标的峰值超调  %.2f °C（%.2f%%）'
      % (hT[n//2:].max() - TARGET, overshoot))

# 对比：不加积分限幅会怎样
hT2, hU2, hE2, hI2, sh2, sl2 = simulate(KP, KI, KD, clamp=False)
print()
print('  对比（不加积分限幅）:')
print('    积分项最大 %.1f（限幅版 %.1f）' % (hI2.max(), hI.max()))
print('    温度范围 %.2f ~ %.2f °C' % (hT2.min(), hT2.max()))

np.savez_compressed(r'D:\work\chipdisheat\dachuang-monthly-report\reports\figs\pid_sim.npz',
                    t=t, heat=heat, T=hT, U=hU, E=hE, I=hI,
                    T_nc=hT2, U_nc=hU2, I_nc=hI2)
print()
print('  已保存 pid_sim.npz')
