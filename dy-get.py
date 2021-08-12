# -*- coding: UTF-8 -*-

import json
import os
import re
import time
import requests
from datetime import datetime
from time import gmtime
from time import strftime
import random
from weblfasr import AsrRequest

# https://v.douyin.com/en5sHBB/ 梅姐
# https://v.douyin.com/encHPdK/ 老石
# https://v.douyin.com/ecFrH4n/ Mia妈妈乐学大本营
# https://v.douyin.com/ecFr2L4/ 游戏程序员陈天霸
#
# 蜗牛叔叔讲绘本
# https://v.douyin.com/eENM3SG/
#
# 桐话创业
# https://v.douyin.com/eEN6unE/
#
# 英语子龙老师
# https://v.douyin.com/eENPdtY/
#
# 路小曼
# https://v.douyin.com/eENGQEU/
#
# 少儿编程李老师
# https://v.douyin.com/eENVxjS/
#
# 活在北京
# https://v.douyin.com/eEF8bTe/
#
# 北京创业故事
# https://v.douyin.com/eEFjxsy/
#
# 演讲黑客王小宁
# https://v.douyin.com/eENTnm9/
#
# 地产酵母
# https://v.douyin.com/eEFFhfR/
#
# 廖恒悦
# https://v.douyin.com/eEF1bYf/
#
# 北大丁教授
# https://v.douyin.com/eENKMc1/

USER_URL = 'https://v.douyin.com/eENVxjS/'

API_AWEME_LIST = 'https://www.iesdouyin.com/web/api/v2/aweme/post/?sec_uid=%s&count=30&max_cursor=%s&aid=1128&_signature=&dytk='
API_ITEM_INFO = 'https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids=%s'
FFMPEG = r'D:\Application\ffmpeg-4.4-full_build\bin\ffmpeg -i "%s" "%s"'
DOWNLOAD_PATH = "Download"

USER_AGENT_LIST = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
]


class VideoInfo:
    def __init__(self, json):
        self.desc = json['desc']
        self.aweme_id = json['aweme_id']
        self.play_url = json['video']['play_addr']['url_list'][0]
        self.create_time = 0
        self.create_datetime = ''
        self.music_title = ''
        self.music_url = ''
        self.music_author = ''
        self.comment_count = json['statistics']['comment_count']
        self.digg_count = json['statistics']['digg_count']
        self.share_count = json['statistics']['share_count']
        self.duration = json['video']['duration']
        self.share_url = ''
        self.author_nickname = re.sub(r'[\\/:*?"<>|\r\n ]+', '_', json['author']['nickname'])
        self.signature = json['author']['signature']
        self.scripts = ''

    def set_extra_info(self, json):
        self.create_time = json['create_time']
        self.create_datetime = datetime.utcfromtimestamp(self.create_time).strftime('%Y/%m/%d %H:%M:%S')
        self.share_url = json['share_url']

        if 'music' in json:
            music = json['music']
            if music is not None:
                self.music_title = music['title']
                self.music_author = music['author']
                if music['play_url'] and music['play_url']['url_list'] and len(music['play_url']['url_list']) > 0:
                    self.music_url = music['play_url']['url_list'][0]


class DYGet:
    def __init__(self, user_url):
        self.user_url = user_url

    def check_download_dir_exist(self, nickname):
        download_dir = os.path.join(os.getcwd(), DOWNLOAD_PATH, nickname)
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

    def get_user_key(self):
        response = requests.get(self.user_url)
        s = response.url[28:]
        key = s[0:s.index('?')]
        return key

    def get_aweme_info(self, aweme_id):
        user_agent = random.choice(USER_AGENT_LIST)
        headers = {'user-agent': user_agent}
        response = requests.get(url=API_ITEM_INFO % aweme_id, headers=headers)
        if len(response.text) <= 0:
            try_count = 0
            while True:
                time.sleep(1 * (try_count + 1))
                user_agent = random.choice(USER_AGENT_LIST)
                headers = {'user-agent': user_agent}
                response = requests.get(url=API_ITEM_INFO % aweme_id, headers=headers)
                if len(response.text) > 0:
                    return json.loads(response.text)
                try_count = try_count + 1
                if try_count > 100:
                    print(f'{aweme_id} 无法获取详情')
                    break
        else:
            return json.loads(response.text)

    def get_author_dir(self, v):
        return os.path.join(os.getcwd(), DOWNLOAD_PATH, v.author_nickname)

    def get_video_list(self):
        key = self.get_user_key()
        max_cursor = 0
        video_info_list = []
        page = 0
        while True:
            print(f'正在获取第{page}页视频列表……')
            url = API_AWEME_LIST % (key, max_cursor)
            response = requests.get(url)
            respJson = json.loads(response.text)

            aweme_list = respJson['aweme_list']
            has_more = respJson['has_more']
            max_cursor = respJson['max_cursor']

            if aweme_list != []:
                for aweme in aweme_list:
                    video_info_list.append(VideoInfo(aweme))

            if has_more == False:
                break

            page = page + 1

        total = len(video_info_list)
        print(f'共{total}个视频')

        count = 0
        for v in video_info_list:
            count = count + 1
            print(f'正在获取详情 {count}, {int((count / total) * 100)}% {v.aweme_id} 【{v.desc}】')
            json_info = self.get_aweme_info(v.aweme_id)
            v.set_extra_info(json_info['item_list'][0])

        return video_info_list

    def download(self, video_list):
        count = 0
        total = len(video_list)
        for v in video_list:
            count = count + 1
            print(f'正在下载 {count}, {int((count / total) * 100)}% {v.aweme_id}【{v.desc}】')

            self.check_download_dir_exist(v.author_nickname)

            author_dir = self.get_author_dir(v)
            file = os.path.join(author_dir, v.aweme_id + '.mp4')
            if os.path.isfile(file):
                print('跳过下载 ' + file)
            else:
                resp = requests.get(v.play_url)
                with open(file, 'wb') as f:
                    f.write(resp.content)

            if len(v.music_url) > 0:
                file = os.path.join(author_dir,
                                    re.sub(r'[\\/:*?"<>|\r\n ]+', '_', v.music_author + '_' + v.music_title + '.mp3'))
                if os.path.isfile(file):
                    print('跳过下载 ' + file)
                else:
                    resp = requests.get(v.music_url)
                    if resp.ok:
                        with open(file, 'wb') as f:
                            f.write(resp.content)

    def write_report(self, video_list):
        author_nickname = 'ERROR_NICKNAME'
        if len(video_list) > 0:
            author_nickname = video_list[0].author_nickname

        self.check_download_dir_exist(author_nickname)

        report = ['\t'.join(['ID', '标题', '文案', '音乐', '创作时间', '视频时长', '点赞', '评论', '分享', '链接'])]
        for v in video_list:
            line = []
            line.append(v.aweme_id)
            line.append(v.desc)
            line.append(v.scripts)
            line.append(v.music_title)
            line.append(v.create_datetime)
            line.append(strftime("%M:%S", gmtime(v.duration * 0.001)))
            line.append(str(v.digg_count))
            line.append(str(v.comment_count))
            line.append(str(v.share_count))
            line.append(v.share_url)

            report.append('\t'.join(line))

        report_str = '\n'.join(report)
        author_dir = os.path.join(os.getcwd(), DOWNLOAD_PATH, author_nickname)
        with open(os.path.join(author_dir, author_nickname + '_统计报表.txt'), 'wb') as f:
            f.write(report_str.encode("UTF-8"))

    def mp4_to_mp3(self, video_list):
        count = 0
        total = len(video_list)
        for v in video_list:
            count = count + 1
            print(f'正在转码 {count}, {int((count / total) * 100)}% {v.aweme_id}【{v.desc}】')

            author_dir = self.get_author_dir(v)
            mp4file = os.path.join(author_dir, v.aweme_id + '.mp4')

            mp3_dir = author_dir + '_mp3'
            if not os.path.exists(mp3_dir):
                os.makedirs(mp3_dir)

            mp3file = os.path.join(mp3_dir, v.aweme_id + '.mp3')

            if os.path.isfile(mp4file) and not os.path.isfile(mp3file):
                os.system(FFMPEG % (mp4file, mp3file))
            else:
                print(f'跳过转码 {mp4file} -> {mp3file}')

    def audio_to_text(self, video_list):
        count = 0
        total = len(video_list)
        for v in video_list:
            count = count + 1
            print(f'正在提取文案 {count}, {int((count / total) * 100)}% {v.aweme_id}【{v.desc}】')

            mp3_dir = self.get_author_dir(v) + '_mp3'
            mp3file = os.path.join(mp3_dir, v.aweme_id + '.mp3')
            if os.path.isfile(mp3file):
                try:
                    asr_req = AsrRequest(mp3file)
                    result = asr_req.request()
                    v.scripts = result
                    print(mp3file + ' ' + result)
                except:
                    print('提取方案异常 ' + mp3file)
            else:
                print('文件不存在 ' + mp3file)


if __name__ == "__main__":
    dyget = DYGet(USER_URL)
    video_list = dyget.get_video_list()
    # dyget.download(video_list)
    # dyget.mp4_to_mp3(video_list)
    # dyget.audio_to_text(video_list)
    dyget.write_report(video_list)

    print('完成')
