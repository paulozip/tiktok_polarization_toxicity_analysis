import json
import os
from re import I
import pandas as pd

from tqdm import tqdm

raw_data_dir = 'data/raw/'
raw_data = os.listdir(raw_data_dir)

parsed_videos_list = []

for file in raw_data:
    if not file.endswith('.json'):
        continue
    
    print('Parsing {} file'.format(file))

    with open(raw_data_dir + file, 'r') as f:
        video_data = json.load(f)

    for video in tqdm(video_data):
        video_dict = {}
                
        # Search metadata
        video_dict['search_tag'] = file.replace('raw_dataset_', '').replace('.json', '')
        video_dict['video_path'] = 'data/videos/{}.mp4'.format(video['id'])
        video_dict['video_classes'] = None

        # Overall information about the video
        video_dict['id'] = video['id']
        video_dict['desc'] = video['desc']
        video_dict['create_time'] = video['createTime']
        video_dict['is_duet_enabled'] = video['duetEnabled']
        video_dict['hashtags'] = ', '.join(tag['hashtagName'] for tag in video['textExtra']) if 'textExtra' in video else None

        # Video info
        video_dict['cover'] = video['video']['cover']
        video_dict['play_address'] = video['video'].get('playAddr')
        video_dict['download_address'] = video['video'].get('downloadAddr')
        video_dict['duration'] = video['video']['duration']
        
        # Collecting text from stickers
        if 'stickersOnItem' in video:
            video_dict['stickers_on_video'] = ' '.join(' '.join(sticker['stickerText']) for sticker in video['stickersOnItem'])
        else:
            video_dict['stickers_on_video'] = None

        # Video music
        video_dict['music_id'] = video['music']['id']
        video_dict['music_title'] = video['music']['title']
        video_dict['music_url'] = video['music'].get('playUrl')
        video_dict['music_author'] = video['music'].get('authorName')
        video_dict['music_is_original_audio'] = video['music']['original']

        # Video duet info
        video_dict['duet_from_id'] = video['duetInfo']['duetFromId']

        # Video stats
        video_dict['digg_count'] = video['stats']['diggCount']
        video_dict['share_count'] = video['stats']['shareCount']
        video_dict['comment_count'] = video['stats']['commentCount']
        video_dict['play_count'] = video['stats']['playCount']

        # Video author
        video_dict['author_unique_id'] = video['author']['uniqueId']
        video_dict['author_nickname'] = video['author']['nickname']
        video_dict['author_avatar'] = video['author']['avatarMedium']
        video_dict['author_signature'] = video['author']['signature']
        video_dict['author_is_verified'] = video['author']['verified']
        video_dict['author_duet_setting'] = video['author']['duetSetting']

        # Author stats
        video_dict['author_following_count'] = video['authorStats']['followingCount']
        video_dict['author_followers_count'] = video['authorStats']['followerCount']
        video_dict['author_heart_count'] = video['authorStats']['heartCount']
        video_dict['author_digg_count'] = video['authorStats']['diggCount']
        video_dict['author_heart'] = video['authorStats']['heart']

        parsed_videos_list.append(video_dict)

# Generating pandas DataFrame
print('Creating dataframe. ', end='')
dataframe = pd.DataFrame.from_dict(parsed_videos_list)
dataframe.to_csv('data/processed/parsed_dataset.csv', sep=';', index=False)
print('Done!')