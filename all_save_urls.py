
#https://chrome.google.com/webstore/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc

###############################################################################################

#使用云cookies
import os
import requests
import glob

# Step 0: Mount Google Drive if you are in a Colab environment.
# Uncomment the following two lines and run them in a separate cell
# if you are running this in Google Colab.
# from google.colab import drive
# drive.mount('/content/drive')

# --- Configuration ---
# The URL for the raw file on GitHub.
github_url = "https://raw.githubusercontent.com/yongbintang31-pixel/g-key/main/www.youtube.com_cookies.txt"
# The target directory where the final file will be saved.
target_dir = "/content/drive/MyDrive"
# The name of the file to download and save.
file_name = "www.youtube.com_cookies.txt"
# The full path for the new file.
final_file_path = os.path.join(target_dir, file_name)

print("使用云cookies!!!开始执行文件操作...")
print("-" * 30)

# Step 1: Download the file from GitHub.
print(f"正在从GitHub下载文件: {github_url}")
try:
    response = requests.get(github_url)
    # Check for a successful response (status code 200)
    response.raise_for_status() 
    downloaded_content = response.text
    print("文件下载成功。")
except requests.exceptions.RequestException as e:
    print(f"下载文件时出错: {e}")
    # Exit the script if download fails
    exit()

# Step 2: Delete any existing files in the target directory that match the pattern.
print(f"\n正在删除目录 '{target_dir}' 中包含 '{file_name}' 的所有旧文件...")
try:
    # Use glob to find all files that match the pattern
    file_pattern = os.path.join(target_dir, f"*{os.path.splitext(file_name)[0]}*.txt")
    files_to_delete = glob.glob(file_pattern)

    if files_to_delete:
        for file_path in files_to_delete:
            os.remove(file_path)
            print(f"已删除: {file_path}")
    else:
        print("未找到需要删除的匹配文件。")

except OSError as e:
    print(f"删除文件时出错: {e}")
    pass

# Step 3: Save the newly downloaded file to the target directory.
print(f"\n正在将新下载的文件保存到: '{final_file_path}'...")
try:
    # Ensure the target directory exists
    os.makedirs(target_dir, exist_ok=True)
    
    # Write the downloaded content to the new file
    with open(final_file_path, 'w', encoding='utf-8') as f:
        f.write(downloaded_content)
    print("文件保存成功。")

except IOError as e:
    print(f"写入文件时出错: {e}")
    exit()

print("-" * 30)
print("所有操作已完成。")

#上传相关数据
#!pip install supabase
import subprocess

try:
    subprocess.check_call(["pip", "install", "supabase"])
    print("supabase 安装成功")
except subprocess.CalledProcessError as e:
    print(f"安装失败: {e}")
from supabase import create_client, Client

# 初始化 Supabase 客户端
import os
from supabase import create_client, Client

url: str = "https://lvpbegckuzmppqcvbtkj.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imx2cGJlZ2NrdXptcHBxY3ZidGtqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQxODM2MDAsImV4cCI6MjA2OTc1OTYwMH0.CxEcETn8zfBRxHC800QIpTgZgqLVNh5ioULMJ64KuBg"
supabase: Client = create_client(url, key)

def insert_unique_url(table: str, channel_name: str) -> str:
    # 查询是否已存在
    check = supabase.table(table).select("channel_name").eq("channel_name", channel_name).execute()

    if check.data:
        return f"✅ 已存在，无需插入: {channel_name}"
    
    # 插入新记录
    response = supabase.table(table).insert({"channel_name": channel_name}).execute()
    if response.data:
        return f"🚀 插入成功: {channel_name}"
    else:
        return f"⚠️ 插入失败，请检查权限或字段结构"

# 示例调用

url_to_insert = channel_url
insert_unique_url_status = insert_unique_url("youtube_url", url_to_insert)
print(insert_unique_url_status)
###############################################################################################
#下载deep-filter
# 定义文件路径
import os
import time
import os
import subprocess
import shutil
from typing import List
from google import genai
import time
import random
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
    try:
        df_and_merge_wav_files(split_output_directory, df_output_directory, final_m4a_to_wav_file)
    except Exception as e:
        print(f" df_and_merge_wav_files发生意外错误: {e}")
        return False
    # 定义要检查的文件的路径
    final_m4a_to_wav_file = "/content/combined_output.wav"
    # 使用 os.path.exists() 函数来检查文件是否存在
    if not os.path.exists(final_m4a_to_wav_file):
        # 如果文件不存在，则打印相关信息
        print(f"文件不存在：{final_m4a_to_wav_file}")
        return False
    else:
        # 如果文件存在，也可以选择打印一条消息
        print(f"文件已找到：{final_m4a_to_wav_file}")
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
    return True

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

def process_wav_file(wav_file, output_dir):
    """
    使用 deep-filter 程序处理 WAV 文件。

    Args:
        wav_file (str): 输入 WAV 文件的路径。
        output_dir (str): 输出目录的路径。

    Returns:
        str or bool: 如果成功，返回输出文件的路径；如果失败，返回 False。
    """
    output_file = os.path.join(output_dir, os.path.basename(wav_file))
    command = f'/content/deep-filter-0.5.6-x86_64-unknown-linux-musl "{wav_file}" --output-dir "{output_dir}"'
    
    print(f"正在执行命令: {command}")
    
    try:
        subprocess.run(command, shell=True, check=True)
        print("命令执行成功。")
        return output_file
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败，错误代码: {e.returncode}")
        print(f"错误输出: {e.stderr}")
        return False
    except Exception as e:
        print(f"发生意外错误: {e}")
        return False

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




def get_refined_youtube_description(
    original_description: str,
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

import os
import hashlib
import datetime

# 1. 生成保存文件路径
# 使用 SHA256 哈希确保文件名唯一且稳定
file_hash = hashlib.sha256(token_path.encode()).hexdigest()
file_path = f"/content/drive/MyDrive/{file_hash}.txt"

# 初始化 urls 变量
urls = []

# 2. 检查文件是否存在并决定是否重新下载
if os.path.exists(file_path):
    print(f"文件 {file_path} 已存在。")

    # 检查文件修改时间是否超过 30 天
    file_mtime = os.path.getmtime(file_path)
    thirty_days_ago = datetime.datetime.now() - datetime.timedelta(days=30)

    if datetime.datetime.fromtimestamp(file_mtime) > thirty_days_ago:
        print("文件未过期，直接从文件中读取链接。")
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                urls = [line.strip() for line in f if line.strip()]
        except Exception as e:
            print(f"读取文件时出错: {e}")
            print("将重新下载链接。")
            urls = get_videos_from_channel(channel_url, min_duration_seconds, max_duration_seconds, max_videos)
    else:
        print("文件已超过 30 天，将重新下载链接并更新文件。")
        urls = get_videos_from_channel(channel_url, min_duration_seconds, max_duration_seconds, max_videos)
        
else:
    print(f"文件 {file_path} 不存在，正在下载链接并保存。")
    urls = get_videos_from_channel(channel_url, min_duration_seconds, max_duration_seconds, max_videos)


# 3. 如果需要，将新下载的链接保存到文件
if not os.path.exists(file_path) or datetime.datetime.fromtimestamp(os.path.getmtime(file_path)) <= thirty_days_ago:
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            for url in urls:
                f.write(f"{url}\n")
        print(f"新下载的 {len(urls)} 个链接已保存到 {file_path}")
    except Exception as e:
        print(f"保存文件时出错: {e}")

# 4. 保持原始逻辑，反转链接列表
urls.reverse()

# 5. 打印最终的链接列表
print("\n最终的视频链接列表:")
print(urls[:10])

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
        if not result['audio_filepath'] or result['audio_filepath'] == None :
          print('下载失败，audio_filepath==None')
          continue
        print('下载成功！',result)
        title = get_refined_audiobook_title(result['title'],ggapi)
        title = format_youtube_title(title)
        print(title)
        description = get_refined_youtube_description(result['description'],ggapi)
        print(description)
        df_reuslt = df_and_create_video(result)
        if not df_reuslt:
            print('df处理失败，跳过这个视频')
            write_url_to_file(processed_urls_file, url)
            continue
        #result = {"title": "我的新视频文件"}
        source_file = "/content/processed_output_video_audio_without_bgm.mp4"
        # 调用函数
        #copy_and_rename_video(source_file, result["title"])
        youtube = authenticate_with_saved_token()
        video_file = source_file
        tags =[]
        days = 1
        upload_video(youtube, video_file, title, description, tags,status,days)
        write_url_to_file(processed_urls_file, url)
        clear_output()
except Exception as e:
    print(e)

print("开始定时发布")
#################################################################################################################################################################################
time.sleep(30)
from IPython.display import clear_output
clear_output()
# 导入必要的库
import os
import datetime
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# 定义 OAuth 2.0 授权范围
# 需要管理视频（更新隐私状态和发布时间），所以使用 'https://www.googleapis.com/auth/youtube'
SCOPES = ['https://www.googleapis.com/auth/youtube']

# 定义客户端密钥文件的名称
# 请确保您已从 Google Cloud Console 下载此文件，并将其命名为 client_secrets.json

def authenticate_with_saved_token(token_path):
    # 加载已保存的令牌
    credentials = Credentials.from_authorized_user_file(token_path)
    return build('youtube', 'v3', credentials=credentials)

def get_my_channel_id(youtube_service):
    """
    获取当前认证用户的 YouTube 频道 ID。
    参数:
        youtube_service: 已认证的 YouTube API 服务对象。
    返回:
        用户的频道 ID 字符串，如果获取失败则返回 None。
    """
    try:
        print("正在获取您的频道 ID...")
        request = youtube_service.channels().list(
            part='id',
            mine=True # 使用 mine=True 来获取当前用户的频道信息
        )
        response = request.execute()
        if response and response.get('items'):
            channel_id = response['items'][0]['id']
            print(f"已获取频道 ID: {channel_id}")
            return channel_id
        else:
            print("未能获取到您的频道 ID。")
            return None
    except HttpError as e:
        print(f"获取频道 ID 时发生错误: {e}")
        return None

def list_unlisted_videos(youtube_service, channel_id):
    """
    列出用户频道中所有不公开的视频。
    参数:
        youtube_service: 经过身份验证的YouTube API服务对象。
        channel_id: 要查询的频道 ID。
    返回:
        一个包含所有不公开视频详细信息的列表，每个视频是一个字典。
    """
    print("正在获取您的频道上传播放列表...")
    uploads_playlist_id = None

    try:
        # 获取当前认证用户的上传播放列表ID
        channels_response = youtube_service.channels().list(
            part='contentDetails',
            id=channel_id # 使用 channelId 参数来获取特定频道
        ).execute()

        for channel in channels_response.get('items', []):
            uploads_playlist_id = channel['contentDetails']['relatedPlaylists']['uploads']
            break

        if not uploads_playlist_id:
            print("无法找到您的频道上传播放列表。")
            return []

        print(f"找到上传播放列表ID: {uploads_playlist_id}")
        print("正在获取播放列表中的所有视频ID...")

        all_video_ids = []
        next_page_token = None

        while True:
            # 获取上传播放列表中的所有视频ID
            playlist_items_request = youtube_service.playlistItems().list(
                part='contentDetails',
                playlistId=uploads_playlist_id,
                maxResults=50, # 每次请求最多返回 50 个结果
                pageToken=next_page_token
            )
            playlist_items_response = playlist_items_request.execute()

            for item in playlist_items_response.get('items', []):
                video_id = item['contentDetails']['videoId']
                all_video_ids.append(video_id)

            next_page_token = playlist_items_response.get('nextPageToken')
            if not next_page_token:
                break # 如果没有下一页，则退出循环

        if not all_video_ids:
            print("您的频道中没有视频。")
            return []

        print(f"找到 {len(all_video_ids)} 个视频ID。正在检查它们的隐私状态...")
        unlisted_videos = []

        # YouTube Data API v3 的 videos.list 方法一次最多支持 50 个视频ID
        # 所以需要分批处理
        for i in range(0, len(all_video_ids), 50):
            batch_video_ids = all_video_ids[i:i+50]
            videos_request = youtube_service.videos().list(
                part='snippet,status', # 请求视频的标题、描述和隐私状态
                id=','.join(batch_video_ids)
            )
            videos_response = videos_request.execute()

            for video_item in videos_response.get('items', []):
                privacy_status = video_item['status']['privacyStatus']
                if privacy_status == 'unlisted':
                    unlisted_videos.append(video_item) # 将不公开视频项添加进来

        print(f"总共找到 {len(unlisted_videos)} 个不公开视频。")
        return unlisted_videos

    except HttpError as e:
        print(f"获取不公开视频时发生错误: {e}")
        return []

def get_latest_published_video_date(youtube_service, channel_id):
    """
    获取最新发布（公开）视频的日期。
    参数:
        youtube_service: 已认证的 YouTube API 服务对象。
        channel_id: 要查询的频道 ID。
    返回:
        最新发布视频的 datetime 对象，如果没有找到则返回 None。
    """
    try:
        # 使用 search().list 来获取最新上传的视频 ID，因为它支持 order='date' 和 channelId
        # 注意：search().list 返回的视频可能不包含隐私状态，需要再次调用 videos().list
        search_request = youtube_service.search().list(
            part='id',
            channelId=channel_id,
            type='video', # 确保只返回视频结果
            order='date', # 按照日期排序，最新上传的在前
            maxResults=1 # 只获取一个结果
        )
        search_response = search_request.execute()

        if search_response and search_response.get('items'):
            latest_video_id = search_response['items'][0]['id']['videoId']

            # 使用 videos().list 来获取视频的详细信息（包括隐私状态和发布日期）
            videos_request = youtube_service.videos().list(
                part='snippet,status',
                id=latest_video_id
            )
            videos_response = videos_request.execute()

            if videos_response and videos_response.get('items'):
                latest_video_details = videos_response['items'][0]
                # 检查视频是否为公开状态
                if latest_video_details['status']['privacyStatus'] == 'public':
                    published_at_str = latest_video_details['snippet']['publishedAt']
                    # 解析 ISO 8601 格式的日期字符串，并确保它是时区感知的 (UTC)
                    published_date = datetime.datetime.fromisoformat(published_at_str.replace('Z', '+00:00'))
                    # 显式地将时区信息设置为 UTC，以防 fromisoformat 在某些情况下未能正确识别
                    if published_date.tzinfo is None:
                        published_date = published_date.replace(tzinfo=datetime.timezone.utc)
                    print(f"找到最新公开视频: {latest_video_details['snippet']['title']}，发布日期: {published_date.date()}")
                    return published_date
                else:
                    print(f"最新视频 '{latest_video_details['snippet']['title']}' 不是公开状态，不作为基准日期。")
        else:
            print("未找到任何已上传的视频。")
        return None
    except HttpError as e:
        print(f"获取最新发布视频时发生错误: {e}")
        return None

def update_video_publish_time(youtube_service, video_id, title, description, tags, category_id, publish_at):
    """
    更新视频的发布时间并将其状态更改为“公开”。
    参数:
        youtube_service: 已认证的 YouTube API 服务对象。
        video_id: 视频的 ID。
        title: 视频标题。
        description: 视频描述。
        tags: 视频标签列表。
        category_id: 视频分类 ID。
        publish_at: 定时发布的时间 (ISO 8601 格式字符串)。
    返回:
        更新后的视频信息，如果失败则返回 None。
    """
    try:
        # 构建视频资源对象
        video_resource = {
            'id': video_id,
            'snippet': {
                'title': title,
                'description': description,
                'tags': tags,
                'categoryId': category_id
            },
            'status': {
                'privacyStatus': 'private', # 将隐私状态设置为 'public'
                'publishAt': publish_at # 设置定时发布时间
            }
        }

        # 调用 videos.update API 更新视频
        request = youtube_service.videos().update(
            part='snippet,status',
            body=video_resource
        )
        response = request.execute()
        print(f"成功更新视频: {title} (ID: {video_id})，定时发布时间为: {publish_at}")
        return response
    except HttpError as e:
        print(f"更新视频 {title} (ID: {video_id}) 时发生错误: {e}")
        return None

def get_latest_published_video_date(youtube_service, channel_id):
    """
    获取最新发布（公开）或最新定时发布视频的日期。
    参数:
        youtube_service: 已认证的 YouTube API 服务对象。
        channel_id: 要查询的频道 ID。
    返回:
        最新发布或最新定时发布视频的 datetime 对象，如果没有找到则返回 None。
    """
    print("正在获取您的频道上传播放列表以查找最新视频...")
    uploads_playlist_id = None
    try:
        channels_response = youtube_service.channels().list(
            part='contentDetails',
            id=channel_id
        ).execute()

        for channel in channels_response.get('items', []):
            uploads_playlist_id = channel['contentDetails']['relatedPlaylists']['uploads']
            break

        if not uploads_playlist_id:
            print("无法找到您的频道上传播放列表。")
            return None

        # 获取上传播放列表中的所有视频ID
        all_video_ids = []
        next_page_token = None
        while True:
            playlist_items_request = youtube_service.playlistItems().list(
                part='contentDetails',
                playlistId=uploads_playlist_id,
                maxResults=50,
                pageToken=next_page_token
            )
            playlist_items_response = playlist_items_request.execute()
            for item in playlist_items_response.get('items', []):
                video_id = item['contentDetails']['videoId']
                all_video_ids.append(video_id)
            next_page_token = playlist_items_response.get('nextPageToken')
            if not next_page_token:
                break

        if not all_video_ids:
            print("您的频道中没有视频。")
            return None

        latest_date = None
        current_utc_time = datetime.datetime.now(datetime.timezone.utc)

        # 批量获取视频详细信息
        for i in range(0, len(all_video_ids), 50):
            batch_video_ids = all_video_ids[i:i+50]
            videos_request = youtube_service.videos().list(
                part='snippet,status',
                id=','.join(batch_video_ids)
            )
            videos_response = videos_request.execute()

            for video_item in videos_response.get('items', []):
                privacy_status = video_item['status']['privacyStatus']

                # 检查公开视频的发布日期
                if privacy_status == 'public':
                    published_at_str = video_item['snippet']['publishedAt']
                    published_date = datetime.datetime.fromisoformat(published_at_str.replace('Z', '+00:00'))
                    if published_date.tzinfo is None:
                        published_date = published_date.replace(tzinfo=datetime.timezone.utc)

                    if latest_date is None or published_date > latest_date:
                        latest_date = published_date
                        print(f"找到最新公开视频: {video_item['snippet']['title']}，发布日期: {published_date.date()}")

                # 检查私密或不公开视频的定时发布日期（如果未来）
                elif privacy_status in ['private', 'unlisted']:
                    if 'publishAt' in video_item['status']:
                        scheduled_at_str = video_item['status']['publishAt']
                        scheduled_date = datetime.datetime.fromisoformat(scheduled_at_str.replace('Z', '+00:00'))
                        if scheduled_date.tzinfo is None:
                            scheduled_date = scheduled_date.replace(tzinfo=datetime.timezone.utc)

                        # 只考虑未来的定时发布日期
                        if scheduled_date > current_utc_time:
                            if latest_date is None or scheduled_date > latest_date:
                                latest_date = scheduled_date
                                print(f"找到最新定时发布视频: {video_item['snippet']['title']}，定时发布日期: {scheduled_date.date()}")

        return latest_date

    except HttpError as e:
        print(f"获取最新发布/定时发布视频时发生错误: {e}")
        return None

def set_videos_schedule(token_path):
    """主函数，执行视频管理逻辑。"""
    youtube_service = authenticate_with_saved_token(token_path)

    if not youtube_service:
        print("无法获取 YouTube 服务，请检查认证设置。")
        return

    # 首先获取频道 ID
    my_channel_id = get_my_channel_id(youtube_service)
    if not my_channel_id:
        print("无法获取频道 ID，请确保您的账户有 YouTube 频道。")
        return

    unlisted_videos = list_unlisted_videos(youtube_service, my_channel_id)
    latest_published_date = get_latest_published_video_date(youtube_service, my_channel_id)
    print("最新发布视频的日期")
    print(latest_published_date)
    if not unlisted_videos:
        print("没有找到任何不公开的视频。")
        return

    # 获取最新发布视频的日期
    latest_published_date = get_latest_published_video_date(youtube_service, my_channel_id)
    print("最新发布视频的日期")
    print(latest_published_date)
    # 定义一个最小缓冲时间，确保定时发布时间在未来 (单位：分钟)
    MIN_BUFFER_MINUTES = 15

    # 获取当前时区感知的 UTC 时间，用于比较和计算
    current_utc_time = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)

    # 确定定时发布的基准日期
    base_schedule_date_candidate = None

    if latest_published_date:
        # 如果有最新发布的视频，则以其第二天为基准，并设置为 UTC 上午 9 点
        base_schedule_date_candidate = latest_published_date + datetime.timedelta(days=1)
        # 确保 proposed_start_date 也是时区感知的，并设置具体时间
        base_schedule_date_candidate = base_schedule_date_candidate.replace(hour=9, minute=0, second=0, microsecond=0, tzinfo=datetime.timezone.utc)
        print(f"基于最新公开视频 ({latest_published_date.date()})，建议起始定时发布日期为: {base_schedule_date_candidate.date()} 9:00 AM UTC。")
    else:
        # 如果没有最新发布的视频，则以明天为基准，并设置为 UTC 上午 9 点
        base_schedule_date_candidate = current_utc_time + datetime.timedelta(days=1)
        # 确保 start_date 也是时区感知的，并设置具体时间
        base_schedule_date_candidate = base_schedule_date_candidate.replace(hour=9, minute=0, second=0, microsecond=0, tzinfo=datetime.timezone.utc)
        print(f"未找到最新发布的公开视频，建议起始定时发布日期为: {base_schedule_date_candidate.date()} 9:00 AM UTC。")

    # 最终确定用于定时发布的起始日期 (start_date)
    # 它必须是：
    # 1. 至少是 `base_schedule_date_candidate`
    # 2. 至少是 `current_utc_time` 加上 `MIN_BUFFER_MINUTES`
    # 取两者中的最大值，确保时间总是在未来且有足够缓冲
    start_date = max(base_schedule_date_candidate, current_utc_time + datetime.timedelta(minutes=MIN_BUFFER_MINUTES))

    if start_date > base_schedule_date_candidate:
        print(f"调整了起始定时发布日期，以确保它在当前时间后 {MIN_BUFFER_MINUTES} 分钟。新的起始日期为: {start_date.isoformat()}。")
    else:
        print(f"起始定时发布日期为: {start_date.isoformat()}。")


    print("\n开始定时发布不公开视频...")
    for i, video in enumerate(unlisted_videos):
        video_id = video['id']
        snippet = video['snippet']
        status = video['status']

        # 计算当前视频的发布时间
        # 第一个视频是基准日期，后面的视频都加一天
        publish_datetime = start_date + datetime.timedelta(days=i)
        # 确保时间字符串不包含微秒，并以 'Z' 结尾
        # .replace(microsecond=0) 移除微秒
        # .isoformat() 生成 YYYY-MM-DDTHH:MM:SS+00:00 格式
        # .replace('+00:00', 'Z') 替换为 YYYY-MM-DDTHH:MM:SSZ 格式
        publish_at_iso = publish_datetime.replace(microsecond=0).isoformat().replace('+00:00', 'Z')

        # 提取视频的现有信息，以便在更新时保留
        title = snippet.get('title', '无标题')
        description = snippet.get('description', '')
        tags = snippet.get('tags', [])
        category_id = snippet.get('categoryId', '22') # '22' 是“People & Blogs”的默认分类ID

        print(f"计划将视频 '{title}' (ID: {video_id}) 设置为 {publish_at_iso} 发布。")
        update_video_publish_time(youtube_service, video_id, title, description, tags, category_id, publish_at_iso)

    print("\n所有不公开视频的定时发布设置已完成。")


set_videos_schedule(token_path)
