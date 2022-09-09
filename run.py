import sys
import comments_collector as cc

api_key = "AIzaSyAl7yjWd1qLxdmANEFNDAC828D2jFjucqY"
video_url = "https://www.youtube.com/watch?v=MDBykpSXsSE"

def get_comments(video_url, order = 'time', maxResults = 100):
    '''
    the function to fetch comments from the helper module for ONE video
    '''    
    # build the service for YT API    
    yt_service = cc.build_service(api_key)    
    # extract video id    
    video_ID = cc.get_id(video_url)    
    # get the comments    
    comments_dict, title = cc.comments_helper(video_ID, yt_service, order , maxResults)    
    # save the output dict to storage as a csv file    
    cc.save_to_csv(comments_dict, title)    
    print(f'Done for {video_url}.')
    

get_comments(video_url)        
