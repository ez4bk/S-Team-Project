# show game in the distributing platform where id = input id
show_game = 'select * from game_store where game_id = "{0}";'

# show top x games
show_top_game = 'select * from game_store order by like_count desc limit {0};'

exist_game_check = 'select exists(select * from game_inventory where parent_id = "{0}" and game_id = "{1}") as result;'

add_to_inventory = 'insert into game_inventory(parent_id, game_id) values ("{0}",{1});'

show_inventory_game = 'select * from game_inventory where parent_id = "{0}"'

search_game = 'select * from game_store where game_name like "%{0}%";'
