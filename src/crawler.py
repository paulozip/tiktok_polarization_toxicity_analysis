import json
import random
import string
from time import sleep

from TikTokApi import TikTokApi
from tqdm import tqdm


def save_to_json(filename, data):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)

def save_to_mp4(filename, data):
    with open(filename, 'wb') as outfile:
        outfile.write(data)

def get_data_by_hashtag(tag, retries=5):
    if retries > 0:
        try:
            return api.by_hashtag(tag, count=RESULTS)
        except Exception as err:
            print('An error ocurred: ', err)
            sleep(30)
            return get_data_by_hashtag(tag, retries=retries-1)
    else:
        raise Exception('Maximum attemps reached. Request failed.')

def download_video(video, retries=5):
    if retries > 0:
        try:
            video_bytes = api.get_video_by_tiktok(video)
            save_to_mp4('data/videos/{}.mp4'.format(video['id']), video_bytes)
        except Exception as err:
            print('An error ocurred while downloading video: ', err)
            sleep(30)
            download_video(video, retries=retries-1)
    else:
        print('Maximum attemps reached to download video. Request failed.')
        return

custom_verify = ''
did = ''.join(random.choice(string.digits) for _ in range(19))

api = TikTokApi.get_instance(custom_verifyFp=custom_verify,
                            use_test_endpoints=True, 
                            did=did)

RESULTS = 1000
TAGS = [
    'direita',
    'esquerda',
    'leftiktok',
    'lefttiktok',
    'rightiktok',
    'righttiktok',
    'lula',
    'ciro',
    'cirogomes',
    'bolsonaro',
    'politica',
    'politicabrasileira'
]

parsed_videos_list = []
parsed_videos_id = [] # Storing videos that were already parsed to avoid duplication

# Parsing each tag
for tag in TAGS:
    print('Parsing videos for "{}" tag'.format(tag))
    raw_videos_list = get_data_by_hashtag(tag)

    # Save raw dataset to file
    save_to_json('data/raw/raw_dataset_{}.json'.format(tag), raw_videos_list)

    for video in tqdm(raw_videos_list, desc=tag):
        # Skipping videos already parsed
        if video['id'] in parsed_videos_id:
            continue

        # Downloading video
        download_video(video)

        parsed_videos_id.append(video['id'])
