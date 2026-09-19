# 看板卡查询 ABC

> `kanban-card-query` · category: `form` · industry: `general`

看板卡查询 Module:提供筛选区(ID、物料、消耗库位、供应商、启用状态)+ 查询/重置按钮 + 分页表格,支持行选中事件。属于纯查询能力,不含写操作。

## 接口契约

### Inputs

| 名称 | 类型 | 说明 | 默认值 |
|------|------|------|--------|
| `resourceId` | string | 资源 ID,由宿主/平台注入 | `""` |
| `pageSize` | string | 每页条数 | `"20"` |
| `readonly` | string | 是否只读 | `"false"` |

### Outputs

| 名称 | 类型 | 说明 |
|------|------|------|
| `result` | array | 看板卡列表 |
| `total` | number | 总条数 |
| `selectedRow` | object | 当前选中看板卡 |
| `pageNumber` | number | 当前页码 |

### Methods

| 名称 | 说明 |
|------|------|
| `search()` | 执行查询 |
| `reset()` | 重置筛选 |

### Events

| 名称 | 说明 |
|------|------|
| `onSearchDone` | 查询完成 |
| `onSelect` | 用户选中一张看板卡 |
| `onError` | 查询失败 |

## 运行时参数说明

> 本 ABC 依赖宿主/平台注入的运行时参数,使用前请确认:

- **`resourceId`**:由宿主在挂载时注入。未注入时,挂载后不会自动查询,需用户手动点击查询按钮。
- **HTTP 通道**:数据请求通过平台 `presetRestApi` 通道发出,鉴权头由平台运行时注入,ABC 内不含任何凭证值。
- **`bodyParams.table`**:请求体中的 `table` 字段(值为 `oet_kanban_cards`)是数据表的结构性 key,不携带敏感数据。

## 脱敏记录

本 ABC 已完成脱敏(`amt2abc.sanitized = true`),处理项:

| 检查点 | 原始值 | 脱敏后 |
|--------|--------|--------|
| `applicationInfo.id` | `6a72a5f0...`(24 位内部库 id) | `000000000000000000000000` |
| `applicationInfo.name` | `abc_kanban_card_query` | `kanban-card-query` |
| `applicationInfo.publicToAll` / `publicToMarketplace` | `true` / `true` | `false` / `false` |
| `inputs.resourceId.testValue` | `resource_d93bd8ab-...`(真实资源 UUID) | `""` |
| `js_kbAutoSearch` 脚本 | 内部 API fetch(`/api/fabric/resource/info`、内部系统名、内部 cookie 名) | 精简为仅按注入的 `resourceId` 自动查询 |
| `setting.category` | `SGNE, Inventory`(含内部业务编码) | `Inventory` |
| `i18n.messages` | `ioap.*` / `$system.*` 冗余翻译 key | 已删除 |

> 其余字段(`inputs/outputs/methods/event/global/ui/preload`)经审查均为通用查询逻辑,无客户、产线、设备、内网地址等敏感信息。

## 用法示例

见 `examples/` 目录:

- `examples/inputs.json` — 一组典型入参
- `examples/outputs.json` — 对应输出

## 来源

内部通用组件(已脱敏)。License: Apache-2.0。
