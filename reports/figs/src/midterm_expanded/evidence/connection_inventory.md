# 整流连接结构汇总

共 10 个方案或版本，原目录已迁移至此。模型、参数、预览、源文件及验收记录一并保留。

| 目录 | 方案或版本 | 数量 |
|---|---|---:|
| lianjie | lianjie1、lianjie2、lianjie3、lianjie4 | 4 |
| 三种1mm连接整流结构_最终版_20260918 | 低阻梭形直导叶、三维蜂窝整流格、双排汇聚复向导叶 | 3 |
| gentle_nozzle_spiral_0p5mm | 渐缩渐扩浅螺旋槽 | 1 |
| gentle_nozzle_spiral_0p5mm_deeper | 螺旋槽加深版 | 1 |
| gentle_nozzle_spiral_0p5mm_dense | 密布螺旋槽版 | 1 |

密布版完整 SolidWorks 零件优先使用 `nozzle_threaded_0p5mm_single_solid.SLDPRT`。
各目录的 `display_cutaway.STEP` 仅供展示，完整几何请按各目录 README 选择。
同一方案的不同格式、装配使用的长度缩放副本不重复计数。已存在装配体及其零件副本保留。

生成螺旋槽模型的脚本仍位于 `../2_0/code/`，输出路径已调整到本目录。
迁移记录、最终文件校验值和更新过的路径文件见 `migration_manifest.json`。
