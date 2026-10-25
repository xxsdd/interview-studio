[书架](../../00%20%E4%B9%A6%E6%9E%B6.md) · [本书目录](../00%20%E7%9B%AE%E5%BD%95.md) · [上一节](23%20RAG%E5%A4%A7%E5%8E%82%E9%9D%A2%E8%AF%95%E9%A2%98%E6%B1%87%E6%80%BB%EF%BC%9A%E5%90%91%E9%87%8F%E6%A3%80%E7%B4%A2%E3%80%81%E6%B7%B7%E5%90%88%E6%A3%80%E7%B4%A2%E3%80%81Rerank%E3%80%81%E5%B9%BB%E8%A7%89%E5%A4%84%E7%90%86%E9%AB%98%E9%A2%91%E9%97%AE%E9%A2%98.md) · [下一节](25%20Spec-Driven%20Development%E8%A7%84%E7%BA%A6%E9%A9%B1%E5%8A%A8%E5%BC%80%E5%8F%91%EF%BC%9AAI%E5%86%99%E4%BB%A3%E7%A0%81%E8%B6%8A%E5%BF%AB%EF%BC%8C%E4%B8%BA%E4%BB%80%E4%B9%88%E8%B6%8A%E8%A6%81%E5%85%88%E5%86%99%E6%B8%85%E6%A5%9A.md)

---

# 大模型面经汇总：Agent、RAG、Transformer、AI编程大厂面试题

<a href="https://programmercarl.com/xunlian/damoxing.html">
  <img src="https://file1.kamacoder.com/i/web/2026-03-02_18-13-50.jpg?v=20261005" style="width:100%;cursor:pointer;" alt="卡码大模型应用开发训练营">
</a>

这里整理了 2026 年**大模型方向的高频面试题和真实面经**，覆盖 **Agent、RAG、Transformer、模型微调、AI 编程（Vibe Coding / Claude Code）** 五大块。不管你投的是大模型应用开发、Agent 开发、LLM 工程还是 AI 后端，这些都是大厂面试官反复深挖的考点。

每一篇都不是让你背答案，而是带你**理解面试官的考察逻辑**——为什么这么问、追问会往哪走、怎么结合项目说清楚。持续更新中，建议收藏。

## 怎么用这一页

录友们可以按目标岗位挑方向刷，不用一上来全看：

- **大模型应用开发 / LLM 工程岗**：[RAG](<23%20RAG%E5%A4%A7%E5%8E%82%E9%9D%A2%E8%AF%95%E9%A2%98%E6%B1%87%E6%80%BB%EF%BC%9A%E5%90%91%E9%87%8F%E6%A3%80%E7%B4%A2%E3%80%81%E6%B7%B7%E5%90%88%E6%A3%80%E7%B4%A2%E3%80%81Rerank%E3%80%81%E5%B9%BB%E8%A7%89%E5%A4%84%E7%90%86%E9%AB%98%E9%A2%91%E9%97%AE%E9%A2%98.md>) + [Agent](<07%20Agent%E5%A4%A7%E5%8E%82%E9%9D%A2%E8%AF%95%E9%A2%98%E6%B1%87%E6%80%BB%EF%BC%9AReAct%E3%80%81Function%20Calling%E3%80%81MCP%E3%80%81RAG%E9%AB%98%E9%A2%91%E9%97%AE%E9%A2%98.md>) + [Transformer](<26%20Transformer%E5%A4%A7%E5%8E%82%E9%9D%A2%E8%AF%95%E9%A2%98%E6%B1%87%E6%80%BB%EF%BC%9A%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91%E8%80%85%E8%A7%86%E8%A7%92.md>) 是地基，先把这三块吃透
- **Agent 开发岗**：重点刷 [Agent 智能体篇](<#agent-智能体篇>)，再配合[字节 Agent 开发四面面经](<01%20%E5%AD%97%E8%8A%82%E8%B7%B3%E5%8A%A8Agent%E5%BC%80%E5%8F%91%E5%9B%9B%E9%9D%A2%E9%9D%A2%E7%BB%8F%EF%BC%9A21%E9%81%93%E5%A4%A7%E6%A8%A1%E5%9E%8B%E9%9D%A2%E8%AF%95%E9%A2%98%E5%85%A8%E8%A7%A3%E6%9E%90%EF%BC%8C%E4%BB%8EPrompt%E5%88%B0Agent%E5%88%B0MCP.md>)和[番茄小说 Agent 应用开发一面](<10%20%E5%AD%97%E8%8A%82Agent%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91%E5%AE%9E%E4%B9%A0%E4%B8%80%E9%9D%A2%EF%BC%9A%E9%A1%B9%E7%9B%AE%E8%A2%AB%E8%BF%9E%E7%BB%AD%E6%B7%B1%E6%8C%96%EF%BC%8C%E5%BA%94%E8%AF%A5%E6%80%8E%E4%B9%88%E7%AD%94%EF%BC%9F.md>)感受项目连续深挖的节奏
- **想体现 AI 编程工程能力**：看 [AI 编程篇](<#ai-编程篇>)，重点是怎么把 AI 用出工程素养，而不是只会调 API
- **查漏补缺**：每篇结尾都有"面试怎么答"，看完能直接在面试里说出来

下面这些文章之间是**互相引用的知识系列**，遇到链接顺着点进去，能把一个方向连成一张网。

## AI 编程篇

AI 编程是 2026 年面试新增的高频方向，考的不是"你会不会用 Cursor"，而是**你能不能在 AI 时代体现工程价值**。

- [Vibe Coding大厂面试题汇总](<28%20Vibe%20Coding%E5%A4%A7%E5%8E%82%E9%9D%A2%E8%AF%95%E9%A2%98%E6%B1%87%E6%80%BB%EF%BC%9AAI%E7%BC%96%E7%A8%8B%E6%97%B6%E4%BB%A3%E4%BD%A0%E7%9A%84%E4%BC%98%E5%8A%BF%E5%88%B0%E5%BA%95%E5%9C%A8%E5%93%AA.md>) — AI编程时代核心竞争力、Token成本控制
- [Vibe Coding避坑指南](<27%20Vibe%20Coding%E9%81%BF%E5%9D%91%E6%8C%87%E5%8D%97%EF%BC%9AGit%E6%8F%90%E4%BA%A4%E3%80%81%E6%95%B0%E6%8D%AE%E5%BA%93%E5%A4%87%E4%BB%BD%E3%80%81%E6%A8%A1%E5%9D%97%E6%8B%86%E5%88%86%E3%80%81%E7%BA%BF%E4%B8%8A%E5%9B%9E%E6%BB%9A%E6%80%8E%E4%B9%88%E5%81%9A.md>) — Git提交、数据库备份、模块拆分、线上回滚怎么避免翻车
- [Claude Code大厂面试题汇总](<12%20Claude%20Code%E5%A4%A7%E5%8E%82%E9%9D%A2%E8%AF%95%E9%A2%98%E6%B1%87%E6%80%BB%EF%BC%9A%E6%BA%90%E7%A0%81%E6%B3%84%E9%9C%B2%E3%80%81Agent%20Loop%E3%80%81%E7%B3%BB%E7%BB%9F%E6%8F%90%E7%A4%BA%E8%AF%8D%E5%85%A8%E6%8B%86%E8%A7%A3%20%E6%B7%B1%E5%BA%A6%E8%A7%A3%E6%9E%90Claude%20Code%E5%B7%A5%E4%BD%9C%E5%8E%9F%E7%90%86.md>) — 源码泄露、Agent Loop、系统提示词全拆解
- [AI增强开发三件套面试详解](<09%20AI%E5%A2%9E%E5%BC%BA%E5%BC%80%E5%8F%91%E4%B8%89%E4%BB%B6%E5%A5%97%EF%BC%9AOpenSpec%E3%80%81Superpowers%E3%80%81gstack%E6%80%8E%E4%B9%88%E6%8A%8A%20Vibe%20Coding%20%E6%8B%89%E5%9B%9E%E5%B7%A5%E7%A8%8B%E4%BA%A4%E4%BB%98.md>) — OpenSpec、Superpowers、gstack如何把Vibe Coding拉回工程交付
- [Spec-Driven Development规约驱动开发详解](<25%20Spec-Driven%20Development%E8%A7%84%E7%BA%A6%E9%A9%B1%E5%8A%A8%E5%BC%80%E5%8F%91%EF%BC%9AAI%E5%86%99%E4%BB%A3%E7%A0%81%E8%B6%8A%E5%BF%AB%EF%BC%8C%E4%B8%BA%E4%BB%80%E4%B9%88%E8%B6%8A%E8%A6%81%E5%85%88%E5%86%99%E6%B8%85%E6%A5%9A.md>) — AI编程为什么要从模糊Prompt走向规格、计划、任务与验证
- [Claude Code为什么不用RAG检索代码](<13%20Claude%20Code%E4%B8%BA%E4%BB%80%E4%B9%88%E4%B8%8D%E7%94%A8RAG%E6%A3%80%E7%B4%A2%E4%BB%A3%E7%A0%81%EF%BC%9FGrep%E3%80%81Glob%E3%80%81Read%E4%B8%8E%E4%BB%A3%E7%A0%81%E6%A3%80%E7%B4%A2%E8%AE%BE%E8%AE%A1%E5%93%B2%E5%AD%A6.md>) — Grep、Glob、Read、子Agent与代码检索设计哲学
- [Claude Code上下文窗口面试详解](<11%20Claude%20Code%E4%B8%8A%E4%B8%8B%E6%96%87%E7%AA%97%E5%8F%A3%E9%9D%A2%E8%AF%95%E8%AF%A6%E8%A7%A3%EF%BC%9AAuto-Compact%E3%80%81%E4%B8%8A%E4%B8%8B%E6%96%87%E5%8E%8B%E7%BC%A9%E4%B8%8EAgent%E8%AE%B0%E5%BF%86%E7%AE%A1%E7%90%86.md>) — Auto-Compact、上下文压缩、任务状态快照与Agent记忆管理

## RAG 检索增强篇

RAG 已经是大模型岗的**必考项**，从向量检索原理到生产落地难点，面试官会一层层往下挖。

- [RAG大厂面试题汇总](<23%20RAG%E5%A4%A7%E5%8E%82%E9%9D%A2%E8%AF%95%E9%A2%98%E6%B1%87%E6%80%BB%EF%BC%9A%E5%90%91%E9%87%8F%E6%A3%80%E7%B4%A2%E3%80%81%E6%B7%B7%E5%90%88%E6%A3%80%E7%B4%A2%E3%80%81Rerank%E3%80%81%E5%B9%BB%E8%A7%89%E5%A4%84%E7%90%86%E9%AB%98%E9%A2%91%E9%97%AE%E9%A2%98.md>) — 向量检索、混合检索、Rerank、幻觉处理
- [RAG落地最难的地方在哪](<22%20RAG%E8%90%BD%E5%9C%B0%E6%9C%80%E9%9A%BE%E7%9A%84%E5%9C%B0%E6%96%B9%E5%9C%A8%E5%93%AA%EF%BC%9F%E6%96%87%E6%A1%A3%E9%A2%84%E5%A4%84%E7%90%86%E3%80%81%E5%8F%AC%E5%9B%9E%E8%B4%A8%E9%87%8F%E3%80%81%E7%94%9F%E6%88%90%E5%BF%A0%E5%AE%9E%E5%BA%A6.md>) — 文档预处理、召回质量、生成忠实度，三个环节级联放大
- [GraphRAG与LightRAG大厂面试题汇总](<16%20GraphRAG%E4%B8%8ELightRAG%E5%A4%A7%E5%8E%82%E9%9D%A2%E8%AF%95%E9%A2%98%E6%B1%87%E6%80%BB%EF%BC%9A%E4%BB%8ERAG%E5%88%B0%E7%9F%A5%E8%AF%86%E5%9B%BE%E8%B0%B1%E6%A3%80%E7%B4%A2.md>) — 从RAG到知识图谱检索，传统RAG天花板与轻量方案

## 模型微调篇

- [SFT、RLHF、DPO面试详解](<14%20%E5%A4%A7%E6%A8%A1%E5%9E%8B%E5%BE%AE%E8%B0%83%E9%9D%A2%E8%AF%95%E6%80%8E%E4%B9%88%E7%AD%94%EF%BC%9FSFT%E3%80%81RLHF%E3%80%81DPO%E3%80%81PPO%20%E5%88%B0%E5%BA%95%E8%BF%98%E6%9C%89%E6%B2%A1%E6%9C%89%E5%BF%85%E8%A6%81%EF%BC%9F.md>) — 微调价值、Prompt/RAG取舍、基模变强后的工程判断

## Agent 智能体篇

Agent 是大模型岗最大的考察块，从 ReAct、Function Calling、MCP 这些基础协议，到多 Agent 编排、Harness 治理、幻觉控制、成本优化，越往生产走越难。

- [Agent大厂面试题汇总](<07%20Agent%E5%A4%A7%E5%8E%82%E9%9D%A2%E8%AF%95%E9%A2%98%E6%B1%87%E6%80%BB%EF%BC%9AReAct%E3%80%81Function%20Calling%E3%80%81MCP%E3%80%81RAG%E9%AB%98%E9%A2%91%E9%97%AE%E9%A2%98.md>) — ReAct、Function Calling、MCP、RAG高频问题
- [Loop详解：从ReAct到Loop Engineering](<18%20Loop%E8%AF%A6%E8%A7%A3%EF%BC%9A%E4%BB%8EReAct%E5%88%B0Loop%20Engineering%EF%BC%8CAgent%E5%88%B0%E5%BA%95%E5%9C%A8%E5%BE%AA%E7%8E%AF%E4%BB%80%E4%B9%88.md>) — Agent到底在循环什么，上下文/状态/预算/工具/终止五类治理
- [Graph Engineering与Agent图编排详解](<15%20Graph%20Engineering%E8%AF%A6%E8%A7%A3%EF%BC%9ALoop%E8%BF%98%E6%B2%A1%E5%AD%A6%E5%AE%8C%EF%BC%8CGraph%E5%8F%88%E6%9D%A5%E4%BA%86%EF%BC%8CAgent%E5%9B%BE%E7%BC%96%E6%8E%92%E5%88%B0%E5%BA%95%E6%98%AF%E4%BB%80%E4%B9%88.md>) — 节点、边、状态、检查点、并行与人工审批，别和GraphRAG混淆
- [Harness Engineering大厂面试题汇总](<17%20Harness%20Engineering%E5%A4%A7%E5%8E%82%E9%9D%A2%E8%AF%95%E9%A2%98%E6%B1%87%E6%80%BB%EF%BC%9A%E4%BB%8EPrompt%E5%88%B0Context%E5%88%B0Harness.md>) — 从Prompt到Context到Harness，Hermes Agent与OpenClaw对比
- [生产级Agent全景面试详解](<21%20%E7%94%9F%E4%BA%A7%E7%BA%A7Agent%E5%85%A8%E6%99%AF%E9%9D%A2%E8%AF%95%E8%AF%A6%E8%A7%A3%EF%BC%9A%E7%B3%BB%E7%BB%9F%E6%9E%B6%E6%9E%84%E3%80%81Harness%E5%B7%A5%E7%A8%8B%E3%80%81%E7%BB%84%E7%BB%87%E5%8D%8F%E4%BD%9C%E4%B8%8E%E4%BA%BA%E6%89%8D%E8%83%BD%E5%8A%9B.md>) — 从Demo到生产，串起系统架构、Harness工程、组织协作与人才能力
- [多Agent通信与编排面试详解](<19%20%E5%A4%9AAgent%E6%9E%B6%E6%9E%84%E9%9D%A2%E8%AF%95%E5%85%A8%E8%A7%A3%E6%9E%90%EF%BC%9A%E9%80%9A%E4%BF%A1%E3%80%81%E7%BC%96%E6%8E%92%E3%80%81Tool%E5%8F%96%E8%88%8D%E4%B8%8E%E5%B7%A5%E7%A8%8B%E4%BB%A3%E4%BB%B7.md>) — 主Agent子Agent通信、编排模式、Tool取舍与工程代价
- [Multi-Agent Harness面试详解](<20%20%E6%9C%AA%E6%9D%A5%E7%9A%84%E7%AB%9E%E4%BA%89%EF%BC%8C%E4%B8%8D%E6%98%AF%20%E8%B0%81%E7%9A%84%20Agent%20%E6%9B%B4%E5%A4%9A%20%EF%BC%8C%E8%80%8C%E6%98%AF%20%E8%B0%81%E7%9A%84%20Harness%20%E6%9B%B4%E7%A8%B3.md>) — 编排调度、工具治理、状态记忆、轨迹评估与成本控制
- [Agent Harness可观测性面试详解](<05%20Agent%20Harness%20%E5%8F%AF%E8%A7%82%E6%B5%8B%E6%80%A7%EF%BC%9A%E7%94%9F%E4%BA%A7%E7%BA%A7%20AI%20%E9%A1%B9%E7%9B%AE%E5%BF%85%E9%A1%BB%E8%A1%A5%E4%B8%8A%E7%9A%84%E4%B8%80%E8%AF%BE.md>) — Trace轨迹、工具调用、上下文、成本与评测闭环
- [Agent Skill面试详解](<08%20Agent%20Skill%20%E9%9D%A2%E8%AF%95%E6%80%8E%E4%B9%88%E7%AD%94%EF%BC%9F%E5%A6%82%E4%BD%95%E5%86%99%E5%87%BA%E9%AB%98%E8%B4%A8%E9%87%8F%20Skill%EF%BC%8C%E7%9C%9F%E6%AD%A3%E6%8F%90%E5%8D%87%20Agent%20%E8%83%BD%E5%8A%9B%EF%BC%9F.md>) — Skill复用、上下文治理、版本管理、评估指标与生产落地
- [Agent框架横评：OpenClaw、Hermes Agent、Claude Code](<03%20OpenClaw%E3%80%81Hermes%20Agent%E3%80%81Claude%20Code%E4%B8%89%E6%A1%86%E6%9E%B6%E6%A8%AA%E8%AF%84%EF%BC%9A%E9%9D%A2%E8%AF%95%E5%BF%85%E6%87%82%E7%9A%84%E5%AF%B9%E6%AF%94.md>) — 记忆机制、工具调用、上下文管理面试对比
- [Agent混合路由优化详解](<06%20Agent%E6%B7%B7%E5%90%88%E8%B7%AF%E7%94%B1%E4%BC%98%E5%8C%96%EF%BC%9A%E4%BB%8E%20%E4%B8%80%E5%88%80%E5%88%87%20%E5%88%B0%20%E7%9C%8B%E8%8F%9C%E4%B8%8B%E7%A2%9F.md>) — 规则路由、模型路由、混合路由，级联降级怎么避坑
- [Agent漂移与幻觉怎么解](<02%20Agent%E4%B8%8A%E4%B8%8B%E6%96%87%E6%BC%82%E7%A7%BB%E4%B8%8E%E5%B7%A5%E5%85%B7%E8%B0%83%E7%94%A8%E5%B9%BB%E8%A7%89%EF%BC%9A%E6%B7%B1%E5%BA%A6%E6%8B%86%E8%A7%A3%E4%B8%8E%E9%9D%A2%E8%AF%95%E5%9B%9E%E7%AD%94%E6%80%9D%E8%B7%AF.md>) — 任务漂移、上下文幻觉、注意力稀释的识别与应对
- [Agent系统如何约束大模型幻觉](<04%20Agent%E7%B3%BB%E7%BB%9F%E5%A6%82%E4%BD%95%E7%BA%A6%E6%9D%9F%E5%A4%A7%E6%A8%A1%E5%9E%8B%E5%B9%BB%E8%A7%89%EF%BC%9F%E7%BA%A6%E6%9D%9F%E5%90%8E%E8%BF%98%E5%B9%BB%E8%A7%89%E6%80%8E%E4%B9%88%E5%8A%9E%EF%BC%9F.md>) — Prompt、工具、证据、输出校验与幻觉兜底处理

## Transformer 原理篇

- [Transformer大厂面试题汇总：应用开发者视角](<26%20Transformer%E5%A4%A7%E5%8E%82%E9%9D%A2%E8%AF%95%E9%A2%98%E6%B1%87%E6%80%BB%EF%BC%9A%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91%E8%80%85%E8%A7%86%E8%A7%92.md>) — Self-Attention、位置编码、三大架构选择、O(n²)复杂度

## 真实面经

- [字节Agent开发四面面经](<01%20%E5%AD%97%E8%8A%82%E8%B7%B3%E5%8A%A8Agent%E5%BC%80%E5%8F%91%E5%9B%9B%E9%9D%A2%E9%9D%A2%E7%BB%8F%EF%BC%9A21%E9%81%93%E5%A4%A7%E6%A8%A1%E5%9E%8B%E9%9D%A2%E8%AF%95%E9%A2%98%E5%85%A8%E8%A7%A3%E6%9E%90%EF%BC%8C%E4%BB%8EPrompt%E5%88%B0Agent%E5%88%B0MCP.md>) — 21道大模型面试题全解析，从Prompt到Agent到MCP
- [字节番茄小说Agent应用开发实习一面](<10%20%E5%AD%97%E8%8A%82Agent%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91%E5%AE%9E%E4%B9%A0%E4%B8%80%E9%9D%A2%EF%BC%9A%E9%A1%B9%E7%9B%AE%E8%A2%AB%E8%BF%9E%E7%BB%AD%E6%B7%B1%E6%8C%96%EF%BC%8C%E5%BA%94%E8%AF%A5%E6%80%8E%E4%B9%88%E7%AD%94%EF%BC%9F.md>) — ES混合检索、三层记忆、DAG编排、Token治理、QKV与算法题现场回答

## 大模型面试常见问题

**大模型面试一般考什么？**
主要五块：[Transformer 原理](<26%20Transformer%E5%A4%A7%E5%8E%82%E9%9D%A2%E8%AF%95%E9%A2%98%E6%B1%87%E6%80%BB%EF%BC%9A%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91%E8%80%85%E8%A7%86%E8%A7%92.md>)（Self-Attention、架构选择）、[RAG 检索增强](<23%20RAG%E5%A4%A7%E5%8E%82%E9%9D%A2%E8%AF%95%E9%A2%98%E6%B1%87%E6%80%BB%EF%BC%9A%E5%90%91%E9%87%8F%E6%A3%80%E7%B4%A2%E3%80%81%E6%B7%B7%E5%90%88%E6%A3%80%E7%B4%A2%E3%80%81Rerank%E3%80%81%E5%B9%BB%E8%A7%89%E5%A4%84%E7%90%86%E9%AB%98%E9%A2%91%E9%97%AE%E9%A2%98.md>)（向量检索、Rerank、幻觉）、[Agent 智能体](<07%20Agent%E5%A4%A7%E5%8E%82%E9%9D%A2%E8%AF%95%E9%A2%98%E6%B1%87%E6%80%BB%EF%BC%9AReAct%E3%80%81Function%20Calling%E3%80%81MCP%E3%80%81RAG%E9%AB%98%E9%A2%91%E9%97%AE%E9%A2%98.md>)（ReAct、Function Calling、MCP）、[模型微调](<14%20%E5%A4%A7%E6%A8%A1%E5%9E%8B%E5%BE%AE%E8%B0%83%E9%9D%A2%E8%AF%95%E6%80%8E%E4%B9%88%E7%AD%94%EF%BC%9FSFT%E3%80%81RLHF%E3%80%81DPO%E3%80%81PPO%20%E5%88%B0%E5%BA%95%E8%BF%98%E6%9C%89%E6%B2%A1%E6%9C%89%E5%BF%85%E8%A6%81%EF%BC%9F.md>)（SFT、RLHF、DPO）、以及 [AI 编程能力](<28%20Vibe%20Coding%E5%A4%A7%E5%8E%82%E9%9D%A2%E8%AF%95%E9%A2%98%E6%B1%87%E6%80%BB%EF%BC%9AAI%E7%BC%96%E7%A8%8B%E6%97%B6%E4%BB%A3%E4%BD%A0%E7%9A%84%E4%BC%98%E5%8A%BF%E5%88%B0%E5%BA%95%E5%9C%A8%E5%93%AA.md>)。应用开发岗更偏 RAG 和 Agent 工程，算法岗更偏 Transformer 和微调原理。

**没有大模型项目经验，怎么准备 Agent / 大模型岗面试？**
先把原理和回答思路吃透，再用一个小项目把链路跑通。面试官不一定要求你做过大厂级系统，但会追问细节——比如 RAG 的 Chunk 怎么切、Agent 的工具调用怎么兜底。可以对照[字节 Agent 开发四面面经](<01%20%E5%AD%97%E8%8A%82%E8%B7%B3%E5%8A%A8Agent%E5%BC%80%E5%8F%91%E5%9B%9B%E9%9D%A2%E9%9D%A2%E7%BB%8F%EF%BC%9A21%E9%81%93%E5%A4%A7%E6%A8%A1%E5%9E%8B%E9%9D%A2%E8%AF%95%E9%A2%98%E5%85%A8%E8%A7%A3%E6%9E%90%EF%BC%8C%E4%BB%8EPrompt%E5%88%B0Agent%E5%88%B0MCP.md>)看考察范围，再看[番茄小说 Agent 应用开发一面](<10%20%E5%AD%97%E8%8A%82Agent%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91%E5%AE%9E%E4%B9%A0%E4%B8%80%E9%9D%A2%EF%BC%9A%E9%A1%B9%E7%9B%AE%E8%A2%AB%E8%BF%9E%E7%BB%AD%E6%B7%B1%E6%8C%96%EF%BC%8C%E5%BA%94%E8%AF%A5%E6%80%8E%E4%B9%88%E7%AD%94%EF%BC%9F.md>)学习怎么回答项目指标、Agent 边界和 Token 治理。

**RAG 和微调，面试时该重点准备哪个？**
大部分应用开发岗 RAG 的权重更高，因为落地场景多。微调更多考"什么时候该微调、和 RAG/Prompt 怎么取舍"。两者的边界判断见 [SFT、RLHF、DPO 面试详解](<14%20%E5%A4%A7%E6%A8%A1%E5%9E%8B%E5%BE%AE%E8%B0%83%E9%9D%A2%E8%AF%95%E6%80%8E%E4%B9%88%E7%AD%94%EF%BC%9FSFT%E3%80%81RLHF%E3%80%81DPO%E3%80%81PPO%20%E5%88%B0%E5%BA%95%E8%BF%98%E6%9C%89%E6%B2%A1%E6%9C%89%E5%BF%85%E8%A6%81%EF%BC%9F.md>)。

**Agent 面试高频考点有哪些？**
ReAct 循环、Function Calling 原理、MCP 协议、记忆系统、幻觉与漂移控制、多 Agent 编排、成本优化。基础看 [Agent 大厂面试题汇总](<07%20Agent%E5%A4%A7%E5%8E%82%E9%9D%A2%E8%AF%95%E9%A2%98%E6%B1%87%E6%80%BB%EF%BC%9AReAct%E3%80%81Function%20Calling%E3%80%81MCP%E3%80%81RAG%E9%AB%98%E9%A2%91%E9%97%AE%E9%A2%98.md>)，循环本身怎么工程化看 [从 ReAct 到 Loop Engineering](<18%20Loop%E8%AF%A6%E8%A7%A3%EF%BC%9A%E4%BB%8EReAct%E5%88%B0Loop%20Engineering%EF%BC%8CAgent%E5%88%B0%E5%BA%95%E5%9C%A8%E5%BE%AA%E7%8E%AF%E4%BB%80%E4%B9%88.md>)，生产全景看 [生产级 Agent 架构、Harness、组织与人才](<21%20%E7%94%9F%E4%BA%A7%E7%BA%A7Agent%E5%85%A8%E6%99%AF%E9%9D%A2%E8%AF%95%E8%AF%A6%E8%A7%A3%EF%BC%9A%E7%B3%BB%E7%BB%9F%E6%9E%B6%E6%9E%84%E3%80%81Harness%E5%B7%A5%E7%A8%8B%E3%80%81%E7%BB%84%E7%BB%87%E5%8D%8F%E4%BD%9C%E4%B8%8E%E4%BA%BA%E6%89%8D%E8%83%BD%E5%8A%9B.md>)，专项治理再看 [Harness Engineering 面试题](<17%20Harness%20Engineering%E5%A4%A7%E5%8E%82%E9%9D%A2%E8%AF%95%E9%A2%98%E6%B1%87%E6%80%BB%EF%BC%9A%E4%BB%8EPrompt%E5%88%B0Context%E5%88%B0Harness.md>) 和 [Multi-Agent Harness 面试详解](<20%20%E6%9C%AA%E6%9D%A5%E7%9A%84%E7%AB%9E%E4%BA%89%EF%BC%8C%E4%B8%8D%E6%98%AF%20%E8%B0%81%E7%9A%84%20Agent%20%E6%9B%B4%E5%A4%9A%20%EF%BC%8C%E8%80%8C%E6%98%AF%20%E8%B0%81%E7%9A%84%20Harness%20%E6%9B%B4%E7%A8%B3.md>)。

**AI 都能写代码了，AI 编程岗面试还看什么？**
看的是你能不能让 AI 写得更对、更稳、更可控——上下文构建、Token 成本控制、代码审查、工程纪律。详见 [Vibe Coding 大厂面试题汇总](<28%20Vibe%20Coding%E5%A4%A7%E5%8E%82%E9%9D%A2%E8%AF%95%E9%A2%98%E6%B1%87%E6%80%BB%EF%BC%9AAI%E7%BC%96%E7%A8%8B%E6%97%B6%E4%BB%A3%E4%BD%A0%E7%9A%84%E4%BC%98%E5%8A%BF%E5%88%B0%E5%BA%95%E5%9C%A8%E5%93%AA.md>)、[Vibe Coding 避坑指南](<27%20Vibe%20Coding%E9%81%BF%E5%9D%91%E6%8C%87%E5%8D%97%EF%BC%9AGit%E6%8F%90%E4%BA%A4%E3%80%81%E6%95%B0%E6%8D%AE%E5%BA%93%E5%A4%87%E4%BB%BD%E3%80%81%E6%A8%A1%E5%9D%97%E6%8B%86%E5%88%86%E3%80%81%E7%BA%BF%E4%B8%8A%E5%9B%9E%E6%BB%9A%E6%80%8E%E4%B9%88%E5%81%9A.md>) 和 [AI 增强开发三件套面试详解](<09%20AI%E5%A2%9E%E5%BC%BA%E5%BC%80%E5%8F%91%E4%B8%89%E4%BB%B6%E5%A5%97%EF%BC%9AOpenSpec%E3%80%81Superpowers%E3%80%81gstack%E6%80%8E%E4%B9%88%E6%8A%8A%20Vibe%20Coding%20%E6%8B%89%E5%9B%9E%E5%B7%A5%E7%A8%8B%E4%BA%A4%E4%BB%98.md>)。

## 推荐阅读

- [Java 面经汇总](<../java/>)
- [C++ 面经汇总](<../cpp/>)
- [大模型专栏](<../../04%20%E5%A4%A7%E6%A8%A1%E5%9E%8B%E7%BB%BC%E5%90%88%E5%8F%82%E8%80%83/00%20%E7%9B%AE%E5%BD%95.md>)

> 面经的价值，不在于"背答案"，而在于理解面试官的考察逻辑。每篇都附回答思路，看完能直接在面试中说出来。


---

[书架](../../00%20%E4%B9%A6%E6%9E%B6.md) · [本书目录](../00%20%E7%9B%AE%E5%BD%95.md) · [上一节](23%20RAG%E5%A4%A7%E5%8E%82%E9%9D%A2%E8%AF%95%E9%A2%98%E6%B1%87%E6%80%BB%EF%BC%9A%E5%90%91%E9%87%8F%E6%A3%80%E7%B4%A2%E3%80%81%E6%B7%B7%E5%90%88%E6%A3%80%E7%B4%A2%E3%80%81Rerank%E3%80%81%E5%B9%BB%E8%A7%89%E5%A4%84%E7%90%86%E9%AB%98%E9%A2%91%E9%97%AE%E9%A2%98.md) · [下一节](25%20Spec-Driven%20Development%E8%A7%84%E7%BA%A6%E9%A9%B1%E5%8A%A8%E5%BC%80%E5%8F%91%EF%BC%9AAI%E5%86%99%E4%BB%A3%E7%A0%81%E8%B6%8A%E5%BF%AB%EF%BC%8C%E4%B8%BA%E4%BB%80%E4%B9%88%E8%B6%8A%E8%A6%81%E5%85%88%E5%86%99%E6%B8%85%E6%A5%9A.md)

<details><summary>原文与配套实操</summary>

本页来自本地教程，阅读版不执行代码。

打开原文件（本机路径未随仓库分发）。需要运行代码时，请打开“大模型实操”工作区。

</details>
