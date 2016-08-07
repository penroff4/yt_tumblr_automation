CREATE TABLE `yt_channel` (
	`channel_id`	TEXT NOT NULL,
	`channel_name`	TEXT,
	`channel_create_date`	TEXT NOT NULL,
	`record_create_date`	TEXT NOT NULL,
	`record_last_modified_date`	TEXT NOT NULL,
	`channel_owner_id`	TEXT NOT NULL,
	PRIMARY KEY(channel_id)
)
