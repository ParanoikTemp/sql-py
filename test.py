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
