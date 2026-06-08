# App 设计规范索引

```yaml
metadata:
  applies_to:
    - frontend-mobile/**
    - touch-client/**
    - mobile-client/**
    - mobile/**
    - design-system/**
  trigger_keywords:
    - app design
    - mobile layout
    - touch interaction
    - safe area
    - accessibility
    - examples
    - App 设计
    - 移动端布局
    - 触控交互
    - 安全区域
    - 无障碍
    - 示例
  must_load_with:
    - {{RULERS_DIR}}/AGENTS.md
    - {{RULERS_DIR}}/core/HARD_CONSTRAINTS.md
    - {{RULERS_DIR}}/frontend/app/INDEX.md
    - {{RULERS_DIR}}/frontend/common/DESIGN_TOKENS.md
```

---

## 1. 必需文档

移动端布局、触控交互、安全区域、主题和无障碍工作需加载这些规则：

- [{{RULERS_DIR}}/frontend/app/design/TOKENS.md]({{RULERS_DIR}}/frontend/app/design/TOKENS.md)
- [{{RULERS_DIR}}/frontend/app/design/LAYOUT.md]({{RULERS_DIR}}/frontend/app/design/LAYOUT.md)
- [{{RULERS_DIR}}/frontend/app/design/COMPONENTS.md]({{RULERS_DIR}}/frontend/app/design/COMPONENTS.md)
- [{{RULERS_DIR}}/frontend/app/design/INTERACTION.md]({{RULERS_DIR}}/frontend/app/design/INTERACTION.md)
- [{{RULERS_DIR}}/frontend/app/design/ACCESSIBILITY.md]({{RULERS_DIR}}/frontend/app/design/ACCESSIBILITY.md)
- [{{RULERS_DIR}}/frontend/app/design/EXAMPLES.md]({{RULERS_DIR}}/frontend/app/design/EXAMPLES.md)

---

## 2. 范围

设计规则治理移动端 token 适配、布局、可复用组件、交互、无障碍和非权威示例。仅实施相关的关注点通过 [{{RULERS_DIR}}/frontend/app/develop/INDEX.md]({{RULERS_DIR}}/frontend/app/develop/INDEX.md) 路由。

---

## 3. AI_FILL 指引

使用 `PROJECT_PROFILE.md` 填写移动端设计来源、token 名称、安全区域约定、组件模式、交互标准、无障碍标准、设备类别和视觉 QA 流程。
