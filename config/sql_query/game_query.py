
# get download dir
get_download_dir_path = 'select download_location from game_store where game_id = "{0}";'

# get like and dislike
get_ratings = 'select like_count, dislike_count from game_store where game_id = "{0}";'

# check if time record already exist, if 0 DNE if 1 exists
time_record_check = 'select exists(select * from kid_playtime where kid_id = "{0}" and game_id = "{1}") as result;'

# insert new time
time_record_update = 'update kid_playtime set playtime = playtime + "{0}" where kid_id = "{1}" and game_id ="{2}";'