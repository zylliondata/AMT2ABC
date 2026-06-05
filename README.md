# AMT2ABC：从原子机理到原子业务能力的工业软件 Compiler

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

**AMT2ABC** 是一个开源的工业软件能力编译生态。它将工业机理（Atomic Mechanism Triplet, AMT）自动编译为可复用的原子业务能力（Atomic Business Capability, ABC），为工业智能化提供从业务目标到可执行应用的自动化编译能力。

> 工业软件缺的不是AI，而是Compiler。  
> —— AMT2ABC 核心主张

## 为什么需要 AMT2ABC？

传统工业软件开发长期陷入"项目制、烟囱式、变更代价高"的困境。不同产线、不同工艺之间难以复用能力，每次变更都需要大量手工修改代码。AMT2ABC 借鉴华为韬(τ)定律和 RISC+Compiler 的历史经验，将复杂度从底层代码转移到实例配置层，让系统自动理解业务目标并编译出最优能力组合。

## 核心概念

| 概念 | 全称 | 说明 |
|------|------|------|
| **AMT** | Atomic Mechanism Triple | 原子机理三元组，不可再拆的最小工业因果单元，如"负载↑ → 振动↑" |
| **SECP** | Structure, Event, Configuration, Process | 工业软件的四维语法，为 AMT 提供统一的结构化标签 |
| **ABC** | Atomic Business Capability | 原子业务能力，可独立部署、跨场景复用的最小软件能力单元 |
| **Compiler** | AMT2ABC Compiler | 从业务目标（GS）自动抽取 AMT Cluster，封装为 ABC 并编排为 App/Agent 的系统 |

## 架构概览

```
Working Domain → Mechanism → AMT → AMT Graph
                                           ↓
GS(目标) → AMT Cluster → ABC
                           ↓
              App/Agent → Scenario → OAO Loop
```

- **人定义的部分**：工作域、机理、AMT、AMT Graph
- **Compiler 自动完成的部分**：GS → AMT Cluster → ABC → App/Agent

## 快速开始

### 前提条件

- 了解工业机理的基本概念
- 熟悉 YAML/JSON 配置

### 安装 Compiler 原型（MVP）

```bash
git clone https://github.com/zylliondata/AMT2ABC.git
cd AMT2ABC
# 具体安装步骤见 docs/installation.md（即将补充）
```

### 最简单的示例

输入目标："降低气孔率"（压铸产线）

Compiler 输出推荐的 ABC 组合（JSON 格式示例）：

```json
{
  "goal": "降低气孔率",
  "recommended_abc": ["模温控制ABC", "压射速度优化ABC", "真空度管理ABC"]
}
```

详细教程请参考 docs/getting-started.md（即将补充）。

## 开源生态计划

| 阶段 | 时间 | 目标 |
|------|------|------|
| 1. 上手原型 | 今年 Q3 | 开源 Compiler MVP + 压铸产线示例 |
| 2. 贡献社区 | 今年 Q4 起 | 开放 AMT/SECP 范式贡献通道 |
| 3. ABC Registry | 明年起 | 类似 Docker Hub 的 ABC 能力市场 |
| 4. 推动标准化 | 三年后 | 国内团体标准 → 国际标准 |

## 参与贡献

我们欢迎所有形式的贡献，包括但不限于：

- 提交新的 AMT 范式或 SECP 指纹
- 封装并共享 ABC 模块
- 改进 Compiler 的匹配算法
- 完善文档和教程

请阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详细流程。

## 行为准则

本项目遵循 Contributor Covenant Code of Conduct。请阅读[全文](CODE_OF_CONDUCT.md)。

## 安全报告

如发现安全漏洞，请参考 [SECURITY.md](SECURITY.md) 中的报告流程。

## 许可证

[Apache 2.0 License](LICENSE) © AMT2ABC Contributors

## 联系我们

- 提交 Issue：<https://github.com/zylliondata/AMT2ABC/issues>
- 社区讨论：<https://github.com/zylliondata/AMT2ABC/discussions>
- 邮箱：info@zylliondata.com
