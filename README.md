# Implementing Data Warehouse on AWS Cloud
A music streaming startup, Sparkify, has grown their user base and song database and want to move their processes and data onto the cloud. Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.
## Summary
* [Project Overview](#Introduction)
* [Project Datasets](#Project-Dataset)
* [Data Warehouse Schema Definition](#Data-Warehouse-Schema-Definition)

## Project Overview
This project entails building an ETL pipeline that extracts their sparkify music data from Amazon S3 bucket, stages them in Amazon Redshift and transforming data into a set of dimensional tables for their analytics team to continue finding insights in what songs their users are listening to.
##### About Amazon S3 and Amazon Redshift Services
Amazon S3 service is a service offered by Amazon Web Services that provides object storage through a web service interface. \
Amazon Redshift is a widely used cloud data warehouse. It makes it fast, simple and cost-effective to analyze all your data using standard SQL.

## Project Datasets
Here are the S3 links for each:
* Song data: s3://udacity-dend/song_data
* Log data: s3://udacity-dend/log_data
* Log data json path: s3://udacity-dend/log_json_path.json

#### Song Dataset
Songs dataset is a subset of [Million Song Dataset](http://millionsongdataset.com/).

**Sample data :**
```
{"num_songs": 1, "artist_id": "ARDNS031187B9924F0", "artist_latitude": 32.67828, "artist_longitude": -83.22295, "artist_location": "Georgia", "artist_name": "Tim Wilson", "song_id": "SONYPOM12A8C13B2D7", "title": "I Think My Wife Is Running Around On Me (Taco Hell)", "duration": 186.48771, "year": 2005}
```

#### Log Dataset
Log dataset was gotten from [Event Simulator](https://github.com/Interana/eventsim).

**Sample Record :**
```
{"artist":"Anjulie","auth":"Logged In","firstName":"Jacqueline","gender":"F","itemInSession":6,"lastName":"Lynch","length":194.63791,"level":"paid","location":"Atlanta-Sandy Springs-Roswell, GA","method":"PUT","page":"NextSong","registration":1540223723796.0,"sessionId":389,"song":"Boom","status":200,"ts":1541991804796,"userAgent":"\"Mozilla\/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit\/537.78.2 (KHTML, like Gecko) Version\/7.0.6 Safari\/537.78.2\"","userId":"29"}
```

## Data Warehouse Schema Definition
Below is the schema of the database in Redshift

#### Staging Tables
The staging table was loaded by using the copy command to bulk insert datasets
from the Amazon S3 bucket.

**EVENT STAGING TABLE**

| COLUMN | TYPE | FEATURES |
| ------ | ---- | ------- |
|num_songs| int| |
|artist_id| varchar| |
|artist_latitude | float | |
|artist_longitude| float | |
|artist_location| varchar| |
|artist_name | varchar | |
|song_id| varchar| |
|title| varchar| |
|duration | float | |
|year | int | |

\
**SONGS STAGING TABLE**

| COLUMN | TYPE | FEATURES |
| ------ | ---- | ------- |
|artist| varchar| |
|auth| varchar| |
|firstName | varchar | |
|gender| varchar| |
|itemInSession | int| |
|lastName | varchar | |
|length| float| |
|level| varchar| |
|location | varchar| |
|method | varchar| |
|page | varchar | |
|registration| varchar| |
|sessionId| int| |
|song | varchar| |
|status| int| |
|ts| timestamp| |
|userAgent| varchar| |
|userId| int| |


#### Dimension tables and Fact table
The dimension and fact tables were loaded by performing ETL on the
staging tables.
#### Dimension tables

**USERS TABLE**

| COLUMN | TYPE | FEATURES |
| ------ | ---- | ------- |
|user_id| int| distkey, primary key |
|first_name| varchar| |
|last_name | varchar | |
|gender| varchar| |
|level| varchar| |

\
**SONGS TABLE**

| COLUMN | TYPE | FEATURES |
| ------ | ---- | ------- |
|song_id| varchar| sortkey, primary key |
|title| varchar| not null |
|artist_id | varchar | not null|
|duration| float| |

\
**ARTISTS TABLE**

| COLUMN | TYPE | FEATURES |
| ------ | ---- | ------- |
|artist_id| varchar| sortkey, primary key |
|name| varchar| not null |
|location | varchar | |
|latitude| float| |
|logitude| float| |

\
**TIME TABLE**

| COLUMN | TYPE | FEATURES |
| ------ | ---- | ------- |
|start_time| timestamp| sortkey, PRIMARY KEY |
|hour| int| |
|day| int| |
|week| int| |
|month| int| |
|year| int| |
|weekday| int| |

#### Fact table

**SONGPLAYS TABLE**

| COLUMN | TYPE | FEATURES |
| ------ | ---- | ------- |
|songplay_id| int| identity (0,1), primary key |
|start_time| timestamp| references  time(start_time), sortkey|
|user_id | int | references  users(user_id), distkey|
|level| varchar| |
|song_id| varchar| references  songs(song_id)|
|artist_id | varchar | references  artists(artist_id)|
|session_id| int| not null|
|location| varchar| |
|user_agent| varchar| |


## How to run
* Create a virtual environment to avoid dependency issues in future
* Next run:
```
pip3 install -r requirements.txt
```
* Next run:
```
python create_tables.py
```
* Finally run:
```
python etl.py
```

**NOTE:**
* Completing the first part of this lesson- [Create AWS Redshift cluster using AWS python SDK](https://shravan-kuchkula.github.io/create-aws-redshift-cluster/#author-shravan-kuchkula) will help create 'dwh.cfg' file. Take note of DWH_ENDPOINT and DWH_ROLE_ARN as it will be needed in the 'dwh.cfg' file.
* Ensure git doesn't track your 'dwh.cfg' file to protect your
Access key ID and Secret access key from being exposed.
* IDENTITY (0,1) is the subtitute for SERIAL used for generating a unique ID in Redshift.

## References
[Create AWS Redshift cluster using AWS python SDK](https://shravan-kuchkula.github.io/create-aws-redshift-cluster/#author-shravan-kuchkula)

[Configparser Documentation](https://docs.python.org/3/library/configparser.html)
