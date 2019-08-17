# coding: utf-8

result = ""
while True:
    input_data = str(input())
    if input_data=="":
        break
    result+='objects.'+input_data+","
print(result)