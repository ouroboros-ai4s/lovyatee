---
tags:
  - context
---

# [SRC-52 ProtaBank](../2026-10-29-3a-src-readme/src-52-protabank-readme.md)

无法获取。ProtaBank 是 Protabit LLC 维护的蛋白设计数据仓库, 对应文章 `ProtaBank: A repository for protein design and engineering data`, Protein Science 2018, doi `10.1002/pro.3585`。没有全库导出。

站点只提供检索与导出单研究数据: 网页界面或 REST API 检索、筛选研究, 打开某个 study 后把该 study 的表格导出成 CSV 或 Excel。论文写的 API 能力是批量**上传**与查询, 没有批量下载。全库导出的入口不存在。

数据内容也不覆盖本研究需要的对象。ProtaBank 收的是氨基酸突变对蛋白性质的影响, 性质包括 activity、binding、stability、folding、solubility, 单位混有 Tm、k_cat、Kd、ΔG 与定性、区间值。宿主蛋白多为酶和模型蛋白 (TEM-1、Gβ1 一类), 抗体-抗原不是它的一条独立分类。它没有抗体链序列字段, 也没有抗原实体字段, 即使逐 study 导出也无法落到 `(ab, ag)` 配对。

论文记录的规模只有示例级: 与 Gβ1 相关的序列约 130 万条, 单个 TEM-1 数据集约 990 个点突变。站点首页写 `1691 studies and counting`, 这不是带亲和力标签的配对数, 不能当作样本量。

ProTherm 的蛋白稳定性数据被并入 ProtaBank, 那部分是稳定性而非结合亲和力。

站点 HTTPS 在当前网络下握手失败, 复现于 `openssl s_client -connect 52.37.195.210:443 -servername www.protabank.org`, 返回 `unexpected eof while reading` 且无证书。上述访问方式来自论文与站点公开描述, 不是本机实测页面。

取得整库导出后仍需先筛出抗体-抗原子集, 才能补三侧统计。
