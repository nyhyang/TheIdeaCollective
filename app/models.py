import sqlite3 as sql
from app import db

def lm_get_user_id(user_id):
    with sql.connect("app.db") as con:
        con.row_factory = sql.Row # Convert rows into a dictionary format
        cur = con.cursor()
        # print("\n\n\n\n\n\n**********\n\n\n\n\n")
        # print(user_id)
        user_id = cur.execute("select user_id from user_profile where user_id  = (?)", ([user_id])).fetchall()
        return user_id[0]['user_id']

def get_user_id(name, email, code, picture):
    with sql.connect("app.db") as con:
        con.row_factory = sql.Row # Convert rows into a dictionary format
        cur = con.cursor()
        user_id = cur.execute("select user_id from user_profile where email = (?)", ([email])).fetchall()
        if user_id == []:
            cur.execute("INSERT INTO user_profile (name, email, pwd_code, bio, picture) VALUES (?,?,?,?,?)", (name, email, code, '', picture))
            user_id_int = cur.lastrowid
        else:
            user_id_int = user_id[0]['user_id']
        return user_id_int

def get_available_skills_per_user(user_id):
	with sql.connect("app.db") as con:
		con.row_factory = sql.Row # Convert rows into a dictionary format
		cur = con.cursor()
		print("get_available_skills_per_user - user_id: ", user_id)
		# result = cur.execute("select s.*, 'checked' as checked from skills s, user_skills u where s.skill_id = u.skill_id and u.user_id = (?) union select s.*, '' as checked from skills s, user_skills u where s.skill_id <> u.skill_id and u.user_id = (?)", (user_id, user_id)).fetchall()
		# result = cur.execute("select *, 'checked' as checked from user_skills where user_id = (?) ", ([user_id])).fetchall()
		result = cur.execute("select s.*, 'checked' as checked from skills s, user_skills u where s.skill_id = u.skill_id and u.user_id = (?) ", ([user_id])).fetchall()
		# result = cur.execute("select s.* from skills s inner join user_skills u on s.skill_id = u.skill_id where u.user_id = (?)", ([user_id])).fetchall()

		return result

def add_user_profile(user_id, name, bio, skills, personal_skill, picture):
    with sql.connect("app.db") as con:
        cur = con.cursor()
        cur.execute("UPDATE user_profile SET name = (?), bio = (?), picture = (?) WHERE user_id = (?)", (name, bio, picture, user_id))
        if personal_skill != None:
            cur.execute("INSERT INTO skills (name) VALUES (?)", ([personal_skill]))
            personal_skill_id = cur.lastrowid
            skills.append(personal_skill_id)
        for skill_id in skills:
            cur.execute("INSERT INTO user_skills (user_id, skill_id) VALUES (?,?)", (user_id, int(skill_id)))

        con.commit()

def get_available_skills():
	with sql.connect("app.db") as con:
		con.row_factory = sql.Row # Convert rows into a dictionary format
		cur = con.cursor()
		result = cur.execute("select * from skills").fetchall()
		return result

def get_skills(idea_id): # Get the skills required for a project
	with sql.connect("app.db") as con:
		con.row_factory = sql.Row # Convert rows into a dictionary format
		cur = con.cursor()
		result = cur.execute("select * from skills inner join idea_skills on idea_skills.skill_id = skills.skill_id where idea_id = (?)", ([idea_id])).fetchall()
		return result

def get_available_tagetories(): # Get the tags
	with sql.connect("app.db") as con:
		con.row_factory = sql.Row # Convert rows into a dictionary format
		cur = con.cursor()
		result = cur.execute("select * from tagetories").fetchall()
		return result   

def get_idea_tag(idea_id): # Anna: Gets the tags for a specific idea
	with sql.connect("app.db") as con:
		con.row_factory = sql.Row # Convert rows into a dictionary format
		cur = con.cursor()
		result = cur.execute("select * from tagetories inner join idea_tag on idea_tag.tag_id = tagetories.tag_id where idea_id = (?)", ([idea_id])).fetchall()
		return result

def add_idea(user_id, name, description, ownership, skills, personal_skill, tagetories, personal_tagetories): 
	with sql.connect("app.db") as con:
		cur = con.cursor()
		cur.execute("INSERT INTO idea (user_id, name, description, ownership) VALUES (?,?,?,?)", (user_id, name, description, ownership))
		idea_id = cur.lastrowid
		if personal_skill != None:
			cur.execute("INSERT INTO skills (name) VALUES (?)", ([personal_skill]))
			personal_skill_id = cur.lastrowid
			skills.append(personal_skill_id)
		for skill_id in skills:
			cur.execute("INSERT INTO idea_skills (idea_id, skill_id) VALUES (?,?)", (idea_id, int(skill_id)))
		con.commit()

		new_cur = con.cursor()
		if personal_tagetories != None:
			new_cur.execute("INSERT INTO tagetories (name) VALUES (?)", ([personal_tagetories]))
			personal_tagetories_id = new_cur.lastrowid
			tagetories.append(personal_tagetories_id)
		for tagetories_id in tagetories:
			new_cur.execute("INSERT INTO idea_tag (idea_id, tag_id) VALUES (?,?)", (idea_id, int(tagetories_id)))
		con.commit()

def get_idea(idea_id): # For an idea, return their ideas
	with sql.connect("app.db") as con:
		con.row_factory = sql.Row
		cur = con.cursor()
		# for user, select trips
		# sql_query = "select * from idea where id = " + idea_id
		# print(sql_query)
		# result = cur.execute(sql_query).fetchall()
		# for i in result:
		# result = cur.execute("select i.*, u.name from idea i, user_profile u where idea_id = (?)", ([idea_id])).fetchall()
		result = cur.execute("select * from idea where idea_id = (?)", ([idea_id])).fetchall()   
		     
		# for each1 in result[0]:
		#     print(each1)
	# return result[0]
	return result

def get_all_ideas(): # Anna: Returns all ideas for the ideafeed
	# with sql.connect("app.db") as con:
	# 	con.row_factory = sql.Row
	# 	cur = con.cursor()
	# 	sql_query = """select user_profile.name AS user_name, idea.idea_id, idea.name AS idea_name, idea.description, idea.ownership
	# 				FROM user_profile
	# 				INNER JOIN idea
	# 				ON user_profile.user_id = idea.user_id"""
	# 	result = cur.execute(sql_query).fetchall()        
	# return result
	with sql.connect("app.db") as con:
		con.row_factory = sql.Row
		cur = con.cursor()
		result = cur.execute("select u.name AS user_name, u.picture, i.idea_id, i.name AS idea_name, i.description, i.ownership from user_profile u, idea i where u.user_id = i.user_id").fetchall()  
	return result

def get_ideas_by_tag(tag_id): 
	with sql.connect("app.db") as con:
		con.row_factory = sql.Row
		cur = con.cursor()
		result = cur.execute("select u.name AS user_name, u.picture ,i.idea_id, i.name AS idea_name, i.description, i.ownership from user_profile u, idea i, idea_tag it where u.user_id = i.user_id and i.idea_id = it.idea_id and it.tag_id = (?)", ([tag_id])).fetchall()  
		# result = cur.execute("select i.* from idea i, idea_tag it where i.idea_id = it.idea_id and it.tag_id = (?)", ([tag_id])).fetchall()       
	return result

def get_ideas_by_description(descr_search): 
	with sql.connect("app.db") as con:
		con.row_factory = sql.Row
		cur = con.cursor()
		result = cur.execute("select u.name AS user_name, u.picture ,i.idea_id, i.name AS idea_name, i.description, i.ownership from user_profile u, idea i where u.user_id = i.user_id and lower(i.description) like (?)", (['%'+str(descr_search).lower()+'%'])).fetchall()  
		# result = cur.execute("select i.* from idea i, idea_tag it where i.idea_id = it.idea_id and it.tag_id = (?)", ([tag_id])).fetchall()       
	return result

def get_all_tags():
	with sql.connect("app.db") as con:
		con.row_factory = sql.Row
		cur = con.cursor()
		sql_query = """select idea_id, name from idea_tag a join tagetories b
						on a.tag_id = b.tag_id"""
		result = cur.execute(sql_query).fetchall()        
	return result

def get_gral_tags():
	with sql.connect("app.db") as con:
		con.row_factory = sql.Row
		cur = con.cursor()
		result = cur.execute("select * from tagetories").fetchall() 
	return result

def get_idea_creator(idea_id): # For an idea, returns the name of the creator
	with sql.connect("app.db") as con:
		con.row_factory = sql.Row
		cur = con.cursor()
		# sql_query = "select user_profile.name, idea.idea_id from user_profile left join idea on idea.user_id = user_profile.user_id where idea_id = (?)"
		result = cur.execute("select user_profile.name, user_profile.email, idea.idea_id from user_profile left join idea on idea.user_id = user_profile.user_id where idea_id = (?)", ([idea_id])).fetchall()
		# print(result[0][1])
	return result

def get_ownership(idea_id): # For an idea, returns the ownership
	with sql.connect("app.db") as con:
		con.row_factory = sql.Row
		cur = con.cursor()
		# sql_query = "select user_profile.name, idea.idea_id from user_profile left join idea on idea.user_id = user_profile.user_id where idea_id = (?)"
		result = cur.execute("select ownership from idea where idea_id = (?)", ([idea_id])).fetchall()
	return result

def add_comment(user_id, idea_id, comment, pub_priv, date_time): # Anna
	with sql.connect("app.db") as con:
		cur = con.cursor()
		sql_query = "INSERT INTO comments (user_id, idea_id, comment, pub_priv, date_time) VALUES (?,?,?,?,?)"
		cur.execute(sql_query, (user_id, idea_id, comment, pub_priv, date_time))
		con.commit()

def get_comment(idea_id): # Anna
	with sql.connect("app.db") as con:
		con.row_factory = sql.Row
		cur = con.cursor()
		result = cur.execute("select *, u.name from comments c, user_profile u where idea_id = (?) and c.user_id = u.user_id", ([idea_id])).fetchall()
	return result   

def get_user(user_id): # Anna: gets user for dashboard
	with sql.connect("app.db") as con:
		con.row_factory = sql.Row
		cur = con.cursor()
		result = cur.execute("select * from user_profile where user_id = (?)", ([user_id])).fetchall()
	return result  

def get_user_skills(user_id):
	with sql.connect("app.db") as con:
		con.row_factory = sql.Row # Convert rows into a dictionary format
		cur = con.cursor()
		result = cur.execute("select * from skills inner join user_skills on user_skills.skill_id = skills.skill_id where user_id = (?)", ([user_id])).fetchall()
		return result

def get_user_ideas(user_id): # Anna: Returns all ideas for the user
	with sql.connect("app.db") as con:
		con.row_factory = sql.Row
		cur = con.cursor()
		sql_query = """select idea.idea_id, idea.name AS idea_name, idea.description
					FROM user_profile
					INNER JOIN idea
					ON user_profile.user_id = idea.user_id where user_profile.user_id = (?)"""
		result = cur.execute(sql_query, ([user_id])).fetchall()        
	return result