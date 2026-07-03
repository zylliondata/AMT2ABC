# 查询 CAPA 列表/详情 ABC

> `query-capa-list-details` · category: `form` · industry: `general`

CAPA 查询的 Module：可根据ID、状态和责任人筛选 + 以列表展示查询数据，选中列表行数据后，展示选中行 CAPA 的详细信息，对外暴露行点击事件，输出选中行数据，使用时需确保已登录。

## 接口契约

### Inputs

| 名称 | 类型 | 是否必填 | 说明 | 默认值 |
|------|------|------|------|--------|
| `resourceId` | string | 是 | 资源ID | `""` |
| `assigneeId` | string | 否 | 分配的责任人ID（输入值后，责任人变为默认查询条件） | `""` |

### Outputs

| 名称 | 类型 | 说明 |
|------|------|------|
| `values` | object | 列表选中行数据 |

### Methods

| 名称 | 说明 |
|------|------|


### Events

| 名称 | 说明 |
|------|------|
| `rowClick` | 行点击（选中表格行数据时触发） |


## 脱敏记录

本 ABC 已完成脱敏（`amt2abc.sanitized = true`），处理项：

| 检查点 | 原始值 | 脱敏后 | 依据 |
|--------|--------|--------|------|


> 其余字段（`inputs/outputs/methods/event/global/ui/i18n`）经审查均为通用业务内容，无客户、产线、设备、内网地址等敏感信息。

## 用法示例

见 `examples/` 目录：

- `examples/inputs.json` — 入参样例
- `examples/outputs.json` — 输出样例

## 来源

内部通用组件（已脱敏）。License: Apache-2.0。
