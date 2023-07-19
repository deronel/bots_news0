import json
# url =  'https://www.securitylab.ru/news/539814.php'

# article_id = url.split("/")[-1]
# article_id = article_id[:-4]
# print(article_id)

with open("news_dict.json")as file:
        news_dict = json.load(file)

search_id = "539834"

if search_id in news_dict:
        print("Новость ужу есть в словаре")
else:
        print("обновился словарь")        
