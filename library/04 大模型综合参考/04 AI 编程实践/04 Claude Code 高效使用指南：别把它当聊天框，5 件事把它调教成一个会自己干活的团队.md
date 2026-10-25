[书架](../../00%20%E4%B9%A6%E6%9E%B6.md) · [本书目录](../00%20%E7%9B%AE%E5%BD%95.md) · [上一节](03%2040%E4%B8%87%E6%AC%A1Claude%20Code%E4%BC%9A%E8%AF%9D%E6%8F%AD%E7%A4%BA%EF%BC%9A%E7%9C%9F%E6%AD%A3%E6%8B%89%E5%BC%80%E5%B7%AE%E8%B7%9D%E7%9A%84%EF%BC%8C%E4%B8%8D%E6%98%AFPrompt.md) · [下一节](05%20%E6%B7%B1%E5%85%A5%E7%90%86%E8%A7%A3%20Claude%20Code%EF%BC%9A%E4%BB%8E%20CLAUDE.md%20%E5%88%B0%20Hooks%E3%80%81Skills%E3%80%81Subagents.md)

---

# Claude Code 高效使用指南：别把它当聊天框，5 件事把它调教成一个会自己干活的团队

录友们好，今天聊一个用的人多、但用对的人少的工具：**Claude Code**。

我观察了一圈，绝大多数人装好 Claude Code 之后，就把它当成一个「会写代码的聊天框」——打开终端，问一句，答一句，复制粘贴，关掉。

这么用没错，但没发挥他的价值。

Claude Code 真正的价值不在「它能写代码」，而在于：你能把它从一个**每次都得从头解释一遍的临时工**，调教成一个**懂你项目、能自己干活、还能并行开多线程的团队**。这中间差的，就是下面这几件事。

前面我们专门讲过 [CLAUDE.md 到底怎么写](<09%20CLAUDE.md%E5%88%B0%E5%BA%95%E6%80%8E%E4%B9%88%E5%86%99%EF%BC%9FClaude%20Code%E9%A1%B9%E7%9B%AE%E8%AE%B0%E5%BF%86%E3%80%81%E5%9B%A2%E9%98%9F%E8%A7%84%E8%8C%83%E5%92%8C%E4%B8%8A%E4%B8%8B%E6%96%87%E7%AE%A1%E7%90%86%E4%B8%80%E7%AF%87%E8%AE%B2%E6%98%8E%E7%99%BD.md>)、[Claude Code 作者说"不写 Prompt，写 Loop"](<07%20Claude%20Code%E4%BD%9C%E8%80%85%E8%AF%B4%E2%80%9C%E4%B8%8D%E5%86%99Prompt%EF%BC%8C%E5%86%99Loop%E2%80%9D%EF%BC%9AAI%E7%BC%96%E7%A8%8B%E4%BB%8E%E6%8F%90%E7%A4%BA%E8%AF%8D%E5%88%B0Agent%E9%97%AD%E7%8E%AF%E5%88%B0%E5%BA%95%E5%8F%98%E4%BA%86%E4%BB%80%E4%B9%88.md>)、[Claude Code 为什么快](<10%20Claude%20Code%20%E4%B8%BA%E4%BB%80%E4%B9%88%E5%BF%AB%EF%BC%9FPrompt%20Cache%E3%80%81Plan%20Mode%E3%80%81MCP%E5%B7%A5%E5%85%B7%E5%8A%A0%E8%BD%BD%E5%92%8C%E4%B8%8A%E4%B8%8B%E6%96%87%E5%8E%8B%E7%BC%A9%E4%B8%80%E7%AF%87%E8%AE%B2%E6%98%8E%E7%99%BD.md>)，那几篇是单点深挖。这一篇把它们串起来，给你一条「从能用到用得高效」的完整路线。

如果你还分不清 CLAUDE.md、Skills、Subagents、MCP、Hooks、Plugins 各自管什么，先看这篇 [Claude Code 扩展能力完整指南](<08%20Claude%20Code%E5%AE%8C%E6%95%B4%E4%BD%BF%E7%94%A8%E6%8C%87%E5%8D%97%EF%BC%9ACLAUDE.md%E3%80%81Skills%E3%80%81Subagents%E3%80%81MCP%E3%80%81Hooks%E3%80%81Plugins%E6%80%8E%E4%B9%88%E7%94%A8.md>)，里面给了目录、配置和组合案例。

<!-- drawio源文件: ./drawio/14_claude_code_solidify_ladder.drawio -->

![Claude Code 高效使用的逐级固化阶梯：从聊天框到 CLAUDE.md、Skill、Hooks、子代理与动态工作流，越往上自动化程度越高越省心](<https://file1.kamacoder.com/i/web/20260624112225.png?v=20261005>)

这张图回答的是：**怎么把 Claude Code 从「聊天框」一步步用高效**。底座那个红色「聊天框」就是大多数人停留的浅用法——问一句答一句、每次从零解释。往上每一级，都是把一类「重复劳动」固化下来：项目规则固化进 CLAUDE.md、专项流程固化成 Skill、必做动作固化成 Hooks、大任务固化成并行编排。固化得越多，你要操的心越少。下面就顺着这条阶梯一级一级讲。

## 第一件事：别让它每次都「从零认识你的项目」

新会话里的 Claude Code，是**失忆**的。它不知道你用什么技术栈、不知道你的代码规范、不知道这个项目哪几个坑不能踩。

你每次都口头交代一遍，就是在重复劳动。**正确的做法是把这些写进 `CLAUDE.md`**——放在项目根目录的一个 markdown 文件，Claude Code 每次开会话都会先读它。编码规范、架构决策、常用命令、踩过的坑，全写进去。

光这一步，就能把「它写出来的东西不符合我项目习惯」这类问题砍掉一大半。

更省心的是，Claude 干活时还会自己攒**自动内存**——构建命令、调试发现这些东西，它会跨会话记住，不用你写。怎么把 CLAUDE.md 写得既管用又不臃肿，[这一篇](<09%20CLAUDE.md%E5%88%B0%E5%BA%95%E6%80%8E%E4%B9%88%E5%86%99%EF%BC%9FClaude%20Code%E9%A1%B9%E7%9B%AE%E8%AE%B0%E5%BF%86%E3%80%81%E5%9B%A2%E9%98%9F%E8%A7%84%E8%8C%83%E5%92%8C%E4%B8%8A%E4%B8%8B%E6%96%87%E7%AE%A1%E7%90%86%E4%B8%80%E7%AF%87%E8%AE%B2%E6%98%8E%E7%99%BD.md>)讲得很细，这里不重复。

**一句话：CLAUDE.md 是你给 Claude 的「项目说明书」，写一次，每个会话都受益。**

## 第二件事：把「每次都要解释一遍的流程」封成 Skill

CLAUDE.md 解决的是「always-on 的项目规则」，但有些活儿是**特定场景才用**的——比如「发版前怎么写 release notes」「我们团队的 PR 评审清单」「部署到 staging 的固定步骤」。

这些东西塞进 CLAUDE.md，会把它撑爆、还白占上下文。**它们该被封成 Skill。**

Skill 是**按需加载的专项能力**：平时不占上下文，Claude 判断这次任务用得上，才把它调起来，像 `/review-pr`、`/deploy-staging` 这样一键触发。而且 Skill 不是一个 markdown 文件，是一个**文件夹**——可以带脚本、带模板、带参考资料。

Anthropic 内部已经在用**几百个 Skill**，他们总结的实战经验我单独写过一篇 [Claude Skills 实战](<11%20Claude%20Skills%E5%AE%9E%E6%88%98%EF%BC%9AAnthropic%E7%94%A8%E4%BA%86%E5%87%A0%E7%99%BE%E4%B8%AASkill%EF%BC%8C%E6%80%BB%E7%BB%93%E5%87%BA9%E5%A4%A7%E5%88%86%E7%B1%BB%E5%92%8C%E5%86%99%E5%A5%BDSkill%E7%9A%84%E5%85%A8%E9%83%A8%E7%BB%8F%E9%AA%8C.md>)，想认真用 Skill 的录友建议读一下。

**一句话：重复三次以上的流程，就该封成 Skill，让团队共享。**

## 第三件事：把「每次都得手动做的事」交给 Hooks 自动跑

有些事不是「让 Claude 决定做不做」，而是**每次都必须做**——比如每次改完文件自动格式化、提交前必须跑一遍 lint。

这种事靠你盯着、靠提醒 Claude，都不靠谱。**这是 Hooks 的活儿。**

Hooks 让你在 Claude Code 动手**之前或之后**自动执行 shell 命令。配一条「文件编辑后自动 format」、一条「commit 前先 lint」，从此这些动作脱离「人的注意力」，变成确定性发生的流程。

**Skill 和 Hooks 的区别记住这一句：Skill 是「需要时才调的能力」，Hooks 是「每次都确定触发的动作」。**

## 第四件事：大活儿别一个人扛——子代理和动态工作流

深度调研、安全审计、大范围重构这种活儿，让**一个** Claude 从头干到尾，上下文很快就撑满，还容易跑偏、偷懒、自夸。

Claude Code 的解法是**开一队 Claude 并行**：

- **子代理（sub-agents）**：主代理把任务拆成几块，分给多个子代理同时干，最后自己汇总合并。每个子代理有独立上下文，互不污染。
- **动态工作流（Dynamic Workflows）**：更进一步，Claude 针对你**当前这个任务**，现场写一套专属的编排（扇出汇总、对抗验证、锦标赛等模式），把活儿拆给一队 Claude 去跑。

这套「为什么要拆、怎么拆」的工程思路，我在 [Managed Agents](<14%20Claude%20Managed%20Agents%E8%AF%A6%E8%A7%A3%EF%BC%9A%E6%8A%8AAgent%E7%9A%84%E3%80%8C%E5%A4%A7%E8%84%91%E3%80%8D%E5%92%8C%E3%80%8C%E5%8F%8C%E6%89%8B%E3%80%8D%E6%8B%86%E5%BC%80%EF%BC%8C%E4%BB%8E%E5%8E%9F%E5%9E%8B%E5%88%B0%E4%B8%8A%E7%BA%BF%E5%8F%AA%E8%A6%81%E5%87%A0%E5%A4%A9.md>) 和 [动态工作流详解](<12%20Claude%20Code%20%E5%8A%A8%E6%80%81%E5%B7%A5%E4%BD%9C%E6%B5%81%E8%AF%A6%E8%A7%A3%EF%BC%9A%E8%AE%A9%20Claude%20%E8%87%AA%E5%B7%B1%E7%8E%B0%E5%86%99%E4%B8%80%E5%A5%97%20harness%EF%BC%8C%E6%8A%8A%E4%B8%80%E4%B8%AA%E4%BB%BB%E5%8A%A1%E6%8B%86%E7%BB%99%E4%B8%80%E9%98%9F%20Claude%20%E5%8E%BB%E5%B9%B2.md>) 两篇里讲透了。

**一句话：上下文是稀缺资源，活儿大就拆开并行，别让一个 Claude 硬扛。**

## 第五件事：跳出聊天框——CLI 管道 + 定时任务

很多录友只在「交互式聊天」里用 Claude Code，其实它遵循 Unix 哲学，**是可以管道化、能塞进脚本和 CI 的**。

用 `claude -p`（print 模式）就能把它当成命令行里的一环：


<details class="code-example"><summary>bash 示例（点击展开）</summary>

```bash
# 盯日志，发现异常就 Slack 我
tail -200 app.log | claude -p "如果发现任何异常就 Slack 通知我"

# 批量审查改动文件的安全问题
git diff main --name-only | claude -p "审查这些改动文件有没有安全问题"
```

</details>

再往上一层是**定时任务**，让重复的活儿自动发生：早晨 PR 审查、夜里跑 CI 失败分析、每周依赖审计。

- 终端里临时轮询，用 [`/loop`](<07%20Claude%20Code%E4%BD%9C%E8%80%85%E8%AF%B4%E2%80%9C%E4%B8%8D%E5%86%99Prompt%EF%BC%8C%E5%86%99Loop%E2%80%9D%EF%BC%9AAI%E7%BC%96%E7%A8%8B%E4%BB%8E%E6%8F%90%E7%A4%BA%E8%AF%8D%E5%88%B0Agent%E9%97%AD%E7%8E%AF%E5%88%B0%E5%BA%95%E5%8F%98%E4%BA%86%E4%BB%80%E4%B9%88.md>)（这背后就是「写 Loop 不写 Prompt」那套思路）；
- 想要**电脑关机也照跑**的，用 **Routines**——它跑在 Anthropic 托管的基础设施上，还能被 API 调用或 GitHub 事件触发。

**一句话：能用一句话提问，也能塞进管道和定时任务无人值守地跑——后者才是效率的天花板。**

## 最后：换个地方接着干

Claude Code 不绑死在一个界面。终端、VS Code / JetBrains、桌面 App、网页，背后是**同一个引擎**——你的 CLAUDE.md、设置、MCP 服务器在哪儿都通用。

离开工位，用手机或浏览器**远程接管**正在跑的会话；网页或 iOS 上起一个长任务，回头用 `claude --teleport` 把它拽回终端继续。**工作跟着你走，不跟着设备走。**

说到底，高效用 Claude Code 就一条主线：**把"每次都要重复的东西"一层层固化下来**——项目规则固化进 CLAUDE.md，专项流程固化成 Skill，必做动作固化成 Hooks，大任务固化成并行编排。固化得越多，你要操的心越少。

## 参考链接

- Claude Code 官方文档（概述）：https://code.claude.com/docs/zh-CN/overview
- Claude Code 官方文档（常见工作流）：https://code.claude.com/docs/zh-CN/common-workflows


---

[书架](../../00%20%E4%B9%A6%E6%9E%B6.md) · [本书目录](../00%20%E7%9B%AE%E5%BD%95.md) · [上一节](03%2040%E4%B8%87%E6%AC%A1Claude%20Code%E4%BC%9A%E8%AF%9D%E6%8F%AD%E7%A4%BA%EF%BC%9A%E7%9C%9F%E6%AD%A3%E6%8B%89%E5%BC%80%E5%B7%AE%E8%B7%9D%E7%9A%84%EF%BC%8C%E4%B8%8D%E6%98%AFPrompt.md) · [下一节](05%20%E6%B7%B1%E5%85%A5%E7%90%86%E8%A7%A3%20Claude%20Code%EF%BC%9A%E4%BB%8E%20CLAUDE.md%20%E5%88%B0%20Hooks%E3%80%81Skills%E3%80%81Subagents.md)

<details><summary>原文与配套实操</summary>

本页来自本地教程，阅读版不执行代码。

打开原文件（本机路径未随仓库分发）。需要运行代码时，请打开“大模型实操”工作区。

</details>
