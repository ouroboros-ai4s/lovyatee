---
tags:
  - context
---

# Certificate Must Be Verifiable Offline

## time

2026-10-22

## lineage

- [[similarity_structure_is_not_a_certificate]]: 该条要求 S 与 C 可分别寻址；本条要求两者都能脱离产生它们的进程被复核。
- [[held_out_certificates_are_relative_to_a_declared_validator]]: 证书是三元组的记录，复核必须能在没有服务器时重放三元组。
- <https://arxiv.org/abs/2312.07852>: Workflow Run RO-Crate 把一次运行的全部对象打包成可归档单元，是"证书即文件"的既有形态。
- <https://arxiv.org/abs/2508.02866>: PROV-AGENT 证明 agent 交互也需要进入 provenance，而不仅是被执行的工作流。

## relation

- [[similarity_structure_is_not_a_certificate]]: A ⊑ B.

## description

原型把全部状态放在进程内的字典里，`evaluate_coverage` 与 `materialize_plan` 都要求对象来自本进程。于是重启、换机、三个月后复查都不可能。而"可复算、可审计"是这件产物存在的理由——一个活不过进程的证书没有这性质。

证书必须是一份**自校验字节**：

1. 内部哈希链：`certificate_hash = H(declaration, s_digest, result)`，任何字段改动都使哈希失配。
2. 每个外部引用带内容摘要，不只带 id：S 摘要、D 版本、`X` 的 adapter 版本与参数。
3. 可选签名，但不作为必要条件——签名解决"谁说的"，哈希解决"有没有被改"，两者不同层。
4. 复核器是一个纯函数：`verify(blob) -> {ok, mismatches}`，不需要数据库、不需要网络、不需要同一套服务端代码。

这条与 RO-Crate / PROV 的关系要说清：它们解决的是"把一次运行的对象打包并记录关系"，本条在此基础上多要求一条——**证书里的结论必须能由证书里的输入重新算出来**。打包不保证可复算；可复算要求 `F` 是纯函数且输入完整。这是证书与 provenance 文档的分界。

**代价**：自校验字节意味着大对象（相似性稀疏结构）要么内联（体积大），要么外置但摘要化。选择外置 + 摘要，并用一个可选的 `bundle` 模式在需要归档时内联。

**可证伪内容**：若存在一类合法证书，其结论依赖不可重现的外部状态（例如某个未冻结版本的在线数据库），则证书只能记录该状态而不能自校验；此时应把它降级为 "report"，不叫 certificate。
