[书架](../../00%20%E4%B9%A6%E6%9E%B6.md) · [本书目录](../00%20%E7%9B%AE%E5%BD%95.md) · [上一节](03%20Agent%E5%88%B0%E5%BA%95%E6%98%AF%E4%BB%80%E4%B9%88%EF%BC%9F%E5%92%8C%E6%99%AE%E9%80%9A%E5%A4%A7%E6%A8%A1%E5%9E%8B%E9%97%AE%E7%AD%94%E6%9C%89%E4%BB%80%E4%B9%88%E5%8C%BA%E5%88%AB%EF%BC%9F.md) · [下一节](05%20Agent%E7%9A%84%E8%AE%B0%E5%BF%86%EF%BC%9A%E7%9F%AD%E6%9C%9F%E3%80%81%E9%95%BF%E6%9C%9F%E3%80%81RAG%E5%88%B0%E5%BA%95%E4%BB%80%E4%B9%88%E5%85%B3%E7%B3%BB%EF%BC%9F.md)

---

# AI Agent 学习路线：程序员怎么从零学 Agent 开发，该按什么顺序学

<a href="https://apidock.ai/">
  <img src="https://file1.kamacoder.com/i/web/2026-07-10_19-29-47.jpg?v=20261005" style="width:100%;cursor:pointer;" alt="KamaClaude">
</a>


很多录友单独来问：**我就想学 AI Agent，该怎么入门？**

先说清一件事：**Agent 学习路线，本质上就是大模型学习路线的一段。** Agent 不是一个独立的新技术，它是"大模型 + 会调工具 + 会用记忆 + 会自己决定下一步"拼出来的系统。所以你没法跳过前面直接学 Agent——前面缺了地基，学 Agent 就是背名词。

如果你还没看过整条主线，建议先扫一眼[大模型学习路线](<../01%20%E5%85%A5%E9%97%A8%E4%B8%8E%E9%80%89%E5%9E%8B/15%20%E5%A4%A7%E6%A8%A1%E5%9E%8B%E5%AD%A6%E4%B9%A0%E8%B7%AF%E7%BA%BF%EF%BC%9A%E7%A8%8B%E5%BA%8F%E5%91%98%E4%BB%8E%E9%9B%B6%E5%85%A5%E9%97%A8%E5%88%B0%E4%B8%8A%E6%89%8B%E9%A1%B9%E7%9B%AE%EF%BC%8C%E8%AF%A5%E6%8C%89%E4%BB%80%E4%B9%88%E9%A1%BA%E5%BA%8F%E5%AD%A6.md>)，知道 Agent 在整张地图的哪个位置。这篇我们把镜头拉近，**只讲 Agent 这一段该怎么走。**

整段路线先放在这，下面六步逐个拆：

![AI Agent 学习路线：从打地基到工程兜底的六个步骤](<https://file1.kamacoder.com/i/web/20260616160117_agentroadmap.png?v=20261005>)

## 学 Agent 之前，先承认一个事实

Agent 是大模型应用里**最容易做出 Demo、也最容易翻车**的方向。

跟着教程，半小时就能搭一个"会调工具的 Agent"，看着很唬人。但一上真实业务，立刻死循环、乱调工具、上下文污染、权限越界……一地鸡毛。

所以学 Agent 的目标不是"搭一个能跑的 Demo"，而是**搞懂它为什么转得动、又为什么会翻车、翻车了怎么兜底**。下面这条路线就是照着这个目标排的。

## 第一步：补好两块地基——Prompt 调用 + Function Calling

别急着学 Agent。先确认两件事你会了：

一是能稳定地调用大模型、拿到**结构化输出**——Agent 的每一步决策都依赖模型吐出可解析的结构，输出不稳定，Agent 直接散架。

二是 **Function Calling**，这是 Agent 的命根子。Agent 之所以能"动手"，靠的就是 Function Calling 去调外部工具。这一篇必须先吃透：

- [结构化输出：JSON Schema 怎么约束](<36%20%E5%A4%A7%E6%A8%A1%E5%9E%8B%E7%BB%93%E6%9E%84%E5%8C%96%E8%BE%93%E5%87%BA%EF%BC%9A%E4%B8%BA%E4%BB%80%E4%B9%88%E8%87%AA%E7%84%B6%E8%AF%AD%E8%A8%80%E4%B8%8D%E7%A8%B3%E5%AE%9A%EF%BC%8CJSON%20Schema%E6%80%8E%E4%B9%88%E7%BA%A6%E6%9D%9F.md>)
- [Function Calling 详解：大模型怎么调用工具，为什么是 Agent 的基础](<16%20Function%20Calling%E8%AF%A6%E8%A7%A3%EF%BC%9A%E5%A4%A7%E6%A8%A1%E5%9E%8B%E6%80%8E%E4%B9%88%E8%B0%83%E7%94%A8%E5%B7%A5%E5%85%B7%EF%BC%8C%E4%B8%BA%E4%BB%80%E4%B9%88%E6%98%AFAgent%E7%9A%84%E5%9F%BA%E7%A1%80.md>)

这一步没过关，后面全是空中楼阁。

## 第二步：建立 Agent 认知——它到底和普通问答差在哪

目标：一句话讲清 Agent 是什么，以及它和"普通大模型问答"的本质区别。

很多人对 Agent 的理解停在"更会聊天"，错得离谱。核心区别是：**普通问答是答一句就结束，Agent 是围绕一个目标持续行动、边做边判断。**

- [Agent 到底是什么？和普通大模型问答有什么区别](<03%20Agent%E5%88%B0%E5%BA%95%E6%98%AF%E4%BB%80%E4%B9%88%EF%BC%9F%E5%92%8C%E6%99%AE%E9%80%9A%E5%A4%A7%E6%A8%A1%E5%9E%8B%E9%97%AE%E7%AD%94%E6%9C%89%E4%BB%80%E4%B9%88%E5%8C%BA%E5%88%AB%EF%BC%9F.md>)

这一篇是整条 Agent 路线的"定盘星"，理解偏了，后面越学越乱。

## 第三步：掌握 Agent 设计模式——ReAct、Reflection、规划执行

目标：知道 Agent 有哪几种主流"思路"，分别适合什么场景，面试被问到能讲出选型依据。

Agent 不是只有一种写法。工具调用型任务用 ReAct，需要自我检查的用 Reflection，复杂任务拆解用 Plan-and-Execute。这三种是面试高频：

- [ReAct、Reflection、规划执行：Agent 三种常见思路怎么选](<33%20ReAct%E3%80%81Reflection%E3%80%81%E8%A7%84%E5%88%92%E6%89%A7%E8%A1%8C%EF%BC%9AAgent%E4%B8%89%E7%A7%8D%E5%B8%B8%E8%A7%81%E6%80%9D%E8%B7%AF%E6%80%8E%E4%B9%88%E9%80%89%EF%BC%9F.md>)

然后是一个最容易被忽视、却最能体现工程判断力的问题——**很多场景根本不需要 Agent**：

- [Agent vs Workflow：什么时候根本不需要 Agent](<07%20Agent%20vs%20Workflow%EF%BC%9A%E4%BB%80%E4%B9%88%E6%97%B6%E5%80%99%E6%A0%B9%E6%9C%AC%E4%B8%8D%E9%9C%80%E8%A6%81%20Agent%EF%BC%9F.md>)

能讲清"什么时候不用 Agent"，比会写十个 Agent Demo 更值钱。"过度 Agent 化"是新手最常踩的坑。

## 第四步：工具与协议——Agent 的上限由工具决定

目标：理解 Agent 能干多少事，取决于你给它的工具设计得好不好；并搞懂 MCP 是怎么回事。

- [工具设计决定 Agent 上限：Tool Use、参数 Schema、返回值怎么设计](<06%20%E5%B7%A5%E5%85%B7%E8%AE%BE%E8%AE%A1%E5%86%B3%E5%AE%9A%20Agent%20%E4%B8%8A%E9%99%90.md>)
- [MCP 协议详解：Agent 工具调用的新标准，和 Function Calling 有什么区别](<21%20MCP%E5%8D%8F%E8%AE%AE%EF%BC%9AAgent%E5%B7%A5%E5%85%B7%E8%B0%83%E7%94%A8%E7%9A%84%E6%96%B0%E6%A0%87%E5%87%86.md>)

MCP 是这两年 Agent 工程绕不开的关键词，面试越来越爱问，务必能讲清它和 Function Calling 的关系。

## 第五步：工程兜底——Agent 为什么翻车，怎么兜住

目标：知道 Agent 在生产里有哪些典型故障，以及怎么设兜底机制。这是从"会做 Demo"到"敢上线"的分水岭。

- [Agent 为什么容易翻车？死循环、误调用、上下文污染、权限越界怎么兜底](<02%20Agent%E4%B8%BA%E4%BB%80%E4%B9%88%E5%AE%B9%E6%98%93%E7%BF%BB%E8%BD%A6%EF%BC%9F.md>)

面试官最爱在这里钻——"你的 Agent 陷入死循环怎么办""它调错工具怎么兜底"。答得上来，立刻和只会跑 Demo 的人拉开差距。

## 第六步：记忆与评估——让 Agent 可靠、可衡量

目标：搞懂 Agent 的记忆机制，以及怎么量化一个 Agent 到底靠不靠谱。

- [Agent 的记忆：短期记忆、长期记忆、RAG 到底什么关系](<05%20Agent%E7%9A%84%E8%AE%B0%E5%BF%86%EF%BC%9A%E7%9F%AD%E6%9C%9F%E3%80%81%E9%95%BF%E6%9C%9F%E3%80%81RAG%E5%88%B0%E5%BA%95%E4%BB%80%E4%B9%88%E5%85%B3%E7%B3%BB%EF%BC%9F.md>)
- [Agent 怎么评估？任务完成率与可靠性度量](<01%20Agent%E6%80%8E%E4%B9%88%E8%AF%84%E4%BC%B0%EF%BC%9F%E4%BB%BB%E5%8A%A1%E5%AE%8C%E6%88%90%E7%8E%87%E4%B8%8E%E5%8F%AF%E9%9D%A0%E6%80%A7%E5%BA%A6%E9%87%8F.md>)

这里你会发现 Agent 和 RAG 是连在一起的——长期记忆很多时候就是用 RAG 实现的。所以如果你 RAG 那段跳过了，建议补回来，看[大模型学习路线](<../01%20%E5%85%A5%E9%97%A8%E4%B8%8E%E9%80%89%E5%9E%8B/15%20%E5%A4%A7%E6%A8%A1%E5%9E%8B%E5%AD%A6%E4%B9%A0%E8%B7%AF%E7%BA%BF%EF%BC%9A%E7%A8%8B%E5%BA%8F%E5%91%98%E4%BB%8E%E9%9B%B6%E5%85%A5%E9%97%A8%E5%88%B0%E4%B8%8A%E6%89%8B%E9%A1%B9%E7%9B%AE%EF%BC%8C%E8%AF%A5%E6%8C%89%E4%BB%80%E4%B9%88%E9%A1%BA%E5%BA%8F%E5%AD%A6.md>)里的 RAG 阶段。

## 这条 Agent 路线要走多久

如果前面 Prompt 和 Function Calling 的底子已经打好，**Agent 这一段大概两到三周能走完一遍**，再配一个能自己干活的小项目（比如一个会查资料、会调工具、能自己规划步骤的小助手），就足以应付大部分 Agent 开发岗的面试。

记住顺序：**先认知 → 再设计模式 → 再工具 → 再兜底 → 再记忆评估。** 别一上来就堆框架、抄 Demo，那样学完只会用，一问原理和兜底就露馅。

## 顺手准备 Agent 面试

Agent 是现在面试问得最细的方向之一。相关面试题我整理在[大模型面经](<../../05%20%E9%9D%A2%E8%AF%95%E7%BB%83%E4%B9%A0/02%20%E5%A4%A7%E6%A8%A1%E5%9E%8B%E4%B8%93%E9%A2%98%E9%9D%A2%E8%AF%95/24%20%E5%A4%A7%E6%A8%A1%E5%9E%8B%E9%9D%A2%E7%BB%8F%E6%B1%87%E6%80%BB%EF%BC%9AAgent%E3%80%81RAG%E3%80%81Transformer%E3%80%81AI%E7%BC%96%E7%A8%8B%E5%A4%A7%E5%8E%82%E9%9D%A2%E8%AF%95%E9%A2%98.md>)里，简历怎么把 Agent 项目写出彩，可以看[简历专栏](<../../05%20%E9%9D%A2%E8%AF%95%E7%BB%83%E4%B9%A0/03%20%E9%A1%B9%E7%9B%AE%E8%A1%A8%E8%BE%BE%E4%B8%8E%E7%AE%80%E5%8E%86/02%20%E7%AE%80%E5%8E%86%E4%B8%93%E6%A0%8F.md>)。

我也在[知识星球](<https://mp.weixin.qq.com/s/lLq0U6momirYMwzqyQ5KXg>)里带过不少录友做 Agent 项目、抠面试细节，路线和项目一路盯着改。

想看完整的大模型知识体系，回到[卡码大模型专栏首页](<../00%20%E7%9B%AE%E5%BD%95.md>)，Agent 只是其中一章，前后串起来才是完整的战斗力。


---

[书架](../../00%20%E4%B9%A6%E6%9E%B6.md) · [本书目录](../00%20%E7%9B%AE%E5%BD%95.md) · [上一节](03%20Agent%E5%88%B0%E5%BA%95%E6%98%AF%E4%BB%80%E4%B9%88%EF%BC%9F%E5%92%8C%E6%99%AE%E9%80%9A%E5%A4%A7%E6%A8%A1%E5%9E%8B%E9%97%AE%E7%AD%94%E6%9C%89%E4%BB%80%E4%B9%88%E5%8C%BA%E5%88%AB%EF%BC%9F.md) · [下一节](05%20Agent%E7%9A%84%E8%AE%B0%E5%BF%86%EF%BC%9A%E7%9F%AD%E6%9C%9F%E3%80%81%E9%95%BF%E6%9C%9F%E3%80%81RAG%E5%88%B0%E5%BA%95%E4%BB%80%E4%B9%88%E5%85%B3%E7%B3%BB%EF%BC%9F.md)

<details><summary>原文与配套实操</summary>

本页来自本地教程，阅读版不执行代码。

打开原文件（本机路径未随仓库分发）。需要运行代码时，请打开“大模型实操”工作区。

</details>
