---
tags:
  - design
---

# AB AG Sequence Data Analysis Design

本次分析固定以下三个 O/X 组合：

1. **AB：CDR-H3 抗体对象** —— `O`：经过 [[2026-10-31-3a-src-tools/imgt_numbering|IMGT unique numbering]] 的抗体可变区中，由 CDR-H3 编号位置定义的氨基酸残基序列；插入位点只保留在编号层，不进入序列。`X`：按 IMGT 编号对齐 CDR-H3，以氨基酸序列和编辑距离进行测量。
2. **AG：抗原表面 patch 对象** —— `O`：抗原结构表面上由一组表面残基组成的局部 patch；对象由残基身份及其空间邻接关系定义，见 [[2026-10-28-ab-ag-data-diversity/antigen_surface_patch_geometry_is_the_unfilled_collection_axis|Antigen Surface Patch Geometry Is The Unfilled Collection Axis]]。`X`：记录 patch 残基、空间坐标、接触图和几何描述，并据此进行表面 patch 比较。
3. **AG：蛋白质表面对象** —— `O`：抗原结构中的单个表面残基或由其组成的表面 patch，按 [[2026-10-31-3a-src-tools/zsasa_surface_area_measurement|zsasa surface area measurement]] 的 residue / surface patch 对象定义。`X`：计算 `SASA_single - SASA_complex`，以 `max(0, measure)` 作为 burial，并使用按埋藏面积加权的氨基酸组成作为表面描述子；固定原子选择、ProtOr 半径、1.4 Å 探针、双精度、采样密度和非标准残基处理规则，并以 [[2026-10-31-3a-src-tools/freesasa_surface_area_control|FreeSASA surface area control]] 做数值控制。
