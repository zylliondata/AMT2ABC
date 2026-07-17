# AMT Graph 快速入门

## 前提条件

- Python 3.8+
- NebulaGraph 已安装并运行
- 已安装 nebula3 Python 客户端

## 连接图谱

```python
import sys
sys.path.insert(0, r"D:\opencode\abl2abc")
from src.nebula_client import NebulaClient

c = NebulaClient()
c.connect()
```

## 查询示例

### 1. 查询所有 Mechanism 节点

```python
rows = c.execute('MATCH (v:Mechanism) RETURN v.Mechanism.amt_id, v.Mechanism.name')
for r in rows:
    print(f"{r['v.Mechanism.amt_id']}: {r['v.Mechanism.name']}")
```

### 2. 查询完整三元组

```python
rows = c.execute('''
    MATCH (m:Mechanism)-[:COMPOSED_OF]->(c:AMT_Cause)
    MATCH (m)-[:COMPOSED_OF]->(e:AMT_Effect)
    MATCH (c)-[ca:CAUSAL]->(e)
    WHERE m.Mechanism.amt_id == "AMT_DC_THERMO_001"
    RETURN m.Mechanism.name, c, e, ca
''')
```

### 3. 根据主体查找机理

```python
rows = c.execute('''
    MATCH (m:Mechanism)-[:COMPOSED_OF]->(c:AMT_Cause)
    WHERE c.AMT_Cause.entity_id == "模具"
    RETURN m.Mechanism.amt_id, m.Mechanism.name
''')
```

### 4. 根据公式查找机理

```python
rows = c.execute('''
    MATCH (c:AMT_Cause)-[ca:CAUSAL]->(e:AMT_Effect)
    WHERE ca.formula CONTAINS "q = -k"
    MATCH (m:Mechanism)-[:COMPOSED_OF]->(c)
    RETURN m.Mechanism.name, ca.formula
''')
```

## 使用编译器

### 加载数据

```python
import json
from amt_compiler import AMTCompiler

# 加载 Mechanism 数据
mechanism_rows = c.execute('''
    MATCH (v:Mechanism) 
    WHERE NOT v.Mechanism.amt_id STARTS WITH "SM_" 
    RETURN v.Mechanism.amt_id, v.Mechanism.name, v.Mechanism.secp, 
           v.Mechanism.cause_id, v.Mechanism.effect_id
''')

# 加载 Cause 数据
cause_rows = c.execute('''
    MATCH (v:AMT_Cause) 
    RETURN v.AMT_Cause.cause_id, v.AMT_Cause.entity_id, v.AMT_Cause.attribute
''')

# 加载 Effect 数据
effect_rows = c.execute('''
    MATCH (v:AMT_Effect) 
    RETURN v.AMT_Effect.effect_id, v.AMT_Effect.event_name
''')

# 加载 CAUSAL 数据
causal_rows = c.execute('''
    MATCH (c:AMT_Cause)-[e:CAUSAL]->(f:AMT_Effect) 
    RETURN c.AMT_Cause.cause_id, e.formula, e.config, e.process
''')
```

### 组装数据

```python
# 转换为编译器格式
mechanisms = []
for r in mechanism_rows:
    amt_id = r['v.Mechanism.amt_id']
    cause_id = r.get('v.Mechanism.cause_id', '')
    effect_id = r.get('v.Mechanism.effect_id', '')
    
    # 获取关联数据
    cause = next((c for c in cause_rows if c['v.AMT_Cause.cause_id'] == cause_id), {})
    effect = next((e for e in effect_rows if e['v.AMT_Effect.effect_id'] == effect_id), {})
    causal = next((ca for ca in causal_rows if ca['c.AMT_Cause.cause_id'] == cause_id), {})
    
    mechanism = {
        'amt_id': amt_id,
        'name': r['v.Mechanism.name'],
        'S': {'subject': cause.get('v.AMT_Cause.entity_id', ''), 
              'attributes': [cause.get('v.AMT_Cause.attribute', '')]},
        'E': [effect.get('v.AMT_Effect.event_name', '')],
        'C': json.loads(causal.get('e.config', '{}') or '{}'),
        'P': json.loads(causal.get('e.process', '[]') or '[]'),
        'formula': causal.get('e.formula', ''),
    }
    mechanisms.append(mechanism)
```

### 运行编译

```python
compiler = AMTCompiler(use_formula=True)

scenario = {
    'goal': '预测缩孔风险',
    'domain': 'die_casting',
    'S': {'subject': '压铸件', 'attributes': ['缩孔体积', '凝固分数']},
    'E': ['缩孔形成', '凝固收缩'],
    'C': {'浇注温度': '680-720°C'},
    'P': ['高速充填', '增压凝固'],
    'signals': ['浇注温度', '保压压力', '模具温度'],
}

result = compiler.compile(
    goal='预测缩孔风险',
    scenario=scenario,
    mechanisms=mechanisms,
    threshold=0.3
)

# 输出结果
for mech, scores in zip(result['recommended_mechanisms'], result['scores']):
    print(f"{mech['name']}: {scores['total']:.2f}")
```

## 数据统计

```python
# 查询各类型节点数量
tags = ['Mechanism', 'AMT_Cause', 'AMT_Effect', 'Entity', 'State']
for tag in tags:
    rows = c.execute(f'MATCH (v:{tag}) RETURN count(v) AS cnt')
    print(f"{tag}: {rows[0].get('cnt', 0)}")

# 查询各类型边数量
edges = ['CAUSAL', 'COMPOSED_OF', 'BELONGS_TO', 'NEXT_STEP']
for edge in edges:
    rows = c.execute(f'MATCH ()-[e:{edge}]->() RETURN count(e) AS cnt')
    print(f"{edge}: {rows[0].get('cnt', 0)}")
```

## 常见问题

### Q: 查询报错 "IndexNotFound"

A: NebulaGraph 对 WHERE 子句中的属性查询需要索引。解决方案：
1. 创建索引: `CREATE TAG INDEX idx_xxx ON Mechanism(amt_id)`
2. 或使用全量加载后在内存中过滤

### Q: 如何添加新的 Mechanism？

A: 按以下步骤：
1. INSERT VERTEX 到 Mechanism 标签
2. INSERT VERTEX 到 AMT_Cause 标签
3. INSERT VERTEX 到 AMT_Effect 标签
4. INSERT EDGE 到 CAUSAL 边
5. INSERT EDGE 到 COMPOSED_OF 边 (2条)

### Q: 如何验证数据一致性？

A: 运行 `verify_consistency_v2.py` 脚本，检查 SECP 与 Cause/Effect 数据是否一致。
