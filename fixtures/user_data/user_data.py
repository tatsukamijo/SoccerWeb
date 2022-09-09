import json
import csv

# データは以下のurlのデータ。ここからcsvファイルで持ってきた。
# https://www.stat.go.jp/data/nihon/back15/21.html

json_list = []
pk = 0

#元データを開く（user_data.csv）
with open('user_data.csv', mode='r', encoding='utf-8') as rf:
    reader = csv.reader(rf)
    next(reader)
    for line in reader:
        pk += 1
        age = line[0]
        male_height = int(float(line[2]))
        male_weight = int(float(line[4]))
        female_height = int(float(line[6]))
        female_weight = int(float(line[8]))
        json_list.append( {'model': 'app.user_data', 'pk':pk, 'fields': {
            'age':age, 'male_height':male_height, 'male_weight':male_weight,'female_height':female_height, 'female_weight':female_weight}
            }
            )

#jsonデータを作成
with open('user_data.json', 'w', encoding='utf-8') as f:
    json.dump(json_list, f, indent=2, ensure_ascii=False)