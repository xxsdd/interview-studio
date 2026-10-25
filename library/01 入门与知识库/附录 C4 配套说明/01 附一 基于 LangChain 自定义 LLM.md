[书架](../../00%20%E4%B9%A6%E6%9E%B6.md) · [本书目录](../00%20%E7%9B%AE%E5%BD%95.md) · [上一节](../%E9%99%84%E5%BD%95%20C3%20%E9%85%8D%E5%A5%97%E8%AF%B4%E6%98%8E/01%20Embedding%E5%B0%81%E8%A3%85%E8%AE%B2%E8%A7%A3.md)

---

# 附一 基于 LangChain 自定义 LLM

LangChain 为基于 LLM 开发自定义应用提供了高效的开发框架，便于开发者迅速地激发 LLM 的强大能力，搭建 LLM 应用。LangChain 也同样支持多种大模型，内置了 OpenAI、LLAMA 等大模型的调用接口。但是，LangChain 并没有内置所有大模型，它通过允许用户自定义 LLM 类型，来提供强大的可扩展性。

在本部分，我们以智谱为例，讲述如何基于 LangChain 自定义 LLM，让我们基于 LangChain 搭建的应用能够支持国内平台。

本部分涉及相对更多 LangChain、大模型调用的技术细节，有精力同学可以学习部署，如无精力可以直接使用后续代码来支持调用。

要实现自定义 LLM，需要定义一个自定义类继承自 LangChain 的 LLM 基类，然后定义两个函数：  
① _generate 方法，接收一系列消息及其他参数，并返回输出；  
② _stream 方法， 接收一系列消息及其他参数，并以流式返回结果。  

首先我们导入所需的第三方库：



<details class="code-example"><summary>python 示例（点击展开）</summary>

```python
from typing import Any, Dict, Iterator, List, Optional
from zhipuai import ZhipuAI
from langchain_core.callbacks import (
    CallbackManagerForLLMRun,
)
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import (
    AIMessage,
    AIMessageChunk,
    BaseMessage,
    SystemMessage,
    ChatMessage,
    HumanMessage
)
from langchain_core.messages.ai import UsageMetadata
from langchain_core.outputs import ChatGeneration, ChatGenerationChunk, ChatResult
import time
```

</details>

由于LangChain的消息类型是`HumanMessage`、`AIMessage`等格式，与一般模型接收的字典格式不一样，因此我们需要先定义一个将LangChain的格式转为字典的函数。



<details class="code-example"><summary>python 示例（点击展开）</summary>

```python
def _convert_message_to_dict(message: BaseMessage) -> dict:
    """把LangChain的消息格式转为智谱支持的格式
    Args:
        message: The LangChain message.
    Returns:
        The dictionary.
    """
    message_dict: Dict[str, Any] = {"content": message.content}
    if (name := message.name or message.additional_kwargs.get("name")) is not None:
        message_dict["name"] = name

    # populate role and additional message data
    if isinstance(message, ChatMessage):
        message_dict["role"] = message.role
    elif isinstance(message, HumanMessage):
        message_dict["role"] = "user"
    elif isinstance(message, AIMessage):
        message_dict["role"] = "assistant"
    elif isinstance(message, SystemMessage):
        message_dict["role"] = "system"
    else:
        raise TypeError(f"Got unknown type {message}")
    return message_dict
```

</details>

接着我们定义一个继承自 LLM 类的自定义 LLM 类：



<details class="code-example"><summary>python 示例（点击展开）</summary>

```python
# 继承自 LangChain 的 BaseChatModel 类
class ZhipuaiLLM(BaseChatModel):
    """自定义Zhipuai聊天模型。
    """
    model_name: str = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    timeout: Optional[int] = None
    stop: Optional[List[str]] = None
    max_retries: int = 3
    api_key: str | None = None
```

</details>

上述初始化涵盖了我们平时常用的参数，也可以根据实际需求与智谱的 API 加入更多的参数。

接下来我们实现_generate方法：



<details class="code-example"><summary>python 示例（点击展开）</summary>

```python
    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        """通过调用智谱API从而响应输入。

        Args:
            messages: 由messages列表组成的prompt
            stop: 在模型生成的回答中有该字符串列表中的元素则停止响应
            run_manager: 一个为LLM提供回调的运行管理器
        """
        # 列表推导式 将 messages 的元素逐个转为智谱的格式
        messages = [_convert_message_to_dict(message) for message in messages]
        # 定义推理的开始时间
        start_time = time.time()
        # 调用 ZhipuAI 对处理消息
        response = ZhipuAI(api_key=self.api_key).chat.completions.create(
            model=self.model_name,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            timeout=self.timeout,
            stop=stop,
            messages=messages
        )
        # 计算运行时间 由现在时间 time.time() 减去 开始时间start_time得到
        time_in_seconds = time.time() - start_time
        # 将返回的消息封装并返回
        message = AIMessage(
            content=response.choices[0].message.content, # 响应的结果
            additional_kwargs={}, # 额外信息
            response_metadata={
                "time_in_seconds": round(time_in_seconds, 3), # 响应源数据 这里是运行时间 也可以添加其他信息
            },
            # 本次推理消耗的token
            usage_metadata={
                "input_tokens": response.usage.prompt_tokens, # 输入token
                "output_tokens": response.usage.completion_tokens, # 输出token
                "total_tokens": response.usage.total_tokens, # 全部token
            },
        )
        generation = ChatGeneration(message=message)
        return ChatResult(generations=[generation])
```

</details>

接下来我们实现另一核心的方法_stream，之前注释的代码本次不再注释：



<details class="code-example"><summary>python 示例（点击展开）</summary>

```python
    def _stream(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> Iterator[ChatGenerationChunk]:
        """通过调用智谱API返回流式输出。

        Args:
            messages: 由messages列表组成的prompt
            stop: 在模型生成的回答中有该字符串列表中的元素则停止响应
            run_manager: 一个为LLM提供回调的运行管理器
        """
        messages = [_convert_message_to_dict(message) for message in messages]
        response = ZhipuAI().chat.completions.create(
            model=self.model_name,
            stream=True, # 将stream 设置为 True 返回的是迭代器，可以通过for循环取值
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            timeout=self.timeout,
            stop=stop,
            messages=messages
        )
        start_time = time.time()
        # 使用for循环存取结果
        for res in response:
            if res.usage: # 如果 res.usage 存在则存储token使用情况
                usage_metadata = UsageMetadata(
                    {
                        "input_tokens": res.usage.prompt_tokens,
                        "output_tokens": res.usage.completion_tokens,
                        "total_tokens": res.usage.total_tokens,
                    }
                )
            # 封装每次返回的chunk
            chunk = ChatGenerationChunk(
                message=AIMessageChunk(content=res.choices[0].delta.content)
            )

            if run_manager:
                # This is optional in newer versions of LangChain
                # The on_llm_new_token will be called automatically
                run_manager.on_llm_new_token(res.choices[0].delta.content, chunk=chunk)
            # 使用yield返回 结果是一个生成器 同样可以使用for循环调用
            yield chunk
        time_in_sec = time.time() - start_time
        # Let's add some other information (e.g., response metadata)
        # 最终返回运行时间
        chunk = ChatGenerationChunk(
            message=AIMessageChunk(content="", response_metadata={"time_in_sec": round(time_in_sec, 3)}, usage_metadata=usage_metadata)
        )
        if run_manager:
            # This is optional in newer versions of LangChain
            # The on_llm_new_token will be called automatically
            run_manager.on_llm_new_token("", chunk=chunk)
        yield chunk
```

</details>

然后我们还需要定义一下模型的描述方法：



<details class="code-example"><summary>python 示例（点击展开）</summary>

```python
    @property
    def _llm_type(self) -> str:
        """获取此聊天模型使用的语言模型类型。"""
        return self.model_name

    @property
    def _identifying_params(self) -> Dict[str, Any]:
        """返回一个标识参数的字典。

        该信息由LangChain回调系统使用，用于跟踪目的，使监视llm成为可能。
        """
        return {
            "model_name": self.model_name,
        }
```

</details>

通过上述步骤，我们就可以基于 LangChain 定义智谱的调用方式了。我们将此代码封装在 zhipu_llm.py 文件中。

---

[书架](../../00%20%E4%B9%A6%E6%9E%B6.md) · [本书目录](../00%20%E7%9B%AE%E5%BD%95.md) · [上一节](../%E9%99%84%E5%BD%95%20C3%20%E9%85%8D%E5%A5%97%E8%AF%B4%E6%98%8E/01%20Embedding%E5%B0%81%E8%A3%85%E8%AE%B2%E8%A7%A3.md)

<details><summary>原文与配套实操</summary>

本页来自本地教程，阅读版不执行代码。

打开原文件（本机路径未随仓库分发）。需要运行代码时，请打开“大模型实操”工作区。

</details>
