# 简单输入表单 ABC

> `create-edit-capa-events` · category: `form` · industry: `general`

创建/编辑 CAPA 事件的 Module：输入表单组件 + 文件上传（常见图片格式、Word文档、表格文件、PDF） + 保存按钮，输入/修改 CAPA 基础信息，对外暴露输入值与保存事件；使用时需确保已登录。

## 接口契约

### Inputs

| 名称 | 类型 | 是否必填 | 说明 | 默认值 |
|------|------|------|------|--------|
| `resourceId` | string | 是 | 资源ID | `""` |
| `capaId` | string | 否 | CAPA ID（默认为创建，输入 CAPA ID 参数后，进入编辑模式） | `""` |
| `sourceRef` | string | 否 | 来源ID（上游事件进入 CAPA 创建时传入） | `""` |

### Outputs

| 名称 | 类型 | 说明 |
|------|------|------|


### Methods

| 名称 | 说明 |
|------|------|


### Events

| 名称 | 说明 |
|------|------|
| `save` | 点击保存按钮时触发 |


## 脱敏记录

本 ABC 已完成脱敏（`amt2abc.sanitized = true`），处理项：

| 检查点 | 原始值 | 脱敏后 | 依据 |
|--------|--------|--------|------|
| https://xxx.com | https://idfp-gateway.data4industry.com | https://xxx.com |  |

> 其余字段（`inputs/outputs/methods/event/global/ui/i18n`）经审查均为通用业务内容，无客户、产线、设备、内网地址等敏感信息。

## 用法示例

见 `examples/` 目录：

- `examples/inputs.json` — 一组典型入参
- `examples/outputs.json` — 对应输出

## 来源

内部通用组件（已脱敏）。License: Apache-2.0。
