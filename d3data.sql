
SELECT
      p.title,
      c.char_name,
      m.act_id,
      m.scene_id,
      m.mono_id,
      m.word_count,
      p.date,
      p.genre_id
FROM
      Characters AS c
JOIN
      Monologues AS m
      ON m.char_id = c.char_id
JOIN
      Plays as p
      ON m.play_id = p.play_id

ORDER BY
      p.title


      
