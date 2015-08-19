-- Select statement for dict that lists all the categories together
SELECT
      p.title, c.char_name, m.act_id, m.scene_id, m.mono_id, m.word_count, p.date, p.genre_id
  FROM
      Characters AS c
      JOIN
        Monologues AS m
        ON m.char_id = c.char_id
      JOIN
        Plays as p
        ON m.play_id = p.play_id
          ORDER BY p.title


-- For dict of Genre names
SELECT genre_name FROM Genres

-- For dict of comedy plays
SELECT play_title FROM Plays WHERE genre_id='c'

-- For dict of history plays
SELECT play_title FROM Plays WHERE genre_id='h'

-- For dict of tragedy plays
SELECT play_title FROM Plays WHERE genre_id='t'

-- For characters in comedic plays
SELECT p.title, c.char_name
  FROM
      Characters AS c
      JOIN
        Plays AS p
        ON c.play_id = p.play_id
      JOIN
        Genres AS g
        ON p.genre_id = g.genre_id
      WHERE g.genre_id='c'
      ORDER BY p.title

-- For characters in history plays
SELECT p.title, c.char_name
  FROM
      Characters AS c
      JOIN
        Plays AS p
        ON c.play_id = p.play_id
      JOIN
        Genres AS g
        ON p.genre_id = g.genre_id
      WHERE g.genre_id='h'
      ORDER BY p.title

-- For characters in tragic plays
SELECT p.title, c.char_name
  FROM
      Characters AS c
      JOIN
        Plays AS p
        ON c.play_id = p.play_id
      JOIN
        Genres AS g
        ON p.genre_id = g.genre_id
      WHERE g.genre_id='t'
      ORDER BY p.title

SELECT p.title, c.char_name, m.mono_id
  FROM
      Characters AS c
      JOIN
        Monologues AS m
        ON c.char_id = m.char_id
      JOIN
        Plays as p
        ON m.play_id = p.play_id
      WHERE p.genre_id = 'c'
      ORDER BY c.char_name


SELECT 
