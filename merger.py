# AUTHOR: David Fuentes Martín 2023

import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "YOUR_CLIENT_SECRET_FILE_LOCATION"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)
    
    # Inputs for the IDs
    my_playlist=input("Insert your playlist ID:\n")

    request = youtube.playlistItems().list(
        part="snippet",
        playlistId=my_playlist,
        maxResults = 1
    )
    response = request.execute()
    
    myplaylist_items = []
    myplaylist_ids_char = []
    myplaylist_ids = []
    current_id=""
    while request is not None:
        response = request.execute()
        myplaylist_items += response["items"]
        myplaylist_ids_char += response["items"][0]['snippet']['resourceId']['videoId']
        for char in myplaylist_ids_char:
            current_id += char
        myplaylist_ids.append(current_id)
        print("Collecting playlist information:\n[IDs]")
        print(myplaylist_ids)
        print("\n")
        current_id=""
        myplaylist_ids_char=[]
        request = youtube.playlistItems().list_next(request,response)


    playlist=input("Insert the playlist ID that you want to add:\n")

    request2 = youtube.playlistItems().list(
        part="snippet",
        playlistId=playlist,
        maxResults = 1
    )
    response2 = request2.execute()

    playlist_items = []
    playlist_ids_char = []
    playlist_ids = []
    current_id=""
    while request2 is not None:
        response2 = request2.execute()
        playlist_items += response2["items"]
        playlist_ids_char += response2["items"][0]['snippet']['resourceId']['videoId']
        for char in playlist_ids_char:
            current_id += char
        playlist_ids.append(current_id)
        print("Collecting playlist information:\n[IDs]")
        print(playlist_ids)
        print("\n")
        current_id=""
        playlist_ids_char=[]
        request2 = youtube.playlistItems().list_next(request2,response2)

    print("Merging...")

    total=0
    aux=0

    for videoId in playlist_ids:
        total+=1
        if myplaylist_ids.count(videoId) == 0:
            request = youtube.playlistItems().insert(
                part="snippet",
                body={
                  "kind": "youtube#playlistItem",
                  "snippet": {
                    "playlistId": my_playlist,
                    "resourceId": {
                      "kind": "youtube#video",
                      "videoId": videoId
                    }
                  },
                }
            )
            response = request.execute()
            aux+=1
        print(f"{round(100*(total/len(playlist_ids)),1)}%")

    print(f"You are done, you have added {aux} items to your playlist. {total-aux} of the {total} items were duplicate.")

if __name__ == "__main__":
    main()