import database

table = database.Database('game_bd.db', True)
table.set_table('players')

print(table.select('balance', 'user_id', balance=66595182, user_id=606843946))
