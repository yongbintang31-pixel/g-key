from typing import List
from google import genai
import time
import random
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



def get_refined_audiobook_title(
    original_title: str,
    ggapi: List[str]
) -> str:
    """
    使用 Gemini 模型重写有冒号的有声书标题。
    冒号前的部分保留不变，冒号后的部分润色为更吸引人的表达。
    依次尝试 ggapk 列表中的 API key，若调用失败则自动切换下一个 Key。
    
    Args:
        original_title: 原始标题，如 "The Practicing Mind: Train Your Mind, Transform Your Life"
        ggapk: API key 列表，用于轮换重试
    
    Returns:
        模型生成的改写后标题
    
    Raises:
        RuntimeError: 所有 API key 均调用失败时抛出
    """
    # 构造提示，仅修改冒号后的部分
    prompt = (
        f"我给你一个标题“{original_title}”。冒号之前的是书名，请保留不变；"
        "请润色冒号后内容，使其更具吸引力。仅返回最终完整标题，不要其他多余输出。"
    )
    
    for api_key in ggapi:
        client = genai.Client(api_key=api_key)
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            # 返回成功生成的文本
            return response.text.strip()
        
        except Exception as e:
            # 打印失败日志，并等待短暂时间后重试下一个 key
            print(f"[Warning] API key {api_key!r} 调用失败：{e}")
            time.sleep(1)
    
    # 若循环结束仍未返回，则全部失败
    raise RuntimeError("所有 API key 调用均失败，无法获取重写后的标题。")


get_refined_audiobook_title("Questions or comments about my work? Send me a message!",ggapi)
