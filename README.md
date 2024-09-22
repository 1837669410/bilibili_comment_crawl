# &#x1F308;&#x1F308;&#x1F308;bilibili评论爬取&#x1F308;&#x1F308;&#x1F308;（代码文件只有crawl.py）

# 如果遇到代码已经无法运行了请及时提醒我，可以提Issues，我会尽快更新！！！！！！

本人比较喜欢做情感分析的NLP项目，因此突发奇想想到去B站收集信息。

1、[声明](#para1) 2、[url参数解析](#para2) 3、[如何爬取想要的视频评论](#para3) 4、[核心代码](#para4) 5、[BUG提示](#para5) 6、[资源包获取方式](#para6)

⭐**重点**：但是本项目只是学习使用，如果用作任何其他用途，本人概不负责！！！⚠⚠⚠

# ⭐<a id="para1"/>声明&#x1F379;&#x1F379;&#x1F379;

### 该项目只适用学习其他任何用途均不可使用！！！

### 该项目只适用学习其他任何用途均不可使用！！！

### 该项目只适用学习其他任何用途均不可使用！！！

# <a id="para2"/>url参数解析（2024.9.22当前api还能使用，请大家放心食用）&#x1F37A;&#x1F37A;&#x1F37A;

expample: https://api.bilibili.com/x/v2/reply/main?csrf=40a227fcf12c380d7d3c81af2cd8c5e8&mode=3&next={}&oid=860478472&plat=1&type=1

csrf：固定是40a227fcf12c380d7d3c81af2cd8c5e8（不太清楚含义）

mode：应该是一种模式 （也不太清楚含义）

⭐**next**：按照实验应该是一个起始页的指示，可以从0开始

⭐**oid**：代表每个视频的唯一标识

plat：不清楚含义

type：不清楚含义

- ⭐**重点**：**修改一词next的值可以爬取到20条评论**，这个我没有分析出来是哪个参数控制的，但是大家也不要去修改，毕竟是学习不要去恶意修改其他的参数。
- ⭐**重点**：**核心参数只需要修改；1、oid：视频唯一标识码；2、next：评论起始页（从0开始）**

# <a id="para3"/>如何爬取想要的视频评论&#x1F345;&#x1F345;&#x1F345;

步骤：

- 1、找到自己想要爬取视频的oid

- 2、设置url比如：

  ```python
  # next={}预留的地方就是用来控制起始页数的位置，经过验证是可以从0开始的，到时候for循环的时候用.fotmat()方法补全即可
  # oid={}只需要找到自己想要爬取的视频的oid码就行了
  url = "https://api.bilibili.com/x/v2/reply/main?csrf=40a227fcf12c380d7d3c81af2cd8c5e8&mode=3&next={}&oid=去找到自己想要爬取的视频的oid码然后把这儿替换掉即可&plat=1&type=1"
  ```

- 3、如何爬取到所有的comment（⭐重点）

  因为我首先没有先去找所有的评论到底有多少，因此需要自行进行逻辑判断，我的方法是：

  ```python
  # 通过判断上一次comment列表的长度和当前的列表长度是否一致来判断时候有新的评论数据加入，如果有则继续爬虫，如果无则停止爬虫，这样可以避免爬虫因error提前退出或者爬取到许多脏数据
  comment = []
  pre_comment_length = 0
  if len(comment) == pre_comment_length:
      print("爬虫退出！！！")
      break
  else:
      pre_comment_length = len(comment)
  ```

# <a id="para4"/>核心代码&#x1F30F;&#x1F30F;&#x1F30F;

```python
import time

import requests
from fake_useragent import UserAgent

# 范例url：https://api.bilibili.com/x/v2/reply/main?csrf=40a227fcf12c380d7d3c81af2cd8c5e8&mode=3&next=3&oid=861032963&plat=1&type=1
# 如果有不懂的参照这个url对比下就知道了
url = "https://api.bilibili.com/x/v2/reply/main?csrf=40a227fcf12c380d7d3c81af2cd8c5e8&mode=3&next={}（这儿提示，从0开始即可）" \
      "&oid=（替换成自己想要爬取的视频的oid码即可）&plat=1&type=1"

header = {
    "user-agent": UserAgent().random,
    "cookie": "替换成自己的cookie即可"
}

comment = []
pre_comment_length = 0
i = 0

while True:
    # 添加重试机制可以让爬虫收集完全部的一级评论，且不会中途停止，可以适当在触发失败后加上一些time.sleep(1)延缓爬虫速度
    try:
        responses = requests.get(url=url.format(i), headers=header).json()
    except:
        time.sleep(1)
        continue
    i += 1 # 获取到下一页

    for content in responses["data"]["replies"]:
        comment.append(content["content"]["message"])
    print("搜集到%d条评论" % (len(comment)))
    # 调整爬虫策略，上一次评论总数和这一次评论总数进行比较，如果有改变说明有新数据，如果没改变说明数据全部搜集完毕，爬虫停止
    if len(comment) == pre_comment_length:
        print("爬虫退出！！！")
        break
    else:
        pre_comment_length = len(comment)

with open("bilibili_comment.txt", "w", encoding="utf-8") as fp:
    for c in comment:
        fp.write(c + "\n")
```

# <a id="para5">BUG提示（⚠⚠）&#x1F30F;&#x1F30F;&#x1F30F;

- 1、有时候爬取了一会就会碰到不足20条的数据，这时候根据我的代码逻辑，就会直接退出爬虫（已修复该**bug**，更改了新的爬虫停止逻辑）
- 2、有时候怕爬取会中途中断解决，采用了重试机制(2024.9.22修复)
- 3、**新的bug坑等着大家来提出**

# <a id="para6">因为api接口已经变成了wbi加密的所以原来的接口寻找方式已经没用了，所以下面的方法就删除了，降低大家的阅读难度。(2024.9.22修改)
