create database if not exists tjpool;
use tjpool;
create table if not exists users (
	username VARCHAR(255) NOT NULL,
	password VARCHAR(255),
	firstName VARCHAR(255),
	lastName VARCHAR(255),
	ridesGiven INT(5),
	ridesTaken INT(5),
	
	PRIMARY KEY (username)
);

create table if not exists carpools (
	pool_id INT(10) NOT NULL,
	pool_size INT(2),
	pool_date DATE,
	driver_id VARCHAR(255),
	leave_location VARCHAR(255),
	come_location VARCHAR(255),
	leave_time TIME,
	come_time TIME,
	comments VARCHAR(1023)
);

create table if not exists links (
	username VARCHAR(255),
	pool_id VARCHAR(255)
);