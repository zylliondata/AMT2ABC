# 贡献 ABC 快速指南

> 没用过 GitHub 也没关系，照着这篇一步步来就行。

## 你要做什么

把一个你做的 ABC（脱敏后）提交到开源仓库。**一共 4 步**。

---

## 第 1 步：导出 ABC

在平台里把 ABC 导出成一个 `.json` 文件。

> 导出后先别急着提交，先做第 2 步。

## 第 2 步：检查有没有敏感信息（最重要）

打开 JSON 文件，搜索下面这些词，**有的话必须改掉或删掉**：

| 找什么 | 改成 |
|--------|------|
| 客户名、公司名（如"某某汽车"） | `CustomerA` |
| 设备型号、品牌 | `Machine` / `Device` |
| IP 地址、内网地址（如 `10.x.x.x`） | `<endpoint>` |
| 真实字段名（如 `dp1_temp_zk01`） | 语义化名字，如 `temperature` |
| 真实人名、地名 | 删掉 |

> [!tip] 不确定就先交
> 你只要"尽量别放敏感信息"。**最终把关由维护者负责**，发现问题会打回来让你改，不会出事。

## 第 3 步：在最前面加一段 `amt2abc` 头

用编辑器打开你的 JSON，在**最外层的 `{` 后面**插入下面这段（改成你的信息）：

```json
{
  "amt2abc": {
    "id": "form-simple-input-submit",
    "name": "简单输入表单 ABC",
    "industry": "general",
    "category": "form",
    "author": "你的名字或团队",
    "sanitized": true
  },

  ... 这里是你原来的内容 ...
}
```

**字段怎么填：**

| 字段 | 填什么 | 例子 |
|------|--------|------|
| `id` | 用英文，`类型-功能` 格式，别用中文别有空格 | `form-simple-input-submit` |
| `name` | 中文名，随便起 | `简单输入表单 ABC` |
| `industry` | 行业；通用的填 `general` | `die-casting` / `general` |
| `category` | 类型 | `form` / `monitoring` / `control` |
| `author` | 你的署名 | `zylliondata` |
| `sanitized` | 你自查过了就填 `true` | `true` |

> [!warning] 逗号别漏
> `amt2abc` 这段结束后**必须有一个逗号**，否则 JSON 会报错。看上面的例子，`}` 后面有个 `,`。

## 第 4 步：提交 PR（Pull Request）

> [!info] 完全没用过 GitHub？
> 先看最后一节「**新手：GitHub 三步速成**」，注册个账号再回来。

1. 在 GitHub 上打开仓库网页版，点 `Add file` → `Create new file`
2. 文件名填：`abc/general/<你的id>/abc.json`（比如 `abc/general/form-simple-input-submit/abc.json`）
3. 把你的 JSON 内容粘进去
4. 拉到最下面，点 `Propose new file` → `Create pull request`
5. 等维护者审核。如果让你改，按提示改就行。

完事。

---

## 新手：GitHub 三步速成

> 只学够交 ABC 用的，3 分钟看完。

**① 注册账号**
访问 [github.com](https://github.com) → `Sign up` → 填邮箱密码。

**② Fork 仓库**
打开仓库页面 → 右上角点 `Fork` → `Create fork`。这等于把仓库复制一份到你自己的账号下。

**③ 改文件 + 提 PR**
在自己 fork 的页面点 `Add file` → `Create new file` → 填路径、粘内容 → 点两次绿色按钮提交 PR。

> 维护者合并后，你的 ABC 就出现在开源仓库里了。

---

## 遇到问题

- JSON 报错？多半是**逗号**漏了或多了一处，检查 `amt2abc` 段前后的逗号。
- 不知道 `industry` / `category` 填啥？通用的都填 `general` / `form`，维护者会帮你调。
- 其他问题：直接问维护者，或提一个 [Issue](https://github.com/zylliondata/AMT2ABC/issues)。

---

## 提完 PR 之后怎么办

维护者会审核你的 PR。**核心一句话：让你改就在原来的分支上改，PR 会自动更新，不要新开 PR。**

### 维护者的反馈 → 你要做什么

| 维护者说 | 你做什么 |
|----------|----------|
| "脱敏漏了一处，把 XX 改掉" | 改那处 → 提交到**原分支** → PR 自动更新 |
| "字段名不够语义化" | 改字段 → 提交到**原分支** |
| "格式/逗号错了" | 修好 → 提交到**原分支** |
| "OK，合并了" | 不用做事，完事 |

### 怎么"提交到原分支"

**方式 A：网页改（新手推荐）**

1. 打开你的 PR 页面，点进文件
2. 点右上角 ✏️ 铅笔图标编辑
3. 改完点 `Commit changes`
4. **分支名选你提 PR 的那个**（别选 `main`）
5. 回到 PR 页面，会看到"已更新"

**方式 B：git 命令（会用 git 的人）**

```bash
git checkout 你提PR的那个分支
# 改文件
git add .
git commit -m "fix: 按审核意见修改"
git push
```

push 完 PR 自动更新。

### 三条心智模型

1. **PR 绑定的是分支** —— 往那个分支 push 新提交，PR 就更新
2. **永远不要新开 PR** 改同一个 ABC，一直在原来那个 PR 上改
3. **改完不用通知维护者** —— PR 更新他们会自动收到提醒

来回改几次很正常，改到维护者满意就合并，你的 ABC 就进开源仓库了。
