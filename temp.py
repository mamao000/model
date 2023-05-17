import csv
import re
import json
from datetime import datetime



### for work

import chardet

work_list=[]

with open ("perfect_user_data.txt","r",newline="",encoding='utf-8' ,errors='ignore') as csvfile:
    rows=csv.reader(csvfile)
    for i in rows: 
        #Work
        # 讀取 JSON 檔案
        with open("data.json", "r") as file:
            data = json.load(file)
        temp=i[0].lower()
        # 以 "、、、" 切割文本成多個片段
        fragments = re.split(r"\s+|、、、", temp)
        print(fragments)

        # 尋找對應的大職業
        temp_work = ""
        for fragment in fragments:
            for occupation, content in data.items():
                # 將每個小職業轉換為小寫形式
                lowercase_content = [occupation.lower() for occupation in content["content"]]
                if fragment in lowercase_content:
                    temp_work=occupation
        work_list.append(temp_work)

print(work_list)
        
