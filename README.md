<div align="center">

<img src="logo.png" alt="Rulers Template" width="120">

# 📏 Rulers Template

**通用 AI 开发规范模板 — Progressive AI Coding Standards for AI-Powered Development**

[![Version](https://img.shields.io/badge/version-v1.0.0-blue)](https://github.com/AndersJet/ai-rulers-template/releases)
[![License](https://img.shields.io/badge/license-MIT-green)](./LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen)](https://github.com/AndersJet/ai-rulers-template/pulls)

[![Claude Code](https://img.shields.io/badge/AI-Claude%20Code-d97757)](https://claude.ai)
[![Cursor](https://img.shields.io/badge/AI-Cursor-6c4df5)](https://cursor.sh)
[![GitHub Copilot](https://img.shields.io/badge/AI-GitHub%20Copilot-0288d1)](https://github.com/features/copilot)

[快速开始](#1-快速开始) •
[激活等级](#2-激活等级) •
[初始化流程](#3-初始化详细流程) •
[日常使用](#4-日常使用) •
[目录说明](#6-目录与文件说明)

</div>

---

> [!IMPORTANT]
> 将本模板放入任意项目后，即可为 AI 编码助手（Claude Code、Cursor、Copilot 等）提供渐进加载的规范约束、激活门禁和领域路由，覆盖从项目发现到生产发布的全生命周期。

---

## 1. 快速开始

### 1.1 获取并放置模板

```bash
# 1. 克隆本仓库
git clone <repo-url> ai-rulers-template

# 2. 将仓库根目录放入目标项目的 documents/ 目录下
mv ai-rulers-template /path/to/target-project/documents/
```

放置后目标项目的目录结构：

```text
target-project/
└── documents/
    └── ai-rulers-template/                  # 默认目录名，可重命名
        ├── README.md                           # 本文件
        ├── AGENTS.md                           # AI 协作协议入口
        ├── INDEX.md                            # 模板导航
        ├── PROJECT_PROFILE.template.md         # 项目画像模板
        ├── core/                                # 全局常驻规则
        ├── backend/                             # 后端领域规范
        ├── database/                            # 数据库领域规范
        ├── frontend/                            # 前端领域规范
        │   ├── common/
        │   ├── web/
        │   └── app/
        ├── bootstrap/                           # 引导与生成指南
        └── scripts/
            └── validate_rulers.py               # 结构校验脚本
```

### 1.2 目录重命名确认

在开始初始化前，AI 会首先确认目录名称：

> 当前规范模板目录名为 `ai-rulers-template`，是否需要重命名？（如 `rulers`、`coding-standards` 等）

- **如果保留原名**：直接进入初始化流程。
- **如果需要重命名**：AI 会将目录重命名，并自动替换模板内所有 `{{RULERS_DIR}}` 占位符为实际路径（如 `documents/rulers`），然后进入初始化流程。

### 1.3 初始化流程

```text
确认目录名 → 替换占位符 → 项目发现 → 生成 PROJECT_PROFILE.md → 生成领域规则 → 校验 → 按等级激活
```

| 步骤 | 做什么 | 谁来做 | 产出 |
|------|--------|--------|------|
| 0. 确认目录名 | 询问是否重命名 `ai-rulers-template`，若重命名则替换 `{{RULERS_DIR}}` 占位符 | AI + 人工确认 | 正确的目录名和路径引用 |
| 1. 项目发现 | 指导 AI 扫描仓库结构、技术栈、命令、安全模型等 | AI + 人工确认 | 事实记录 |
| 2. 生成项目画像 | 基于 `PROJECT_PROFILE.template.md` 填入已确认事实 | AI + 人工审阅 | `PROJECT_PROFILE.md` |
| 3. 生成领域规则 | 基于项目画像为每个领域生成专属叶子规则 | AI + 人工审阅 | 各领域 `INDEX.md` + 叶子规则 |
| 4. 校验 | 运行 `validate_rulers.py` 检查结构完整性 | AI/自动化 | 校验通过 |
| 5. 激活 | 按激活等级逐级解锁工作范围 | 人工审阅确认 | 可工作的 AI 规范体系 |

---

## 2. 激活等级

模板采用四级激活门禁，防止未经审阅的规则控制高风险工作：

| Level | 状态 | 允许的工作 | 关键前置条件 |
|-------|------|-----------|-------------|
| **Level 0** | 模板已放入，无项目画像 | 仅项目发现 | — |
| **Level 1** | 项目画像存在且已审阅 | 只读分析、低风险文档、小型本地修复 | `PROJECT_PROFILE.md` 经人工审阅，置信度与未确认事实已标注 |
| **Level 2** | 领域规则已生成并审阅 | 在已激活领域内工作 | 领域规则已生成、已校验、已审阅（高风险领域需审阅人接受记录） |
| **Level 3** | 发布/安全/质量门禁已审阅 | 生产影响工作 | 发布流程、回滚方案、CI/CD 与安全影响已记录并审阅 |

**高风险工作最低要求：**

| 工作类型 | 最低等级 |
|----------|----------|
| 认证/授权/安全敏感变更 | Level 2 |
| 数据库 schema/migration/seed/backfill | Level 2 |
| 外部支付/消息/通知等集成 | Level 2 或 Level 3 |
| 发布/部署/CI/CD 变更 | Level 3 |

---

## 3. 初始化详细流程

### 3.1 第一步：项目发现（Level 0）

在 AI 编码助手中打开项目，给出以下指令：

> 加载 `documents/ai-rulers-template/AGENTS.md` 和 `documents/ai-rulers-template/bootstrap/PROJECT_DISCOVERY.md`。当前处于 Level 0，请执行项目发现，扫描仓库结构、技术栈、命令、安全模型、持久化方案、API 契约、前端平台、CI/CD 流程和高风险区域。将发现结果整理为事实列表，区分已确认事实和未确认事实。

AI 会扫描并报告以下九个维度的发现结果：

1. 仓库形态与模块边界
2. 技术栈与版本来源
3. 命令与工作区目录
4. 安全模型
5. 持久化与 migration 模型
6. API 契约与外部集成
7. 前端平台与设计系统
8. CI/CD、部署、发布与回滚
9. 高风险区域与人工审阅要求

### 3.2 第二步：生成项目画像（Level 0 → Level 1）

> 基于 `documents/ai-rulers-template/PROJECT_PROFILE.template.md` 和上一轮的发现结果，生成 `PROJECT_PROFILE.md`。已确认事实填入对应章节并标注证据来源；未确认事实填入第 12 节并说明需要谁确认。不要编造任何事实。

生成后需要人工审阅：

- 逐项检查已确认事实是否准确
- 补充未确认事实
- 确认各领域的激活状态建议是否合理
- 审阅通过后，项目进入 **Level 1**

### 3.3 第三步：生成领域规则（Level 1 → Level 2）

对于项目中实际存在的每个领域，逐领域生成规则。以 backend 为例：

> 加载 `documents/ai-rulers-template/bootstrap/BROWNFIELD_RULE_GENERATION.md`。基于 `PROJECT_PROFILE.md` 为 backend 领域生成专属规则：更新 `AGENTS.md` 路由、生成 `backend/INDEX.md` 和必要的叶子规则。删除不适用于本项目的模板示例。

每个领域的生成结果必须经过人工审阅：

- 规则是否与项目实际技术栈匹配
- 验证命令是否正确
- 约束强度是否合理
- 高风险领域的审阅人必须明确接受

重复此流程处理 database、frontend/common、frontend/web、frontend/app 等所有存在的领域。每完成一个领域并审阅通过后，该领域进入 **Level 2**。

### 3.4 第四步：激活发布级别（Level 2 → Level 3）

当需要执行生产部署、发布或 CI/CD 变更时：

> 基于 `PROJECT_PROFILE.md` 中记录的 CI/CD、部署和发布事实，生成 release 领域规则，包括回滚流程、质量门禁和生产数据安全要求。审阅通过后激活 Level 3。

### 3.5 第五步：维护

规范体系不是一成不变的。当项目技术栈、架构或工作流发生变化时：

> 加载 `documents/ai-rulers-template/core/RULER_MAINTENANCE.md`，执行 ruler impact assessment。

---

## 4. 日常使用

初始化完成后，AI 在每次会话中按以下顺序加载规范：

```text
AGENTS.md → core 常驻规则 → PROJECT_PROFILE.md → 领域 INDEX.md → 命中的叶子规则
```

只需在 AI 指令中引用对应的领域即可，例如：

- 后端接口开发：AI 自动加载 `backend/INDEX.md` 及其叶子规则
- 数据库变更：AI 自动加载 `database/INDEX.md` 及其叶子规则
- 前端页面开发：AI 自动加载 `frontend/INDEX.md` 及对应平台的 develop/design 规则
- 修改规范本身：AI 自动加载 `core/DOC_GOVERNANCE.md` 和 `core/RULER_MAINTENANCE.md`

不需要每次手动列出要加载的文件。

---

## 5. 校验

每次修改规则文件后，运行结构校验确保完整性：

```bash
python3 documents/ai-rulers-template/scripts/validate_rulers.py
```

校验内容：

- Markdown 链接有效性（不指向模板外部）
- 每个权威文档必须包含 `metadata`（applies_to、trigger_keywords、must_load_with）
- `must_load_with` 路径可解析且在模板范围内
- 每个 `INDEX.md` 覆盖了同级目录中的所有叶子文档
- `AGENTS.md` 引用了所有 core 规则
- `ACTIVATION_LEVELS.md` 包含 Level 0-3 定义
- 高风险文档包含 Level 2 或 Level 3 激活语言

---

## 6. 目录与文件说明

### 入口文件

| 文件 | 说明 |
|------|------|
| `AGENTS.md` | AI 协作协议入口，定义渐进加载顺序、激活门禁和任务路由 |
| `INDEX.md` | 模板导航，列出所有领域入口和采用路径 |
| `PROJECT_PROFILE.template.md` | 项目画像模板，初始化的核心产出 |

### core/ — 全局常驻规则

| 文件 | 说明 |
|------|------|
| `HARD_CONSTRAINTS.md` | 全局硬约束：安全、测试、禁令、完成门禁 |
| `WORKFLOW.md` | 实施工作流与推理顺序 |
| `DOC_GOVERNANCE.md` | 规范文档治理规则 |
| `RULER_MAINTENANCE.md` | 规则维护决策树 |
| `GIT_COMMIT_CONVENTION.md` | Git 提交规范（中文 subject，英文 type） |

### backend/ — 后端规范

架构、API 安全、数据访问、配置、可观测性、测试。

### database/ — 数据库规范

Schema 设计、Migration、评审清单、Seed 与 Backfill。

### frontend/ — 前端规范

- `common/`：共享设计 token、样式、无障碍基线
- `web/develop/`：Web 端架构、API 集成、授权、状态管理、测试
- `web/design/`：Web 端视觉系统、组件模式、无障碍
- `app/develop/`：移动端架构、UI 模式、测试
- `app/design/`：移动端 token、布局、组件、交互、无障碍、示例

### bootstrap/ — 引导指南

| 文件 | 说明 |
|------|------|
| `PROJECT_DISCOVERY.md` | 项目发现流程，定义九个发现维度和证据规则 |
| `BROWNFIELD_RULE_GENERATION.md` | 棕地项目规则生成指南，包含模板清理、生成规则、审阅激活 |
| `ACTIVATION_LEVELS.md` | 四级激活门禁的详细定义和晋级标准 |
| `RULES_COMPLETENESS_CHECKLIST.md` | 完整性检查清单，跟踪各领域的生成和审阅状态 |

### scripts/

`validate_rulers.py` — 结构校验脚本。不翻译、不修改，直接使用。

---

## 7. 关键约定

### 必须保护的内容

以下内容在生成项目专属规则时**保持稳定**，不翻译、不重命名、不删除：

- `metadata:` / `applies_to` / `trigger_keywords` / `must_load_with` — 机器可解析元数据键
- `AI_FILL` — 标记需要 AI 根据项目事实填充的章节
- `PROJECT_PROFILE.md` / `PROJECT_PROFILE.template.md` / `AGENTS.md` / `INDEX.md` — 协议文件名
- `Level 0` / `Level 1` / `Level 2` / `Level 3` — 激活等级标识
- `<type>[optional scope]: <subject>` — Conventional Commits 格式

### trigger_keywords 策略

每个规则文件的 `trigger_keywords` 采用中英双语，确保跨模型命中率：

```yaml
trigger_keywords:
  - git
  - commit
  - conventional commits
  - 提交
  - 提交规范
```

### 冲突裁决

```
core 全局硬约束 > 安全规则 > 激活门禁 > 领域规则 > 专题规则 > 示例
```

### 提交规范

- `type` 英文（feat/fix/docs/refactor/test/chore/build/ci）
- `subject` 中文，动宾结构，不以句号结尾
- `body` 中文，说明"改了什么"和"为什么"

---

## 8. 常见问题

### Q: 是否必须使用全部领域？

不需要。如果目标项目没有移动端，删除 `frontend/app/` 并更新 `AGENTS.md` 和 `INDEX.md` 中的路由。完整性检查清单也应相应更新。

### Q: 可以直接在 Level 0 下写代码吗？

不可以。Level 0 只允许项目发现。在 `PROJECT_PROFILE.md` 完成审阅前，禁止功能、架构、安全、数据库、发布或部署变更。

### Q: AI 会自动遵守这些规则吗？

主流 AI 编码助手会读取 `AGENTS.md` 作为入口。渐进加载设计确保 AI 按需加载相关规则，而不是一次性读入全部文档，避免上下文窗口浪费。

### Q: 校验脚本报错怎么办？

按错误提示逐项修复。常见问题包括：链接指向不存在的文件、metadata 缺失、INDEX 遗漏叶子文档等。

### Q: 如何更新已激活的规则？

修改规则前执行 ruler impact assessment（见 `core/RULER_MAINTENANCE.md`）：判断是否需要更新、确定变更层级、选择目标文件、修改后运行校验。

---

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=AndersJet/ai-rulers-template&type=Date)](https://star-history.com/#AndersJet/ai-rulers-template&Date)

---

<div align="center">

### 💖 如果这个项目对你有帮助，欢迎给我们一个 ⭐️ Star！

**[快速开始](#1-快速开始)** • **[初始化流程](#3-初始化详细流程)** • **[提交 Issue](https://github.com/AndersJet/ai-rulers-template/issues)**

Made with ❤️ by [AndersJet](https://github.com/AndersJet)

</div>