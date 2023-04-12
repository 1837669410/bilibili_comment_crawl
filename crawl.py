import requests

# 范例url：https://api.bilibili.com/x/v2/reply/main?csrf=40a227fcf12c380d7d3c81af2cd8c5e8&mode=3&next=3&oid=861032963&plat=1&type=1
# 如果有不懂的参照这个url对比下就知道了
url = "https://api.bilibili.com/x/v2/reply/main?csrf=40a227fcf12c380d7d3c81af2cd8c5e8&mode=3&next={}（这儿提示，从0开始即可）" \
      "&oid=（替换成自己想要爬取的视频的oid码即可）&plat=1&type=1"

header = {
    "user-agent": "替换成自己的user-agent即可",
    "cookie": "替换成自己的cookie即可"
}

comment = []
pre_comment_length = 0

for i in range(200):
    responses = requests.get(url=url.format(i), headers=header).json()
    for content in responses["data"]["replies"]:
        comment.append(content["content"]["message"])
    print("搜集到%d条评论" % (len(comment)))
    # 调整爬虫策略，从必须每20条评论调整成上一次评论数和这一次评论数进行比较，如果有改变说明有新数据，如果没改变说明数据全部搜集完毕，爬虫停止
    if len(comment) == pre_comment_length:
        print("爬虫退出！！！")
        break
    else:
        pre_comment_length = len(comment)

with open("bilibili_comment.txt", "w", encoding="utf-8") as fp:
    for c in comment:
        fp.write(c + "\n")