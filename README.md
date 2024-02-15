# YouTube-Data-Harvesting-and-Warehousing-using-SQL-MongoDB-and-Streamlit

## Introduction
YouTube Data Harvesting and Warehousing is a project that aims to Building a system to harvest YouTube data, store it in databases like SQL and MongoDB, and creating a user interface using Streamlit

### Technologies Used

The following technologies are used in this project:

* Python:The programming language used for building the application and scripting tasks.
* Pandas: A data manipulation library used for data processing and analysis.
* YouTube API:Google API is used to retrieve channel and video data from YouTube.
* MongoDB:A NoSQL database used as a data lake for storing retrieved YouTube data.
* SQL (PostgreSQL): A relational database used as a data warehouse for storing migrated YouTube data.
* Streamlit:A Python library used for creating interactive web applications and data visualizations.


#### Prerequisites
Install the below packages using pip install in terminal:
- pymongo
- psycopg2
- pandas as pd
- streamlit as st
- googleapiclient.discovery import build

### Work flow
#### 1.YouTube Data Harvesting:
-Use the YouTube Data API to fetch data from YouTube. 
-This API allows us to retrieve information about videos, channels, playlists, etc.
-Python script were written to interact with the YouTube API, fetch the data, and store it in a structured format.

#### 2.Data Storage:
-The retrieved data from the YouTube API,is stored in a MongoDB data lake.
-MongoDB is a NoSQL database that allows more flexibility with schema design.

#### 3.Data Warehousing:
-After Data Storage which has the collected data for multiple channels,is migrated to a SQL data warehouse,I have used PostgreSQL in this project

#### 4. Integration with SQL and MongoDB:
 -Python script were written to interact with the SQL and MongoDB databases for storing and retrieving data.SQL queries were written to join the tables in the SQL data warehouse and retrieve data for specific channels based on user input.

 #### 5.Streamlit Dashboard:
 -Streamlit is a Python library for building interactive web applications.I have used it to create a user interface for this project YouTube data warehouse
 -Dashboard interface is Designed to display relevant information from the SQL and MongoDB databases.

 #### To Run the Streamlit app in the terminal:
Use command: streamlit run .py

### User Guide
Step 1. Data collection
Search channel_id, copy and paste on the input box and click the Get data and stored button in the Data collection zone.
Step 2. Data Migrate zone
Select the channel name and click the Migrate to MySQL button to migrate the specific channel data to the MySQL database from MongoDB in the Data Migrate zone.
Step 3. Channel Data Analysis zone
Select a Question from the dropdown option you can get the results in Dataframe format or bar chat format.
