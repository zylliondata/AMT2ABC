# AMT Graph SECP 格式规范

## 概述

AMT Graph 采用 **Mechanism + AMT Triplet** 的组合结构来表示工业机理知识。

- **Mechanism**: SECP 源节点，存储四维指纹和元数据
- **AMT Triplet**: 由 Cause、Effect、CAUSAL 组成的因果三元组

## 数据模型

### 1. Mechanism 节点 (SECP 源)

```json
{
  "amt_id": "AMT_DC_THERMO_001",
  "name": "傅里叶热传导-模具温度场",
  "name_en": "Fourier Heat Conduction - Mold Temperature Field",
  "layer": "天理",
  "evidence_source": "physics_law",
  "mcl_engine": "numerical_calculation",
  "source_apps": "App_001, App_002",
  "reference": "ISO 10816-3",
  "formula_dsl": "q = -k * dT/dx",
  "secp_category": "Mechanism",
  "cause_id": "CAUSE_AMT_DC_THERMO_001",
  "effect_id": "EFFECT_AMT_DC_THERMO_001",
  "secp": {
    "S": {
      "subject": "模具",
      "attributes": ["模温分布", "温度场"]
    },
    "E": ["热传导", "温度变化"],
    "C": {
      "k": "80-120 W/(m·K)",
      "dT/dx": "100-500 K/m"
    },
    "P": ["冷却水", "带热", "降温"]
  }
}
```

#### 字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| amt_id | string | ✅ | 唯一标识，格式: `AMT_{DOMAIN}_{TYPE}_{SEQ}` |
| name | string | ✅ | 中文名称 |
| name_en | string | ❌ | 英文名称 |
| layer | string | ❌ | 三理分层: 天理/法理/人理 |
| evidence_source | string | ❌ | 证据来源: physics_law/empirical_formula/expert_knowledge |
| mcl_engine | string | ❌ | 计算引擎: numerical_calculation/rule_engine/machine_learning |
| source_apps | string | ❌ | 来源 App，逗号分隔 |
| reference | string | ❌ | ISO 参考标准 |
| formula_dsl | string | ❌ | 公式 DSL 表达式 |
| secp_category | string | ✅ | SECP 分类: Mechanism/ProcessDefinition/State |
| cause_id | string | ✅ | 引用 AMT_Cause 的 cause_id |
| effect_id | string | ✅ | 引用 AMT_Effect 的 effect_id |
| secp | string | ✅ | SECP 四维指纹 JSON |

### 2. AMT_Cause 顶点 (S 维度)

```json
{
  "cause_id": "CAUSE_AMT_DC_THERMO_001",
  "name": "模具-模温分布",
  "name_en": "Mold - Temperature Distribution",
  "entity_id": "模具",
  "attribute": "模温分布",
  "value_range": "200-400°C",
  "description": "模具温度场分布状态",
  "secp_category": "Structure"
}
```

#### 字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| cause_id | string | ✅ | 唯一标识，格式: `CAUSE_{amt_id}` |
| name | string | ✅ | 名称，格式: `{entity}-{attribute}` |
| name_en | string | ❌ | 英文名称 |
| entity_id | string | ✅ | 实体标识 (对应 SECP.S.subject) |
| attribute | string | ✅ | 属性名称 (对应 SECP.S.attributes[0]) |
| value_range | string | ❌ | 值域范围 |
| description | string | ❌ | 描述 |
| secp_category | string | ✅ | 固定值: "Structure" |

### 3. AMT_Effect 顶点 (E 维度)

```json
{
  "effect_id": "EFFECT_AMT_DC_THERMO_001",
  "name": "热量传递",
  "name_en": "Heat Transfer",
  "entity_id": "冷却水道",
  "attribute": "温度",
  "value_range": "20-30°C",
  "event_name": "热传导",
  "description": "热量从模具传递到冷却水",
  "secp_category": "Event"
}
```

#### 字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| effect_id | string | ✅ | 唯一标识，格式: `EFFECT_{amt_id}` |
| name | string | ✅ | 名称 |
| name_en | string | ❌ | 英文名称 |
| entity_id | string | ✅ | 实体标识 |
| attribute | string | ❌ | 属性名称 |
| value_range | string | ❌ | 值域范围 |
| event_name | string | ✅ | 事件名称 (对应 SECP.E[0]) |
| description | string | ❌ | 描述 |
| secp_category | string | ✅ | 固定值: "Event" |

### 4. CAUSAL 边 (C/P/F 维度)

```json
{
  "weight": 1.0,
  "confidence": 0.8,
  "mechanism_id": "AMT_DC_THERMO_001",
  "mechanism_name": "傅里叶热传导-模具温度场",
  "description": "热量通过热传导从高温区传递到低温区",
  "config": {
    "k": "80-120 W/(m·K)",
    "dT/dx": "100-500 K/m"
  },
  "process": ["冷却水", "带热", "降温"],
  "formula": "q = -k * dT/dx",
  "input_vars": ["k (热导率)", "dT/dx (温度梯度)"],
  "output_vars": ["q (热通量)"]
}
```

#### 字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| weight | float | ❌ | 权重，默认 1.0 |
| confidence | float | ❌ | 置信度，0-1 |
| mechanism_id | string | ✅ | 关联的 Mechanism ID |
| mechanism_name | string | ❌ | 机理名称 |
| description | string | ❌ | 描述 |
| config | string | ❌ | 配置参数 JSON (对应 SECP.C) |
| process | string | ❌ | 工艺步骤 JSON 数组 (对应 SECP.P) |
| formula | string | ❌ | 数学公式表达式 |
| input_vars | string | ❌ | 输入变量 JSON 数组 |
| output_vars | string | ❌ | 输出变量 JSON 数组 |

## SECP 维度映射

| SECP 维度 | 权重 | 存储位置 | 说明 |
|-----------|------|---------|------|
| **S (Structure)** | 0.30 | Mechanism.secp.S → AMT_Cause | 主体结构 |
| **E (Event)** | 0.20 | Mechanism.secp.E → AMT_Effect | 事件/动作 |
| **C (Configuration)** | 0.15 | Mechanism.secp.C → CAUSAL.config | 配置参数 |
| **P (Process)** | 0.10 | Mechanism.secp.P → CAUSAL.process | 工艺步骤 |
| **F (Formula)** | 0.25 | CAUSAL.formula | 数学公式 |

## 图结构

```
Mechanism ──COMPOSED_OF──→ AMT_Cause
    │
    └────COMPOSED_OF──→ AMT_Effect

AMT_Cause ──CAUSAL──→ AMT_Effect
```

### 边类型

| 边类型 | 源节点 | 目标节点 | 说明 |
|--------|--------|---------|------|
| COMPOSED_OF | Mechanism | AMT_Cause/AMT_Effect | 组合关系 |
| CAUSAL | AMT_Cause | AMT_Effect | 因果关系 |

## 查询示例

### 1. 查询完整三元组

```ngql
MATCH (m:Mechanism)-[:COMPOSED_OF]->(c:AMT_Cause)
MATCH (m)-[:COMPOSED_OF]->(e:AMT_Effect)
MATCH (c)-[ca:CAUSAL]->(e)
WHERE m.Mechanism.amt_id == "AMT_DC_THERMO_001"
RETURN m.Mechanism.name, c, e, ca
```

### 2. 根据主体查找机理

```ngql
MATCH (m:Mechanism)-[:COMPOSED_OF]->(c:AMT_Cause)
WHERE c.AMT_Cause.entity_id == "模具"
RETURN m.Mechanism.amt_id, m.Mechanism.name
```

### 3. 根据公式查找机理

```ngql
MATCH (c:AMT_Cause)-[ca:CAUSAL]->(e:AMT_Effect)
WHERE ca.formula CONTAINS "q = -k"
MATCH (m:Mechanism)-[:COMPOSED_OF]->(c)
RETURN m.Mechanism.name, ca.formula
```

### 4. 场景匹配查询

```ngql
-- 查找 subject=压铸件 的所有机理
MATCH (m:Mechanism)-[:COMPOSED_OF]->(c:AMT_Cause)
WHERE c.AMT_Cause.entity_id == "压铸件"
MATCH (m)-[:COMPOSED_OF]->(e:AMT_Effect)
MATCH (c)-[ca:CAUSAL]->(e)
RETURN m.Mechanism.name, ca.formula, ca.config
```

## 数据示例

### 傅里叶热传导

```json
{
  "mechanism": {
    "amt_id": "AMT_DC_THERMO_001",
    "name": "傅里叶热传导-模具温度场",
    "secp": {
      "S": {"subject": "模具", "attributes": ["模温分布", "温度场"]},
      "E": ["热传导", "温度变化"],
      "C": {"k": "80-120 W/(m·K)", "dT/dx": "100-500 K/m"},
      "P": ["冷却水", "带热", "降温"]
    }
  },
  "cause": {
    "cause_id": "CAUSE_AMT_DC_THERMO_001",
    "entity_id": "模具",
    "attribute": "模温分布",
    "value_range": "200-400°C"
  },
  "effect": {
    "effect_id": "EFFECT_AMT_DC_THERMO_001",
    "event_name": "热传导",
    "entity_id": "冷却水道"
  },
  "causal": {
    "formula": "q = -k * dT/dx",
    "config": {"k": "80-120 W/(m·K)", "dT/dx": "100-500 K/m"},
    "process": ["冷却水", "带热", "降温"],
    "input_vars": ["k (热导率)", "dT/dx (温度梯度)"],
    "output_vars": ["q (热通量)"]
  }
}
```

### 压射充填

```json
{
  "mechanism": {
    "amt_id": "AMT_DC_FLUID_001",
    "name": "压射充填-高速流动",
    "secp": {
      "S": {"subject": "压铸机", "attributes": ["压射速度", "充填时间"]},
      "E": ["高速流动", "充填"],
      "C": {"压射速度": "2-6 m/s", "铝液温度": "680-720°C"},
      "P": ["低速排气", "高速充填", "增压凝固"]
    }
  },
  "cause": {
    "cause_id": "CAUSE_AMT_DC_FLUID_001",
    "entity_id": "压铸机",
    "attribute": "压射速度",
    "value_range": "2-6 m/s"
  },
  "effect": {
    "effect_id": "EFFECT_AMT_DC_FLUID_001",
    "event_name": "高速流动",
    "entity_id": "模具型腔"
  },
  "causal": {
    "formula": "P + ½ρv² + ρgh = const (伯努利方程)",
    "config": {"压射速度": "2-6 m/s"},
    "process": ["低速排气", "高速充填", "增压凝固"],
    "input_vars": ["P (压力)", "ρ (密度)", "v (流速)"],
    "output_vars": ["v (充填速度)"]
  }
}
```

## 编译器使用

### 加载数据

```python
from amt_compiler import AMTCompiler

# 从 NebulaGraph 加载数据
compiler = AMTCompiler(use_formula=True)

# 准备 scenario
scenario = {
    'goal': '预测缩孔风险',
    'domain': 'die_casting',
    'S': {'subject': '压铸件', 'attributes': ['缩孔体积', '凝固分数']},
    'E': ['缩孔形成', '凝固收缩'],
    'C': {'浇注温度': '680-720°C'},
    'P': ['高速充填', '增压凝固'],
    'signals': ['浇注温度', '保压压力', '模具温度'],
}

# 编译
result = compiler.compile(
    goal='预测缩孔风险',
    scenario=scenario,
    mechanisms=mechanisms,
    threshold=0.3
)

# 获取推荐结果
for mech, scores in zip(result['recommended_mechanisms'], result['scores']):
    print(f"{mech['name']}: {scores['total']:.2f}")
```

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0 | 2026-07-16 | 初始版本，支持 AMT Triplet 结构 |
