# python3.10 scraping.pyで実行

import requests
from bs4 import BeautifulSoup
# 文字列のパターンで検索できるモジュールreをインポート
import re
# サーバ負荷軽減のために処理の時間をずらすためのtimeをインポート
import time
# jsonファイル作成のため
import json

# youtube data api v3を利用するために必要なもの
# ここから------------------------------------------
from apiclient.discovery import build

import os
from datetime import datetime
import json
from googleapiclient.discovery import build

from .youtube_key import YOUTUBE_KEY, YOUTUBE_SERVICE, YOUTUBE_VERSION, GOOGLE_API,GOOGLE_ID

DEVELOPER_KEY = YOUTUBE_KEY
YOUTUBE_API_SERVICE_NAME = YOUTUBE_SERVICE
YOUTUBE_API_VERSION = YOUTUBE_VERSION
GOOGLE_API_KEY = GOOGLE_API
engine_id = GOOGLE_ID


youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)
# ------------------------------------------ここまで

# 平均の体重・身長を出すために配列に一旦格納しておく。
# height_total_array = [] # 1回目は使う。2回目はコメントアウト
# weight_total_array = [] # 1回目は使う。2回目はコメントアウト
weight_average = 75 # 1回目はコメントアウト。2回目は使う
height_average = 182 # 1回目はコメントアウト。2回目は使う

# ここから、各選手のurl取得、次ページの取得、各選手のページからの情報取得、次のページへの遷移を全て15回繰り返す。
# サーバの負荷軽減のため10秒の間隔をあけて。25回で。
for z in range(25):

    # スクレイピングするページのurl（Top Rated Players）
    url = f'https://en.soccerwiki.org/search/player?firstname=&surname=&nationality=&leagueid=&position=&minrating=90&maxrating=99&minage=15&maxage=60&country=&minheight=150&maxheight=220&foot=&submit=15&offset={z*15}'
    # urlのページをスクレイピング（一番下で更新）
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")

    # pidで検索をかける。各選手のurl取得のため。
    elems = soup.find_all(href=re.compile("pid"))
    # 各選手のurlを配列に保管する。ここで、長さは15でなければいけない。
    url_array_players = []
    for i in range(30):
        if i % 2 == 0:
            url_array_players.append(elems[i].attrs['href'])
    # ここまではできた。url_array_playersの配列の中に、上位15人の選手のurlが入った。

    for i in range(3,15): # 15
        # 各選手のurlに遷移していく。
        right_url = 'https://en.soccerwiki.org' + url_array_players[i]
        r_1 = requests.get(right_url)
        soup_1 = BeautifulSoup(r_1.content, "html.parser")
        # 選手のプロフィールを抽出する（利き足のところを含んだ数個だけclassが違ったため_1と_2ができた。
        player_profiles_1 = soup_1.find_all("p", class_="player-info-subtitle mb-2")
        player_profiles_2 = soup_1.find_all("p", class_="player-info-subtitle mt-3 mb-2")
        player_profile_image = soup_1.find_all("img", class_="lozad img-fluid bg-light")
        for j in range(len(player_profiles_1)):
            if j == 0:
                p = player_profiles_1[j].contents
                player_full_name = p[1]
                print(player_full_name)
            elif j == 1:
                p = player_profiles_1[j].contents
                player_short_name = p[1]
                print(player_short_name)
            elif j == 2:
                p = player_profiles_1[j].contents
                player_position = p[2].text
                print(player_position)
            elif j == 4:
                p = player_profiles_1[j].contents
                player_age = p[1]
                print(player_age)
            elif j == 6:
                p = player_profiles_1[j].contents
                player_height = int(p[1])
                print(player_height)
            elif j == 7:
                p = player_profiles_1[j].contents
                player_weight = int(p[1])
                print(player_weight)
        p = player_profiles_2[1].contents
        player_foot = p[1]
        if player_foot == ' Both':
            player_foot = 'Right and Left'
        print(player_foot)
        # 選手の特徴のタグを抽出。
        player_attributes = soup_1.find_all(True, class_="col-12 col-md-12 col-lg-4 mb-2")
        player_attributes_array = []
        for j in range(len(player_attributes)):
            player_attributes_array.append(player_attributes[j].text)
        print(player_attributes_array)

        # positionの括弧内のものをうまく全部反映させる。
        player_position_list = list(map(str,player_position.split(',')))
        print(player_position_list)
        if player_position_list[0] != 'Gk':
            for pos in range(len(player_position_list)):
                if player_position_list[len(player_position_list) - pos - 1][-1] == ')':
                    for comma in range(len(player_position_list[len(player_position_list) - pos - 1])):
                        add_comma = list(map(str, player_position_list[len(player_position_list) - pos - 1].split('(')))
                        inside_comma = list(map(str, add_comma[1].split(')')))
                        inside = inside_comma[0]
                else:
                    player_position_list[len(player_position_list) - pos - 1] = player_position_list[len(player_position_list) - pos - 1] + '(' + inside + ')'
            for hey in range(len(player_position_list)):
                if hey == 0:
                    player_position = player_position_list[hey]
                else:
                    player_position = player_position + ', ' + player_position_list[hey]
        print(player_position)
        
        # for image in player_profile_image:
        #     player_image = image['data-src']
        # print(player_image)





        # Google検索から選手の日本語名を取得。
        q_google = player_full_name + '　' + 'サッカー' + '　' + 'ウィキペディア'
        google_url = 'https://www.google.com/search?q=' + q_google
        google = requests.get(google_url)
        google.raise_for_status()
        soup_google = BeautifulSoup(google.content, "html.parser")
        google_list = soup_google.select('div.kCrYT > a')
        name = list(google_list[0].text)
        cnt = 0
        for text in range(len(name)):
            if name[text] == '-':
                cnt = text - 1
                break
        japanese_array = name[:cnt]
        japanese_name = "".join(japanese_array)
        print(japanese_name)



        # Google検索からWikipediaでの選手の表示名を取得（英語）。
        q_google_english = player_full_name + 'football' + 'wikipedia'
        google_url_english = 'https://www.google.com/search?q=' + q_google_english
        google_english = requests.get(google_url_english)
        google_english.raise_for_status()
        soup_google_english = BeautifulSoup(google_english.content, "html.parser")
        google_list_english = soup_google_english.select('div.kCrYT > a')
        # google_list_english = soup_google_english.find("h3", class_=True)
        if google_list_english == []:
            wiki_name = player_full_name
            # google_list_english = soup_google_english.find("h3", class_=True)
            # print('wow')
        else:
            # print(google_list_english)
            name_english = list(google_list_english[0].text)
            cnt_english = 0
            for text in range(len(name_english)):
                if name_english[text] == '-':
                    cnt_english = text - 1
                    break
            wiki_array = name_english[:cnt_english]
            wiki_name = "".join(wiki_array)
            print(wiki_name)
            # <h3 class="LC20lb MBeuO DKV0Md">Mohamed Salah - Wikipedia</h3>



        # Wikipediaから選手の画像を入手
        wiki_url = 'https://en.wikipedia.org/wiki/' + wiki_name
        wiki = requests.get(wiki_url)
        soup_wiki = BeautifulSoup(wiki.content, "html.parser")
        wiki_image = soup_wiki.find_all("a", class_="image")
        wiki_i = wiki_image[0].find("img")
        print(wiki_i)
        wiki_image = wiki_i.get('src')
        if wiki_image == '//upload.wikimedia.org/wikipedia/commons/thumb/f/f1/Sports_current_event.svg/46px-Sports_current_event.svg.png':
            wiki = requests.get(wiki_url)
            soup_wiki = BeautifulSoup(wiki.content, "html.parser")
            wiki_image = soup_wiki.find_all("a", class_="image")
            wiki_i = wiki_image[1].find("img")
            wiki_image = wiki_i.get('src')
            if wiki_image == 'http://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Disambig_gray.svg/25px-Disambig_gray.svg.png':
                wiki = requests.get(wiki_url)
                soup_wiki = BeautifulSoup(wiki.content, "html.parser")
                wiki_image = soup_wiki.find_all("a", class_="image")
                wiki_i = wiki_image[2].find("img")
                wiki_image = wiki_i.get('src')
        elif wiki_image == '//upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Disambig_gray.svg/25px-Disambig_gray.svg.png':
            wiki = requests.get(wiki_url)
            soup_wiki = BeautifulSoup(wiki.content, "html.parser")
            wiki_image = soup_wiki.find_all("a", class_="image")
            wiki_i = wiki_image[1].find("img")
            wiki_image = wiki_i.get('src')
        player_image = 'http:' + wiki_image
        # print(wiki_image['src'])
        print(player_image)

        # 27 カゼミーロ
        # https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/20180610_FIFA_Friendly_Match_Austria_vs._Brazil_Casemiro_850_1575.jpg/800px-20180610_FIFA_Friendly_Match_Austria_vs._Brazil_Casemiro_850_1575.jpg
        # 35 ヴィニシウス・ジュニオール
        # https://upload.wikimedia.org/wikipedia/commons/thumb/f/f3/Vinicius_Jr_2021.jpg/400px-Vinicius_Jr_2021.jpg
        # 45 ロバートソン　
        # （サッカー選手）を消す。

        # Googleのcustom search apiで画像を入手
        KEYWORD = player_full_name + 'wikipedia'
        if __name__ == '__main__':
            # Google Customサーチ結果を取得
            s = build("customsearch", 'v1', developerKey = GOOGLE_API_KEY)
            r = s.cse().list(q = KEYWORD,
            cx = engine_id,
            lr = 'lang_ja',
            num = 1,
            start = 1).execute()

        # レスポンスをjson形式で保存
        s = json.dumps(r, ensure_ascii = False, indent = 4)
        now = datetime.today().strftime("%Y%m%d%H%M%S")
        with open('./res_' + now + '.json', mode='w') as f:
            f.write(s)

        # youtubeのapiを利用して検索結果を保存
        # ここから-------------------------------
        # q = player_full_name + ' ' + 'soccer' + ' ' + 'skills'
        # max_results = 1
        # search_response = youtube.search().list(
        # q=q,
        # # part="id,snippet",
        # part="id",
        # # fields='items(id(videoId),snippet(title,thumbnails(default(url))))',
        # fields='items(id(videoId))',
        # type='video',
        # maxResults=max_results
        # ).execute()

        # youtube_results = search_response['items']
        # print(youtube_results)

        # # # 1つ目
        # youtube_result_1 = youtube_results[0]
        # # print(youtube_result_1)
        # # print(youtube_result_1['snippet']['title'])
        # # print(youtube_result_1['snippet']['thumbnails']['default']['url'])
        # # player_youtube1_title = youtube_result_1['snippet']['title']
        # # player_youtube1_image_url = youtube_result_1['snippet']['thumbnails']['default']['url']
        # # player_youtube1_url = 'https://www.youtube.com/watch?v=%s' % youtube_result_1["id"]["videoId"]
        # # print(player_youtube1_url)
        # player_videoID = youtube_result_1["id"]["videoId"]
        # print(player_videoID)

        # # # 2つ目
        # # youtube_result_2 = youtube_results[1]
        # # print(youtube_result_2['snippet']['title'])
        # # print(youtube_result_2['snippet']['thumbnails']['default']['url'])
        # # player_youtube2_title = youtube_result_2['snippet']['title']
        # # player_youtube2_image_url = youtube_result_2['snippet']['thumbnails']['default']['url']
        # # player_youtube2_url = 'https://www.youtube.com/watch?v=%s' + youtube_result_2["id"]["videoId"]

        # # # 3つ目
        # # youtube_result_3 = youtube_results[2]
        # # print(youtube_result_3['snippet']['title'])
        # # print(youtube_result_3['snippet']['thumbnails']['default']['url'])
        # # player_youtube3_title = youtube_result_3['snippet']['title']
        # # player_youtube3_image_url = youtube_result_3['snippet']['thumbnails']['default']['url']
        # # player_youtube3_url = 'https://www.youtube.com/watch?v=%s' + youtube_result_3["id"]["videoId"]
        # # # -------------------------------ここまで



        # # 平均の体重・身長を出すために配列に格納しておく。
        # # weight_total_array.append(player_weight) # 1回目は使う。2回目はコメントアウト
        # # height_total_array.append(player_height) # 1回目は使う。2回目はコメントアウト

        # # # 平均との差を出しておく。
        player_weight_diff = player_weight - weight_average # 1回目はコメントアウト。2回目は使う
        player_height_diff = player_height - height_average # 1回目はコメントアウト。2回目は使う

        


        # ここからjsonファイル作成のためのコード！
        # 全ての要素を格納する辞書を作成。
        item = {
        'model': 'app.data',
        'pk': z*15+i+1,
        'fields': {
            'full_name': player_full_name,
            'short_name': player_short_name,
            'position': player_position,
            'age': player_age,
            'height': player_height,
            'weight': player_weight ,
            'height_diff': player_height_diff, # 1回目はコメントアウト。2回目は使う
            'weight_diff': player_weight_diff, # 1回目はコメントアウト。2回目は使う
            'attributes': player_attributes_array,
            # 'youtube1_title': player_youtube1_title,
            # 'youtube1_image': player_youtube1_image_url,
            # 'youtube1_url': player_youtube1_url,
            # 'youtube2_title': player_youtube2_title,
            # 'youtube2_image': player_youtube2_image_url,
            # 'youtube2_url': player_youtube2_url,
            # 'youtube3_title': player_youtube3_title,
            # 'youtube3_image': player_youtube3_image_url,
            # 'youtube3_url': player_youtube3_url,
            'image': player_image,
            # 'video': player_videoID,
            'foot': player_foot,
            'name_nihon': japanese_name,
        } 
        }

        # iが0の時は上書き保存して、iが1の時は配列を作成して、それ以外の場合は読み込んだ後に配列を分解して、
        # 新たな配列に追加する。（分解しないと多重配列になっていってしまったため）
        filename = './data2.json'
        if z == 0 and i == 0:
            json_file = open(filename, mode="w")
            json.dump(item, json_file, indent=2, ensure_ascii=False)
            json_file.close()    
        elif z == 0 and i == 1:
            with open(filename, 'r') as f:
                read_data = json.load(f)
            save_data = read_data, item
            with open(filename, 'w') as f:
                json.dump(save_data, f, indent=2, ensure_ascii=False)
        else:
            with open(filename, 'r') as f:
                read_data = json.load(f)
            save_data = []
            for j in range(len(read_data)):
                save_data.append(read_data[j])
            save_data.append(item)
            with open(filename, 'w') as f:
                json.dump(save_data, f, indent=2, ensure_ascii=False)

        # サーバの負荷軽減。
        time.sleep(2)
    
    print('------------------------------------------------------------------')
    
    # サーバの負荷軽減。
    time.sleep(3)

# 一旦平均を出すため
# weight_average = sum(weight_total_array) // len(weight_total_array) # 1回目は使う。2回目はコメントアウト
# height_average = sum(height_total_array) // len(height_total_array) # 1回目は使う。2回目はコメントアウト
# print(weight_average)
# print(height_average)