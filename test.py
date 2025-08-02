import requests
import random
# 原始文件地址（raw 内容）
url = 'https://raw.githubusercontent.com/yongbintang31-pixel/g-key/main/test.txt'

# 发起请求并检查状态
response = requests.get(url)
response.raise_for_status()

# 将文件内容按行拆分，存入 ggapi 列表
ggapi = response.text.splitlines()

random.shuffle(ggapi)
# 输出查看
print(ggapi)
print(outside_w)
