CREATE TABLE `yt_user` (
	`user_id`	TEXT NOT NULL UNIQUE,
	`user_name`	TEXT NOT NULL,
	`user_create_date`	TEXT NOT NULL,
	`record_create_date`	TEXT NOT NULL,
	`record_last_modified_date`	TEXT NOT NULL,
	PRIMARY KEY(user_id)
)
