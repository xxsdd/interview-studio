[书架](../../00%20%E4%B9%A6%E6%9E%B6.md) · [本书目录](../00%20%E7%9B%AE%E5%BD%95.md) · [上一节](14%20Claude%20Managed%20Agents%E8%AF%A6%E8%A7%A3%EF%BC%9A%E6%8A%8AAgent%E7%9A%84%E3%80%8C%E5%A4%A7%E8%84%91%E3%80%8D%E5%92%8C%E3%80%8C%E5%8F%8C%E6%89%8B%E3%80%8D%E6%8B%86%E5%BC%80%EF%BC%8C%E4%BB%8E%E5%8E%9F%E5%9E%8B%E5%88%B0%E4%B8%8A%E7%BA%BF%E5%8F%AA%E8%A6%81%E5%87%A0%E5%A4%A9.md) · [下一节](../05%20%E5%8A%A8%E6%80%81%E4%B8%8E%E5%BB%B6%E4%BC%B8%E9%98%85%E8%AF%BB/01%20ChatGPT%E3%80%81Claude%E3%80%81Grok%E5%90%8C%E6%97%B6%E5%AE%95%E6%9C%BA%EF%BC%9A%E9%87%8D%E5%8F%A093%E5%88%86%E9%92%9F%EF%BC%8C%E4%BD%86%E2%80%9C%E5%90%8C%E4%B8%80%E4%B8%AA%E5%85%83%E5%87%B6%E2%80%9D%E6%B2%A1%E6%9C%89%E8%AF%81%E6%8D%AE.md)

---

# Claude学习专栏

<a href="https://notes.kamacoder.com/qita/0024.claude-opus-5-china-guide.html">
  <img src="https://file1.kamacoder.com/i/web/2026-07-30_21-45-21.jpg?v=20261005" style="width:100%;cursor:pointer;" alt="">
</a>


> 从会用 Claude Code，到能把它接进真实工程。

很多人第一次用 Claude Code，只把它当成终端里的聊天框：问一句，改一段，出错了再补一句。

这样当然能用，但只用到了最浅的一层。

Claude Code 真正的价值，是把项目规则、上下文管理、工具调用、测试验证和多 Agent 协作串成一个可以持续运行的工程闭环。

这个专栏不按功能列表堆文章，而是沿着一条学习路线讲清楚：**先知道 Claude Code 能做什么，再理解它为什么这样工作，最后把能力沉淀成团队可复用的工程资产。**

## 第一阶段：先把 Claude Code 用明白

先建立完整能力地图，避免一上来就在 Skills、Hooks、MCP 之间来回试错。

- [Claude Code高效使用指南：5件事把它调教成一个会自己干活的团队](<04%20Claude%20Code%20%E9%AB%98%E6%95%88%E4%BD%BF%E7%94%A8%E6%8C%87%E5%8D%97%EF%BC%9A%E5%88%AB%E6%8A%8A%E5%AE%83%E5%BD%93%E8%81%8A%E5%A4%A9%E6%A1%86%EF%BC%8C5%20%E4%BB%B6%E4%BA%8B%E6%8A%8A%E5%AE%83%E8%B0%83%E6%95%99%E6%88%90%E4%B8%80%E4%B8%AA%E4%BC%9A%E8%87%AA%E5%B7%B1%E5%B9%B2%E6%B4%BB%E7%9A%84%E5%9B%A2%E9%98%9F.md>)
- [Claude Code完整使用指南：CLAUDE.md、Skills、Subagents、MCP、Hooks、Plugins怎么用](<08%20Claude%20Code%E5%AE%8C%E6%95%B4%E4%BD%BF%E7%94%A8%E6%8C%87%E5%8D%97%EF%BC%9ACLAUDE.md%E3%80%81Skills%E3%80%81Subagents%E3%80%81MCP%E3%80%81Hooks%E3%80%81Plugins%E6%80%8E%E4%B9%88%E7%94%A8.md>)
- [CLAUDE.md到底怎么写？项目记忆、团队规范和上下文管理一篇讲明白](<09%20CLAUDE.md%E5%88%B0%E5%BA%95%E6%80%8E%E4%B9%88%E5%86%99%EF%BC%9FClaude%20Code%E9%A1%B9%E7%9B%AE%E8%AE%B0%E5%BF%86%E3%80%81%E5%9B%A2%E9%98%9F%E8%A7%84%E8%8C%83%E5%92%8C%E4%B8%8A%E4%B8%8B%E6%96%87%E7%AE%A1%E7%90%86%E4%B8%80%E7%AF%87%E8%AE%B2%E6%98%8E%E7%99%BD.md>)

## 第二阶段：理解上下文和代码库

Claude Code 不是把整个仓库塞进上下文。它需要搜索、读取、压缩和缓存，也需要你给它清楚的项目入口。

- [Claude Code怎么读懂大代码库？Agent搜索、CLAUDE.md、Hooks、Skills、MCP和LSP一篇讲明白](<06%20Claude%20Code%E6%80%8E%E4%B9%88%E8%AF%BB%E6%87%82%E5%A4%A7%E4%BB%A3%E7%A0%81%E5%BA%93%EF%BC%9FAgent%E6%90%9C%E7%B4%A2%E3%80%81CLAUDE.md%E3%80%81Hooks%E3%80%81Skills%E3%80%81MCP%E5%92%8CLSP%E4%B8%80%E7%AF%87%E8%AE%B2%E6%98%8E%E7%99%BD.md>)
- [Claude Code为什么快？Prompt Cache、Plan Mode、MCP工具加载和上下文压缩一篇讲明白](<10%20Claude%20Code%20%E4%B8%BA%E4%BB%80%E4%B9%88%E5%BF%AB%EF%BC%9FPrompt%20Cache%E3%80%81Plan%20Mode%E3%80%81MCP%E5%B7%A5%E5%85%B7%E5%8A%A0%E8%BD%BD%E5%92%8C%E4%B8%8A%E4%B8%8B%E6%96%87%E5%8E%8B%E7%BC%A9%E4%B8%80%E7%AF%87%E8%AE%B2%E6%98%8E%E7%99%BD.md>)
- [为什么Agent时代大家都在做CLI？Claude Code、Codex与命令行的前世今生](<01%20%E4%B8%BA%E4%BB%80%E4%B9%88Agent%E6%97%B6%E4%BB%A3%E5%A4%A7%E5%AE%B6%E9%83%BD%E5%9C%A8%E5%81%9ACLI%EF%BC%9FClaude%20Code%E3%80%81Codex%E4%B8%8E%E5%91%BD%E4%BB%A4%E8%A1%8C%E7%9A%84%E5%89%8D%E4%B8%96%E4%BB%8A%E7%94%9F.md>)

## 第三阶段：从Prompt走向Agent Loop

当任务从“一次回答”变成“读取代码、执行修改、检查结果、继续修正”，重点就不再是某一句 Prompt，而是整个闭环能不能稳定运行。

- [Claude Code作者说“不写Prompt，写Loop”：AI编程从提示词到Agent闭环到底变了什么](<07%20Claude%20Code%E4%BD%9C%E8%80%85%E8%AF%B4%E2%80%9C%E4%B8%8D%E5%86%99Prompt%EF%BC%8C%E5%86%99Loop%E2%80%9D%EF%BC%9AAI%E7%BC%96%E7%A8%8B%E4%BB%8E%E6%8F%90%E7%A4%BA%E8%AF%8D%E5%88%B0Agent%E9%97%AD%E7%8E%AF%E5%88%B0%E5%BA%95%E5%8F%98%E4%BA%86%E4%BB%80%E4%B9%88.md>)
- [深入理解Claude Code：从CLAUDE.md到Hooks、Skills、Subagents](<05%20%E6%B7%B1%E5%85%A5%E7%90%86%E8%A7%A3%20Claude%20Code%EF%BC%9A%E4%BB%8E%20CLAUDE.md%20%E5%88%B0%20Hooks%E3%80%81Skills%E3%80%81Subagents.md>)
- [Claude Skills实战：Anthropic几百个Skill总结出的9大分类和实战经验](<11%20Claude%20Skills%E5%AE%9E%E6%88%98%EF%BC%9AAnthropic%E7%94%A8%E4%BA%86%E5%87%A0%E7%99%BE%E4%B8%AASkill%EF%BC%8C%E6%80%BB%E7%BB%93%E5%87%BA9%E5%A4%A7%E5%88%86%E7%B1%BB%E5%92%8C%E5%86%99%E5%A5%BDSkill%E7%9A%84%E5%85%A8%E9%83%A8%E7%BB%8F%E9%AA%8C.md>)
- [Claude Code动态工作流详解：让Claude自己现写一套harness](<12%20Claude%20Code%20%E5%8A%A8%E6%80%81%E5%B7%A5%E4%BD%9C%E6%B5%81%E8%AF%A6%E8%A7%A3%EF%BC%9A%E8%AE%A9%20Claude%20%E8%87%AA%E5%B7%B1%E7%8E%B0%E5%86%99%E4%B8%80%E5%A5%97%20harness%EF%BC%8C%E6%8A%8A%E4%B8%80%E4%B8%AA%E4%BB%BB%E5%8A%A1%E6%8B%86%E7%BB%99%E4%B8%80%E9%98%9F%20Claude%20%E5%8E%BB%E5%B9%B2.md>)
- [Loop Engineering实战：14步路线图，从判断要不要做到上线后守住](<13%20Loop%20Engineering%20%E5%AE%9E%E6%88%98%EF%BC%9A14%20%E6%AD%A5%E8%B7%AF%E7%BA%BF%E5%9B%BE%EF%BC%8C%E4%BB%8E%E5%88%A4%E6%96%AD%E8%A6%81%E4%B8%8D%E8%A6%81%E5%81%9A%E5%88%B0%E4%B8%8A%E7%BA%BF%E5%90%8E%E5%AE%88%E4%BD%8F.md>)

## 第四阶段：团队与生产工程

最后再看规模化问题：怎么拆任务、怎么隔离执行环境、怎么验证迁移结果，以及怎样让 Agent 真正进入生产系统。

- [百万行代码两周迁完：Anthropic如何用Claude Code做大规模代码迁移](<02%20%E7%99%BE%E4%B8%87%E8%A1%8C%E4%BB%A3%E7%A0%81%E4%B8%A4%E5%91%A8%E8%BF%81%E5%AE%8C%EF%BC%9AAnthropic%E5%A6%82%E4%BD%95%E7%94%A8Claude%20Code%E5%81%9A%E5%A4%A7%E8%A7%84%E6%A8%A1%E4%BB%A3%E7%A0%81%E8%BF%81%E7%A7%BB.md>)
- [Claude Managed Agents详解：把Agent的“大脑”和“双手”拆开](<14%20Claude%20Managed%20Agents%E8%AF%A6%E8%A7%A3%EF%BC%9A%E6%8A%8AAgent%E7%9A%84%E3%80%8C%E5%A4%A7%E8%84%91%E3%80%8D%E5%92%8C%E3%80%8C%E5%8F%8C%E6%89%8B%E3%80%8D%E6%8B%86%E5%BC%80%EF%BC%8C%E4%BB%8E%E5%8E%9F%E5%9E%8B%E5%88%B0%E4%B8%8A%E7%BA%BF%E5%8F%AA%E8%A6%81%E5%87%A0%E5%A4%A9.md>)

## 第五阶段：看清AI编程真正改变了什么

工具会继续变，但人和Agent怎么分工、什么能力会变得更值钱，是更长期的问题。

- [40万次Claude Code会话揭示：真正拉开差距的不是Prompt](<03%2040%E4%B8%87%E6%AC%A1Claude%20Code%E4%BC%9A%E8%AF%9D%E6%8F%AD%E7%A4%BA%EF%BC%9A%E7%9C%9F%E6%AD%A3%E6%8B%89%E5%BC%80%E5%B7%AE%E8%B7%9D%E7%9A%84%EF%BC%8C%E4%B8%8D%E6%98%AFPrompt.md>)

如果你刚开始用 Claude Code，从第一阶段按顺序看就够了。

如果你已经在项目里使用，可以直接从自己卡住的位置进入：规则总失效看 CLAUDE.md，仓库太大看大代码库，任务跑不稳看 Agent Loop，需要并行和隔离再看动态工作流与 Managed Agents。


---

[书架](../../00%20%E4%B9%A6%E6%9E%B6.md) · [本书目录](../00%20%E7%9B%AE%E5%BD%95.md) · [上一节](14%20Claude%20Managed%20Agents%E8%AF%A6%E8%A7%A3%EF%BC%9A%E6%8A%8AAgent%E7%9A%84%E3%80%8C%E5%A4%A7%E8%84%91%E3%80%8D%E5%92%8C%E3%80%8C%E5%8F%8C%E6%89%8B%E3%80%8D%E6%8B%86%E5%BC%80%EF%BC%8C%E4%BB%8E%E5%8E%9F%E5%9E%8B%E5%88%B0%E4%B8%8A%E7%BA%BF%E5%8F%AA%E8%A6%81%E5%87%A0%E5%A4%A9.md) · [下一节](../05%20%E5%8A%A8%E6%80%81%E4%B8%8E%E5%BB%B6%E4%BC%B8%E9%98%85%E8%AF%BB/01%20ChatGPT%E3%80%81Claude%E3%80%81Grok%E5%90%8C%E6%97%B6%E5%AE%95%E6%9C%BA%EF%BC%9A%E9%87%8D%E5%8F%A093%E5%88%86%E9%92%9F%EF%BC%8C%E4%BD%86%E2%80%9C%E5%90%8C%E4%B8%80%E4%B8%AA%E5%85%83%E5%87%B6%E2%80%9D%E6%B2%A1%E6%9C%89%E8%AF%81%E6%8D%AE.md)

<details><summary>原文与配套实操</summary>

本页来自本地教程，阅读版不执行代码。

打开原文件（本机路径未随仓库分发）。需要运行代码时，请打开“大模型实操”工作区。

</details>
