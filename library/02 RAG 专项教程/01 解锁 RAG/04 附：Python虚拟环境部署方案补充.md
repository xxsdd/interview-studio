[书架](../../00%20%E4%B9%A6%E6%9E%B6.md) · [本书目录](../00%20%E7%9B%AE%E5%BD%95.md) · [上一节](03%20%E7%AC%AC%E4%B8%89%E8%8A%82%20%E5%9B%9B%E6%AD%A5%E6%9E%84%E5%BB%BARAG.md) · [下一节](../02%20%E6%95%B0%E6%8D%AE%E5%87%86%E5%A4%87/01%20%E7%AC%AC%E4%B8%80%E8%8A%82%20%E6%95%B0%E6%8D%AE%E5%8A%A0%E8%BD%BD.md)

---

# 附：Python虚拟环境部署方案补充

本项目由于涉及到的包过多，并且**依赖问题**自始至终都是Python的老大难问题，这就造成了 Python 工程化方面生态非常割裂。

对于这种问题，uv提供了统一的虚拟环境管理入口，同时吸收了 Rust 语言先进的包管理经验，使用它可以减少我们在 Python 工程方面折腾的时间，下面我们使用uv来安装项目的虚拟环境。

## 1.1 uv 环境管理

### 1.1.1 Windows 系统

**使用powershell 安装 uv**


<details class="code-example"><summary>bash 示例（点击展开）</summary>

```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

</details>

**安装成功后，按照提示输入以下命令添加环境变量**。这里注意，**不同的人的安装路径不同**，请按照提示自行复制粘贴命令。



<details class="code-example"><summary>bash 示例（点击展开）</summary>

```bash
$env:Path = "C:\Users\michaelbradley\.local\bin;$env:Path" 
```

</details>

![安装成功的提示](<../../_resources/9a34e23f80152831.webp>)


**输入 uv 命令，如果出现以下提示，说明安装成功**

![成功安装uv](<../../_resources/df080298a4a0b25f.webp>)

### 1.1.2 Linux / MacOS 系统

**使用 curl 安装 uv**


<details class="code-example"><summary>bash 示例（点击展开）</summary>

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

</details>

如果无法使用 curl 命令，**使用 wget 命令**安装 uv


<details class="code-example"><summary>bash 示例（点击展开）</summary>

```bash
wget -qO- https://astral.sh/uv/install.sh | sh
```

</details>

**输入 uv 命令，如果出现以下提示，说明安装成功**

![成功安装uv](<../../_resources/0f5bab327b05de78.webp>)


## 1.2 创建并激活虚拟环境

### 1.2.1  **创建虚拟环境**


<details class="code-example"><summary>bash 示例（点击展开）</summary>

```bash
uv venv rag --python 3.12.7
```

</details>

代码创建的虚拟环境名称为 rag ，使用Python版本为 3.12.7

Windows 系统创建成功后显示如下信息：


<details class="code-example"><summary>bash 示例（点击展开）</summary>

```bash
PS C:\Users\parallel> uv venv rag --python 3.12.7
Using CPython 3.12.7
Creating virtual environment at: rag
Activate with: rag\Scripts\activate
```

</details>

Linux / MacOS 系统创建成功后显示如下信息：


<details class="code-example"><summary>bash 示例（点击展开）</summary>

```bash
┌──(parallel㉿pacman)-[~/桌面]
└─$ uv venv rag -p 3.12.7
Using CPython 3.12.7
Creating virtual environment at: rag
Activate with: source rag/bin/activate
```

</details>

### 1.2.2  **激活虚拟环境**

Windows 系统激活虚拟环境命令为：


<details class="code-example"><summary>bash 示例（点击展开）</summary>

```bash
rag\Scripts\activate
```

</details>

Linux / MacOS 系统激活虚拟环境命令为：


<details class="code-example"><summary>bash 示例（点击展开）</summary>

```bash
source rag/bin/activate
```

</details>


---

[书架](../../00%20%E4%B9%A6%E6%9E%B6.md) · [本书目录](../00%20%E7%9B%AE%E5%BD%95.md) · [上一节](03%20%E7%AC%AC%E4%B8%89%E8%8A%82%20%E5%9B%9B%E6%AD%A5%E6%9E%84%E5%BB%BARAG.md) · [下一节](../02%20%E6%95%B0%E6%8D%AE%E5%87%86%E5%A4%87/01%20%E7%AC%AC%E4%B8%80%E8%8A%82%20%E6%95%B0%E6%8D%AE%E5%8A%A0%E8%BD%BD.md)

<details><summary>原文与配套实操</summary>

本页来自本地教程，阅读版不执行代码。

打开原文件（本机路径未随仓库分发）。需要运行代码时，请打开“大模型实操”工作区。

</details>
