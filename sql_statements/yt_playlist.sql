CREATE TABLE "yt_playlist" (
	`playlist_id`	TEXT NOT NULL UNIQUE,
	`playlist_channel_id`	TEXT,
	`playlist_name`	TEXT,
	`playlist_owner_id`	TEXT NOT NULL,
	`playlist_create_date`	TEXT NOT NULL,
	`record_create_date`	TEXT NOT NULL,
	`record_last_modified_date`	TEXT NOT NULL,
	PRIMARY KEY(playlist_id)
)
