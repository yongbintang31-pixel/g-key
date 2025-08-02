
#https://chrome.google.com/webstore/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc




#下载deep-filter
# 定义文件路径
import os
import time
import os
import subprocess
import shutil
file_name = "deep-filter-0.5.6-x86_64-unknown-linux-musl"
source_dir = "/content/"
drive_dir = "/content/drive/MyDrive/"
source_path = os.path.join(source_dir, file_name)
drive_path = os.path.join(drive_dir, file_name)

# 检查/content/目录中是否存在文件
if not os.path.exists(source_path):
    # 检查/content/drive/MyDrive/目录中是否存在文件
    if not os.path.exists(drive_path):
        # 下载文件
        subprocess.run(["wget", "https://github.com/Rikorose/DeepFilterNet/releases/download/v0.5.6/deep-filter-0.5.6-x86_64-unknown-linux-musl", "-P", source_dir])
        # 赋予执行权限
        subprocess.run(["chmod", "+x", source_path])
        # 复制到/content/drive/MyDrive/目录
        shutil.copy(source_path, drive_path)
        print(1)
    else:
        # 复制到/content/目录
        shutil.copy(drive_path, source_path)
        # 赋予执行权限
        subprocess.run(["chmod", "+x", source_path])
        print(2)


#@title 安装
#!pip install yt-dlp
import subprocess

try:
    subprocess.check_call(["pip", "install", "yt-dlp"])
    print("yt-dlp 安装成功")
except subprocess.CalledProcessError as e:
    print(f"安装失败: {e}")

from IPython.display import clear_output
clear_output()
# @title #安装下载必要的库
#安装下载必要的库
#!unzip /content/drive/MyDrive/transnetv2.zip -d /content/
#from transnetv2 import TransNetV2
from IPython.display import clear_output
clear_output()
import os
from moviepy.editor import VideoFileClip, concatenate_audioclips
import subprocess
import shutil
import os
import sys
from moviepy.editor import *

from IPython.display import clear_output
import shutil
import pickle
clear_output()

#@title 必要函数

import re

def format_youtube_title(title: str) -> str:
    """
    格式化YouTube视频标题，以确保其符合API上传要求。

    该函数执行以下操作：
    1. 移除标题两端的空白字符。
    2. 将标题中连续的多个空格替换为单个空格。
    3. 移除常见的非打印字符（如控制字符）。
    4. 将标题截断到YouTube允许的最大长度（通常是100个字符）。

    Args:
        title (str): 原始的视频标题字符串。

    Returns:
        str: 格式化后的视频标题。
    """
    if not isinstance(title, str):
        # 确保输入是字符串类型，如果不是则转换为字符串
        title = str(title)

    # 1. 移除标题两端的空白字符
    formatted_title = title.strip()

    # 2. 将标题中连续的多个空格替换为单个空格
    formatted_title = re.sub(r'\s+', ' ', formatted_title)

    # 3. 移除常见的非打印字符（例如ASCII控制字符）
    # YouTube API通常对标题字符集比较宽容，但移除控制字符是良好的实践。
    # 这里我们保留所有可打印的ASCII字符以及常见的Unicode字符。
    # 更严格的过滤可能需要根据具体API错误进行调整。
    formatted_title = ''.join(char for char in formatted_title if char.isprintable() or char in ('\n', '\r', '\t'))

    # 4. 将标题截断到YouTube允许的最大长度（通常是100个字符）
    # YouTube API会自行截断过长的标题，但提前处理可以避免潜在的警告或错误。
    MAX_TITLE_LENGTH = 100
    if len(formatted_title) > MAX_TITLE_LENGTH:
        # 可以选择添加省略号，但YouTube通常会直接截断
        formatted_title = formatted_title[:MAX_TITLE_LENGTH]

    return formatted_title


import os
import shutil

#@title 主要流程
def df_and_create_video(results):
    split_output_directory = "/content/output_segments/"
    os.makedirs(split_output_directory, exist_ok=True)
    df_output_directory = "/content/df/"
    os.makedirs(df_output_directory, exist_ok=True)
    final_m4a_to_wav_file = "/content/combined_output.wav"
    without_bgm_output_file = "/content/without_bgm.mp4"
    work_dir = "/content/my_youtube_downloads"
    #folders = [f for f in os.listdir(work_dir) if os.path.isdir(os.path.join(work_dir, f))]
    all_p_path = work_dir
    print(results)
    m4a_files = [f for f in os.listdir(all_p_path) if f.endswith('.m4a')]
    print(m4a_files)
    audio_path = "/content/my_youtube_downloads/" + m4a_files[0]
    print(audio_path)
    clear_folder(split_output_directory)
    split_m4a_to_wav(audio_path, split_output_directory,segment_duration_minutes =60, sample_rate=16000, mono=True, bit_depth=16)
    df_and_merge_wav_files(split_output_directory, df_output_directory, final_m4a_to_wav_file)
    image_file = find_image_files(work_dir)
    bgm_audio_path = select_random_bgm('/content/drive/MyDrive/bgm')
    create_video_with_audio(
        image_file,  # 图片文件路径
        final_m4a_to_wav_file,  # 音频文件路径
        43200,  # 视频时长（秒）
        "/content/12h_output_video_audio.mp4"  # 输出视频文件路径
    )
    output_without_bgm = "/content/output_video_audio_without_bgm.mp4"
    cut_video_baseon_audio("/content/12h_output_video_audio.mp4", final_m4a_to_wav_file, output_without_bgm)
    fin_video_path = add_bgm_to_video(output_without_bgm, bgm_audio_path, adelay_ms=0, volume=bgm_volum)


def clear_folder(folder_path):
    """清空指定文件夹中的所有文件和子文件夹"""
    if not os.path.exists(folder_path):
        print(f"文件夹 {folder_path} 不存在")
        return

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"删除 {file_path} 时出错: {e}")
import math
def split_m4a_to_wav(input_file, output_dir, segment_duration_minutes=60, sample_rate=16000, mono=True, bit_depth=16):
    """
    将 M4A 音频文件分割成每 segment_duration_minutes 分钟一段，并转换为压缩的 WAV 格式。

    Args:
        input_file: 输入 M4A 音频文件的完整路径。
        output_dir: 输出目录的完整路径。
        segment_duration_minutes: 每个分割段的持续时间 (分钟)。
        sample_rate: 采样率 (Hz)，较低的值会减小文件大小。
        mono: 如果为 True，则将音频转换为单声道，可减小文件大小。
        bit_depth: 比特深度，16比特比24比特产生更小的文件。
    """
    try:
        # 1. 获取音频总时长 (秒)
        duration_process = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
             '-of', 'default=noprint_wrappers=1:nokey=1', input_file],
            capture_output=True, text=True, check=True
        )
        total_duration_seconds = float(duration_process.stdout.strip())
        print(f"音频总时长: {total_duration_seconds} 秒")

        # 2. 计算分割段的数量
        segment_duration_seconds = segment_duration_minutes * 60
        num_segments = math.ceil(total_duration_seconds / segment_duration_seconds)
        print(f"分割段的数量: {num_segments}")

        # 3. 创建输出目录 (如果不存在)
        os.makedirs(output_dir, exist_ok=True)

        # 4. 循环分割音频
        for i in range(num_segments):
            start_time_seconds = i * segment_duration_seconds
            output_file = os.path.join(output_dir, f"segment_{i + 1:03d}.wav")  # 命名: segment_001.wav, segment_002.wav ...

            segment_duration = min(segment_duration_seconds, total_duration_seconds - start_time_seconds)  # 最后一个片段的时间可能小于 segment_duration_seconds

            # 配置 FFmpeg 命令，添加参数以减小输出文件大小
            ffmpeg_command = [
                'ffmpeg',
                '-ss', str(start_time_seconds),  # 开始时间
                '-t', str(segment_duration),     # 持续时间
                '-i', input_file,                # 输入文件
                '-vn',                           # 禁用视频
                '-ar', str(sample_rate),         # 设置采样率
                '-ac', '2',     # 设置为单声道或双声道
                '-sample_fmt', f's{bit_depth}',  # 设置比特深度
                '-acodec', 'pcm_s16le',          # WAV PCM 编码
                '-y',
                output_file                      # 输出文件 (WAV)
            ]

            try:
                result = subprocess.run(ffmpeg_command , capture_output=True, text=True, check=True)
                print(result)
                print(f"成功分割 {input_file} 到 {output_file} (开始时间: {start_time_seconds} 秒, 持续时间: {segment_duration} 秒)")
            except subprocess.CalledProcessError as e:
                print(f"分割 {output_file} 失败: {e}")

    except subprocess.CalledProcessError as e:
        print(f"操作失败: {e}")
        print("请确保已安装 FFmpeg 并且已将其添加到系统 PATH 环境变量中。")
    except FileNotFoundError:
        print("未找到 FFmpeg。请确保已安装 FFmpeg 并且已将其添加到系统 PATH 环境变量中。")
    except Exception as e:
        print(f"发生错误: {e}")


import os
import glob
import subprocess
from pydub import AudioSegment
from concurrent.futures import ThreadPoolExecutor

def process_wav_file(wav_file, output_dir):
    output_file = os.path.join(output_dir, os.path.basename(wav_file))
    command = f'/content/deep-filter-0.5.6-x86_64-unknown-linux-musl "{wav_file}" --output-dir "{output_dir}"'
    print(command)
    subprocess.run(command, shell=True, check=True)
    return output_file

def df_and_merge_wav_files(input_dir, output_dir, final_output_file):
    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 获取所有wav文件并按修改时间排序
    video_extensions = ['.wav']
    wav_files = []

    for file in os.listdir(input_dir):
        if os.path.splitext(file)[1].lower() in video_extensions:
            wav_files.append(os.path.join(input_dir, file))
    wav_files.sort(key=os.path.getmtime)

    # 用自然数重新命名wav文件
    renamed_files = []
    for idx, wav_file in enumerate(wav_files, start=1):
        new_name = f"{idx}.wav"
        new_path = os.path.join(input_dir, new_name)
        os.rename(wav_file, new_path)
        renamed_files.append(new_path)

    # 使用多线程处理每个wav文件，线程数等于CPU核心数
    processed_files = []
    num_threads = os.cpu_count()
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        processed_files = list(executor.map(lambda wav_file: process_wav_file(wav_file, output_dir), renamed_files))

    # 确保processed_files按自然数从小到大重新排序
    processed_files.sort(key=lambda x: int(os.path.splitext(os.path.basename(x))[0]))
    print(processed_files)
    # 合并所有处理后的wav文件
    combined = AudioSegment.empty()
    for file in processed_files:
        audio = AudioSegment.from_wav(file)
        combined += audio

    # 导出合并后的wav文件
    combined.export(final_output_file, format="wav")



def find_image_files(work_dir):
    """查找指定目录及其子目录中的所有 .jpg 和 .png 文件"""
    img_files = []

    for root, _, files in os.walk(work_dir):
        for file in files:
            if file.endswith(('.jpg', '.png')):
                img_files.append(os.path.join(root, file))

    return img_files[0]


import os
import random

def select_random_bgm(bgm_folder):
    """从指定文件夹中随机选择一个背景音乐文件"""
    bgm_files = [f for f in os.listdir(bgm_folder) if f.endswith(('.mp3', '.wav'))]

    if not bgm_files:
        print("没有找到背景音乐文件")
        return None

    bgm_file = random.choice(bgm_files)
    bgm_path = os.path.join(bgm_folder, bgm_file)
    return bgm_path


from moviepy.editor import ImageClip, AudioFileClip, CompositeAudioClip

def create_video_with_audio(image_path, audio_path, duration, output_path):
    """
    使用一张图片、音频文件和指定的时长创建视频

    参数:
        image_path: 图片文件路径
        audio_path: 音频文件路径
        duration: 视频时长（秒）
        output_path: 输出视频文件路径
    """
    # 创建图片剪辑
    image_clip = ImageClip(image_path, duration=duration)

    # 设置视频分辨率为1080p (1920x1080)
    image_clip = image_clip.resize(newsize=(1920, 1080))

    # 设置视频的帧率为1/duration，确保总帧数为1
    image_clip = image_clip.set_fps(1)

    # 加载音频剪辑
    audio_clip = AudioFileClip(audio_path)

    # 将音频剪辑设置为视频的音频
    final_clip = image_clip.set_audio(audio_clip)

    # 写入视频文件
    final_clip.write_videofile(output_path, codec='libx264', fps=1 / 100)
    print(f"带有音频的视频已生成: {output_path}")


import json

def cut_video_baseon_audio(o_video_path, audio_path, output_path):
    """
    使用一张图片和音频文件创建视频，视频时长与音频时长相同

    参数:
        image_path: 图片文件路径
        audio_path: 音频文件路径
        output_path: 输出视频文件路径
    """
    # 获取音频时长
    probe_cmd = [
        'ffprobe',
        '-v', 'quiet',
        '-print_format', 'json',
        '-show_format',
        audio_path
    ]

    result = subprocess.run(probe_cmd, capture_output=True, text=True)
    audio_info = json.loads(result.stdout)
    duration = float(audio_info['format']['duration'])

    # 截取视频以确保时长与音频一致
    trim_cmd = [
        'ffmpeg',
        '-i', o_video_path,
        '-t', str(duration),
        '-c:v', 'copy',
        '-c:a', 'copy',
        '-y',
        output_path
    ]

    subprocess.run(trim_cmd)
    print(f"视频已生成并截取: {output_path}")


import subprocess
import os

def add_bgm_to_video(input_video_path, bgm_audio_path, adelay_ms=0, volume=bgm_volum):
    #!ffmpeg -stream_loop -1 -i "{bgm_audio_path}" -t 12:00:00 -c copy -y "/content/tem.mp3"
    import subprocess
    bgm_audio_path = bgm_audio_path  # 替换为你自己的音频路径
    output_path = "/content/tem.mp3"
    
    command = [
        "ffmpeg",
        "-stream_loop", "-1",
        "-i", bgm_audio_path,
        "-t", "12:00:00",
        "-c", "copy",
        "-y", output_path
    ]
    
    try:
        subprocess.run(command, check=True)
        print("处理完成 ✅")
    except subprocess.CalledProcessError as e:
        print(f"执行出错：{e}")

    bgm_audio_path = "/content/tem.mp3"
    # Extract the directory and base name of the input video
    input_dir = os.path.dirname(input_video_path)
    input_base_name = os.path.basename(input_video_path)
    input_name, input_ext = os.path.splitext(input_base_name)

    # Define the output file path with the same name but with a prefix
    output_video_path = os.path.join(input_dir, f"processed_{input_name}{input_ext}")

    # Step 1: Speed up the video and audio
    temp_video_path = input_video_path

    # 生成随机延迟值，范围在 2000 到 3000 之间
    adelay_ms = 0

    # Step 2: Add background music to the sped-up video

    add_bgm_cmd = [
        'ffmpeg',
        '-i', temp_video_path,
        '-i', bgm_audio_path,
        '-filter_complex',
         f'[1:a]adelay={adelay_ms}|{adelay_ms},volume={volume}[bgm];[0:a][bgm]amix=inputs=2:duration=first:dropout_transition=0',
        '-ar', '44100',  # 设置音频采样率
        '-c:v', 'copy',  # 复制视频流
        '-c:a', 'aac',  # 使用 AAC 编码器
        '-b:a', '128k',  # 设置音频比特率为 128 kbps
        '-shortest',  # 确保输出长度与最短流一致
        '-y',  # 覆盖输出文件
        output_video_path
    ]
    try:
        result = subprocess.run(add_bgm_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print("FFmpeg Output:")
        print(result.stdout)
        print("FFmpeg Error:")
        print(result.stderr)
        print(f"Background music added: {output_video_path}")
    except subprocess.CalledProcessError as e:
        print("FFmpeg Command Failed:")
        print(f"Command: {e.cmd}")
        print(f"Return Code: {e.returncode}")
        print(f"Output: {e.stdout}")
        print(f"Error: {e.stderr}")
    print(f"Background music added: {output_video_path}")

    # Optional: Remove the temporary file
    #os.remove(temp_video_path)
    #print(f"Temporary file removed: {temp_video_path}")
    return output_video_path


import shutil
import os

def copy_and_rename_video(source_file_path, new_title):
    """
    复制一个视频文件并根据提供的新标题重命名。

    Args:
        source_file_path (str): 源视频文件的完整路径。
        new_title (str): 新文件的标题（不包含扩展名）。
                        文件扩展名将自动添加为 '.mp4'。
    Returns:
        bool: 如果文件复制成功则返回 True，否则返回 False。
    """
    # 确保添加文件扩展名
    destination_filename = new_title + ".mp4"
    # 假设目标路径与源文件在同一目录，或者您可以指定一个不同的目录
    # 这里我们假设目标路径也在 /content/
    destination_path = os.path.join("/content/drive/MyDrive/英文电子书/", destination_filename)

    try:
        # 复制文件
        shutil.copy2(source_file_path, destination_path)
        print(f"文件 '{source_file_path}' 已成功复制并重命名为 '{destination_filename}' 到 '{destination_path}'")
        return True
    except FileNotFoundError:
        print(f"错误：源文件 '{source_file_path}' 未找到。")
        return False
    except Exception as e:
        print(f"复制文件时发生错误：{e}")
        return False

# 示例用法：
# 假设 result 变量已定义，并且包含 'title' 键

#@title ai重写标题简介
from google import genai

def get_refined_audiobook_title(original_title: str) -> str:
    """
    Refines the part of an audiobook title after the colon to make it more appealing
    using the Gemini model. The part before the colon is preserved.

    Args:
        original_title: The original audiobook title string,
                        e.g., "The Practicing Mind :Train Your Mind, Transform Your Life (Audiobook)".

    Returns:
        The refined audiobook title as generated by the Gemini model.
    """
    # Construct the prompt based on the user's instructions for the Gemini model.
    # It explicitly tells the AI to keep the part before the colon unchanged
    # and refine the part after it to be more attractive, returning only the refined title.
    prompt_for_gemini = f"我给你一个标题“{original_title}”，因为“：”之前的是书名，不用修改，后面要修改表达，润色使其更吸引人，直接返回你认为修改好的标题，不要其他多余的输出"
    prompt_for_gemini = f"I'm giving you a title: '{original_title}'. The part before the colon is the book's name and should remain unchanged. Please rephrase and polish the text after the colon to make it more appealing and engaging. Return only the improved title, with no other additional output."
    prompt_for_gemini = f"There isn't an {original_title} provided in your request. Please provide the title so I can help you rephrase and polish the text after the colon to make it more appealing and engaging, while keeping the entire title under 100 characters.Return only the improved title, with no other additional output"
    # Initialize the Gemini client with the provided example API key.
    # In a production environment, it's recommended to load API keys securely
    # (e.g., from environment variables) rather than hardcoding them.
    client = genai.Client(api_key="AIzaSyCXWOrTYaX6oliwbcmH5-jCy_kn_SQ0R2k")

    # Call the Gemini model to generate the refined content.
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt_for_gemini
    )

    # Return the text generated by the model, which should be the refined title.
    return response.text

from google import genai

def get_refined_youtube_description(original_description: str) -> str:
    """
    Refines a YouTube video description using the Gemini model based on specific instructions.

    The function will:
    - Remove all external links (purchase links, channel join links).
    - Delete original channel information.
    - Keep the "Timestamps" section unchanged.
    - Make the beginning of the description more engaging, highlighting core value and transformation.
    - Use stronger, more compelling calls to action at the end (like, subscribe, share).
    - Return only the revised content, with no additional output.

    Args:
        original_description: The original YouTube video description string.

    Returns:
        The refined YouTube video description as generated by the Gemini model.
    """
    # Construct the prompt for the Gemini model based on the detailed instructions.
    prompt_for_gemini = f"""
Please help me rewrite the following YouTube video description. Remove all external links (such as purchase links and channel join links), delete the original channel information, and keep the "Timestamps" section unchanged. Please make the beginning of the description more engaging, highlighting the core value and transformation this audiobook can bring to the audience. The ending should use stronger, more compelling calls to action, encouraging viewers to like, subscribe, and share,Please return only the revised content you deem best, with no additional output.

Here is the original description content:

“{original_description}”
"""

    # Configure the Gemini API with the provided API key.
    # In a production environment, it's recommended to load API keys securely
    # (e.g., from environment variables) rather than hardcoding them).
    client = genai.Client(api_key=gemimi_api)

    # Call the Gemini model to generate the refined content.
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt_for_gemini
    )

    # Return the text generated by the model, which should be the refined title.
    return response.text


import requests
import random
import time
# 原始文件地址（raw 内容）
url = 'https://raw.githubusercontent.com/yongbintang31-pixel/g-key/main/test.txt'
# 添加随机参数避免缓存
timestamp = str(int(time.time()))
modified_url = f"{url}?_t={timestamp}"
# 发起请求并检查状态
response = requests.get(modified_url)
response.raise_for_status()

# 将文件内容按行拆分，存入 ggapi 列表
ggapi = response.text.splitlines()

random.shuffle(ggapi)
# 输出查看
print("下载成功",ggapi)




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
    prompt_for_gemini = f"""
    Please help me rewrite the following YouTube video description. Remove all external links (such as purchase links and channel join links), delete the original channel information, and keep the "Timestamps" section unchanged. Please make the beginning of the description more engaging, highlighting the core value and transformation this audiobook can bring to the audience. The ending should use stronger, more compelling calls to action, encouraging viewers to like, subscribe, and share,Please return only the revised content you deem best, with no additional output.
    
    Here is the original description content:
    
    “{original_description}”
    """
    
    for api_key in ggapi:
        client = genai.Client(api_key=api_key)
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt_for_gemini
            )
            # 返回成功生成的文本
            return response.text[:5000]
        
        except Exception as e:
            # 打印失败日志，并等待短暂时间后重试下一个 key
            print(f"[Warning] API key {api_key!r} 调用失败：{e}")
            time.sleep(1)
    
    # 若循环结束仍未返回，则全部失败
    raise RuntimeError("所有 API key 调用均失败，无法获取重写后的标题。")


def get_refined_youtube_description(
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
      f"There isn't an {original_title} provided in your request. Please provide the title so I can help you rephrase and polish the text after the colon to make it more appealing and engaging, while keeping the entire title under 100 characters.Return only the improved title, with no other additional output"
      )
    
    for api_key in ggapi:
        client = genai.Client(api_key=api_key)
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            # 返回成功生成的文本
            return response.text[:100]
        
        except Exception as e:
            # 打印失败日志，并等待短暂时间后重试下一个 key
            print(f"[Warning] API key {api_key!r} 调用失败：{e}")
            time.sleep(1)
    
    # 若循环结束仍未返回，则全部失败
    raise RuntimeError("所有 API key 调用均失败，无法获取重写后的标题。")


#@title youtube下载相关函数
import os
import time
import yt_dlp
from IPython.display import display, Javascript
from IPython.display import clear_output
clear_output()
def read_urls_from_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

def write_url_to_file(file_path, url):
    with open(file_path, 'a') as file:
        file.write(url + '\n')

def is_url_processed(file_path, url):
    with open(file_path, 'r') as file:
        processed_urls = file.readlines()
    return url + '\n' in processed_urls

def get_short_videos_from_channel(channel_url, max_duration=600000, max_videos=500):
    """
    从指定的 YouTube 频道获取时长少于 max_duration 秒的视频 URL 列表。

    :param channel_url: YouTube 频道的 URL
    :param max_duration: 视频的最大时长（秒）
    :param max_videos: 要获取的最新视频数量
    :return: 时长少于 max_duration 秒的视频 URL 列表
    """
    ydl_opts = {
        'ignoreerrors': True,
        'playlistend': max_videos,
        'extract_flat': True,
    }

    urls = []

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(channel_url, download=False)
        videos = info_dict.get('entries', [])

        for video in videos:
            if video:
                duration = video.get('duration', 0)
                if duration < max_duration:
                    urls.append(video['url'])

    return urls


def get_videos_from_channel(channel_url, min_duration_seconds=1200, max_duration_seconds=43200, max_videos=1000):
    """
    从指定的 YouTube 频道获取时长介于 min_duration_seconds 和 max_duration_seconds 之间的视频 URL 列表。

    :param channel_url: YouTube 频道的 URL
    :param min_duration_seconds: 视频的最小时长（秒），默认为 20 分钟 (1200 秒)
    :param max_duration_seconds: 视频的最大时长（秒），默认为 12 小时 (43200 秒)
    :param max_videos: 要获取的最新视频数量
    :return: 时长介于 min_duration_seconds 和 max_duration_seconds 之间的视频 URL 列表
    """
    ydl_opts = {
        'ignoreerrors': True,  # 忽略提取错误
        'playlistend': max_videos,  # 限制获取的视频数量
        'extract_flat': True,  # 只提取信息，不下载视频
    }

    urls = []

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(channel_url, download=False)
        videos = info_dict.get('entries', [])

        for video in videos:
            if video:
                duration = video.get('duration', 0)
                # 检查视频时长是否在指定范围内
                if min_duration_seconds <= duration <= max_duration_seconds:
                    urls.append(video['url'])

    return urls

def create_output_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def alert_popup(message):
    display(Javascript(f'alert("{message}");'))


#@title download_audio_and_thumbnail_separately
import yt_dlp
import os
from PIL import Image # Import Pillow library, needs to be installed first: pip install Pillow

def download_audio_and_thumbnail_separately(url, download_folder="downloads"):
    """
    Downloads the best quality audio from a YouTube video and
    the video's thumbnail separately. The audio will be converted to M4A,
    and the thumbnail will be downloaded in its original format, then converted to JPG using Pillow.
    Also, saves the video title and description to a text file.

    Args:
        url (str): The YouTube video URL.
        download_folder (str): The folder where downloaded files will be saved.

    Returns:
        dict: A dictionary containing details of the downloaded files and video info,
              or None if a critical error occurred.
              Keys include: 'title', 'description', 'audio_filepath', 'thumbnail_filepath', 'info_filepath'.
    """
    print(f"Processing video: {url}")

    # Create the download folder if it doesn't exist
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
        print(f"Created download folder: '{download_folder}'")

    video_info = None # Initialize video_info to store extracted video details
    download_results = {
        'title': None,
        'description': None,
        'audio_filepath': None,
        'thumbnail_filepath': None,
        'info_filepath': None
    }

    # --- Extract video information first (needed for both audio, thumbnail, title, and description) ---
    info_ydl_opts = {
        'skip_download': True, # Only extract info, do not download files yet
        'noplaylist': True, # If the URL is a playlist, only extract info for a single video
    }
    print("\n--- Extracting video information ---")
    try:
        with yt_dlp.YoutubeDL(info_ydl_opts) as ydl:
            video_info = ydl.extract_info(url, download=False) # download=False to just get info
            download_results['title'] = video_info.get('title', 'Unknown Title')
            download_results['description'] = video_info.get('description', 'No description available.')
            print(f"✅ Video information extracted successfully for '{download_results['title']}'.")
    except Exception as e:
        print(f"❌ Error extracting video information: {e}")
        return None # Return None on critical error

    if not video_info:
        print("❌ Could not get video information. Aborting.")
        return None

    audio_title = download_results['title']
    thumbnail_title = download_results['title'] # Use same title for thumbnail
    video_description = download_results['description']

    # --- Save video title and description to a text file ---
    info_filepath = os.path.join(download_folder, f"{audio_title}.txt")
    download_results['info_filepath'] = info_filepath
    print(f"\n--- Saving video title and description to: '{info_filepath}' ---")
    try:
        with open(info_filepath, 'w', encoding='utf-8') as f:
            f.write(f"Title: {audio_title}\n\n")
            f.write(f"Description:\n{video_description}\n")
        print(f"✅ Video title and description saved to '{info_filepath}'.")
    except Exception as e:
        print(f"❌ Error saving title and description: {e}")

    # --- Audio download options (convert to M4A) ---
    audio_ydl_opts = {
        'format': 'bestaudio', # Download the best audio format
        'postprocessors': [
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'm4a', # Convert audio to M4A format (CHANGED from 'wav')
            }
        ],
        # Output file name includes the specified download folder
        'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s'),
        'noplaylist': True, # If the URL is a playlist, only download a single video
        'progress_hooks': [lambda d: print(f"Audio download progress: {d['_percent_str']}")] # Print download progress
    }

    print("\n--- Starting audio download (M4A format) ---")
    try:
        with yt_dlp.YoutubeDL(audio_ydl_opts) as ydl:
            ydl.download([url])
            # Determine the actual audio file path after download
            # yt-dlp usually names it based on outtmpl and the actual video title/ext
            # Adjust the extension check for m4a
            audio_ext_from_info = video_info.get('ext', 'm4a') # Use info_dict for more accurate ext
            download_results['audio_filepath'] = os.path.join(download_folder, f"{audio_title}.{audio_ext_from_info}")
            # Verify file existence (optional but good practice)
            if not os.path.exists(download_results['audio_filepath']):
                # If the inferred path doesn't exist, try common audio extensions including m4a
                for ext in ['m4a', 'wav', 'mp3']:
                    temp_path = os.path.join(download_folder, f"{audio_title}.{ext}")
                    if os.path.exists(temp_path):
                        download_results['audio_filepath'] = temp_path
                        break

            if download_results['audio_filepath'] and os.path.exists(download_results['audio_filepath']):
                print(f"✅ Audio '{download_results['audio_filepath']}' downloaded successfully.")
            else:
                print(f"❌ Audio download completed, but actual file path could not be confirmed: {os.path.join(download_folder, audio_title)}.m4a (or similar).")
                # This doesn't stop execution, but flags an issue

    except Exception as e:
        print(f"❌ Error downloading audio: {e}")
        # Continue to thumbnail download even if audio fails, if info was extracted

    # --- Thumbnail download options (yt-dlp directly downloads original format) ---
    thumbnail_ydl_opts = {
        'skip_download': True, # Key: do not download the video itself
        'writethumbnail': True, # Write the thumbnail file
        # Output file name includes the specified download folder and temporary name
        'outtmpl': os.path.join(download_folder, '%(title)s_original_thumb.%(ext)s'),
        'noplaylist': True, # If the URL is a playlist, only download a single video
    }

    print("\n--- Starting original thumbnail download ---")
    original_thumbnail_filepath = None
    try:
        with yt_dlp.YoutubeDL(thumbnail_ydl_opts) as ydl:
            ydl.download([url]) # Download the thumbnail (skip_download=True, writethumbnail=True)

            # After download, find the actual filename generated by yt-dlp
            # We'll rely on listing the directory for the _original_thumb file
            found_thumb_file = False
            for fname in os.listdir(download_folder):
                if (fname.endswith('.webp') or fname.endswith('.jpg') or fname.endswith('.png') or fname.endswith('.jpeg')):
                    original_thumbnail_filepath = os.path.join(download_folder, fname)
                    print(f"💡 Found original thumbnail file: '{original_thumbnail_filepath}'")
                    found_thumb_file = True
                    break

            if not found_thumb_file:
                print(f"❌ Original thumbnail could not be downloaded or found. Please check yt-dlp detailed output.")
                # This doesn't stop execution, but flags an issue
                # return None # Do not return None here to allow partial success

    except Exception as e:
        print(f"❌ Error downloading thumbnail: {e}")
        # return None # Do not return None here to allow partial success

    # --- Convert thumbnail to JPG using Pillow ---
    if original_thumbnail_filepath and os.path.exists(original_thumbnail_filepath):
        try:
            jpg_thumbnail_filepath = os.path.join(download_folder, f"{thumbnail_title}.jpg")
            download_results['thumbnail_filepath'] = jpg_thumbnail_filepath
            print(f"\n--- Converting thumbnail '{original_thumbnail_filepath}' to '{jpg_thumbnail_filepath}' ---")

            # Open image using Pillow
            with Image.open(original_thumbnail_filepath) as img:
                # Convert to RGB mode if image has an alpha channel (e.g., PNG) to save as JPG
                if img.mode == 'RGBA':
                    img = img.convert('RGB')
                # Save as JPG format
                img.save(jpg_thumbnail_filepath, 'jpeg')

            print(f"✅ Thumbnail successfully converted to JPG format: '{jpg_thumbnail_filepath}'.")

            # Optional: Delete the original downloaded thumbnail file
            if os.path.exists(original_thumbnail_filepath):
                os.remove(original_thumbnail_filepath)
                print(f"🗑️ Original thumbnail file deleted: '{original_thumbnail_filepath}'.")

        except Exception as e:
            print(f"❌ Error converting thumbnail to JPG: {e}")
    else:
        print("Skipping JPG conversion as original thumbnail was not found or downloaded.")

    return download_results




def download_video(url, output_folder, processed_urls_file):
    if is_url_processed(processed_urls_file, url):
        print(f'视频 {url} 已下载，跳过。')
        return False


    # Example usage:
    # Replace the URL below with the YouTube video link you want to download
    # You can also change 'my_downloads' to any folder name you prefer.
    video_url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
    video_url = url
        # 检查输出目录是否存在
    if not os.path.exists("/content/my_youtube_downloads"):
        os.makedirs("/content/my_youtube_downloads")
        print("创建目录/content/my_youtube_downloads成功")
    else:
        print("目录/content/my_youtube_downloads已存在" )
    clear_folder("/content/my_youtube_downloads")
    download_folder_name = 'my_youtube_downloads' # Set your desired download folder here

    # Call the function and get the results
    results = download_audio_and_thumbnail_separately(video_url, download_folder=download_folder_name)

    if results:
        print("\n--- Download Summary ---")
        print(f"Video Title: {results['title']}")
        print(f"Video Description: {results['description'][:100]}...") # Print first 100 chars
        print(f"Audio File: {results['audio_filepath']}")
        print(f"Thumbnail File (JPG): {results['thumbnail_filepath']}")
        print(f"Info File: {results['info_filepath']}")
    else:
        print("\n--- Download failed or was incomplete ---")

    return results



import shutil
import os

def clear_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

# 使用示例
#clear_folder('/content/')


def get_video_files(directory):
    video_extensions = ('.mp4', '.avi', '.mkv', '.mov', '.flv', '.webm')  # 根据需要添加更多视频格式
    video_files = []

    for file in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, file)) and file.lower().endswith(video_extensions):
            video_files.append(os.path.join(directory, file))
            output_path = os.path.join(directory, '916' + file)
    print(video_files[0],output_path)
    return video_files[0],output_path
# 使用示例


#input_video_path = r'/content/fr_jEdun0GM--Fails of the Week ｜ Crazy and Outrageous 🫨.webm'
#output_video_path = r'/content/916.mp4'
#crop_video_to_9_16(input_video_path, output_video_path)


import os
import yt_dlp
from PIL import Image

import os

def search_cookies_file(directory):
    """
    在指定目录中搜索文件名包含“www.youtube.com_cookies”的文件

    参数:
    directory (str): 要搜索的目录路径

    返回:
    str: 找到的文件路径，如果未找到则返回None
    """
    # 只搜索当前目录，不递归子目录
    for file in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, file)) and "www.youtube.com_cookies" in file:
            return os.path.join(directory, file)
    return None



def download_audio_and_thumbnail_separately(url, download_folder="downloads", cookies_file="/content/drive/MyDrive/www.youtube.com_cookies.txt"):
    """
    Downloads the best quality audio from a YouTube video and
    the video's thumbnail separately. The audio will be converted to M4A,
    and the thumbnail will be downloaded in its original format, then converted to JPG using Pillow.
    Also, saves the video title and description to a text file.

    Args:
        url (str): The YouTube video URL.
        download_folder (str): The folder where downloaded files will be saved.
        cookies_file (str, optional): Path to a Netscape-format cookies file.
                                      If provided, yt-dlp will use these cookies for authentication.

    Returns:
        dict: A dictionary containing details of the downloaded files and video info,
              or None if a critical error occurred.
              Keys include: 'title', 'description', 'audio_filepath', 'thumbnail_filepath', 'info_filepath'.
    """
    print(f"Processing video: {url}")
    cookies_file="/content/drive/MyDrive/www.youtube.com_cookies.txt"
    # 指定要搜索的目录
    search_directory = "/content/drive/MyDrive/"

    # 调用函数搜索文件
    cookies_file = search_cookies_file(search_directory)
    # Create the download folder if it doesn't exist
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
        print(f"Created download folder: '{download_folder}'")

    video_info = None # Initialize video_info to store extracted video details
    download_results = {
        'title': None,
        'description': None,
        'audio_filepath': None,
        'thumbnail_filepath': None,
        'info_filepath': None
    }

    # Common yt-dlp options, including cookies if provided
    common_ydl_opts = {
        'noplaylist': True, # If the URL is a playlist, only process a single video
    }

    # Add cookiefile option if a cookies_file path is provided and exists
    if cookies_file:
        if os.path.exists(cookies_file):
            common_ydl_opts['cookiefile'] = cookies_file
            print(f"Using cookies from: '{cookies_file}'")
        else:
            print(f"⚠️ Warning: Cookies file '{cookies_file}' not found. Proceeding without cookies.")

    # --- Extract video information first (needed for both audio, thumbnail, title, and description) ---
    info_ydl_opts = {
        **common_ydl_opts, # Merge common options
        'skip_download': True, # Only extract info, do not download files yet
    }
    print("\n--- Extracting video information ---")
    try:
        with yt_dlp.YoutubeDL(info_ydl_opts) as ydl:
            video_info = ydl.extract_info(url, download=False) # download=False to just get info
            download_results['title'] = video_info.get('title', 'Unknown Title')
            download_results['description'] = video_info.get('description', 'No description available.')
            print(f"✅ Video information extracted successfully for '{download_results['title']}'.")
    except Exception as e:
        print(f"❌ Error extracting video information: {e}")
        return None # Return None on critical error

    if not video_info:
        print("❌ Could not get video information. Aborting.")
        return None

    audio_title = download_results['title']
    thumbnail_title = download_results['title'] # Use same title for thumbnail
    video_description = download_results['description']

    # --- Save video title and description to a text file ---
    # Sanitize title for filename to avoid issues with invalid characters
    sanitized_title = "".join([c for c in audio_title if c.isalnum() or c in (' ', '.', '_', '-')]).strip()
    info_filepath = os.path.join(download_folder, f"{sanitized_title}.txt")
    download_results['info_filepath'] = info_filepath
    print(f"\n--- Saving video title and description to: '{info_filepath}' ---")
    try:
        with open(info_filepath, 'w', encoding='utf-8') as f:
            f.write(f"Title: {audio_title}\n\n")
            f.write(f"Description:\n{video_description}\n")
        print(f"✅ Video title and description saved to '{info_filepath}'.")
    except Exception as e:
        print(f"❌ Error saving title and description: {e}")

    # --- Audio download options (convert to M4A) ---
    audio_ydl_opts = {
        **common_ydl_opts, # Merge common options
        'format': 'bestaudio', # Download the best audio format
        'postprocessors': [
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'm4a', # Convert audio to M4A format
            }
        ],
        # Output file name includes the specified download folder
        'outtmpl': os.path.join(download_folder, f"{sanitized_title}.%(ext)s"),
        'progress_hooks': [lambda d: print(f"Audio download progress: {d.get('_percent_str', 'N/A')}")], # Print download progress
    }

    print("\n--- Starting audio download (M4A format) ---")
    try:
        with yt_dlp.YoutubeDL(audio_ydl_opts) as ydl:
            ydl.download([url])
            # Determine the actual audio file path after download
            # yt-dlp usually names it based on outtmpl and the actual video title/ext
            audio_ext_from_info = video_info.get('ext', 'm4a') # Use info_dict for more accurate ext
            download_results['audio_filepath'] = os.path.join(download_folder, f"{sanitized_title}.m4a")

            # Verify file existence
            if not os.path.exists(download_results['audio_filepath']):
                # If the inferred path doesn't exist, try common audio extensions
                for ext in ['m4a', 'mp3', 'wav', 'aac', 'flac']: # Added more common audio extensions
                    temp_path = os.path.join(download_folder, f"{sanitized_title}.{ext}")
                    if os.path.exists(temp_path):
                        download_results['audio_filepath'] = temp_path
                        break

            if download_results['audio_filepath'] and os.path.exists(download_results['audio_filepath']):
                print(f"✅ Audio '{download_results['audio_filepath']}' downloaded successfully.")
            else:
                print(f"❌ Audio download completed, but actual file path could not be confirmed for '{sanitized_title}'.m4a (or similar).")

    except Exception as e:
        print(f"❌ Error downloading audio: {e}")

    # --- Thumbnail download options (yt-dlp directly downloads original format) ---
    thumbnail_ydl_opts = {
        **common_ydl_opts, # Merge common options
        'skip_download': True, # Key: do not download the video itself
        'writethumbnail': True, # Write the thumbnail file
        # Output file name includes the specified download folder and temporary name
        'outtmpl': os.path.join(download_folder, f"{sanitized_title}_original_thumb.%(ext)s"),
    }

    print("\n--- Starting original thumbnail download ---")
    original_thumbnail_filepath = None
    try:
        with yt_dlp.YoutubeDL(thumbnail_ydl_opts) as ydl:
            ydl.download([url]) # Download the thumbnail (skip_download=True, writethumbnail=True)

            # After download, find the actual filename generated by yt-dlp
            # We'll rely on listing the directory for the _original_thumb file
            found_thumb_file = False
            for fname in os.listdir(download_folder):
                if fname.startswith(f"{sanitized_title}_original_thumb.") and \
                   (fname.endswith('.webp') or fname.endswith('.jpg') or fname.endswith('.png') or fname.endswith('.jpeg')):
                    original_thumbnail_filepath = os.path.join(download_folder, fname)
                    print(f"💡 Found original thumbnail file: '{original_thumbnail_filepath}'")
                    found_thumb_file = True
                    break

            if not found_thumb_file:
                print(f"❌ Original thumbnail could not be downloaded or found. Please check yt-dlp detailed output.")

    except Exception as e:
        print(f"❌ Error downloading thumbnail: {e}")

    # --- Convert thumbnail to JPG using Pillow ---
    if original_thumbnail_filepath and os.path.exists(original_thumbnail_filepath):
        try:
            jpg_thumbnail_filepath = os.path.join(download_folder, f"{sanitized_title}.jpg")
            download_results['thumbnail_filepath'] = jpg_thumbnail_filepath
            print(f"\n--- Converting thumbnail '{original_thumbnail_filepath}' to '{jpg_thumbnail_filepath}' ---")

            # Open image using Pillow
            with Image.open(original_thumbnail_filepath) as img:
                # Convert to RGB mode if image has an alpha channel (e.g., PNG) to save as JPG
                if img.mode == 'RGBA':
                    img = img.convert('RGB')
                # Save as JPG format
                img.save(jpg_thumbnail_filepath, 'jpeg')

            print(f"✅ Thumbnail successfully converted to JPG format: '{jpg_thumbnail_filepath}'.")

            # Optional: Delete the original downloaded thumbnail file
            if os.path.exists(original_thumbnail_filepath):
                os.remove(original_thumbnail_filepath)
                print(f"🗑️ Original thumbnail file deleted: '{original_thumbnail_filepath}'.")

        except Exception as e:
            print(f"❌ Error converting thumbnail to JPG: {e}")
    else:
        print("Skipping JPG conversion as original thumbnail was not found or downloaded.")

    return download_results

#@title youtube上传相关函数
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from datetime import datetime, timedelta
import os
SCOPES = ['https://www.googleapis.com/auth/youtube']

def find_file(directory, pattern):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(pattern):
                return os.path.join(root, file)
    return None

client_secret = find_file('/content/drive/MyDrive', 'googleusercontent.com.json')
from urllib.parse import urlparse, parse_qs

def get_code_from_url(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    code = query_params.get('code', [None])[0]
    return code

# 示例URL

# 检查 token.json 文件是否存在以及修改日期是否超过7天
if not os.path.exists(token_path) or (time.time() - os.path.getmtime(token_path)) > 600 * 24 * 60 * 60:
    flow = InstalledAppFlow.from_client_secrets_file(client_secret, SCOPES)
    flow.redirect_uri = 'http://localhost'
    auth_url, _ = flow.authorization_url(prompt='consent')
    print(f"请访问以下链接完成授权：\n{auth_url}")
    code = input("")
    code = get_code_from_url(code)
    print(code)
    flow.fetch_token(code=code)

    # 保存凭据到 token.json 文件
    with open(token_path, 'w') as token_file:
        token_file.write(flow.credentials.to_json())
    print("身份验证成功，令牌已保存为 token.json")
else:
    print("使用已存在的令牌文件。")
from IPython.display import clear_output
clear_output()




def upload_video(youtube, video_file, title, description, tags,status,days):
    # 定义视频元数据
    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags,
        },
        'status': {
            'privacyStatus': status,  # 根据传入的 status 参数设置隐私状态
        }
    }

    if status == 'private':
        body['status']['publishAt'] = (datetime.utcnow() + timedelta(days=days)).isoformat("T") + "Z"  # 定时发布，1 天后
    elif status == 'publish':
        body['status']['privacyStatus'] = 'public'  # 立即公开发布
    elif status == 'unlisted':
        body['status']['privacyStatus'] = 'unlisted'  # 立即公开但不列出

    media = MediaFileUpload(video_file, chunksize=-1, resumable=True)
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"上传进度：{int(status.progress() * 100)}%")
    print("上传完成，视频 ID:", response['id'])
    return response['id']

def authenticate_with_saved_token():
    # 加载已保存的令牌
    #token_path = "/content/drive/MyDrive/Timeless Echoes_token.json"#@param {type:'string'}
    credentials = Credentials.from_authorized_user_file(token_path)
    return build('youtube', 'v3', credentials=credentials)

#@title 主要流程

processed_urls_file = '/content/drive/MyDrive/ok_url_test2.txt'

create_output_folder(output_folder)

if not os.path.exists(processed_urls_file):
    open(processed_urls_file, 'w').close()

urls = get_videos_from_channel(channel_url,min_duration_seconds,max_duration_seconds,max_videos=max_videos)
urls.reverse()
print(urls)
n = 1
try:
    for url in urls:
        if one_time_to_make_videos < n:
          break
        create_output_folder(output_folder)
        result = download_video(url, output_folder, processed_urls_file)
        print('result',result)
        if not result:
          print('下载失败，可能已经处理过了')
          continue
        print('下载成功！',result)
        df_and_create_video(result)
        #result = {"title": "我的新视频文件"}
        source_file = "/content/processed_output_video_audio_without_bgm.mp4"
        # 调用函数
        #copy_and_rename_video(source_file, result["title"])
        youtube = authenticate_with_saved_token()
        video_file = source_file
        title = get_refined_audiobook_title(result['title'])
        title = format_youtube_title(title)
        print(title)
        description = get_refined_youtube_description(result['description'])
        print(description)
        tags =[]
        days = 1
        upload_video(youtube, video_file, title, description, tags,status,days)
        write_url_to_file(processed_urls_file, url)
except Exception as e:
    print(e)
