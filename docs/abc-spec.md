# ABC 完整规范

> 状态：正式
> 受众：维护者（审阅 PR 的依据）、进阶贡献者
> 普通贡献者只需阅读 [`contribute-abc-quickstart.md`](./contribute-abc-quickstart.md)。

本文是审阅 ABC PR 的**标尺**：一个 ABC 是否合格、能否入库，逐项对照下表即可判定。配合 [`desensitization-guide.md`](./desensitization-guide.md)（脱敏）和 [`pr-review-sop.md`](./pr-review-sop.md)（审阅流程）使用。

## 1. 文件结构

一个 ABC 是一个目录，路径遵循 `abc/<industry>/<id>/`：

```text
abc/<industry>/<id>/
  ├── abc.json          # 必备：脱敏后的 ABC（amt2abc 头 + 原始 DSL）
  ├── README.md         # 必备：能力说明 + 接口契约 + 脱敏记录
  └── examples/         # 可选：输入/输出示例
      ├── inputs.json
      └── outputs.json
```

| 项 | 必备 | 说明 |
|----|------|------|
| `abc.json` | ✅ | ABC 主体，结构见第 2 节 |
| `README.md` | ✅ | 接口契约（inputs/outputs/methods/events）+ 脱敏记录 |
| `examples/` | 可选 | 典型入参与对应输出，方便复用者验证 |

## 2. abc.json 三层结构

```text
abc.json = {
  "amt2abc": { ... },          ← 贡献元信息（第 3 节，贡献者填）
  "applicationInfo": { ... },  ← 模块元数据（第 4 节，须脱敏）
  "applicationDSL": { ... }    ← 可运行定义（第 5 节，重点审查）
}
```

> 三个顶层 key 顺序固定：`amt2abc` → `applicationInfo` → `applicationDSL`。`amt2abc` 必须在最外层。

## 3. `amt2abc` 头（贡献者必填）

| 字段 | 必填 | 类型 | 规则 | 示例 |
|------|------|------|------|------|
| `id` | ✅ | string | 全局唯一；`<category>-<slug>`；全小写、连字符分隔；无空格无中文 | `form-simple-input-submit` |
| `name` | ✅ | string | 中文名，人类可读 | `简单输入表单 ABC` |
| `industry` | ✅ | string | 行业/产线；通用组件填 `general` | `die-casting` / `general` |
| `category` | ✅ | string | 能力类型，取值见 3.1 | `form` |
| `author` | ✅ | string | 署名（团队或个人） | `zylliondata` |
| `sanitized` | ✅ | boolean | 自查脱敏完毕填 `true` | `true` |

### 3.1 `category` 允许取值

| 取值 | 含义 | 典型 |
|------|------|------|
| `form` | 表单、输入、交互界面 | 输入表单、配置面板 |
| `monitoring` | 监控、数据展示 | 仪表盘、趋势图 |
| `control` | 控制、指令下发 | 设备启停、参数下发 |
| `general` | 通用 UI/工具 | 与 `industry=general` 搭配 |

> 新增 category 需维护者评审，贡献者不得自造。

### 3.2 `id` 命名规则

- 格式：`<category>-<语义 slug>`
- slug 部分：小写英文 + 连字符，语义化描述能力，**不要**含设备型号、客户名、内部编号
- ✅ `form-simple-input-submit`、`monitoring-furnace-temperature`
- ❌ `form1`、`test`、`dp1_zk01`、`customerA-form`

## 4. `applicationInfo`（模块元数据，**必须脱敏**）

| 字段 | 处理要求 |
|------|----------|
| `name` | 语义化，去除内部模块名痕迹（如 `test1` → `simple-input-form`） |
| `type` | 保留原值（通常 `module`） |
| `id` | **必须**替换为 `000000000000000000000000`（24 位 0），去除与内部库的关联 |
| `createBy` | 清空为 `""` |
| `createAt` | **必须**置为 `0`，去除时间戳痕迹 |
| `publicToAll` / `publicToMarketplace` | 保留 `false` |

## 5. `applicationDSL`（可运行定义，**审阅重点**）

以下子节点是脱敏与规范的审查重点（详见 [`desensitization-guide.md`](./desensitization-guide.md)）：

| 子节点 | 说明 | 审查点 |
|--------|------|--------|
| `inputs` | 模块入参 | 字段名是否语义化；默认值无敏感数据 |
| `outputs` | 模块出参 | 字段名语义化；无内部字段名泄露 |
| `methods` | 可调用方法 | 方法名/参数无内部接口痕迹 |
| `event.list` | 暴露事件 | 事件名规范；描述无业务机密 |
| `global` | 临时状态变量 | 初始值无敏感内容 |
| `ui` | 界面组件树 | 占位符/文案/标题无客户、设备、人名 |
| `i18n.messages` | 国际化文案 | 中英文均需脱敏审查 |
| `preload` | 预加载脚本 | **重点**：script/style 不得引用内网 URL、IP |
| `canvasSetting` | 画布设置 | 无敏感背景/配置 |
| `setting` | 模块设置 | description 无敏感描述 |

> 任何疑似客户名、IP、内网地址、真实字段名、真实人名/地名，一律视为泄露风险。

## 6. 校验清单（审阅时逐项打勾）

提交前自查、审阅时复核，同一张表：

- [ ] 路径为 `abc/<industry>/<id>/abc.json`
- [ ] `abc.json` 是合法 JSON
- [ ] `amt2abc` 6 字段齐全且符合第 3 节规则
- [ ] `id` 全局唯一，命名规范（3.2）
- [ ] `applicationInfo` 已按第 4 节脱敏
- [ ] `applicationDSL` 各子节点按第 5 节审查通过
- [ ] 配备 `README.md`（接口契约 + 脱敏记录）
- [ ] 脱敏自查 `sanitized = true` 且经得起复核

## 7. 相关

- [`desensitization-guide.md`](./desensitization-guide.md) — 脱敏红线与逐字段审查
- [`pr-review-sop.md`](./pr-review-sop.md) — PR 审阅流程与自动合并边界
- [`contribute-abc-quickstart.md`](./contribute-abc-quickstart.md) — 贡献者快速指南
- [`proposal-abc-pipeline.md`](./proposal-abc-pipeline.md) — 流水线总方案
