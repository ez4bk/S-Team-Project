# match input username and password to db
# return 1 when success, return 0 when password does not match or user does not exist
parent_signin = 'select user_name, password, icon_image from parents where user_id = "{0}";'

parent_id_check = 'select exists(select * from parents where user_id = "{0}") as result;'
parent_signup = 'insert into parents(user_id, user_name, password) values("{0}", "{1}", "{2}");'

# show kids user have where parent_id = input id
kids_select = 'select * from kids where parent_id = "{0}";'
# add a new child account with selected icon, name, and default time limit
add_kid = 'insert into kids (kids_name,parent_id,icon_image,time_limit) values ("{0}","{1}","{2}","{3}");'

# show games user own where parent_id = input id
show_parent_inventory = 'select * from game_inventory where parent_id = "{0}";'

# check last login
get_last_played = 'select last_played from kids where id = "{0}";'

# update last login
update_last_played = 'update kids set last_played = "{0}" where id = "{1}";'

# update time played today
update_time_played_today = 'update kids set time_played_today = "{0}" where id = "{1}";'
