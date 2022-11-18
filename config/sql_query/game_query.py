
# get download dir
get_download_dir_path = 'select download_location from game_store where game_id = "{0}";'

# get like and dislike
get_ratings = 'select like_count, dislike_count from game_store where game_id = "{0}";'