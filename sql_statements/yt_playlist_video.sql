CREATE TABLE `yt_playlist_video` (
	`playlist_id`	TEXT NOT NULL,
	`video_id`	TEXT NOT NULL,
	`has_been_posted`	INTEGER NOT NULL,
	PRIMARY KEY(playlist_id,video_id)
);
