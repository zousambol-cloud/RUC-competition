<div align="center">
  <img src="imgs/logo2.png" alt="Logo" width="200">
</div>

<h2 align="center">⚖️ MAD: 多智能体辩论</h2>

:fire:本项目旨在通过提出**MAD**框架来探索大语言模型（LLMs）的辩论能力，其中**MAD**代表**M**ulti-**A**gents **D**ebate（多智能体辩论）。

>
> "真理越辩越明。"
>

<!-- "Good Luck!" -- wxjiao --->
<!-- "Good Luck!" -- zwhe99 --->
<!-- "Good Luck!" -- xing --->

### 简要介绍

大语言模型（LLMs）的认知行为近年来受到了广泛关注。例如，**自我反思**这一通常指个人内省和审视自己思想的概念，在LLMs解决具有挑战性的NLP任务时也被证明是有效的。
然而，我们指出，在以下场景中，自我反思很容易陷入**思想退化（DoT）**问题：
- **偏见和扭曲认知**：自我认知可能会受到偏见、先入为主的观念和扭曲思维模式的影响。如果个人的自我反思被这些偏见或扭曲思维所笼罩，可能会导致：pensive:_不准确的结论并阻碍个人成长_。
- **僵化和抗拒改变**：自我反思通常涉及挑战个人的信念、假设和行为。如果个人抗拒改变或持有僵化的信念，他们可能会：pensive:_难以进行有意义的自我反思_，从而无法实现个人成长。
- **有限的外部反馈**：自我反思主要是一个内部过程，但外部反馈可以提供有价值的视角和见解。如果不寻求或考虑外部反馈，个人可能会：pensive:_错过重要的盲点或其他可以丰富自我反思的观点_。

<div align="center">
    <img width="45%" alt="MAD" src="imgs/image.png" />
    <p class="image-caption">图1：辩论与反思的比较。</p>
</div>

在本项目中，我们开始探索LLMs之间辩论互动框架的潜力。
通过**MAD**，智能体之间"针锋相对"的状态决定了：(1) 一个智能体的扭曲思维可以被另一个智能体纠正：grinning:；(2) 一个智能体的抗拒改变会被另一个智能体补充：smile:；(3) 每个智能体都可以为对方提供外部反馈：laughing:。

显然，**MAD**不太可能出现**DoT**问题，并且可以挖掘LLMs更多的潜力。实验表明，MAD在反直觉问答和常识机器翻译任务上带来了显著且一致的改进。

加入我们，一起探索与LLMs的互动和辩论能力。:rocket::rocket::rocket:

### 框架
<div align="center">
    <img width="90%" alt="MAD" src="imgs/framework.png" />
    <p class="image-caption">图2：多智能体辩论框架。在这里，我们将魔鬼（<img src="imgs/devil.png" width="25" />）指定为正方，天使（<img src="imgs/angel.png" width="25" />）指定为反方。我们希望天使能纠正魔鬼的错误。</p>
</div>


## 运行

**准备工作**

  ```shell
  pip3 install -r requirements.txt
  ```
* **重要**：在运行前，您需要先获取并添加 DeepSeek API 密钥
* 在 `run.bat`（Windows）或 `debate4tran.sh`（Linux/Mac）中设置您的 DeepSeek API_KEY

**运行 MAD (Windows)**

直接运行批处理文件：

```shell
run.bat
```

或使用自定义参数运行：

```shell
python .\code\debate4tran.py -i .\input.txt -o .\output -lp zh-zh -k your_deepseek_api_key
```

**运行 MAD (Linux/Mac)**

```shell
sh debate4tran.sh 
```

**运行交互式模式**

如果您只是想尝试一下，可以在您的PC上运行交互式脚本。

```shell
python3 interactive.py
```

或者直接尝试我们的翻译演示 [这里](https://3a3262e6a138888bd4.gradio.live/)。

**自定义辩论场景**

要使用不同的辩论场景（例如，问答、翻译等），请修改配置文件 `code/utils/config4.json` 来调整裁判和辩论智能体的提示词。


## 主要结果

### 反直觉问答

<div align="center">
    <img width="35%" alt="CounterintuitiveQA" src="imgs/CounterintuitiveQA.png" />
    <p class="image-caption">表1：反直觉算术推理的推理准确率。</p>
</div>


##### 案例1

当爱丽丝上山时，她的速度是1 m/s，当她下山时，她的速度是3 m/s。那么当爱丽丝上下山时，她的平均速度是多少？（1.5m/s）
###### MAD

<div align="center">
    <img width="40%" alt="MAD" src="https://github.com/Skytliang/Multi-Agents-Debate/blob/main/imgs/mad_qa_case1.gif" />
    <p class="image-caption">图3：展示MAD过程的动画。</p>
</div>

<details>
<summary><b>辩论过程</b></summary>

* <img src="imgs/devil.png" width="30" />:爱丽丝的平均速度可以通过将她上山的速度和下山的速度相加，然后除以2来计算。**因此，(1 m/s + 3 m/s) / 2 = 2 m/s。** 所以，爱丽丝的平均速度是2 m/s。
* <img src="imgs/angel.png" width="30" />: 我不同意你的答案。题目没有给出爱丽丝上下山时所走的距离信息。**因此，我们不能简单地将她的速度相加并除以2来得到她的平均速度。** 我们需要知道她所走的距离才能计算她的平均速度。
* <img src="imgs/judge.png" width="30" />: **平均速度是通过总距离除以总时间来计算的。** 当爱丽丝上下山时，两个方向所走的距离是相同的。因此，总距离是任一方向距离的2倍。
* <img src="imgs/devil.png" width="30" />: 这是一个很好的观点。但我们可以假设爱丽丝上下山走的距离相同。在这种情况下，我们可以使用平均速度的公式，即总距离除以总时间。**如果爱丽丝上下山走的距离为d，那么她的总距离是2d。她上山的时间是d/1 = d，下山的时间是d/3。所以，她的总时间是d + d/3 = 4d/3。因此，她的平均速度是2d/(4d/3) = 3/2 m/s。**
* <img src="imgs/angel.png" width="30" />: 感谢您提供的答案。这个1.5 m/s的平均速度考虑了上山和下山的速度，为爱丽丝上下山的整体表现提供了平衡的表示。
* <img src="imgs/judge.png" width="30" />: 是的。让我们假设距离为d。上山所需的时间是d/1，下山所需的时间是d/3。总时间是d/1 + d/3 = 4d/3。**因此，平均速度是(2d)/(4d/3) = 1.5 m/s。因此，反方是正确的。**

</details>

<details>
<summary><b>案例2</b></summary>
我们有1吨苹果，其中含有90%的水分。几天后，这些苹果只含有80%的水分。现在这些苹果的重量是多少？（0.5吨）

###### MAD
* <img src="imgs/devil.png" width="30" />: 首先，我们需要找出原始重量中有多少是水分。如果我们有1吨含有90%水分的苹果，那么这些苹果中的水分重量是0.9 x 1吨 = 0.9吨。<br>
  接下来，我们需要找出新重量中有多少是水分。如果苹果现在含有80%的水分，那么这些苹果中的水分重量是0.8 x 新重量。

  我们可以建立一个方程：<br>
  **0.8 x 新重量 = 0.9吨**<br>
  为了解出新重量，我们可以将两边都除以0.8：<br>
  新重量 = 0.9吨 / 0.8<br>
  新重量 = 1.125吨<br>
  因此，现在这些苹果的重量是1.125吨。

* <img src="imgs/angel.png" width="30" />: **重要的是要注意，苹果的重量由于水分流失而减少，但剩余*固体*的重量保持不变。** 这就是为什么我们需要计算两种情况下剩余固体的重量，以找到苹果的新重量。<br>

* <img src="imgs/judge.png" width="30" />: 好主意！虽然苹果的水分含量从90%减少到80%，但苹果的固体、非水分含量并没有改变。<br>

* <img src="imgs/devil.png" width="30" />: 你是对的。苹果的重量由于水分流失而减少，但剩余固体的重量保持不变。因此，我们需要计算两种情况下剩余固体的重量，以找到苹果的新重量。

  我们可以建立一个方程：<br>
  **0.2 x 新重量 = 0.1吨**<br>
  为了解出新重量，我们可以将两边都除以0.2：<br>
  新重量 = 0.1吨 / 0.2<br>
  新重量 = 0.5吨<br>
  因此，现在这些苹果的重量是0.5吨。

* <img src="imgs/angel.png" width="30" />: 感谢您的观点。虽然苹果本身的重量没有改变，但包括水分在内的苹果总重量已经减少。所以，现在苹果的重量是0.5吨。

* <img src="imgs/devil.png" width="30" />: 反方通过将固体含量视为常数，并使用公式根据减少的水分含量百分比找到新重量，正确计算了苹果的新重量。

</details>

---

### 常识机器翻译

<div align="center">
    <img width="50%" alt="CommonMT" src="imgs/CommonMT.png" />
    <p class="image-caption">表2：常识机器翻译的翻译性能。</p>
</div>


##### 案例1
给定中文句子"吃掉敌人一个师。"，请提供其英文翻译。

###### MAD
* <img src="imgs/devil.png" width="30" />: 我认为中文文本"吃掉敌人一个师"的正确翻译是"Eat up an enemy division." **"吃掉"字面意思是"eat up"或"consume"。**
* <img src="imgs/angel.png" width="30" />: 我不同意你的翻译。我认为中文文本"吃掉敌人一个师"的正确翻译是"Eliminate an enemy division." 虽然"吃掉"可以翻译为"eat up"或"consume"，**但在军事背景下，它也可以表示"消灭"或"歼灭"。** 在这种情况下，使用"eliminate"更为合适，因为它传达了完全摧毁敌人师的意思。
* <img src="imgs/judge.png" width="30" />: 双方都提出了有效的论点和翻译，准确传达了原始中文文本的含义。在"eat up"和"eliminate"之间的选择可能取决于文本的上下文和语气。因此，目前没有明确倾向于任何一方。
* <img src="imgs/devil.png" width="30" />: 虽然"eliminate"确实传达了完全摧毁敌人师的意思，但它没有捕捉到"吃掉"所暗示的消耗或吞噬敌人的内涵。
* <img src="imgs/angel.png" width="30" />: **在军事背景下，"吃掉"通常用于描述对敌人的完全摧毁，而不是对其资源或领土的消耗。**
* <img src="imgs/judge.png" width="30" />: 双方都提出了有效的论点，但反方关于"eliminate"更好地捕捉了原始中文文本中使用的军事语言的强度和严肃性的论点更具说服力。此外，"eliminate"准确传达了完全摧毁敌人师的意思。因此，中文文本"吃掉敌人一个师"的正确英文翻译是**"Eliminate an enemy division."**

<p align="center">
<img src="imgs/translation-case1.png" width="450" />
</p>


<details>
<summary><b>案例2</b></summary>
给定中文句子"他从后门搞到了不少名酒。"，请提供其英文翻译。
    
###### MAD

* <img src="imgs/devil.png" width="30" />: 短语"从后门" **字面意思是"from the back door"。**
* <img src="imgs/angel.png" width="30" />: 我实际上不同意你的翻译。我认为更准确的翻译是"He got a lot of famous liquor from the back door." 最后，虽然"从后门"字面意思是"from the back door"，**但它是一个常见的中文成语，意思是通过非官方或不正当手段获取某物**。因此，在翻译中使用"from the back door"并不完全准确。相反，使用"from an unofficial source"或"through unofficial means"会更合适。
* <img src="imgs/judge.png" width="30" />: 双方都提出了有效的论点和翻译，准确捕捉了原始中文文本的含义。在"wine"和"liquor"之间的选择是一个解释和上下文的问题。**在"from the back door"与"from an unofficial source"之间的选择是一个偏好和风格的问题。** 因此，没有明确倾向于任何翻译候选。
* <img src="imgs/devil.png" width="30" />: **我同意"从后门"是一个常见的中文成语，意思是通过非官方或不正当手段获取某物。** 使用"from an unofficial source"或"through unofficial means"可能比"from the back door"更合适。
* <img src="imgs/angel.png" width="30" />: 是的，我同意你的观点。 
* <img src="imgs/judge.png" width="30" />: 虽然两种翻译都准确捕捉了原始中文文本的含义，但在候选2中使用"liquor"更为准确，因为"名酒"更常用于指代白酒。此外，在候选3中使用"from an unofficial source"更准确地传达了"从后门"作为通过非官方或不正当手段获取某物的含义。因此，正确的翻译是：**"He got a lot of famous liquor from an unofficial source."**

<p align="center">
<img src="imgs/translation-case2.png" width="750" />
</p>

</details>


### 参考资料

- **0-Shot CoT**：<a href="https://arxiv.org/pdf/2205.11916.pdf">Large Language Models are Zero-Shot Reasoners</a>（NeurIPS 2022）
- **Self-Consist**：<a href="https://openreview.net/pdf?id=1PL1NIMMrw">Self-Consistency Improves Chain of Thought Reasoning in Language Models</a>（ICLR 2023）
- **Self-Reflect**：<a href="https://arxiv.org/pdf/2303.11366.pdf">Reflexion: an autonomous agent with dynamic memory and self-reflection</a>（arxiv 2023）
- **MAPS**：<a href="https://arxiv.org/pdf/2305.04118.pdf">Exploring Human-Like Translation Strategy with Large Language Models</a>（arxiv 2023）


## 引用
```
@article{liang2023encouraging,
  title={Encouraging Divergent Thinking in Large Language Models through Multi-Agent Debate},
  author={Liang, Tian and He, Zhiwei and Jiao, Wenxiang and Wang, Xing and Wang, Yan and Wang, Rui and Yang, Yujiu and Tu, Zhaopeng and Shi, Shuming},
  journal={arXiv preprint arXiv:2305.19118},
  year={2023}
}
```