import csv
import re
import json
from datetime import datetime

work_list=[]
edu_list=[]
age_list=[]
state_list=[]
gender_list=[]
zodiac_list=[]

def check_whether_time(part):
    for i in range(1980,2024):
        if part.find(str(i))!=-1:
            return True
    
    for i in ["January","February","March","April","May","June","July","August","September","October","November","December"]: 
        if part.find(i)!=-1:
            return True
    
    return False



### for work

import chardet

# 讀取 CSV 檔案
# with open("perfect_user_data.csv", 'rb') as f:
#     data = f.read()

# # 使用 chardet 模組來推測編碼方式
# result = chardet.detect(data)
# encoding = result['encoding']

# print(encoding)

# with open ("perfect_user_data.csv","r",newline="",encoding=encoding) as csvfile:
#     # rows = csvfile.read().decode("utf-8")
#     rows=csv.reader(csvfile)
#     #data = csvfile.read().decode("utf")
#     #rows = csv.reader(data.splitlines())
    
#     ### Naive Crawl for job list (slot before time)

#     ### we can design more rule like the slot space to precisely get it

#     ### we can regular these varifying jobs to normal jobs like 20 category (by hard code?)

#     for row_num,i in enumerate(rows):
#         i=i[0]
#         analyza_row=i.split("、、、")
#         work_list.append([])
#         for index,work_part in enumerate(analyza_row):
#             if check_whether_time(work_part) == True and index-1 >=0:
#                 #print("get work : ", analyza_row[index-1])
#                 work_list[row_num].append(analyza_row[index-1])
#             else:
#                 pass


with open ("perfect_user_data.txt","r",newline="",encoding='utf-8' ,errors='ignore') as csvfile:
    rows=csv.reader(csvfile)
    for i in rows:
        #Education
        if i[1]=="":
            edu_list.append(i[1])
        else:
            temp_edu=""
            if i[1].find("High school")!=-1:
                temp_edu="High School"
            if i[1].find("College")!=-1 or i[1].find("Bachelor")!=-1 or i[1].find("University")!=-1:
                temp_edu="University"
            if i[1].find("Master")!=-1 or i[1].find("Graduate School")!=-1:
                temp_edu="Master"

            if temp_edu=="":
                temp_edu="" 
                print("Error convertion check ",i)

            edu_list.append(temp_edu)

        #Age
        match = re.search(r"\d{4}", i[2])
        temp_age=""
        if match:
            #print("ok")
            date_obj = datetime.strptime(i[2], "%B %d, %Y")
            temp_age = date_obj.year
            age_list.append(temp_age)
        else:
            age_list.append(temp_age)

        #State
        state_categories = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']
        temp_state=""
        for state in state_categories:
            if state in i[3]:
                temp_state=state
        state_list.append(temp_state)

        #Gender
        gender_categories = ['Male', 'Female']

        temp_gender=""
        for gender in gender_categories:
            if gender in i[4]:
                temp_gender=gender
        gender_list.append(temp_gender)

        #Zodiac
        zodiac_categories = ['Aquarius', 'Pisces', 'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn','Aquarius']
        zodiac_end_dates = [20, 19, 21, 20, 21, 22, 23, 23, 23, 22, 21, 22]
        pattern = r"^\b(January|February|March|April|May|June|July|August|September|October|November|December)\b\s\d{1,2}(?:,\s\d{4})?$"
        match = re.search(pattern, i[2])
        temp_zodiac=""
        if match:
            #print("ok")
            try:
                date = datetime.strptime(i[2], "%B %d, %Y")
            except ValueError:
            # 轉換失敗，試著加上當前年份再轉換
                i[2] += " " + str(datetime.now().year)
                date = datetime.strptime(i[2], "%B %d %Y")
            month, day = date.month, date.day
            #print(month, day)
            temp_zodiac=zodiac_categories[month - (day < zodiac_end_dates[month - 1])]
            zodiac_list.append(temp_zodiac)
        else:
            zodiac_list.append(temp_zodiac)
        
        #Work
        # 讀取 JSON 檔案
        with open("data.json", "r") as file:
            data = json.load(file)
        temp=i[0].lower()
        # 以 "、、、" 切割文本成多個片段
        #fragments = temp.split("、、、"," ")
        fragments = re.split(r"\s+|、、、", temp)

        # 尋找對應的大職業
        temp_work = ""
        for fragment in fragments:
            for occupation, content in data.items():
                # 將每個小職業轉換為小寫形式
                lowercase_content = [occupation.lower() for occupation in content["content"]]
                if fragment in lowercase_content:
                    print(fragment)
                    temp_work=occupation
        work_list.append(temp_work)

        

# 將所有列表合併為一個列表
rows = zip( edu_list, age_list, state_list, gender_list,zodiac_list,work_list)

#print(rows)

# 開啟 CSV 檔案，指定編碼為 UTF-8
with open('output.csv', mode='w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    
    # 寫入表頭
    writer.writerow([ 'education', 'birth_year', 'state', 'gender','zodiac','work'])
    
    # 寫入資料
    for row in rows:
        writer.writerow(row)



#### now you can use edu_list , work_list for each user

print("Edu length=",len(edu_list))
print("Work length=",len(work_list))

"""
for index,i in enumerate(work_list):
    print(i)
    if index >= 50:
        break
"""


