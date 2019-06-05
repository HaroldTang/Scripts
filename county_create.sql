drop table if exists county;
create table county(
county_id int auto_increment not null comment '自增列',
county_code varchar(100) not null comment '区块代码',
county_name varchar(100) not null comment '区块名称',
city_id int not null comment '市编号',
primary key (county_id),
foreign key (city_id) references city(city_id)
);