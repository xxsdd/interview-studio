[书架](../../00%20%E4%B9%A6%E6%9E%B6.md) · [本书目录](../00%20%E7%9B%AE%E5%BD%95.md) · [上一节](../%E7%AC%AC%E4%B8%83%E7%AB%A0%20%E9%AB%98%E7%BA%A7%20RAG/02%20%E6%A3%80%E7%B4%A2%E4%BC%98%E5%8C%96/01%202.%20%E5%AF%B9%E9%BD%90%20query%20%E5%92%8C%E6%96%87%E6%A1%A3.md) · [下一节](../%E9%99%84%E5%BD%95%20C4%20%E9%85%8D%E5%A5%97%E8%AF%B4%E6%98%8E/01%20%E9%99%84%E4%B8%80%20%E5%9F%BA%E4%BA%8E%20LangChain%20%E8%87%AA%E5%AE%9A%E4%B9%89%20LLM.md)

---

# Embedding封装讲解
LangChain 为基于 LLM 开发自定义应用提供了高效的开发框架，便于开发者迅速地激发 LLM 的强大能力，搭建 LLM 应用。LangChain 也同样支持多种大模型的 Embeddings，内置了 OpenAI、LLAMA 等大模型 Embeddings 的调用接口。但是，LangChain 并没有内置所有大模型，它通过允许用户自定义 Embeddings 类型，来提供强大的可扩展性。

在本部分，我们以智谱 AI 为例，讲述如何基于 LangChain 自定义 Embeddings。

本部分涉及相对更多 LangChain、大模型调用的技术细节，有精力同学可以学习部署，如无精力可以直接使用后续代码来支持调用。

要实现自定义 Embeddings，需要定义一个自定义类继承自 LangChain 的 Embeddings 基类，然后定义两个函数：① embed_query 方法，用于对单个字符串（query）进行 embedding；②embed_documents 方法，用于对字符串列表（documents）进行 embedding。

首先我们导入所需的第三方库：



<details class="code-example"><summary>python 示例（点击展开）</summary>

```python
from typing import List
from langchain_core.embeddings import Embeddings
```

</details>

这里我们定义一个继承自 Embeddings 类的自定义 Embeddings 类：



<details class="code-example"><summary>python 示例（点击展开）</summary>

```python
class ZhipuAIEmbeddings(Embeddings):
    """`Zhipuai Embeddings` embedding models."""
    def __init__(self):
        """
        实例化ZhipuAI为values["client"]

        Args:

            values (Dict): 包含配置信息的字典，必须包含 client 的字段.
        Returns:

            values (Dict): 包含配置信息的字典。如果环境中有zhipuai库，则将返回实例化的ZhipuAI类；否则将报错 'ModuleNotFoundError: No module named 'zhipuai''.
        """
        from zhipuai import ZhipuAI
        self.client = ZhipuAI()
```

</details>

embed_documents 是对字符串列表（List[str]）计算embedding 的方法，这里我们重写该方法，调用验证环境时实例化的`ZhipuAI`来 调用远程 API 并返回 embedding 结果。



<details class="code-example"><summary>python 示例（点击展开）</summary>

```python
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        生成输入文本列表的 embedding.
        Args:
            texts (List[str]): 要生成 embedding 的文本列表.

        Returns:
            List[List[float]]: 输入列表中每个文档的 embedding 列表。每个 embedding 都表示为一个浮点值列表。
        """
        embeddings = self.client.embeddings.create(
            model="embedding-3",
            input=texts
        )
        return [embeddings.embedding for embeddings in embeddings.data]
```

</details>

`embed_query` 是对单个文本（str）计算 embedding 的方法，这里我们调用刚才定义好的`embed_documents`方法，并返回第一个子列表即可。



<details class="code-example"><summary>python 示例（点击展开）</summary>

```python
    def embed_query(self, text: str) -> List[float]:
        """
        生成输入文本的 embedding.

        Args:
            texts (str): 要生成 embedding 的文本.

        Return:
            embeddings (List[float]): 输入文本的 embedding，一个浮点数值列表.
        """

        return self.embed_documents([text])[0]
```

</details>

对于以上方法可以加入一些内容处理后再请求 embedding，比如文本特别长，我们可以考虑对文本分段，防止超过最大 token 限制，这些都是可以的，靠大家发挥自己的主观能动性完善啦，这里只是给出一个简单的 demo。

通过上述步骤，我们就可以基于 LangChain 与 智谱 AI 定义 embedding 的调用方式了。我们将此代码封装在 zhipuai_embedding.py 文件中。

---

[书架](../../00%20%E4%B9%A6%E6%9E%B6.md) · [本书目录](../00%20%E7%9B%AE%E5%BD%95.md) · [上一节](../%E7%AC%AC%E4%B8%83%E7%AB%A0%20%E9%AB%98%E7%BA%A7%20RAG/02%20%E6%A3%80%E7%B4%A2%E4%BC%98%E5%8C%96/01%202.%20%E5%AF%B9%E9%BD%90%20query%20%E5%92%8C%E6%96%87%E6%A1%A3.md) · [下一节](../%E9%99%84%E5%BD%95%20C4%20%E9%85%8D%E5%A5%97%E8%AF%B4%E6%98%8E/01%20%E9%99%84%E4%B8%80%20%E5%9F%BA%E4%BA%8E%20LangChain%20%E8%87%AA%E5%AE%9A%E4%B9%89%20LLM.md)

<details><summary>原文与配套实操</summary>

本页来自本地教程，阅读版不执行代码。

打开原文件（本机路径未随仓库分发）。需要运行代码时，请打开“大模型实操”工作区。

</details>
