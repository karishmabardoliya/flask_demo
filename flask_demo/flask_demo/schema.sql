drop table if exists 'user';
create table 'user' (
    'id' integer primary key autoincrement,
    'name' text not null,
    'username' text not null,
    'password' text not null,
    'c_password' text not null,
    'email' text not null
); 

drop table if exists 'fi';
create table 'fi' (
  'id' integer primary key autoincrement,
  'title' text not null,
  'text' text not null,
  'u_name' text not null,
  FOREIGN KEY(u_name) REFERENCES user(username)
);
