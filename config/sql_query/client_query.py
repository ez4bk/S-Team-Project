# show game in the distributing platform where id = input id
show_game = 'select * from game_library where game_id = "{0}";'

# show top x games
show_top_game = 'select * from game_library order by copies_sold desc limit "{0}";'