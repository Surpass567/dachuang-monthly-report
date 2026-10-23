# 资料来源与证据边界

本目录仅保存小型来源记录的副本。原始CAD、网格及CFD场文件未修改，也未打包到本报告。
路径及SHA-256见source_manifest.json。生成时检查日期：2026-10-12。

| 来源 | 报告用途 | 不支持的结论 |
|---|---|---|
| mesh_results_02s.csv及结论 | 第三章七档网格敏感性 | 全部网格已经无关、连接结构优势 |
| water_udf_comparison.md | 物性实现一致性与限定计时 | CFD绝对实验精度、代理加速 |
| water_properties_current.c | 函数、温度范围与焓积分 | 任意压力或温度范围准确性 |
| whole_plate_current.md及verification | 当前整板几何与热源对应 | 整板流热已计算完成 |
| strip_assembly_current.md | 条带尺寸、导叶与翼型配置 | 所有连接对照的最终版本或性能 |
| heat_mapping_verification.json | 热源格数量和总功率 | 散热能力与控制效果 |
| historical_dynamic_heat_udf.c | 时间热源探索 | 100区空间独立随机负荷已实现 |
| pressure_audit.json | 压降定义与网格敏感性 | 通用泵电耗与连接优势 |

连接结构已有性能优势、最小闭环已初步验证以及总体演化顺序来自用户提供的阶段进展说明；本次未找到其完整成对数据/控制日志。正文保留这些阶段事实，同时明确量化与证据待补。
较旧intial/output/README.md存在几何未完成的历史说明，以whole_plate/说明.md及其verification作为当前几何状态，不能将旧说明当作当前进度。几何完成不等于求解完成。
