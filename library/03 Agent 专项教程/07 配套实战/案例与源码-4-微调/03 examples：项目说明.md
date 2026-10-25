[书架](../../../00%20%E4%B9%A6%E6%9E%B6.md) · [本书目录](../../00%20%E7%9B%AE%E5%BD%95.md) · [上一节](02%20%E6%8F%90%E7%A4%BA%E8%AF%8D%E4%B8%8E%20Adapter%EF%BC%9A%E9%80%90%E6%9D%A1%E6%A0%B8%E5%AF%B9%E8%AE%B0%E5%BD%95.md) · [下一节](04%20%E9%AA%8C%E8%AF%81%E6%A0%B7%E6%9C%AC%E7%9A%84%E5%8F%82%E8%80%83%E6%A0%87%E6%B3%A8%E5%A4%8D%E6%A0%B8.md)

---

# 微调示例：阅读、比较与复算

这里保存正文用到的回答与检查结果。先读对应章节，再选一组示例对照；不需要连接 GPU 就能阅读或重新评分。模型原始回答保留了分析段、英文片段、漏词和重复，方便区分格式问题与内容问题。

## 按问题查找

| 想弄清的问题 | 示例 |
| --- | --- |
| 换提示词与加载 Adapter 分别有什么影响？ | [10 条输入、40 份回答](<02%20%E6%8F%90%E7%A4%BA%E8%AF%8D%E4%B8%8E%20Adapter%EF%BC%9A%E9%80%90%E6%9D%A1%E6%A0%B8%E5%AF%B9%E8%AE%B0%E5%BD%95.md>)；[A/B/C 提示词定义](<LOCAL_FILE_NOT_INCLUDED> ':ignore') |
| 为什么关闭思考后仍输出分析？ | [两种模型状态、两种模板的 12 份回答](<05%20%E6%80%9D%E8%80%83%E6%A8%A1%E5%BC%8F%E8%AF%8A%E6%96%AD%EF%BC%9A12%20%E6%9D%A1%E9%A2%84%E6%B5%8B%E9%80%90%E6%9D%A1%E6%A0%B8%E5%AF%B9.md>) |
| 参考答案也需要检查吗？ | [10 条参考标注审核草案](<04%20%E9%AA%8C%E8%AF%81%E6%A0%B7%E6%9C%AC%E7%9A%84%E5%8F%82%E8%80%83%E6%A0%87%E6%B3%A8%E5%A4%8D%E6%A0%B8.md>) |
| 用户输入与答案如何成为 token 和标签？ | [预处理报告](<LOCAL_FILE_NOT_INCLUDED> ':ignore') 与 [1,800 条长度记录](<LOCAL_FILE_NOT_INCLUDED> ':ignore')，配合第 30 章第 4.2 节阅读 |
| 部署环境与接口返回应检查什么？ | [依赖版本清单](<LOCAL_FILE_NOT_INCLUDED> ':ignore')、[Python 请求与响应](<LOCAL_FILE_NOT_INCLUDED> ':ignore')，配合第 32 章阅读 |

标注草案用于讨论选词规则，没有替换 `keywords-clean` 数据，也没有用于修改配套分数。提示词比较和模板比较使用验证集中的少量样本，不能当作正式业务准确率。

## 查看实际输入

`thinking-control/prompt-inspection.json` 保存两种模板生成的完整输入、token 编号、输入末尾与答案隔离检查。查看 `decoded_input` 可以读到模型实际接收的文本；查看 `input_ids` 可以逐个核对 token。

在该示例锁定的 LLaMA-Factory 版本中，`qwen3_nothink` 没有加入空思考区块，`qwen3` 配合 `enable_thinking=False` 会在助手起始位置加入。三条输入的两种包装仅相差末尾四个 token，用户消息相同，参考答案没有进入生成输入。

四组使用同一个 Qwen3-0.6B 基础模型；需要 Adapter 的组加载同一份 Adapter。实际参数均为 FP16，每批 1 条，关闭采样，生成上限 256，重复惩罚 1.0，种子 42。比较改变的是推理模板和是否加载 Adapter；Adapter 的训练模板为 `qwen3_nothink`。

原始模型加入空区块后，这三条回答不再含分析段，但仍有英文改写、漏词和重复。这说明输入包装会影响回答形式，不能据此保证所有输入都有效，或断言关键词质量已经合格。实际输入见 `thinking-control/prompt-inspection.json`，四份回答文件直接放在 `thinking-control/` 中，文件名标明模型状态、模板及关闭思考设置。

## 在本机复算模板示例

以下命令在**课程项目根目录**运行，使用 Python 3.10 或以上版本。它只读取已保存的回答，不生成新预测：


<details class="code-example"><summary>bash 示例（点击展开）</summary>

```bash
thinking_review_dir=$(mktemp -d)
python3 案例与源码-4-微调/examples/thinking-control/convert_control_predictions.py \
  --reference 案例与源码-4-微调/examples/thinking-control/验证输入.jsonl \
  --predictions 案例与源码-4-微调/examples/thinking-control/原始模型-qwen3-关闭思考.jsonl \
  --template qwen3 \
  --output "$thinking_review_dir/原始模型-qwen3-关闭思考.jsonl"
python3 案例与源码-4-微调/evaluate_keywords_predictions.py \
  --reference 案例与源码-4-微调/examples/thinking-control/验证输入.jsonl \
  --predictions "$thinking_review_dir/原始模型-qwen3-关闭思考.jsonl" \
  --require-all \
  --output "$thinking_review_dir/原始模型-qwen3-关闭思考-评分.json"
```

</details>

四组共用 `examples/thinking-control/验证输入.jsonl`。查看或复算时，按下表选择回答文件与模板参数；这些文件都位于 `examples/thinking-control/`：

| 原始回答文件 | `--template` |
| --- | --- |
| [原始模型-qwen3_nothink-关闭思考.jsonl](<LOCAL_FILE_NOT_INCLUDED> ":ignore") | `qwen3_nothink` |
| [原始模型-qwen3-关闭思考.jsonl](<LOCAL_FILE_NOT_INCLUDED> ":ignore") | `qwen3` |
| [Adapter-qwen3_nothink-关闭思考.jsonl](<LOCAL_FILE_NOT_INCLUDED> ":ignore") | `qwen3_nothink` |
| [Adapter-qwen3-关闭思考.jsonl](<LOCAL_FILE_NOT_INCLUDED> ":ignore") | `qwen3` |

专用转换脚本检查两种已核验的完整输入包装，并复用课程通用转换器配对输入和参考答案；它不会删除或改写模型回答。错误包装、重复或缺失记录，以及参考答案不一致都会报错。

各 200 条测试预测的复算方法见[第 32 章第 4.4 节](<../../05%20%E5%BE%AE%E8%B0%83%E4%B8%8E%E9%83%A8%E7%BD%B2/05%2032-%E5%BE%AE%E8%B0%83%E6%95%88%E6%9E%9C%E8%AF%84%E4%BC%B0%E4%B8%8E%E6%A8%A1%E5%9E%8B%E9%83%A8%E7%BD%B2.md>)。提示词对照可以按下一节复算，部署版本与接口返回见本页开头的示例表。

## 在本机复算提示词示例

`prompt-comparison/data/` 保存三种提示词对应的完整输入与参考答案，四份原始回答文件直接放在 `prompt-comparison/` 中。原始模型分别使用 A、B、C；加载 Adapter 后使用同一份 B 输入。每组 10 条，共 40 条。

四组均使用 Qwen3-0.6B、`qwen3_nothink` 模板、关闭思考设置、FP16、每批 1 条、输入上限 2,048 token、关闭采样、生成上限 256、重复惩罚 1.0 和种子 42。原始模型在这些设置下仍输出分析，因此要同时检查格式和内容，不能仅凭关闭思考设置判断回答形式。

下面以原始模型 B 组为例，在**课程项目根目录**运行，只转换和评分已保存的回答：


<details class="code-example"><summary>bash 示例（点击展开）</summary>

```bash
prompt_review_dir=$(mktemp -d)
python3 案例与源码-4-微调/convert_keywords_predictions.py \
  --reference 案例与源码-4-微调/examples/prompt-comparison/data/keywords_prompt_b.jsonl \
  --predictions 案例与源码-4-微调/examples/prompt-comparison/原始模型-提示词B.jsonl \
  --output "$prompt_review_dir/原始模型-提示词B.jsonl"
python3 案例与源码-4-微调/evaluate_keywords_predictions.py \
  --reference 案例与源码-4-微调/examples/prompt-comparison/data/keywords_prompt_b.jsonl \
  --predictions "$prompt_review_dir/原始模型-提示词B.jsonl" \
  --require-all \
  --output "$prompt_review_dir/原始模型-提示词B-评分.json"
```

</details>

复算其他组时，同时替换参考文件、回答文件和输出文件名。下表中的路径均相对于 `examples/prompt-comparison/`：

| 原始回答文件 | 对应的参考文件 |
| --- | --- |
| [原始模型-提示词A.jsonl](<LOCAL_FILE_NOT_INCLUDED> ":ignore") | `data/keywords_prompt_a.jsonl` |
| [原始模型-提示词B.jsonl](<LOCAL_FILE_NOT_INCLUDED> ":ignore") | `data/keywords_prompt_b.jsonl` |
| [原始模型-提示词C.jsonl](<LOCAL_FILE_NOT_INCLUDED> ":ignore") | `data/keywords_prompt_c.jsonl` |
| [Adapter-提示词B.jsonl](<LOCAL_FILE_NOT_INCLUDED> ":ignore") | `data/keywords_prompt_b.jsonl` |

参考文件必须与该组提示词一致，不能直接使用未添加提示词要求的验证集，也不能使用 200 条测试集替代。自动精确匹配分数还需结合原文依据、术语全称和参考标注疑点阅读。


---

[书架](../../../00%20%E4%B9%A6%E6%9E%B6.md) · [本书目录](../../00%20%E7%9B%AE%E5%BD%95.md) · [上一节](02%20%E6%8F%90%E7%A4%BA%E8%AF%8D%E4%B8%8E%20Adapter%EF%BC%9A%E9%80%90%E6%9D%A1%E6%A0%B8%E5%AF%B9%E8%AE%B0%E5%BD%95.md) · [下一节](04%20%E9%AA%8C%E8%AF%81%E6%A0%B7%E6%9C%AC%E7%9A%84%E5%8F%82%E8%80%83%E6%A0%87%E6%B3%A8%E5%A4%8D%E6%A0%B8.md)

<details><summary>原文与配套实操</summary>

本页来自本地教程，阅读版不执行代码。

打开原文件（本机路径未随仓库分发）。需要运行代码时，请打开“大模型实操”工作区。

</details>
