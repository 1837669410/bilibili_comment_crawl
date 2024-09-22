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