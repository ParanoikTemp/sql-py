# sql-py
python script for sql  

Наверное это глупо, но почему бы не попробовать.  
Я сделаю управление sql таблицами через класс в Python.  
Если че по голове не бейте дурачка. Погнали. 

Для удобства некоторые функции получили "синонимы". Пример: функция `create_table` выполняет абсолютно туже самую функцию что и `add_table`

# Класс Database
## Database(sqlfile, autosave=False)  
Создает класс объекта Database. С помощью этого объекта вы будете работать с выбранным вами файлом базы данных.  
Аргумент `sqlfile` принимает в себя файл базы данных (str). Если файла не существует, он автоматически создается.
Аргумент `autosave` принимает в себя True/False (bool). Если он установлен на True, то после каких либо обновлений БД они будут автоматически сохраняться.  
  
  
# Метод command
## command(cmd)
Я почти уверен что я не учел какую нибудь херню, либо у вас какой то очень извращенный запрос.  
На этот случай я создал этот метод. Он просто выполняет вашу команду в БД.  
Аргумент `cmd` принимает в себя строку (str) с вашей командой и выполняет её.  
  
  
# Метод set_table
## set_table(table)
Что бы работать с таблицами в моей библиотеке, эту таблицу надо выбрать.  
Аргумент `table` принимает в себя строку (str) с названием таблицы, которую вы будете использовать в последующих командах.  
Удобно если вы во всем проекте используете, например, всего одну таблицу.  
  
  
# Метод add_table, create_table
## add_table(table_name), create_table(table_name)
Эти методы создают новую таблицу в вашей базе данных.  
По умолчания, для корректного создания таблицы, в ней автоматически создается столбец с названием `sqlpynull`.  
При желании вы можете удалить его.  
Аргумент `table_name` принимает в себя строку (str) с названием новой таблицы.  


# Метод delete_table, drop_table
## delete_table(table_name=''), drop_table(table_name='')
Эти методы удаляют уже существующие таблицы в БД.  
Аргумент `table_name` принимает в себя строку (str) с названием удаляемой таблицы. Если аргумент не задан, то удаляется выбранная на момент удаления таблица.


# Метод db_save
## db_save()
Этот метод будет вам полезен если вы не используете автосохранение БД.
Вызов этого метода сохраняет внесенные вами изменения.  


# Метод rename_table
## rename_table(new_name)
Этот метод переименовывает выбранную на данный момент таблицу.  
Аргумент `new_name` принимает в себя строку (str) с новым названием таблицы.  


# Вспомогательный метод where
## where(_or=False, **cond)
Данный статический метод помогает в создании простейшего условия.  
Пример его работы покажу в этом коде:  
```python
import database

cond = database.Database.where(id=12345, name='Вася', name2='Пупкин')
print(cond)
# Выведет: id == 12345 AND name == "Вася" AND name2 == "Пупкин"
```
Вы можете заметить, что данный метод возвращает условие, которое будет удобно вставлять в другие методы.  
Аргумент `_or` принимает в себя True/False (bool). Если установить значение на True то смысл условия поменяется:  
```python
import database

cond = database.Database.where(_or=True, id=12345, name='Вася', name2='Пупкин')
print(cond)
# Выведет: id == 12345 OR name == "Вася" OR name2 == "Пупкин"
```  


# Метод select, search
## select(*names, _or=False, where=None, **cond), search(*names, _or=False, where=None, **cond)
Метод строит команду так:  
+ Сначала вводятся поочередно строковые аргументы. Их будет искать запрос
+ Далее в случае если вы не планируете использовать аргумент `where` то можете указать аргумент `_or`. Совокупность аргументов `_or` и `**cond` выполняет ту же функцию что и метод `where()`.
+ На случай если вам проще использовать вспомогательный метод `where()` либо у вас сложное условия которое вы напишете самостоятельно, то его нужно поместить в аргумент `where`.
Приведу пример: 
```python
import database

db = database.Database('game_bd.db', True)
db.set_table('players')
print(db.select('user_id', 'balance', sleep=0, sleep_timestamp=0))
# эквивалентно
print(db.select('user_id', 'balance', where=db.where(sleep=0, sleep_timestamp=0)))
# эквивалентно
print(db.select('user_id', 'balance', where='sleep == 0 AND sleep_timestamp == 0'))
# sql команда
# SELECT user_id, balance FROM players WHERE sleep == 0 AND sleep_timestamp == 0

print(db.select('user_id', 'balance', _or=True, sleep=0, sleep_timestamp=0))
# эквивалентно
print(db.select('user_id', 'balance', where=db.where(_or=True, sleep=0, sleep_timestamp=0)))
# эквивалентно
print(db.select('user_id', 'balance', where='sleep == 0 OR sleep_timestamp == 0'))
# sql команда
# SELECT user_id, balance FROM players WHERE sleep == 0 OR sleep_timestamp == 0
```
Данный метод вернет вам список кортежей с значениями из таблицы.  


# Методы add, insert
## add(**items), insert(**items)
Данные методы вставляют строку в таблицу.  
Приведу пример:
```python
import database

db = database.Database('game_bd.db', True)
db.set_table('players')
db.add(user_id=123, balance=100)
# sql команда
# INSERT INTO players(user_id, balance) VALUES(123, 100);
```


# Методы edit, insert
## insert(where=None, **items), edit(where=None, **items)
Данные методы изменяют значения в таблице
Аргумент `where` принимает условия замены. Для него нужно использовать либо метод `where()` либо своё условие. (str)
Приведу пример: 
```python
import database

db = database.Database('game_bd.db', True)
db.set_table('players')
db.update(where=db.where(user_id=123, balance=100), user_name='Вася Пупкин')
# sql команда
# UPDATE players SET user_name = "Вася Пупкин" WHERE user_id == 123 AND balance == 100
```


# Методы delete, remove
## delete(_or=False, where=None, **cond), remove(_or=False, where=None, **cond)
Данный метод удаляет данные из таблицы.
Аргумент `where` нужен в случае если у вас сложное условие или вы хотите использовать функцию `where()`. (str)
Приведу пример: 
```python
import database

db = database.Database('game_bd.db', True)
db.set_table('players')
db.delete(user_id=123, balance=100)
# эквивалентно
db.delete(where=db.where(user_id=123, balance=100))
# эквивалентно
db.delete(where='user_id == 123 AND balance == 100')
# sql команда
# DELETE FROM players WHERE user_id == 123 AND balance == 100;

db.delete(_or=True, user_id=123, balance=100)
# эквивалентно
db.delete(where=db.where(_or=True, user_id=123, balance=100))
# эквивалентно
db.delete(where='user_id == 123 OR balance == 100')
# sql команда
# DELETE FROM players WHERE user_id == 123 OR balance == 100;
```

## На этом пока что все
Библиотека пока что в разработке, так что если кто то захочет ее использовать то я охренею, но жду ваших пожеланий и нахождений багов и недоработок.