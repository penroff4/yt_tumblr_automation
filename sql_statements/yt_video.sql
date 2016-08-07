CREATE TABLE "yt_video" (
	`video_id`	TEXT NOT NULL UNIQUE,
	`channel_id`	TEXT NOT NULL,
	`video_owner_id`	TEXT NOT NULL,
	`video_name`	TEXT,
	`video_published_date`	TEXT,
	`record_created_date`	TEXT NOT NULL,
	`record_last_modified_date`	TEXT NOT NULL,
	PRIMARY KEY(video_id)
)
