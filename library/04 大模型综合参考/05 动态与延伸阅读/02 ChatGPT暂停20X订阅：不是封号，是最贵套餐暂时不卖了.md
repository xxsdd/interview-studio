[书架](../../00%20%E4%B9%A6%E6%9E%B6.md) · [本书目录](../00%20%E7%9B%AE%E5%BD%95.md) · [上一节](01%20ChatGPT%E3%80%81Claude%E3%80%81Grok%E5%90%8C%E6%97%B6%E5%AE%95%E6%9C%BA%EF%BC%9A%E9%87%8D%E5%8F%A093%E5%88%86%E9%92%9F%EF%BC%8C%E4%BD%86%E2%80%9C%E5%90%8C%E4%B8%80%E4%B8%AA%E5%85%83%E5%87%B6%E2%80%9D%E6%B2%A1%E6%9C%89%E8%AF%81%E6%8D%AE.md) · [下一节](03%20Claude%E8%AF%B4%E6%B0%B8%E4%B9%85%2B25%25%EF%BC%8CCodex%E7%BB%99%E4%BD%A0%E9%87%8D%E7%BD%AE%E9%A2%9D%E5%BA%A6%EF%BC%9A%E4%B8%A4%E5%AE%B6%E5%85%AC%E5%8F%B8%E7%BB%88%E4%BA%8E%E5%BC%80%E5%A7%8B%E8%A7%A3%E9%87%8A%E2%80%9C%E9%A2%9D%E5%BA%A6%E5%8E%BB%E5%93%AA%E4%BA%86%E2%80%9D.md)

---

# ChatGPT暂停20X订阅：不是封号，是最贵套餐暂时不卖了

GPT-6 Astra 需求过大，导致 OpenAI 停售 pro 20X。

![](<https://file1.kamacoder.com/i/web/d1ca3c402ba6cf688ef71ca01d608273.jpg?v=20261005>) 

前几天写 [GPT-6 Astra](<30%20GPT-6%20Astra%E5%8F%91%E5%B8%83%EF%BC%9A%E8%B7%91%E5%88%86%E5%87%A0%E4%B9%8E%E5%88%B7%E6%BB%A1%EF%BC%8C%E4%BD%86%E6%88%91%E6%9B%B4%E5%9C%A8%E6%84%8F%E5%AE%83%E5%BC%80%E5%A7%8B%E6%8E%A5%E7%AE%A1%E9%BC%A0%E6%A0%87%E4%BA%86.md>) 时，最现实的问题还是“什么时候轮到我的账号”。

现在问题变成了：**就算你想花每月 200 美元，也不一定买得到最高档 Pro。**

2026 年 9 月 10 日，OpenAI 暂停了 ChatGPT Pro 200 美元套餐，也就是 Pro 20X 的新订阅和升级。

目前国内知名的ChatGPT代充平台 [PayAI.plus](<https://payai.plus/chatgpt>) ，也显示 20x全面缺货：

![](<https://file1.kamacoder.com/i/web/20260911094411-av8nss.png?v=20261005>) 

**但 5x 依然可以购买，大家需要pro 5x ，可以抓紧去  [PayAI.plus](<https://payai.plus/chatgpt>) 冲，估计 5x也很快就没货了**。 

![](<https://file1.kamacoder.com/i/web/20260911094445-buzfvg.png?v=20261005>)


## 购买页已经置灰：20X有钱也暂时买不到

用户公开的购买页截图里，20X 已经变灰，并提示“暂时不接受新购买，现有订阅不受影响”。

![](<https://file1.kamacoder.com/i/web/20260911095655-lapq99.png?v=20261005>)

OpenAI 帮助中心随后把边界写得更细：Free、Go、Plus 和 Pro 100 美元用户都不能在暂停期间升到 Pro 200 美元。

原来已经订阅 200 美元档的用户，权益和自动续费不变。

真正容易踩坑的是“我先降级，下个月再升回来”。

如果你安排了降级或取消，在当前计费周期结束前仍能撤销；一旦变更正式生效，20X 权益结束，就不能重新购买，直到 OpenAI 解除暂停。

续费失败也要小心。支付问题如果最终导致订阅被取消，同样可能暂时回不去。通过 Apple 或 Google Play 订阅的用户，要按应用商店的支付恢复流程处理。

## 为什么偏偏暂停最贵的套餐

OpenAI 给出的直接原因不是支付问题，也不是套餐重做，而是 **GPT-6 Astra 带来的容量压力**。

9 月 9 日，OpenAI 的 Tibo Sottiaux 已经公开预警：Astra 的需求“前所未有”，团队在调动所有能用的资源；如果需求继续上涨，可能暂时停止新的 Pro 订阅，以优先保证现有用户体验。

![](<https://file1.kamacoder.com/i/web/ac95dff98ce278234583e1bf93f8e888.jpg?v=20261005>)

一天后，预警变成实际措施。

Tibo 随后说明，200 美元 Pro 给系统带来的压力最大。暂停这一档，是 OpenAI 认为影响面最小、又能继续让更多用户使用 Astra 的办法；其他套餐和 API 保持开放，公司正在增加容量。

这和 Astra 的使用方式有关。

传统聊天通常是一问一答。Astra 在 Work 和 Codex 里会读文件、调用工具、操作电脑、运行代码、失败重试，一项任务可能连续跑很久。模型越强、Agent 跑得越长，每位重度用户占用的推理算力就越高。

OpenAI 官方按五小时窗口给出的估算也能看出跨度：Pro 20X 用 Astra 可能覆盖约 100～900 条本地消息，而用较轻的 Luna 可能达到 5,000～40,000 条。

这不是固定消息数，任务复杂度、推理档位和工具使用都会改变消耗。但它至少解释了，为什么“20 倍额度”并不等于 Astra 可以随便跑。


## 这次停售真正说明了什么

过去的云服务喜欢讲“弹性无限”，现在的 AI 服务开始反复提醒我们：最先进模型的算力仍然是稀缺资源。

当一个每月 200 美元的高价套餐，因为需求过大而停止接收新用户，说明竞争已经不只是“谁的模型分数高”。

模型公司还要回答另一道更难的题：**能力发布之后，能不能稳定、透明、可持续地供给给所有付费用户。**

对录友来说也一样。

别把生产力绑在一个随时可能满载的套餐上。把模型分层、任务分级、上下文和交付物留在本地，才不会在下一次停售、限流或宕机时原地停工。

20X 只是暂时关门。

但算力不再能靠一句“升级最高档”解决，这件事已经很清楚了。

## 资料来源

* OpenAI 帮助中心：ChatGPT Pro 套餐与 200 美元档暂停 FAQ：https://help.openai.com/en/articles/9793128-about-chatgpt-pro-tiers

* Tibo Sottiaux：暂停 200 美元 Pro 新订阅的公开说明：https://x.com/thsottiaux/status/2098113585683808624

* OpenAI：GPT-6 Astra 官方发布与开放范围：https://openai.com/index/gpt-6-astra/

* OpenAI 帮助中心：Astra 在 Work 和 Codex 中的用量说明：https://help.openai.com/en/articles/20001516-managing-usage-with-gpt-6-astra-in-work-and-codex

* OpenAI：ChatGPT Pro 200 美元套餐最初发布公告：https://openai.com/index/introducing-chatgpt-pro/



---

[书架](../../00%20%E4%B9%A6%E6%9E%B6.md) · [本书目录](../00%20%E7%9B%AE%E5%BD%95.md) · [上一节](01%20ChatGPT%E3%80%81Claude%E3%80%81Grok%E5%90%8C%E6%97%B6%E5%AE%95%E6%9C%BA%EF%BC%9A%E9%87%8D%E5%8F%A093%E5%88%86%E9%92%9F%EF%BC%8C%E4%BD%86%E2%80%9C%E5%90%8C%E4%B8%80%E4%B8%AA%E5%85%83%E5%87%B6%E2%80%9D%E6%B2%A1%E6%9C%89%E8%AF%81%E6%8D%AE.md) · [下一节](03%20Claude%E8%AF%B4%E6%B0%B8%E4%B9%85%2B25%25%EF%BC%8CCodex%E7%BB%99%E4%BD%A0%E9%87%8D%E7%BD%AE%E9%A2%9D%E5%BA%A6%EF%BC%9A%E4%B8%A4%E5%AE%B6%E5%85%AC%E5%8F%B8%E7%BB%88%E4%BA%8E%E5%BC%80%E5%A7%8B%E8%A7%A3%E9%87%8A%E2%80%9C%E9%A2%9D%E5%BA%A6%E5%8E%BB%E5%93%AA%E4%BA%86%E2%80%9D.md)

<details><summary>原文与配套实操</summary>

本页来自本地教程，阅读版不执行代码。

打开原文件（本机路径未随仓库分发）。需要运行代码时，请打开“大模型实操”工作区。

</details>
