drop table if exists `province`;
create table province(
	province_id int auto_increment comment '自增列',
    province_name varchar(100) not null comment '省名',
    primary key (province_id)
);