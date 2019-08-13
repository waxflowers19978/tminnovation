# coding: utf-8

# コード説明
# input:1
# input:2
# input:3
# output:['1','1'],[2','2'],[3','3']


result = "['"

while True:
    text = str(input("input:"))
    if text=="":
        result = result[:-5]
        text+="']"
        result+=text
        break
    else:
        text = text+"','"+text+"'],['"
        result+=text
print(result)


# 全国大会優勝レベル
# 全国大会入賞レベル
# 全国大会出場常連レベル
# 全国大会出場レベル
# 都道府県大会入賞レベル
# 都道府県大会常連レベル
# 都道府県大会出場レベル
# 地区大会入賞レベル
# 地区大会常連レベル


