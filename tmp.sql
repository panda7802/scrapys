--SELECT * FROM get_web_data_platformstatistics GROUP BY vid_id-- ORDER BY get_time DESC
--SELECT count(1) FROM get_web_data_videolist;

--SELECT Max(cast(play as int)) from  get_web_data_videodetail where video_id = 726;

SELECT
  a.video_id,
  b.title,
  datetime(b.created, 'unixepoch', 'localtime'),
  min(cast(a.play AS INT)),
  Max(cast(a.play AS INT)),
  (Max(cast(a.play AS INT)) - min(cast(a.play AS INT))) AS addNum
FROM get_web_data_videodetail a, get_web_data_videolist b
WHERE a.video_id = b.id --and a.video_id in (1,2,3)
GROUP BY video_id
ORDER BY addNum
  DESC;

--SELECT video_id,max(play) FROM get_web_data_videodetail where video_id in (1,2,3) GROUP BY video_id