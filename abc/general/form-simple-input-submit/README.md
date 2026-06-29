# 简单输入表单 ABC

> `form-simple-input-submit` · category: `form` · industry: `general`

一个最小可运行的表单 Module：标题 + 输入框 + 提交/取消按钮，对外暴露输入值与提交/取消事件。作为 **AMT2ABC 仓库的第一个标杆范例**，演示完整的脱敏与入库流程。

## 接口契约

### Inputs

| 名称 | 类型 | 说明 | 默认值 |
|------|------|------|--------|
| `title` | string | 表单标题文字 | `请输入信息` |
| `placeholder` | string | 输入框占位符 | `在此输入...` |
| `defaultValue` | string | 输入框默认值 | `""` |

### Outputs

| 名称 | 类型 | 说明 |
|------|------|------|
| `inputValue` | string | 当前输入框的值（提交后更新） |
| `isSubmitted` | boolean | 是否已点击提交 |

### Methods

| 名称 | 说明 |
|------|------|
| `clear()` | 清空输入框并重置提交状态 |

### Events

| 名称 | 说明 |
|------|------|
| `onSubmit` | 点击提交按钮时触发（`inputValue` 已更新） |
| `onCancel` | 点击取消按钮时触发 |

## 脱敏记录

本 ABC 已完成脱敏（`amt2abc.sanitized = true`），处理项：

| 检查点 | 原始值 | 脱敏后 | 依据 |
|--------|--------|--------|------|
| `applicationInfo.name` | `test1` | `simple-input-form` | 5.2 语义化命名 |
| `applicationInfo.id` | `6a3a1884a4c46a7c40616a75` | `000000000000000000000000` | 5.2 重新生成，去除内部库关联 |
| `applicationInfo.createAt` | `1749000000000` | `0` | 去除时间戳痕迹 |
| `applicationInfo.createBy` | `""` | `""`（已为空） | 无敏感信息 |

> 其余字段（`inputs/outputs/methods/event/global/ui/i18n`）经审查均为通用业务内容，无客户、产线、设备、内网地址等敏感信息。

## 用法示例

见 `examples/` 目录：

- `examples/inputs.json` — 一组典型入参
- `examples/outputs.json` — 对应输出

## 来源

内部通用组件（已脱敏）。License: Apache-2.0。
