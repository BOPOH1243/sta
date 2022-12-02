# REST API для ФСТР
Реализовал метод submitData для работы с REST запросом формы
```sh
{
  "beauty_title": "пер. ",
  "title": "Пхия",
  "other_titles": "Триев",
  "connect": "",
 
  "add_time": "2021-09-22 13:18:13",
  "user": {"email": "qwerty@mail.ru", 		
        "fam": "Пупкин",
	"name": "Василий",
	"otc": "Иванович",
        "phone": "+7 555 55 55"}, 
	
   "coords":{
  "latitude": "45.3842",
  "longitude": "7.1525",
  "height": "1200"},
  
  "level":{
      "winter": "", 
      "summer": "1А",
      "autumn": "1А",
      "spring": ""},
 
   "images": [{"data":"<картинка1>", "title":"Седловина"}, {"data":"<картинка2>", "title":"Подъём"}]
}
```
## Содержание
- [Технологии](#технологии)
- [API](#api)
## Технологии
- [Python](https://www.python.org/)
## API
сам метод 
>submitData 
нужен только для того, чтобы загружать данные на сервер, сами же данные я предлагаю брать с помощью методов, описанных с помощью swagger
>/swagger
GET/POST/PUT/DELETE 
/perevals возвращает список перевалов с пагинацией
/perevals/*id* возвращает информацию по перевалу, где:
```sh
"id":уникальный идентификатор
"beauty_title":название типа
"title":название
"other_titles":третье название
"add_time":время добавления
"status":статус(new, pending, accepted или rejected)
"coords":ссылка на id модели координат /coords/*id*
"level":ссылка на id модели сложности перевала /level/*id*
"images":массив ссылок на картинки перевала с описаниями /images/*id*
"areas":массив ссылок на зоны перевала /areas/*id*
```
также есть возможность фильтровать перевалы по id создателя и уникальному email создателя с помощью параметров 
>/perevals/?user_id= & user_email= 
соответственно


а лучше просто не пользуйтесь submitData, а делайте post /perevals, ибо submitData в данном случае как телеге пятое колесо, я не знаю зачем его делать надо было
