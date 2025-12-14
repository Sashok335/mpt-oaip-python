import json
data={'название':'Франция', 'столица':'Париж', 'население':'67000000'}

with open('country.json','w',encoding='utf-8',newline="") as file:
    json.dump(data,file,ensure_ascii=False,indent=2)
