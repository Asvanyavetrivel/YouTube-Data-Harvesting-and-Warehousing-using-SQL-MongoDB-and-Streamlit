#importing the necessary libraries

# Youtube API libraries
from googleapiclient.discovery import build

# MongoDB
from pymongo import MongoClient

# SQL libraries
import psycopg2

# Pandas
import pandas as pd

# Dash board libraries
import streamlit as st
from PIL import Image
from streamlit_option_menu import option_menu

#Connection created to interact with YouTube API
def Api_connect():
    Api_Id="AIzaSyCq3PJs-YEBoZzYdqqk6iV7HP-U8dPE278" # API Key

    api_service_name = "youtube"
    api_version = "v3"
    youtube = build(api_service_name,api_version,developerKey=Api_Id)
    return youtube

youtube=Api_connect()

# Function to get channel details from YouTube

#Function Definition:
def get_channel_info(channel_id):

    #API Request
    request = youtube.channels().list(
                part = "snippet,contentDetails,Statistics",
                id = channel_id)
            
    response1=request.execute()

    for i in range(0,len(response1["items"])):
        data = dict(
                    Channel_Name = response1["items"][i]["snippet"]["title"],
                    Channel_Id = response1["items"][i]["id"],
                    Subscription_Count= response1["items"][i]["statistics"]["subscriberCount"],
                    Views = response1["items"][i]["statistics"]["viewCount"],
                    Total_Videos = response1["items"][i]["statistics"]["videoCount"],
                    Channel_Description = response1["items"][i]["snippet"]["description"],
                    Playlist_Id = response1["items"][i]["contentDetails"]["relatedPlaylists"]["uploads"],
                    )
        return data

# Function to get playlist details of a channel from YouTube

#Function Definition:
def get_playlist_info(channel_id):
    #Initialize Empty List
    All_data = []
    next_page_token = None
    next_page = True
    while next_page:

        request = youtube.playlists().list(
            part="snippet,contentDetails",
            channelId=channel_id,
            maxResults=50,
            pageToken=next_page_token
            )
        response = request.execute()

        for item in response['items']: 
            data={'PlaylistId':item['id'],
                    'Title':item['snippet']['title'],
                    'ChannelId':item['snippet']['channelId'],
                    'ChannelName':item['snippet']['channelTitle'],
                    'PublishedAt':item['snippet']['publishedAt'],
                    'VideoCount':item['contentDetails']['itemCount']}
            All_data.append(data)
        next_page_token = response.get('nextPageToken')
        if next_page_token is None:
            next_page=False
    return All_data
    
# Function to get Video Ids of a channel from YouTube
#Function Definition:
def get_channel_videos(channel_id):
    video_ids = []
    # get Uploads playlist id
    response = youtube.channels().list(id=channel_id, 
                                  part='contentDetails').execute()
    playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    next_page_token = None
    
    while True:
        response = youtube.playlistItems().list( 
                                           part = 'snippet',
                                           playlistId = playlist_id, 
                                           maxResults = 50,
                                           pageToken = next_page_token).execute()
        
        for i in range(len(response['items'])):
            video_ids.append(response['items'][i]['snippet']['resourceId']['videoId'])
        next_page_token = response.get('nextPageToken')
        
        if next_page_token is None:
            break
    return video_ids

# Function to get video details of all video IDS from YouTube
#Function Definition:
def get_video_info(video_ids):

    video_data = []

    for video_id in video_ids:
        request = youtube.videos().list(
                    part="snippet,contentDetails,statistics",
                    id= video_id)
        response = request.execute()

        for item in response["items"]:
            data = dict(Channel_Name = item['snippet']['channelTitle'],
                        Channel_Id = item['snippet']['channelId'],
                        Video_Id = item['id'],
                        Title = item['snippet']['title'],
                        Tags = item['snippet'].get('tags'),
                        Thumbnail = item['snippet']['thumbnails']['default']['url'],
                        Description = item['snippet']['description'],
                        Published_Date = item['snippet']['publishedAt'],
                        Duration = item['contentDetails']['duration'],
                        Views = item['statistics']['viewCount'],
                        Likes = item['statistics'].get('likeCount'),
                        Comments = item['statistics'].get('commentCount'),
                        Favorite_Count = item['statistics']['favoriteCount'],
                        Definition = item['contentDetails']['definition'],
                        Caption_Status = item['contentDetails']['caption']
                        )
            video_data.append(data)
    return video_data

# Function to get comments for all video IDs from YouTube
#Function Definition:
def get_comment_info(video_ids):
        Comment_Information = []
        try:
                for video_id in video_ids:

                        request = youtube.commentThreads().list(
                                part = "snippet",
                                videoId = video_id,
                                maxResults = 50
                                )
                        response5 = request.execute()
                        
                        for item in response5["items"]:
                                comment_information = dict(
                                        Comment_Id = item["snippet"]["topLevelComment"]["id"],
                                        Video_Id = item["snippet"]["videoId"],
                                        Comment_Text = item["snippet"]["topLevelComment"]["snippet"]["textOriginal"],
                                        Comment_Author = item["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"],
                                        Comment_Published = item["snippet"]["topLevelComment"]["snippet"]["publishedAt"])

                                Comment_Information.append(comment_information)
        except:
                pass
                
        return Comment_Information

# Streamlit-Page Configuration and adding name to browser tab
st.set_page_config(
        page_title="GUVI Capstone Project-1",
        layout="wide",
        initial_sidebar_state="expanded"
    )


# Streamlit-Sidebar Option creation
img=Image.open("youtube.png")
with st.sidebar:
    st.image(img)
with st.sidebar:
    selected = option_menu(None, ["Home","Extract and Transform","Data Analysis"], 
                           icons=["house-door-fill","database-fill-gear","file-earmark-bar-graph"],
                           default_index=0,
                           orientation="vertical",
                           )

#Streamlit-Setting up option 'Extract and Transform'
if selected == "Home":
    st.title("YouTube Data Harvesting and Warehousing using SQL, MongoDB and Streamlit")
    st.header(":white[Project Overview]")
    st.markdown("""
 YouTube Data Harvesting and Warehousing is a project that aims to Building a system to harvest YouTube data, store it in a MongoDB data lake, perform data transformations, and migrate it to a SQL database for structured storage. The project includes a user-friendly Streamlit web app for interactive data analysis
- Data Retrieval: Utilizing the YouTube Data API to fetch data from YouTube.This API allows us to retrieve information about videos, channels, playlists, etc.
- Data Lake (MongoDB): The retrieved data from the YouTube API,is stored in a Mongo DB data lake.Mongo DB is a NoSQL database that allows more flexibility with schema design.
- Data Migration & Transformation: Data is Transfered from MongoDB to a SQL database for structured storage. Perform necessary data transformations and cleaning to ensure data quality and consistency
- Streamlit App: A user-friendly UI built using Streamlit library, allowing users to interact with the application and perform data retrieval and analysis tasks.            
""")
    st.balloons()

elif selected == "Extract and Transform":
    st.header("Data Extraction and Data Migration")
    st.markdown("(This will utilize the YouTube API to extract channel information, storing it in a structured format in MongoDB, and subsequently migrating the data into SQL tables.)")       
   
    #MongoDB Connection
    client = MongoClient('mongodb://localhost:27017/')
    db = client["Youtube_data_project"]

    #Retrived Data stored in Mongo DB

    def channel_details(channel_id):
        ch_details = get_channel_info(channel_id)
        pl_details = get_playlist_info(channel_id)
        vi_ids = get_channel_videos(channel_id)
        vi_details = get_video_info(vi_ids)
        com_details = get_comment_info(vi_ids)

        coll1 = db["channel_details"]
        coll1.insert_one({"channel_information":ch_details,"playlist_information":pl_details,"video_information":vi_details,
                        "comment_information":com_details})
        
        return "Data uploaded to MongoDB sucessfully"

    #sqlconnection-table creation for channels
    def channels_table():
        mydb = psycopg2.connect(host="localhost",
                user="postgres",
                password="2112",
                database= "youtube_data",
                port = "5432"
                )
        cursor = mydb.cursor()

        #table drop query if already existing channel id is uploaded it will show an error as channel id is pk

        drop_query = "drop table if exists channels"
        cursor.execute(drop_query)
        mydb.commit()

        #create a table named "channels" in a PostgreSQL database
        
        try:
            create_query = '''create table if not exists channels(Channel_Name varchar(100),
                            Channel_Id varchar(80) primary key, 
                            Subscription_Count bigint, 
                            Views bigint,
                            Total_Videos int,
                            Channel_Description text,
                            Playlist_Id varchar(50))'''
            cursor.execute(create_query)
            mydb.commit()
        except:
            st.write("Channels Table already created in the database")    


        ch_list = []
        db = client["Youtube_data_project"]
        coll1 = db["channel_details"]
        #data extraction
        for ch_data in coll1.find({},{"_id":0,"channel_information":1}):
            ch_list.append(ch_data["channel_information"])
        #data frame formate
        df = pd.DataFrame(ch_list)
        
        for index,row in df.iterrows():
            insert_query = '''INSERT into channels(Channel_Name,
                                                        Channel_Id,
                                                        Subscription_Count,
                                                        Views,
                                                        Total_Videos,
                                                        Channel_Description,
                                                        Playlist_Id)
                                            VALUES(%s,%s,%s,%s,%s,%s,%s)'''
                

            values =(
                    row['Channel_Name'],
                    row['Channel_Id'],
                    row['Subscription_Count'],
                    row['Views'],
                    row['Total_Videos'],
                    row['Channel_Description'],
                    row['Playlist_Id'])
            try:                     
                cursor.execute(insert_query,values)
                mydb.commit()    
            except:
                st.write("Channels values was already inserted")

    #sqlconnection-table creation for playlists
                            
    def playlists_table():
        mydb = psycopg2.connect(host="localhost",
                user="postgres",
                password="2112",
                database= "youtube_data",
                port = "5432"
                )
        cursor = mydb.cursor()

        drop_query = "drop table if exists playlists"
        cursor.execute(drop_query)
        mydb.commit()

        #create a table named "Playlists" in a PostgreSQL database
        try:
            create_query = '''create table if not exists playlists(PlaylistId varchar(100) primary key,
                            Title varchar(80), 
                            ChannelId varchar(100), 
                            ChannelName varchar(100),
                            PublishedAt timestamp,
                            VideoCount int
                            )'''
            cursor.execute(create_query)
            mydb.commit()
        except:
            st.write("Playlists Table already created in the database")    


        db = client["Youtube_data_project"]
        coll1 =db["channel_details"]
        pl_list = []
        for pl_data in coll1.find({},{"_id":0,"playlist_information":1}):
            for i in range(len(pl_data["playlist_information"])):
                    pl_list.append(pl_data["playlist_information"][i])
        df = pd.DataFrame(pl_list)
        
        for index,row in df.iterrows():
            insert_query = '''INSERT into playlists(PlaylistId,
                                                        Title,
                                                        ChannelId,
                                                        ChannelName,
                                                        PublishedAt,
                                                        VideoCount)
                                            VALUES(%s,%s,%s,%s,%s,%s)'''            
            values =(
                    row['PlaylistId'],
                    row['Title'],
                    row['ChannelId'],
                    row['ChannelName'],
                    row['PublishedAt'],
                    row['VideoCount'])
                    
            try:                     
                cursor.execute(insert_query,values)
                mydb.commit()    
            except:
                st.write("Playlists values was already inserted")
    
    #sqlconnection-table creation for videos
    def videos_table():

        mydb = psycopg2.connect(host="localhost",
                    user="postgres",
                    password="2112",
                    database= "youtube_data",
                    port = "5432"
                    )
        cursor = mydb.cursor()

        drop_query = "drop table if exists videos"
        cursor.execute(drop_query)
        mydb.commit()

        #create a table named "videos" in a PostgreSQL database
        
        try:
            create_query = '''create table if not exists videos(
                            Channel_Name varchar(150),
                            Channel_Id varchar(100),
                            Video_Id varchar(50) primary key, 
                            Title varchar(150), 
                            Tags text,
                            Thumbnail varchar(225),
                            Description text, 
                            Published_Date timestamp,
                            Duration interval, 
                            Views bigint, 
                            Likes bigint,
                            Comments int,
                            Favorite_Count int, 
                            Definition varchar(10), 
                            Caption_Status varchar(50) 
                            )''' 
                            
            cursor.execute(create_query)             
            mydb.commit()
        except:
            st.write("Videos Table already created in the database")

        vi_list = []
        db = client["Youtube_data_project"]
        coll1 = db["channel_details"]
        for vi_data in coll1.find({},{"_id":0,"video_information":1}):
            for i in range(len(vi_data["video_information"])):
                vi_list.append(vi_data["video_information"][i])
        df2 = pd.DataFrame(vi_list)
            
        
        for index, row in df2.iterrows():
            insert_query = '''
                        INSERT INTO videos (Channel_Name,
                            Channel_Id,
                            Video_Id, 
                            Title, 
                            Tags,
                            Thumbnail,
                            Description, 
                            Published_Date,
                            Duration, 
                            Views, 
                            Likes,
                            Comments,
                            Favorite_Count, 
                            Definition, 
                            Caption_Status 
                            )
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)

                    '''
            values = (
                        row['Channel_Name'],
                        row['Channel_Id'],
                        row['Video_Id'],
                        row['Title'],
                        row['Tags'],
                        row['Thumbnail'],
                        row['Description'],
                        row['Published_Date'],
                        row['Duration'],
                        row['Views'],
                        row['Likes'],
                        row['Comments'],
                        row['Favorite_Count'],
                        row['Definition'],
                        row['Caption_Status'])
                                    
            try:    
                cursor.execute(insert_query,values)
                mydb.commit()
            except:
                st.write("video values was already inserted")
            
     #sqlconnection-table creation for comments
    def comments_table():
        
        mydb = psycopg2.connect(host="localhost",
                    user="postgres",
                    password="2112",
                    database= "youtube_data",
                    port = "5432"
                    )
        cursor = mydb.cursor()

        drop_query = "drop table if exists comments"
        cursor.execute(drop_query)
        mydb.commit()
        
        #create a table named "comments" in a PostgreSQL database
        
        try:
            create_query = '''CREATE TABLE if not exists comments(Comment_Id varchar(100) primary key,
                        Video_Id varchar(80),
                        Comment_Text text, 
                        Comment_Author varchar(150),
                        Comment_Published timestamp)'''
            cursor.execute(create_query)
            mydb.commit()
            
        except:
            st.write("Comments Table already created in the database")

        com_list = []
        db = client["Youtube_data_project"]
        coll1 = db["channel_details"]
        for com_data in coll1.find({},{"_id":0,"comment_information":1}):
            for i in range(len(com_data["comment_information"])):
                com_list.append(com_data["comment_information"][i])
        df3 = pd.DataFrame(com_list)


        for index, row in df3.iterrows():
                insert_query = '''
                    INSERT INTO comments (Comment_Id,
                                        Video_Id ,
                                        Comment_Text,
                                        Comment_Author,
                                        Comment_Published)
                    VALUES (%s, %s, %s, %s, %s)

                '''
                values = (
                    row['Comment_Id'],
                    row['Video_Id'],
                    row['Comment_Text'],
                    row['Comment_Author'],
                    row['Comment_Published']
                )
                try:
                    cursor.execute(insert_query,values)
                    mydb.commit()
                except:
                 st.write("comments was already exist in comments table")
                    
    #Migrates data from MongoDB to the SQL databas
    
    def tables():
        channels_table()
        playlists_table()
        videos_table()
        comments_table()
        return "Data Migrated to the SQL database and Table created successfully"
        
    def show_channels_table():
        ch_list = []
        db = client["Youtube_data_project"]
        coll1 = db["channel_details"] 
        for ch_data in coll1.find({},{"_id":0,"channel_information":1}):
            ch_list.append(ch_data["channel_information"])
        channels_table = st.dataframe(ch_list)
        return channels_table

    def show_playlists_table():
        db = client["Youtube_data_project"]
        coll1 =db["channel_details"]
        pl_list = []
        for pl_data in coll1.find({},{"_id":0,"playlist_information":1}):
            for i in range(len(pl_data["playlist_information"])):
                    pl_list.append(pl_data["playlist_information"][i])
        playlists_table = st.dataframe(pl_list)
        return playlists_table

    def show_videos_table():
        vi_list = []
        db = client["Youtube_data_project"]
        coll2 = db["channel_details"]
        for vi_data in coll2.find({},{"_id":0,"video_information":1}):
            for i in range(len(vi_data["video_information"])):
                vi_list.append(vi_data["video_information"][i])
        videos_table = st.dataframe(vi_list)
        return videos_table

    def show_comments_table():
        com_list = []
        db = client["Youtube_data_project"]
        coll3 = db["channel_details"]
        for com_data in coll3.find({},{"_id":0,"comment_information":1}):
            for i in range(len(com_data["comment_information"])):
                com_list.append(com_data["comment_information"][i])
        comments_table = st.dataframe(com_list)
        return comments_table

    channel_id = st.text_input("Enter the Channel id")
    channels = channel_id.split(',')
    channels = [ch.strip() for ch in channels if ch]

    if st.button("Data Storage-MongoDB"):
        for channel in channels:
            ch_ids = []
            db = client["Youtube_data_project"]
            coll1 = db["channel_details"]
            for ch_data in coll1.find({},{"_id":0,"channel_information":1}):
                ch_ids.append(ch_data["channel_information"]["Channel_Id"])
            if channel in ch_ids:
                st.success("Channel details of the given channel id: " + channel + " already exists")
            else:
                output = channel_details(channel)
                st.success(output)

    if st.button("Data Migration-SQL"):
        display = tables()
        st.success(display)
                
    st.header('Select option to view')
    show_table = st.selectbox("Choose a Table",("Channels", "Playlists", "Videos", "Comments"))

    if show_table == "Channels":
        show_channels_table()
    elif show_table == "Playlists":
        show_playlists_table()
    elif show_table =="Videos":
        show_videos_table()
    elif show_table == "Comments":
        show_comments_table()


#Streamlit-Setting up option 'Data Analysis'
elif selected == "Data Analysis":
    st.header('Data Analysis-SQL Query Output')
    st.caption("(This analyzes a dataset of channel information, presenting the outcomes in a table format according to the chosen queries.)")

    #SQL connection
    mydb = psycopg2.connect(host="localhost",
                user="postgres",
                password="2112",
                database= "youtube_data",
                port = "5432"
                )
    cursor = mydb.cursor()
        
    question = st.selectbox(
        'Please Select Your Question',
        ('1.What are the names of all the videos and their corresponding channels',
        '2.Which channels have the most number of videos, and how many videos do they have',
        '3.What are the top 10 most viewed videos and their respective channels',
        '4.How many comments were made on each video, and what are their corresponding video names',
        '5.Which videos have the highest number of likes, and what are their corresponding channel names',
        '6.What is the total number of likes for each video, and what are their corresponding video names',
        '7.What is the total number of views for each channel, and what are their corresponding channel names',
        '8.What are the names of all the channels that have published videos in the year 2022',
        '9.What is the average duration of all videos in each channel, and what are their corresponding channel names',
        '10.Which videos have the highest number of comments, and what are their corresponding channel names'))

        
    if question == '1.What are the names of all the videos and their corresponding channels':
        query1 = "select Channel_Name as ChannelName, Title as videos from videos;"
        cursor.execute(query1)
        mydb.commit()
        t1=cursor.fetchall()
        st.write(pd.DataFrame(t1, columns=["Channel Name","Video Name"]))

    elif question == '2.Which channels have the most number of videos, and how many videos do they have':
        query2 = "select Channel_Name as ChannelName,Total_Videos as NO_Videos from channels order by Total_Videos desc;"
        cursor.execute(query2)
        mydb.commit()
        t2=cursor.fetchall()
        st.write(pd.DataFrame(t2, columns=["Channel Name","Total Video Count"]))

    elif question == '3.What are the top 10 most viewed videos and their respective channels':
        query3 = '''select Channel_Name as ChannelName,Title as VideoTitle,Views as views from videos 
                            where Views is not null order by Views desc limit 10;'''
        cursor.execute(query3)
        mydb.commit()
        t3 = cursor.fetchall()
        st.write(pd.DataFrame(t3, columns = ["Channel Name","Top 10 most viewed videos title","Views"]))

    elif question == '4.How many comments were made on each video, and what are their corresponding video names':
        query4 = "select Title as VideoTitle ,Comments as No_comments from videos where Comments is not null;"
        cursor.execute(query4)
        mydb.commit()
        t4=cursor.fetchall()
        st.write(pd.DataFrame(t4, columns=["Video Name","No Of Comments"]))

    elif question == '5.Which videos have the highest number of likes, and what are their corresponding channel names':
        query5 = '''select Channel_Name as ChannelName,Title as VideoTitle, Likes as LikesCount from videos 
                        where Likes is not null order by Likes desc;'''
        cursor.execute(query5)
        mydb.commit()
        t5 = cursor.fetchall()
        st.write(pd.DataFrame(t5, columns=["Channel Name","Video Name","Likes count"]))

    elif question == '6.What is the total number of likes for each video, and what are their corresponding video names':
        query6 = '''select Title as VideoTitle,Likes as likeCount from videos;'''
        cursor.execute(query6)
        mydb.commit()
        t6 = cursor.fetchall()
        st.write(pd.DataFrame(t6, columns=["Video Names","Total Like count"]))

    elif question == '7.What is the total number of views for each channel, and what are their corresponding channel names':
        query7 = "select Channel_Name as ChannelName, Views as Channelviews from channels;"
        cursor.execute(query7)
        mydb.commit()
        t7=cursor.fetchall()
        st.write(pd.DataFrame(t7, columns=["Channel name","Total views"]))

    elif question == '8.What are the names of all the channels that have published videos in the year 2022':
        query8 = '''select Channel_Name as ChannelName,Title as Video_Title, Published_Date as VideoRelease from videos 
                    where extract(year from Published_Date) = 2022;'''
        cursor.execute(query8)
        mydb.commit()
        t8=cursor.fetchall()
        st.write(pd.DataFrame(t8,columns=[ "Channel Name","Video Name", "Video Publised On"]))

    elif question == '9.What is the average duration of all videos in each channel, and what are their corresponding channel names':
        query9 =  "SELECT Channel_Name as ChannelName, AVG(Duration) AS average_duration FROM videos GROUP BY Channel_Name;"
        cursor.execute(query9)
        mydb.commit()
        t9=cursor.fetchall()
        t9 = pd.DataFrame(t9, columns=['ChannelTitle', 'Average Duration'])
        T9=[]
        for index, row in t9.iterrows():
            channel_title = row['ChannelTitle']
            average_duration = row['Average Duration']
            average_duration_str = str(average_duration)
            T9.append({"Channel Title": channel_title ,  "Average Duration": average_duration_str})
        st.write(pd.DataFrame(T9))

    elif question == '10.Which videos have the highest number of comments, and what are their corresponding channel names':
        query10 = '''select Channel_Name as ChannelName,Title as VideoTitle,Comments as Comments from videos 
                        where Comments is not null order by Comments desc;'''
        cursor.execute(query10)
        mydb.commit()
        t10=cursor.fetchall()
        st.write(pd.DataFrame(t10, columns=['Channel Name','Video Name','No Of Comments']))
