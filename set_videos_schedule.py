
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
