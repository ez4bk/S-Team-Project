# match input username and password to db
# return 1 when success, return 0 when password does not match or user does not exist
parent_signin = 'select password from parents where parent_id = "{0}"'

parent_id_check = 'select exists(select* from parents where parent_id = "{0}") as result;'
parent_signup = 'insert into parents(parent_id, user_name, password) values("{0}", "{1}", "{2}");'

# show kids user have where parent_id = input id
kids_select = 'select * from kids where parent_id = "{0}";'

# show games user own where parent_id = input id
show_inventory = 'select * from game_inventory where parent_id = "{0}";'

# show game in the distributing platform where id = input id
show_game = 'select * from game_library where game_id = "{0}";'


