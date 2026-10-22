# 配图目录说明

本目录存放报告用到的**图片**，以及生成配图的**代码与数据**。

---

## 一、目录结构

```
reports/figs/
├── README.md                          ← 本文件
├── 01_temperature_midplane.png        ┐
├── 02_pressure_midplane.png           │
├── ...                                ├ 逻辑月1 在用的 12 张图
├── 11_speed_midplane.png              │  （报告里按 figs/01_xxx.png 引用）
├── 12_copper_base_temperature.png     ┘
└── src/                               ← 代码 / 数据 / 脚本产出的图
    ├── PID仿真.py                      （生成 pid_sim.npz）
    ├── 生成配图.py                      （由 npz 画图）
    ├── pid_sim.npz                     （中间数据）
    ├── fig_block.png                   ┐
    ├── fig_metrics.png                 ├ 控制算法旧图（备用，
    ├── fig_pid_sim.png                 │  当前无报告引用）
    └── fig_step_response.png           ┘
```

**为什么这么分**：

| 位置 | 放什么 | 规则 |
|---|---|---|
| `figs/` 根 | **报告里引用的图片** | 只有 `\includegraphics` 真会用到的才放这 |
| `figs/src/` | 代码、中间数据、脚本产出的图 | 不需要按图号管理的东西 |

这样 `figs/` 根目录一眼就能看清"报告一共用了几张图"。

---

## 二、当前图片清单

### 报告引用的（figs/ 根目录）

| 文件 | 内容 | 用在哪 |
|---|---|---|
| `01_temperature_midplane.png` | 温度云图（中面） | 逻辑月1 |
| `02_pressure_midplane.png` | 压力云图（中面） | 逻辑月1 |
| `03_speed_midplane.png` | 速度云图（中面） | 逻辑月1 |
| `04_copper_base_temperature.png` | 铜底板温度 | 逻辑月1 |
| `05_temperature_midplane.png` | 温度云图（第二工况） | 逻辑月1 |
| `06_pressure_midplane.png` | 压力云图（第二工况） | 逻辑月1 |
| `07_speed_midplane.png` | 速度云图（第二工况） | 逻辑月1 |
| `08_copper_base_temperature.png` | 铜底板温度（第二工况） | 逻辑月1 |
| `09_temperature_midplane.png` | 温度云图（第三工况） | 逻辑月1 |
| `10_pressure_midplane.png` | 压力云图（第三工况） | 逻辑月1 |
| `11_speed_midplane.png` | 速度云图（第三工况） | 逻辑月1 |
| `12_copper_base_temperature.png` | 铜底板温度（第三工况） | 逻辑月1 |

引用写法：

```latex
\includegraphics[width=\linewidth]{figs/01_temperature_midplane.png}
```

### 备用的（src/ 里，报告未引用）

| 文件 | 内容 |
|---|---|
| `fig_block.png` | 控制系统变量结构（含待辨识函数 f、g） |
| `fig_step_response.png` | 二阶系统阶跃响应，六个阻尼比对比 |
| `fig_metrics.png` | 超调量、调节时间随阻尼比的变化 |
| `fig_pid_sim.png` | 增量式 PID 温控仿真时程 |

**这 4 张是上一版控制算法报告用的。**
逻辑月2 的控制部分若沿用 PID 内容 → 可移回 `figs/` 引用；
若改用规则控制（队长 `control_toy_model` 方案）→ 需重新出图。

---

## 三、两个必须注意的坑

### 坑 1：图片找不到时 LaTeX 不中断编译

它会照样生成 PDF，只是**那个位置是空的**。
所以**不要被"PDF 生成了"骗过去**——要查日志里的 `File ... not found`。

### 坑 2：路径与下划线

| 写法 | 结果 |
|---|---|
| `\includegraphics{figs/01_temperature_midplane.png}` | 正常（文件名里 `_` 安全） |
| `\caption{图1_温度场}` | **报错** `Missing $ inserted`（要写 `\_`） |
| `\includegraphics{D:\...\图.png}` | **报错** `Undefined control sequence` |

→ 图题里**别直接贴文件名**；路径**只用相对路径** `figs/文件名`。

---

## 四、重新生成控制算法配图

```powershell
cd reports\figs\src
python PID仿真.py      # ① 先生成 pid_sim.npz
python 生成配图.py      # ② 再画图（输出到 src/）
```

**顺序不能反**：`生成配图.py` 要读 `pid_sim.npz`。

脚本已改成**相对路径**（基于脚本自身位置），换电脑也能跑。

### 仿真参数（改时两处要同步）

`PID仿真.py` 里的参数必须与逻辑月2 报告「仿真工况与控制器参数」一致：

| 参数 | 取值 |
|---|---|
| 目标温度 | 68 ℃ |
| 热源基础温度 / 波动幅度 | 82 ℃ / ±12 ℃，周期 15 s |
| 初始温度 / 环境温度 | 50 ℃ / 25 ℃ |
| 加热系数 a | 0.45 |
| 散热系数 k | 0.03（全关）~ 0.20（全开） |
| PID 参数 | Kp=8.0, Ki=0.5, Kd=2.0 |
| 控制周期 | 50 ms |

改完重跑 `PID仿真.py`，把结果数值同步更新到报告的「闭环仿真结果」表。

---

## 五、新增图片的流程

```
① 画图 / 导出图片
② 命名：月N_图M_简述.png（N=月号，M=图号）
   或沿用现有编号风格 13_xxx.png
③ 放进 reports/figs/
④ 报告里写 \includegraphics[width=\linewidth]{figs/你的图.png}
⑤ 加 \caption 和 \label，并在正文引用一次
⑥ 编译两遍，确认日志 Overfull / Missing / Error 都为 0
```
