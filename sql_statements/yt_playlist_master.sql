DROP VIEW IF EXISTS
  yt_yt_playlist_master;

CREATE VIEW yt_yt_playlist_master AS
SELECT
  -- Bring in video info
   yt_playlist_video.video_id
  ,yt_video.video_name
  ,yt_video.channel_id AS video_channel_id
  ,yt_video.video_owner_id
  ,yt_video.video_published_date
  ,yt_video.record_created_date AS video_record_create_date
  ,yt_video.record_last_modified_date AS video_record_last_modified_date
  -- Bring in video channel info
  ,yt_video_channel.channel_name AS video_channel_name
  ,yt_video_channel.channel_create_date AS video_channel_create_date
  ,yt_video_channel.record_create_date AS video_channel_record_create_date
  ,yt_video_channel.record_last_modified_date AS video_channel_record_last_modified_date
  ,yt_video_channel.channel_owner_id AS video_channel_owner_id
  -- Bring in video channel owner info
  ,yt_video_channel_user.user_id AS video_channel_owner_id
  ,yt_video_channel_user.user_name AS video_channel_owner_name
  ,yt_video_channel_user.user_create_date AS video_channel_owner_create_date
  ,yt_video_channel_user.record_create_date AS video_channel_owner_record_create_date
  ,yt_video_channel_user.record_last_modified_date AS video_channel_owner_record_last_modified_date
  -- Bring in video owner info
  ,yt_video_user.user_name AS video_owner_name
  ,yt_video_user.user_create_date AS video_owner_create_date
  ,yt_video_user.record_create_date AS video_owner_record_create_date
  ,yt_video_user.record_last_modified_date AS video_owner_record_last_modified_date
  -- Bring in playlist info
  ,yt_playlist_video.playlist_id
  ,yt_playlist.playlist_name
  ,yt_playlist.playlist_owner_id
  ,yt_playlist.playlist_name
  ,yt_playlist.playlist_create_date
  ,yt_playlist.record_create_date
  ,yt_playlist.record_last_modified_date
  -- Bring in playlist owner info
  ,yt_playlist.playlist_owner_id
  ,yt_playlist_user.user_name AS playlist_owner_name
  ,yt_playlist_user.user_create_date AS playlist_owner_create_date
  ,yt_playlist_user.record_create_date AS playlist_owner_record_create_date
  ,yt_playlist_user.record_last_modified_date AS playlist_owner_record_last_modified_date
  -- Bring in playlist channel info
  ,yt_playlist.playlist_channel_id
  ,yt_playlist_channel.channel_name AS playlist_channel_name
  ,yt_playlist_channel.channel_create_date AS playlist_channel_create_date
  ,yt_playlist_channel.record_create_date AS playlist_channel_record_create_date
  ,yt_playlist_channel.record_last_modified_date AS playlist_channel_record_last_modified_date
  ,yt_playlist_channel.channel_owner_id AS playlist_channel_owner_id
  -- Bring in playlist channel owner info
  ,yt_playlist_channel_owner.user_name AS playlist_channel_owner_name
  ,yt_playlist_channel_owner.user_create_date AS playlist_channel_owner_create_date
  ,yt_playlist_channel_owner.record_create_date AS playlist_channel_owner_record_create_date
  ,yt_playlist_channel_owner.record_last_modified_date AS playlist_channel_owner_record_last_modified_date
  -- Bring in has been posted
  ,yt_playlist_video.has_been_posted

 FROM yt_playlist_video
  LEFT JOIN yt_video
    ON yt_playlist_master.video_id = yt_video.video_id
  LEFT JOIN yt_playlist
    ON yt_playlist_master.playlist_id = yt_playlist.playlist_id
  LEFT JOIN yt_channel AS yt_video_channel
    ON yt_video.channel_id = yt_video_channel.channel_id
  LEFT JOIN yt_user AS yt_video_channel_user
    ON yt_video_channel.channel_owner_id = yt_video_channel_user.user_id
  LEFT JOIN yt_user AS yt_video_user
    ON yt_video.video_owner_id = yt_video_user.user_id
  LEFT JOIN yt_user AS yt_playlist_user
    ON yt_playlist.playlist_owner_id = yt_playlist_user.user_id
  LEFT JOIN yt_channel AS yt_playlist_channel
    ON yt_playlist.playlist_channel_id = yt_playlist_channel.channel_id
  LEFT JOIN yt_user AS yt_playlist_channel_owner
    ON yt_playlist_channel.channel_owner_id = yt_playlist_channel_owner.user_id;
