# bilibili评论爬取

本人比较喜欢做情感分析的NLP项目，因此突发奇想想到去B站收集信息。

⭐**重点**：**但是本项目只是学习使用，如果用作任何其他用途，本人概不负责！！！**⚠⚠⚠

# ⭐重点（申明）

###⭐该项目只适用学习其他任何用途均不可使用！！！

###⭐该项目只适用学习其他任何用途均不可使用！！！

###⭐该项目只适用学习其他任何用途均不可使用！！！

# url参数解析

expample: https://api.bilibili.com/x/v2/reply/main?csrf=40a227fcf12c380d7d3c81af2cd8c5e8&mode=3&next={}&oid=860478472&plat=1&type=1

csrf：固定是40a227fcf12c380d7d3c81af2cd8c5e8（不太清楚含义）

mode：应该是一种模式 （也不太清楚含义）

⭐**next**：按照实验应该是一个起始页的指示，可以从0开始

⭐**oid**：代表每个视频的唯一标识

plat：不清楚含义

type：不清楚含义

- ⭐**重点**：**修改一词next的值可以爬取到20条评论**，这个我没有分析出来是哪个参数控制的，但是大家也不要去修改，毕竟是学习不要去恶意修改其他的参数。
- ⭐**重点**：**核心参数只需要修改；1、oid：视频唯一标识码；2、next：评论起始页（从0开始）**

# 如何爬取想要的视频评论

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
  # 就是只爬取能搜索到20条完整评论的评论，在最后的时候如果评论数已经不足20条，则放弃，这样也不会损失多少数据对于评论比较多的视频，如果评论数太少的视频大家可以自行修改代码将这部分删除即可。
  comment = []
  if len(comment) % 20 != 0:
      print("一共爬取到{}条评论".format(len(comment)))
      break
  else:
      print("搜集到%d条评论" % (len(comment)))
  ```

# 核心代码

```python
import requests

# 范例url：https://api.bilibili.com/x/v2/reply/main?csrf=40a227fcf12c380d7d3c81af2cd8c5e8&mode=3&next=3&oid=861032963&plat=1&type=1
# 如果有不懂的参照这个url对比下就知道了

url = "https://api.bilibili.com/x/v2/reply/main?csrf=40a227fcf12c380d7d3c81af2cd8c5e8&mode=3&next={}（这儿提示，从0开始即可）&oid=（替换成自己想要爬取的视频的oid码即可）&plat=1&type=1"

header = {
    "user-agent": "替换成自己的user-agent即可",
    "cookie": "替换成自己的cookie即可"
}

comment = []
for i in range(100):
    responses = requests.get(url=url.format(i), headers=header).json()
    for content in responses["data"]["replies"]:
        comment.append(content["content"]["message"])
    if len(comment) % 20 != 0:
        print("一共爬取到{}条评论".format(len(comment)))
        break
    else:
        print("搜集到%d条评论" % (len(comment)))

with open("bilibili_comment.txt", "w", encoding="utf-8") as fp:
    for c in comment:
        fp.write(c + "\n")
```

# 资源包获取方式（重点⭐），如果只是使用代码则不需要看此处！⭐⭐⭐⭐⭐⭐⭐在此重申，本项目只适用学习，任何其他用途本人概不负责！！！！！！！！！！！！

1、评论包的位置步骤：

- 1、首先找到任一视频打开F12

  ![F12打开时候的样子](../bilibili_comment_crawl/F12打开时候的样子.png)

  

- 2、因为比较杂乱，点击该位置将这些资源包删除

  ![点击此处删除](../bilibili_comment_crawl/点击此处删除.png)

  

- 3、拖动滚轮向下滑动直到出现一个这样的资源包即可

  ![评论资源包](../bilibili_comment_crawl/评论资源包.png)

  

- 4、将其点开，就能找到对应视频的oid码了

  ![oid码所在位置](../bilibili_comment_crawl/oid码所在位置.png)

  

- 5、评论资源所在位置，点击方框处

  ![响应](../bilibili_comment_crawl/响应.png)



- 6、看到其中的内容然后Crtl-A + Crtl-C，全选复制，然后在网上随便搜一个在线JSON解释器粘贴进去即可

  ![json解析后的样子](../bilibili_comment_crawl/json解析后的样子.png)

- 7、然后点击那些（➖减号）啥的符号慢慢整理可以看到一个这样的列表

  ![整理后的json解析文件](../bilibili_comment_crawl/整理后的json解析文件.png)

- 8、最后所需要的评论就在

  ![comment所在的位置](../bilibili_comment_crawl/comment所在的位置.png)

- 9、对应的python字典获取格式就是：

  ```python
  # 可以发现data下的replies其实通过字典访问的方式就可以得到一个长度为20的列表了（这儿看第7步的图片就可以看出来）
  # 每个列表下又是一个字典，这时候通过访问key："content",然后又是一个字典在访问key："message"就可以拿到数据了
  # 举个例子：
  responses = requests.get(url=url, headers=header).json()
  # 拿到返回了的json数据
  replies = responses["data"]["replies"] # 这样就可以得到一个长度为20的列表了
  # 然后在循环该列表，就可以拿到数据了
  for content in replies:
      print(content["content"]["message"])
  ```

  
