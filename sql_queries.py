import configparser


# Read 'dwh.cfg' files
config = configparser.ConfigParser()
config.read('dwh.cfg')

LOG_DATA = config.get("S3", "LOG_DATA")
LOG_JSON_PATH = config.get("S3", "LOG_JSON_PATH")
SONG_DATA = config.get("S3", "SONG_DATA")
ARN = config.get("IAM_ROLE", "DWH_ROLE_ARN")
REGION = config.get('GEO', 'REGION')


# Drop table queries
staging_events_table_drop = "DROP table IF EXISTS staging_events;"
staging_songs_table_drop = "DROP table IF EXISTS staging_songs;"
songplays_table_drop = "DROP table IF EXISTS songplays;"
users_table_drop = "DROP table IF EXISTS users;"
songs_table_drop = "DROP table IF EXISTS songs;"
artists_table_drop = "DROP table IF EXISTS artists;"
time_table_drop = "DROP table IF EXISTS time;"


# Create table queries
staging_events_table_create= """
CREATE TABLE staging_songs
(
  num_songs         INT,
  artist_id         VARCHAR,
  artist_latitude   FLOAT,
  artist_longitude  FLOAT,
  artist_location   VARCHAR,
  artist_name       VARCHAR,
  song_id           VARCHAR,
  title             VARCHAR,
  duration          FLOAT,
  year              INT
);
"""

staging_songs_table_create = """
CREATE TABLE staging_events
(
    artist          VARCHAR,
    auth            VARCHAR,
    firstName       VARCHAR,
    gender          VARCHAR,
    itemInSession   INT,
    lastName        VARCHAR,
    length          FLOAT,
    level           VARCHAR,
    location        VARCHAR,
    method          VARCHAR,
    page            VARCHAR,
    registration    VARCHAR,
    sessionId       INT,
    song            VARCHAR,
    status          INT,
    ts              TIMESTAMP,
    userAgent       VARCHAR,
    userId          INT
);
"""

songplay_table_create = """
CREATE TABLE songplays(
    songplay_id   INT IDENTITY (0,1),
    start_time    TIMESTAMP REFERENCES  time(start_time) SORTKEY,
    user_id       INT       REFERENCES  users(user_id) DISTKEY,
    level         VARCHAR,
    song_id       VARCHAR   REFERENCES  songs(song_id),
    artist_id     VARCHAR   REFERENCES  artists(artist_id),
    session_id    INT       NOT NULL,
    location      VARCHAR,
    user_agent    VARCHAR,
    PRIMARY KEY (songplay_id)
    );
"""

user_table_create = """
CREATE TABLE IF NOT EXISTS users(
    user_id     INT     DISTKEY,
    first_name  VARCHAR,
    last_name   VARCHAR,
    gender      VARCHAR,
    level       VARCHAR,
    PRIMARY KEY (user_id)
    );
"""

song_table_create = """
CREATE TABLE IF NOT EXISTS songs(
    song_id     VARCHAR SORTKEY,
    title       VARCHAR NOT NULL,
    artist_id   VARCHAR NOT NULL,
    year        INT,
    duration    FLOAT,
    PRIMARY KEY (song_id)
    );
"""

artist_table_create = """
CREATE TABLE IF NOT EXISTS artists(
    artist_id   VARCHAR SORTKEY,
    name        VARCHAR NOT NULL,
    location    VARCHAR,
    latitude    FLOAT,
    logitude    FLOAT,
    PRIMARY KEY (artist_id)
    );
"""

time_table_create = ("""
CREATE TABLE IF NOT EXISTS time(
    start_time      TIMESTAMP   SORTKEY,
    hour            INT         NOT NULL,
    day             INT         NOT NULL,
    week            INT         NOT NULL,
    month           INT         NOT NULL,
    year            INT         NOT NULL,
    weekday         INT         NOT NULL,
    PRIMARY KEY (start_time)
    );
""")


# Staging tables
staging_events_copy = """
COPY staging_events
    FROM {}
    IAM_ROLE {}
    REGION {}
    FORMAT AS JSON {}
    TIMEFORMAT 'epochmillisecs'
    TRUNCATECOLUMNS BLANKSASNULL EMPTYASNULL;
""".format(LOG_DATA, ARN, REGION, LOG_JSON_PATH)

staging_songs_copy = """
COPY staging_songs
    FROM {}
    IAM_ROLE {}
    REGION {}
    FORMAT AS JSON 'auto'
    TRUNCATECOLUMNS BLANKSASNULL EMPTYASNULL;
""".format(SONG_DATA, ARN, REGION)


# Final Redshift table
songplay_table_insert = """
INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
    SELECT DISTINCT se.ts,
                    se.userId,
                    se.level,
                    ss.song_id,
                    ss.artist_id,
                    se.sessionId,
                    se.location,
                    se.userAgent
      FROM staging_events se
INNER JOIN staging_songs ss
        ON se.song = ss.title AND se.artist = ss.artist_name
     WHERE se.page = 'NextSong';
"""

user_table_insert = """
INSERT INTO users (user_id, first_name, last_name, gender, level)
    SELECT DISTINCT se.userId,
                    se.firstName,
                    se.lastName,
                    se.gender,
                    se.level
     FROM staging_events se
    WHERE se.userId IS NOT NULL;
"""


song_table_insert = """
INSERT INTO songs (song_id, title, artist_id, year, duration)
    SELECT DISTINCT ss.song_id,
                    ss.title,
                    ss.artist_id,
                    ss.year,
                    ss.duration
     FROM staging_songs ss
    WHERE ss.song_id IS NOT NULL;

"""

artist_table_insert = """
INSERT INTO artists (artist_id, name, location, latitude, logitude)
    SELECT DISTINCT ss.artist_id,
                    ss.artist_name,
                    ss.artist_location,
                    ss.artist_latitude,
                    ss.artist_longitude
     FROM staging_songs ss
    WHERE ss.artist_id IS NOT NULL;

""")

time_table_insert = """
INSERT INTO time (start_time, hour, day, week, month, year, weekday)
    SELECT DISTINCT  se.ts,
                     EXTRACT(hour from se.ts),
                     EXTRACT(day from se.ts),
                     EXTRACT(week from se.ts),
                     EXTRACT(month from se.ts),
                     EXTRACT(year from se.ts),
                     EXTRACT(weekday from se.ts)
     FROM staging_events se
    WHERE se.page = 'NextSong';

"""


# List of queries
create_table_queries = [staging_events_table_create, staging_songs_table_create, user_table_create,
                        song_table_create, artist_table_create, time_table_create, songplay_table_create]

drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplays_table_drop, users_table_drop,
                      songs_table_drop, artists_table_drop, time_table_drop]

copy_table_queries = [staging_events_copy, staging_songs_copy]

insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert,
                        artist_table_insert, time_table_insert]
