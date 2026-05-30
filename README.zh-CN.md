<div align="center">

# AI-First CLI

### 一套面向「AI Agent 而非人类」为首要使用者的命令行工具设计哲学。

[English](./README.md) · **简体中文**

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](./LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](./CONTRIBUTING.md)
[![Claude Skill](https://img.shields.io/badge/Claude-Skill-d97757.svg)](./skill/ai-first-cli)
[![Validate](https://github.com/yzfly/ai-first-cli/actions/workflows/validate.yml/badge.svg)](https://github.com/yzfly/ai-first-cli/actions/workflows/validate.yml)
[![Stars](https://img.shields.io/github/stars/yzfly/ai-first-cli?style=social)](https://github.com/yzfly/ai-first-cli/stargazers)

*12 条原则 · 一份 Vercel 案例 · 一张可直接套用的审查清单 · 一个开箱即装的 Claude skill。*

</div>

---

> **CLI 的首要读者，正从人变成 agent。**
> 过去三十年，我们为「会读报错、会敲 `--help`、会手动调试」的人设计命令行工具。agent 这些都不擅长。**AI-First CLI** 就是把「机器可调用、可预测、可解析」当成主路径的设计纪律——同时不丢掉人的那条路。

一句话判据：

> **agent 读完一条命令的输出，应当确切知道下一步做什么——不用猜、不用幻觉命令、不用卡住。**

这**不是**「给旧 CLI 加个 `--json`」。而是把每个接口里隐含的人类假设——调用者会读散文报错、会交互式调试、会读外部文档——**整个倒过来**，为「这些都不做」的调用者重做接口。

## 目录

- [为什么需要它](#为什么需要它)
- [12 条原则](#12-条原则)
- [一个例子：散文报错 vs 可执行报错](#一个例子散文报错-vs-可执行报错)
- [CLI vs MCP——该做哪个](#cli-vs-mcp该做哪个)
- [案例：Vercel 如何把它推到极致](#案例vercel-如何把它推到极致)
- [作为 Claude skill 使用](#作为-claude-skill-使用)
- [自检清单](#自检清单)
- [文档](#文档)
- [贡献](#贡献)
- [许可证](#许可证)
- [引用](#引用)
- [作者](#作者)

## 为什么需要它

Claude Code、OpenClaw 以及形形色色的 coding agent，每天调用 CLI 数以百万次。Vercel CEO Guillermo Rauch 把 CLI 称为「cloud for agents」的关键嵌入接口。当调用者是模型，旧的设计默认就开始**主动伤害**你：交互式提示让 headless 运行卡死，彩色表格污染管道，散文报错既费 token 又诱发幻觉修复。

本项目从 **Vercel 一方方法论** + 独立实践者来源中提炼，并经对抗式交叉验证，梳理出「agent-first」在工程上到底意味着什么。每条原则都有出处，见 [`docs/sources.md`](./docs/sources.md)（含诚实的偏差声明）。

## 12 条原则

| # | 原则 | 一句话 |
|---|------|--------|
| 1 | **机器输出是默认，不是选项** | 非 TTY 给结构化信封；漂亮输出只留给终端前的人 |
| 2 | **stdout / stderr 分流** | 数据走 stdout，诊断/日志/错误走 stderr，管道才干净 |
| 3 | **接收原始 payload** | 直接收与 API schema 同构的 JSON，LLM 零翻译损失 |
| 4 | **错误要可执行** | 退出码 + 稳定错误码 + message + 修复命令 + 是否可重试 |
| 5 | **自描述、可发现** | `--help`、schema introspection、`explain CODE`；CLI 是「此刻 API 接受什么」的唯一真相源 |
| 6 | **默认非交互** | 每个提示都有 flag 旁路；env var 认证，绝不走浏览器登录 |
| 7 | **零依赖、自包含** | 单一签名二进制：快启动、可信、沙箱里无依赖链惊喜 |
| 8 | **可组合（Unix）** | 可 pipe、读 stdin、NDJSON 流式分页 |
| 9 | **自治护栏** | `--dry-run`、幂等键、输入加固、响应净化防注入 |
| 10 | **省 token** | 字段裁剪、分页、简洁输出，别撑爆上下文窗口 |
| 11 | **确定性优先** | 稳定输出契约 + 版本化 schema，agent 要可预测胜过聪明 |
| 12 | **一核多面** | CLI / MCP / SDK / env var 共享同一能力核心 |

完整展开、do/don't 与边界情况见 **[`docs/principles.md`](./docs/principles.md)**。

## 一个例子：散文报错 vs 可执行报错

```diff
- Error: something went wrong
- (exit 1)
```

```json
{
  "ok": false,
  "error": {
    "code": "AUTH_004",
    "message": "Token expired",
    "fix": "run `tool auth login`",
    "retryable": false
  }
}
```

错误**码稳定**，agent 靠 `AUTH_004` 精确匹配而非解析英文；`tool explain AUTH_004` 再给结构化解释——agent 永远不用去爬外部文档。

## CLI vs MCP——该做哪个

| 维度 | 做好一个 CLI | 写专用 MCP server |
|------|-------------|------------------|
| 集成成本 | 零——agent 直接 shell out | 每个集成建一个 server |
| 可组合 | Unix pipe 天然 | 协议内组合较弱 |
| 发现 | `--help` 自带 | 需 schema 定义 |
| 权限/审计 | 复用系统权限 + shell history | 另建 |
| 何时选 MCP | 需要持久连接、结构化双向流、富类型协商时 |

**经验法则**：先把 CLI 做成 agent-first，多数场景就够了；MCP 留给真正有状态的协议。「一核多面」（原则 12）让两者共享同一底座。

## 案例：Vercel 如何把它推到极致

Vercel 围绕 agent 重构了它的整个表面，是这套哲学最完整的现实落地——完整、带来源验证的版本见 **[`docs/vercel-case-study.md`](./docs/vercel-case-study.md)**。要点：

- **CLI → 零依赖、自更新、代码签名的原生二进制**：无 Node 运行时、快启动、OS 可验证来源——正是原则 7。
- **Docker in Vercel Sandbox**，跑在 **trust-domain microVM** 上，而非共享内核的容器。被低估的论点：*agent 生成的代码默认不可信*，所以隔离要做到 VM 级（原则 9 的极限）。
- **一核多面**：CLI、API、MCP server、git 都被定位为 agent 接口；Vercel MCP 是 OAuth 合规 server；AI SDK 6 把 `Agent` 从类重定义为*接口*；`mcp-to-ai-sdk` 把动态 MCP 编译成版本化静态工具（原则 5 + 11 的工程化）。
- **Zero** 语言：Vercel Labs 的系统语言，编译器吐带稳定码与 typed repair 的 JSON 诊断——把这套哲学一路贯彻到语言本身。

> ⚠️ 该案例几乎全部基于 Vercel 一方来源，并附明确偏差声明；其中一条营销话术（「单 API 克隆百万 agent」）已被对抗式验证**驳回**并标注。

## 作为 Claude skill 使用

本方法论以可安装的 [Claude Code](https://claude.com/claude-code) skill 形式交付，agent 在你设计或评审 CLI 时会自动套用这些原则。

```bash
# 安装到 Claude Code
git clone git@github.com:yzfly/ai-first-cli.git
cp -r ai-first-cli/skill/ai-first-cli ~/.claude/skills/
```

当你在为命令行工具决定输出格式、错误处理、flag、打包或自治安全时，skill 会自动触发。源码：[`skill/ai-first-cli`](./skill/ai-first-cli)。

## 自检清单

可直接用于任何 CLI 评审。带说明的完整版见 **[`docs/checklist.md`](./docs/checklist.md)**。

- [ ] 非 TTY 下默认结构化输出？`--json` 存在？
- [ ] 数据→stdout，日志/错误→stderr？
- [ ] 失败退出码非 0，且带 `code` + `message` + `fix` + `retryable`？
- [ ] 错误码稳定且有 `explain`？
- [ ] 每个交互提示都有 flag 旁路？env var 认证？
- [ ] 变更操作有 `--dry-run` / 幂等？
- [ ] 输入对路径穿越、控制字符、注入做了加固？
- [ ] 输出契约稳定、版本化、省 token？
- [ ] `--help` / schema 自描述完整？
- [ ] 打包尽量零依赖、可信？

## 文档

| 文档 | 内容 |
|------|------|
| [`docs/principles.md`](./docs/principles.md) | 12 原则深度展开 + do/don't |
| [`docs/vercel-case-study.md`](./docs/vercel-case-study.md) | 来源验证的 Vercel 方法论 + 偏差声明 |
| [`docs/checklist.md`](./docs/checklist.md) | 完整自检清单 |
| [`docs/sources.md`](./docs/sources.md) | 全部来源，含置信度与偏差说明 |
| [`skill/ai-first-cli`](./skill/ai-first-cli) | 可安装的 Claude skill（中文，agent 优化版） |

## 贡献

热忱欢迎贡献——一条更锋利的原则、一个反例、一个新案例、一份翻译。请先读 **[CONTRIBUTING.md](./CONTRIBUTING.md)** 与 **[行为准则](./CODE_OF_CONDUCT.md)**。提出或挑战某条原则，请用 *Principle proposal* issue 模板。

## 许可证

[**Creative Commons Attribution 4.0 International (CC BY 4.0)**](./LICENSE) —— 任意使用（含商用），署名即可。

## 引用

若本作品启发了你的工具或写作，请引用（见 [`CITATION.cff`](./CITATION.cff)）：

```
云中江树 (yzfly). AI-First CLI: A design philosophy for command-line tools whose
primary user is an AI agent. 2026. https://github.com/yzfly/ai-first-cli
```

## 作者

**云中江树** · 微信公众号：**云中江树** · GitHub：[@yzfly](https://github.com/yzfly)

<div align="center">

如果它让你重新理解了面向 agent 的工具，欢迎点一颗 ⭐。

</div>
