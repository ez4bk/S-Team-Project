# get download dir
get_download_dir_path = 'select download_location from game_store where game_id = "{0}";'

# get like and dislike
get_ratings = 'select like_count, dislike_count from game_store where game_id = "{0}";'

# check if time record already exist, if 0 DNE if 1 exists
time_record_check = 'select exists(select * from kid_playtime where kid_id = "{0}" and game_id = "{1}") as result;'

# insert new time
time_record_update = 'update kid_playtime set playtime = playtime + "{0}" where kid_id = "{1}" and game_id ="{2}";'

# get kid id base on parent id and kid name
get_kid_id = 'select kid_id from kids where kids_name="{0}" and parent_id="{1}";'

# search game with name
search_game_by_name = 'select * from game_store where game_name like "%{0}%";'

# search game with id
search_game_by_id = 'select * from game_store where game_id = "{0}";'

# add likes
add_likes = 'update game_store set like_count = like_count + 1 where game_id = "{0}";'

# remove likes
remove_likes = 'update game_store set like_count = like_count - 1 where game_id = "{0}";'