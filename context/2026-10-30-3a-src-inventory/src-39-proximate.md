---
- tags:
  - context
---

# SRC-39 PROXiMATE

无法获取。PROXiMATE (PROtein-protein CompleX MutAtion ThErmodynamics) 由 IIT Madras 的 Gromiha 实验室维护, 对应文章 `PROXiMATE: a database of mutant protein-protein complex thermodynamics and kinetics`, Bioinformatics 2017, 33(17):2787。全库数据只发邮件申请, 站点没有批量文件。

站点 `https://www.iitm.ac.in/bioinfo/PROXiMATE/` 在线, 首页标注最后更新 2021-02-11。Download 页只有一张表, 要求填写姓名、身份、单位、地址、邮箱五项, 全部必填, 提交后由维护者处理。直接访问数据目录 `/bioinfo/cgi-bin/PROXiMATE/data/` 返回 404。其余入口是 Search、Wild-type Data、Homodimer Data 三个逐条查询的 CGI 页面, 可以按蛋白、PDB ID、ΔΔG 区间、突变、实验方法检索单条记录, 没有整表导出。

Usage Notice 限定用途为教育与科研, 维护者不作完整性与准确性担保。

论文与站点的口径: 6,000 条以上错义突变, 160 个以上异二聚体复合物, 早期论文写作 174 个。带亲和力、k_on、k_off、ΔG、ΔΔG、ΔH、ΔS 与实验条件、文献来源, 另有 STRING 网络、DSSP 二级结构与相对可及性。包含的体系不全是抗体-抗原, 混有一般蛋白-蛋白界面突变。

PROXiMATE 的一部分记录已进入 SKEMPI 2.0。SKEMPI 2.0 论文说明收集时把 PROXiMATE 的文献纳入核对; 引用 PROXiMATE 的综述常写作被 SKEMPI 2.0 吸收。两库按测量身份重叠, 将来取得 PROXiMATE 时应与 SKEMPI 去重, 不求和。

取得授权后可补 Antibody / Antigen / Affinity 三侧统计。
