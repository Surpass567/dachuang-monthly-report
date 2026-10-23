# 逻辑月3网格检验补充材料

当前报告的所有两档相对差异统一以 N=3235081 为分母。errors_reference323.csv 由 raw_02s.csv 和 dimensionless_02s.csv 计算，包含全部七档；不删除461万档，不将参考档零差异视为通过证明。

流场图取同批t=0.2 s的中高平面与出口截面，323万为上排参考、461万为下排对照。flowfield_notes.md 和 flowfield_comparison.csv 保留定量出处，flowfield_manifest.json 记录来源SHA256。原始说明可能保留早期参考口径，仅作历史证据；当前报告误差分析以 errors_reference323.csv 为准。

执行 finalize_month3_reference323.py 可从已归档CSV重新计算统一误差、作图，并导入本机既有流场图。update_month3_mesh.py 执行后也会调用该脚本生成当前版本。仅整理现有结果，未重新运行Fluent。
