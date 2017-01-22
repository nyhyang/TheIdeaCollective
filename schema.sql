-- drop table if exists idea;
-- create table idea(
--     id integer primary key,
--     title text not null,
--     username text not null,
--     description text not null
-- );


-- insert into idea values(1, 'my Idea1!!', 'nancy', 'this is my super idea');
-- insert into idea values(2, 'my Idea2!!', 'anna', 'this is my super idea2');
-- insert into idea values(3, 'my Idea3!!', 'malu', 'this is my super idea3');
-- insert into idea values(4, 'my Idea4!!', 'nancy', 'this is my super idea4');

-- select * from user_profile
-- select * from user_skills
-- select * from skills
-- select * from idea_skills
-- select * from idea
-- select * from comments
-- select * from idea_tag
-- select * from tagetories

-- drop table if exists user;
-- create table user(
--     user_id integer primary key,
--     user_name text not null,
--     user_email text not null
-- );

drop table if exists user_profile;
create table user_profile(
    user_id integer primary key,
    name text not null,
    email text not null,
    pwd_code text not null,
    bio text not null,
    picture text not null
);

drop table if exists user_skills;
create table user_skills(
    id integer primary key,
    user_id integer not null,
    skill_id integer not null,
        foreign key (user_id) references user(user_profile),
        foreign key (skill_id) references trip(skills)
);

drop table if exists skills;
create table skills(
    skill_id integer primary key,
    name text not null
);

drop table if exists idea_skills;
create table idea_skills(
    id integer primary key,
    idea_id integer not null,
    skill_id integer not null,
        foreign key (idea_id) references user(idea),
        foreign key (skill_id) references trip(skills)
);

drop table if exists idea;
create table idea(
    idea_id integer primary key,
    user_id integer not null,
    name text not null,
    description text not null,
    ownership text not null,
        foreign key (user_id) references user(user_profile)
);

drop table if exists comments;
create table comments(
    comment_id integer primary key,
    user_id integer not null,
    idea_id integer not null,
    comment text not null,
    pub_priv text not null,
    date_time datetime not null,
        foreign key (idea_id) references user(idea),
        foreign key (user_id) references user(user_profile)
);

drop table if exists idea_tag;
create table idea_tag(
    id integer primary key,
    tag_id integer not null,
    idea_id integer not null,
        foreign key (tag_id) references user(tagetories),
        foreign key (idea_id) references user(idea)
);

drop table if exists tagetories;
create table tagetories(
    tag_id integer primary key,
    name text not null
);

-- -- (tag_id,name)
insert into tagetories values(1, 'Technology');
insert into tagetories values(2, 'Education');
insert into tagetories values(3, 'Music');
insert into tagetories values(4, 'Data');
insert into tagetories values(5, 'Health');

-- -- (skill_id, name)
insert into skills values(1, 'UX');
insert into skills values(2, 'Data Science');
insert into skills values(3, 'Front-End');
insert into skills values(4, 'Back-End');
insert into skills values(5, 'Design');
insert into skills values(6, 'Product Management');
-- insert into skills values(7, 'My skill');


--     /* DUMMY */

-- -- (id, tag_id, idea_id)
-- insert into idea_tag values(1, 1, 1);
-- insert into idea_tag values(2, 3, 1);
-- insert into idea_tag values(3, 5, 1);
-- insert into idea_tag values(4, 3, 2);
-- insert into idea_tag values(5, 4, 2);

-- -- (user_id, name, email, pwd_code, bio)
insert into user_profile values(1, 'TestUser', 'testuser@gmail.com', 'pwd123', 'Im a user bot', 'http://www.sdpk.eu/wp-content/uploads/2014/07/number-2-u-s-president-barack-obama-second-most-admired-person-planet.jpg');
-- insert into user_profile values(2, 'Malavika', 'malu@gmail.com', 'pwdmalu123', 'Love dogs and awww pictures', 'pic');
-- insert into user_profile values(3, 'Anna', 'anna@gmail.com', 'pwdanna123', 'I like pet sitting and love awww pictures', 'pic');
-- insert into user_profile values(4, 'Selenne', 'sel@gmail.com', 'pwdsel123', 'I love zombie movies and hate hate', 'pic');

-- -- (comment_id, user_id, idea_id, comment, pub_priv, date_time)
-- insert into comments values(1, 1, 1, 'Nice idea 1 for idea 1', 'Public', '1117201612121200');
-- insert into comments values(2, 2, 1, 'Nice idea 2 for idea 1', 'Public', '1117201612121200');
-- insert into comments values(3, 3, 2, 'Nice idea 1 for idea 2', 'Private', '1117201612121200');
-- insert into comments values(4, 3, 2, 'Nice idea 2 for idea 2', 'Public', '1117201612121200');
-- insert into comments values(5, 3, 2, 'Nice idea 3 for idea 2', 'Private', '1117201612121200');

-- -- (idea_id, user_id, name, description, ownership)
-- insert into idea values(1, 1, 'Idea 1', 'Description for Idea 1', 'off');
-- insert into idea values(2, 2, 'Idea 2', 'Description for Idea 2', 'on');
-- insert into idea values(3, 2, 'Other Idea', 'Great descr for idea other Idea 2', 'on');

-- -- (id, idea_id, skill_id)
-- insert into idea_skills values(1, 1, 2);
-- insert into idea_skills values(2, 1, 4);
-- insert into idea_skills values(3, 1, 6);
-- insert into idea_skills values(4, 2, 1);
-- insert into idea_skills values(5, 2, 3);
-- insert into idea_skills values(6, 2, 5);

-- -- (id, user_id, skill_id)
insert into user_skills values(1, 1, 1);
-- insert into user_skills values(2, 2, 2);
-- insert into user_skills values(3, 2, 3);
-- insert into user_skills values(4, 3, 4);
-- insert into user_skills values(5, 3, 5);
-- insert into user_skills values(6, 4, 6);
