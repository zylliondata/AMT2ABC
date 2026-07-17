# AMT 图谱总结报告

> 压铸领域工业机理知识图谱 (AMT_Graph)
> 生成日期: 2026-07-17

## 1. 概述

AMT (Atomic Mechanism Triplet, 原子机理三元组) 图谱是一个面向**压铸制造领域**的工业机理知识图谱，采用 NebulaGraph 3.8.0 作为图数据库存储。AMT 是**不可再拆的最小工业因果单元**，如"负载↑ → 振动↑"。图谱以 **SECP 四维语法**（Structure / Event / Configuration / Process）为核心组织方式，将工业机理建模为原子机理三元组。

## 2. 统计信息

### 2.1 节点统计

| 节点标签 | 数量 | 说明 |
|---------|------|------|
| **Mechanism** | 44 | 机理节点 (34个压铸机理 + 10个状态机机理) |
| **AMT_Cause** | 34 | 原因维度节点 (S维度) |
| **AMT_Effect** | 34 | 结果维度节点 (E维度) |
| **Entity** | 133 | 实体节点 (设备、物料、人员、文档) |
| **Event** | 72 | 事件节点 |
| **State** | 78 | 状态节点 (设备状态、工单状态) |
| **UIAction** | 1,151 | UI操作节点 (来自222个Tulip应用) |
| **ProcessDefinition** | 237 | 流程定义节点 |
| **合计** | **1,783** | |

### 2.2 边统计

| 边类型 | 数量 |
|--------|------|
| CONTAINS_UIACTION | 2,264 |
| CONTAINS_EVENT | 242 |
| COMPOSED_OF | 68 |
| NEXT_STEP | 70 |
| CAUSAL | 34 |

### 2.3 实体分类

| 类型 | 数量 | 示例 |
|------|------|------|
| 设备 (equipment) | 32 | 压铸机、模具、熔炉、合模系统、温控器 |
| 物料 (material) | 28 | 压铸件、铝合金、脱模剂、工单 |
| 人员 (personnel) | 17 | 质检员、维修工程师、操作员 |
| 工艺 (process) | 13 | 凝固组织、厚壁区、工艺定义 |
| 质量 (quality) | 12 | 检验计划、纠正预防、质量事件 |
| 数据记录 (DataRecord) | 12 | 模具使用记录、追溯记录、报废记录 |
| 位置 (location) | 7 | 车间、生产线、工作站、仓库 |
| 文档 (document) | 5 | SOP、作业指导书 |
| 订单 (order) | 5 | 生产计划、班次、工单 |

## 3. 机理分类

### 3.1 按物理领域

全部34个压铸机理属于**天理层**（不变的物理定律），分为6大类：

#### 热力学 (THERMO, 9个)

| ID | 名称 | 公式 | 证据来源 | 计算引擎 |
|----|------|------|----------|----------|
| AMT_DC_THERMO_001 | 傅里叶热传导-模具温度场 | q = -k * dT/dx | physics_law | numerical_calculation |
| AMT_DC_THERMO_002 | 牛顿冷却定律-模具散热 | Q = h*A*(Tw-Tinf) | physics_law | numerical_calculation |
| AMT_DC_THERMO_003 | 凝固相变-潜热释放 | Q = L * dm/dt | physics_law | numerical_calculation |
| AMT_DC_THERMO_004 | 模具预热温度场均匀性 | dT/dt = Q/(m*Cp) | physics_law | numerical_calculation |
| AMT_DC_THERMO_005 | 冷却水道散热效率 | Q = m_dot*Cp*dT | physics_law | numerical_calculation |
| AMT_DC_THERMO_006 | 浇注温度对流动性影响 | mu = mu_0*exp(Ea/RT) | physics_law | numerical_calculation |
| AMT_DC_THERMO_007 | 凝固收缩-体积变化 | dV/V = beta*dT | physics_law | numerical_calculation |
| AMT_DC_THERMO_008 | 热平衡-模具温度波动 | Q_in = Q_out | physics_law | numerical_calculation |
| AMT_DC_THERMAL_EXPANSION_001 | 热膨胀量计算 | dL = alpha * L * dT | physics_law | numerical_calculation |

#### 力学 (MECH, 6个)

| ID | 名称 | 公式 | 证据来源 | 计算引擎 |
|----|------|------|----------|----------|
| AMT_DC_MECH_001 | 热应力-模具疲劳裂纹 | s = E*a*dT/(1-n) | physics_law | numerical_calculation |
| AMT_DC_MECH_002 | 锁模力-飞边控制 | F >= P*A | physics_law | rule_engine |
| AMT_DC_MECH_003 | 压射压力-内部致密度 | P = F/A_shot | physics_law | numerical_calculation |
| AMT_DC_MECH_004 | 模具变形-尺寸精度 | d = F*L^3/(3*E*I) | physics_law | numerical_calculation |
| AMT_DC_MECH_005 | 残余应力-铸件变形 | s = s_thermal + s_mechanic | physics_law | numerical_calculation |
| AMT_DC_MECH_006 | 顶出力-铸件脱模 | F = u*P*A + Fsh | physics_law | rule_engine |

#### 流体力学 (FLUID, 7个)

| ID | 名称 | 公式 | 证据来源 | 计算引擎 |
|----|------|------|----------|----------|
| AMT_DC_FLUID_001 | 压射充填-高速流动 | Navier-Stokes | physics_law | numerical_calculation |
| AMT_DC_FLUID_002 | 气体卷吸-气孔形成 | Re = rho*v*L/mu | physics_law | numerical_calculation |
| AMT_DC_FLUID_003 | 排气设计-气体排出效率 | Q = A*Cd*sqrt(2dP/r) | physics_law | numerical_calculation |
| AMT_DC_FLUID_004 | 内浇口设计-充填模式 | v = Q/A_gate | physics_law | numerical_calculation |
| AMT_DC_FLUID_005 | 真空度对气孔率影响 | P = P_amb*(1-Ve) | physics_law | numerical_calculation |
| AMT_DC_FLUID_006 | 压射三段-慢速高速增压 | v1<v2>v3 | empirical | rule_engine |
| AMT_DC_FLUID_007 | 脱模剂喷涂-表面状态 | m = Cd*A*sqrt(2rho*dP) | empirical | numerical_calculation |

#### 材料科学 (MATL, 7个)

| ID | 名称 | 公式 | 证据来源 | 计算引擎 |
|----|------|------|----------|----------|
| AMT_DC_MATL_001 | 缩孔形成-最后凝固区 | V = V*beta*(1-fs) | physics_law | numerical_calculation |
| AMT_DC_MATL_002 | 微观组织-晶粒度 | d = b*G^(-1/2)*R^(-1/3) | physics_law | numerical_calculation |
| AMT_DC_MATL_003 | 气体溶解度-氢含量 | S = A*sqrt(P)*exp(-E/RT) | physics_law | numerical_calculation |
| AMT_DC_MATL_004 | 氧化皮-夹渣缺陷 | dx/dt = k_ox * exp(-Q/RT) | empirical | numerical_calculation |
| AMT_DC_MATL_005 | 合金成分-力学性能 | UTS = f(Si,Cu,Mg,Fe,CR) | empirical | rule_engine |
| AMT_DC_MATL_006 | 模具寿命-磨损机理 | W = K*P*V*t | empirical | rule_engine |
| AMT_DC_MATL_007 | 热裂纹-模具失效 | N = C*(de)^(-m) | empirical | rule_engine |

#### 综合评估 (Other, 5个)

| ID | 名称 | 公式 | 证据来源 | 计算引擎 |
|----|------|------|----------|----------|
| AMT_DC_RISK_CLASSIFY_001 | 飞边风险等级分类 | <=0.5%->Low, >0.8%->High | threshold_rule | rule_engine |
| AMT_DC_QUALITY_ALERT_001 | 缩孔超限报警 | if shrinkage > 0.5% | threshold_rule | rule_engine |
| AMT_DC_FLASH_DEFECT_MAP_001 | 飞边缺陷率映射 | P_flash = f(gap,pressure,T) | empirical | rule_engine |
| AMT_DC_GAP_EVALUATION_001 | 动态合模间隙评估 | Gap = Gap0 - dL | empirical | rule_engine |
| AMT_DC_PROCESS_PARAM_ADJUST_001 | 工艺参数调整 | Expert Rule + Optimization | experience_rule | rule_engine |

## 4. AMT 原子机理三元组

AMT (Atomic Mechanism Triplet) 是**不可再拆的最小工业因果单元**。每个机理节点通过COMPOSED_OF边连接到对应的原因和结果节点，形成三元组：

```
AMT_Cause (S: 结构/主体)
    |-- entity_id: 目标对象 (如"模具"、"压铸件")
    |-- attribute: 关键属性 (如"模温分布"、"收缩率")
    |-- value_range: 值域范围
    |
    |  CAUSAL边 (C/P: 配置/流程)
    |  |-- config: 工艺参数和阈值
    |  |-- process: 工艺步骤
    |  |-- formula: 物理公式 (附注)
    |
    v
AMT_Effect (E: 事件/触发)
    |-- event_name: 事件名称 (如"缩孔形成"、"飞边形成")
    |-- entity_id: 受影响实体
```

### 4.1 三元组示例

| 机理 | Cause (S) | CAUSAL (C/P) | Effect (E) |
|------|-----------|--------------|------------|
| AMT_DC_THERMO_001 | 模具.模温分布 | q = -k * dT/dx | 温度场变化 |
| AMT_DC_MECH_002 | 压铸机.锁模力 | F >= P * A | 飞边控制 |
| AMT_DC_MATL_001 | 压铸件.收缩率 | V = V0 * beta * (1-fs) | 缩孔缺陷 |

## 5. 压铸工艺流程

6个完整的工艺定义，包含30个状态节点：

- **5.1 熔炼**: 加料 → 熔化 → 成分检测 → 温度控制 → 保温
- **5.2 压铸**: 合模 → 浇注 → 压射 → 保压 → 凝固 → 喷涂
- **5.3 取件**: 开模 → 顶出 → 机器人取件 → 切边 → 喷模
- **5.4 后处理**: 切割 → 去毛刺 → 清洗 → 洗涤 → 干燥
- **5.5 检测**: 目视检查 → 尺寸测量 → X光检测 → 力学测试 → 判定
- **5.6 包装**: 称重 → 贴标 → 包装 → 入库

## 6. SECP 四维语法

| 维度 | 全称 | 含义 | 示例 |
|------|------|------|------|
| **S** | Structure (结构/主体) | 目标对象及其属性 | 模具、压铸件、压铸机 |
| **E** | Event (事件/触发) | 产生的效果或事件 | 温度超标、飞边检测 |
| **C** | Configuration (配置/约束) | 工艺参数和阈值 | 阈值、参数、规则 |
| **P** | Process (流程/步骤) | 工艺步骤 | 检测→分析→调整 |

## 7. 应用场景

- **7.1 缩孔预测 (SC_DC_001)**: 匹配8个机理，最高分0.51
- **7.2 飞边风险预测 (SC_DC_FLASH_001)**: 匹配2个机理，最高分0.35
- **7.3 气孔率控制 (SC_DC_003)**: 匹配8个机理，最高分0.47
- **7.4 模具寿命预测 (SC_DC_004)**: 匹配18个机理，最高分0.47

## 8. 编译器性能

| 指标 | 值 |
|------|-----|
| 图谱数据加载 | 0.736s |
| 单次编译 | 2.55ms (平均) |
| 编译吞吐量 | 393次/秒 |
| 单机理评分 | 0.062ms |
| 评分吞吐量 | 16,041个机理/秒 |
| 三元组图查询 | 28.81ms |

---

> 报告由 AMT_Graph NebulaGraph 数据库生成。版本: AMT_Graph v1.0 | 引擎: NebulaGraph 3.8.0
