import requests
import json
import pandas as pd
from apiclient.discovery import build
from csv import writer
from urllib.parse import urlparse, parse_qs


def build_service(api_key):
    '''
    To build the YT API service
    '''    
    key = api_key
    YOUTUBE_API_SERVICE_NAME = "youtube"    
    YOUTUBE_API_VERSION = "v3"    
    return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey = key)
    
def get_id(url):
    '''
    To get the video id from the video url, example: 
    'https://www.youtube.com/watch?v=wfAPXlFu8', videoId = wfAPXlFu8
    '''   
    u_pars = urlparse(url)    
    quer_v = parse_qs(u_pars.query).get('v')    
    if quer_v:        
        return quer_v[0]    
    pth = u_pars.path.split('/')    
    if pth:        
        return pth[-1]
    
def save_to_csv(output_dict, filename):
    '''
    To save the comments + other columns to the csv file specified with name
    ''' 
    
    print('Saving to CSV')
    output_df = pd.DataFrame(output_dict, columns = output_dict.keys())    
    output_df.to_csv(f'data/{filename}.csv')
	
def comments_helper(video_ID, yt_service, order, maxResults):	
    # put comments extracted in specific lists for each column
    comments, commentsId, likesCount, authors = [], [], [], []
                                       
    #get the first response from the YT service
    response = yt_service.commentThreads().list(
                                        part="snippet",   
                                        videoId = video_ID,   
                                        textFormat="plainText",
                                        order = order, 
                                        maxResults = maxResults,
                                        ).execute()
                                        
    page = 0
    while len(comments)<1000:    
        page += 1    
        index = 0    
        # for every comment in the response received    
        for item in response['items']:        
            index += 1
            comment    = item["snippet"]["topLevelComment"]        
            author     = comment["snippet"]["authorDisplayName"]        
            text       = comment["snippet"]["textDisplay"]        
            comment_id = item['snippet']['topLevelComment']['id']        
            like_count = item['snippet']['topLevelComment']['snippet']['likeCount']  
            
            #print(comment)
            
            # append the comment to the lists        
            comments.append(text)        
            commentsId.append(comment_id)        
            likesCount.append(like_count)        
            authors.append(author)    
            # get next page of comments    
        if 'nextPageToken' in response: 
            # can also specify if number of comments intended to collect reached like: len(comments) > 1001 
            response = yt_service.commentThreads().list(
                                                part="snippet",        
                                                videoId = video_ID,        
                                                textFormat="plainText",                                                    
                                                pageToken=response['nextPageToken'],
                                                order = order, 
                                                maxResults = maxResults
                                                ).execute()    
     
        # if no response is received, break     
        else:         
            break  
            
    # response to get the title of the video
    response_title = yt_service.videos().list(part = 'snippet', id = video_ID).execute()
    # get the video title
    video_title = response_title['items'][0]['snippet']['title']
    # return the whole thing as a dict and the video title to calling function in run.py    
    return dict({'Comment' : comments, 
                 'Author' : authors, 
                 'Comment ID' : commentsId, 
                 'Like Count' : likesCount}), video_title