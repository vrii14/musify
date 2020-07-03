from django import forms
from django.conf import settings
import requests
import base64
import datetime
from urllib.parse import urlencode

class SpotifyAPI(object):
    access_token = None
    access_token_expires = datetime.datetime.now()
    access_token_did_expire = True
    client_id = None
    client_secret = None
    token_url = "https://accounts.spotify.com/api/token"
    
    
    def get_client_credentials(self):
        """
        Returns a base64 encoded string
        """
        client_id = settings.SPOTIFY_CLIENT_ID
        client_secret = settings.SPOTIFY_CLIENT_SECRET
        if client_secret == None or client_id == None:
            raise Exception("You must set client_id and client_secret")
        client_creds = f"{client_id}:{client_secret}"
        client_creds_b64 = base64.b64encode(client_creds.encode())
        return client_creds_b64.decode()
    
    def get_token_headers(self):
        client_creds_b64 = self.get_client_credentials()
        return {
            "Authorization": f"Basic {client_creds_b64}"
        }
    
    def get_token_data(self):
        return {
            "grant_type": "client_credentials"
        } 
    
    def perform_auth(self):
        token_url = self.token_url
        token_data = self.get_token_data()
        token_headers = self.get_token_headers()
        r = requests.post(token_url, data=token_data, headers=token_headers)
        if r.status_code not in range(200, 299):
            raise Exception("Could not authenticate client.")
            # return False
        data = r.json()
        now = datetime.datetime.now()
        access_token = data['access_token']
        expires_in = data['expires_in'] # seconds
        expires = now + datetime.timedelta(seconds=expires_in)
        self.access_token = access_token
        self.access_token_expires = expires
        self.access_token_did_expire = expires < now
        return True
    
    def get_access_token(self):
        token = self.access_token
        expires = self.access_token_expires
        now = datetime.datetime.now()
        if expires < now:
            self.perform_auth()
            return self.get_access_token()
        elif token == None:
            self.perform_auth()
            return self.get_access_token() 
        return token
    
    def get_resource_header(self):
        access_token = self.get_access_token()
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        return headers
        
        
    def get_resource(self, lookup_id, resource_type='albums', version='v1'):
        endpoint = f"https://api.spotify.com/{version}/{resource_type}/{lookup_id}"
        headers = self.get_resource_header()
        r = requests.get(endpoint, headers=headers)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()
    
    def get_album(self, name):
        _id = self.get_album_id(name)
        return self.get_resource(_id, resource_type='albums')
    
    def get_artist(self, name):
        _id = self.get_artist_id(name)
        return self.get_resource(_id, resource_type='artists')

    def get_artist_id(self, artist_name):
        results = self.search(query = "artist:" + artist_name, search_type= "artist")
        items = results["artists"]["items"]
        if len(items) == 0:
            return None
        else:
            d = items[0]
        art_id = d["id"] 
        return(art_id)
    
    def get_album_id(self, album_name):
        results = self.search(query = "album:" + album_name, search_type= "album")
        album_id = results['albums']['items'][0]['id']
        return(album_id)
    
    def base_search(self, query_params): # type
        headers = self.get_resource_header()
        endpoint = "https://api.spotify.com/v1/search"
        lookup_url = f"{endpoint}?{query_params}"
        r = requests.get(lookup_url, headers=headers)
        if r.status_code not in range(200, 299):  
            return {}
        return r.json()

    
    def search(self, query=None, operator=None, operator_query=None, search_type='artist' ):
        if query == None:
            raise Exception("A query is required")
        if isinstance(query, dict):
            query = " ".join([f"{k}:{v}" for k,v in query.items()])
        if operator != None and operator_query != None:
            if operator.lower() == "or" or operator.lower() == "not":
                operator = operator.upper()
                if isinstance(operator_query, str):
                    query = f"{query} {operator} {operator_query}"
        query_params = urlencode({"q": query, "type": search_type.lower()})
        return self.base_search(query_params)


    def get_recommendations(self, seed_artists=None, seed_genres=None, seed_tracks=None):
        headers = self.get_resource_header()
        endpoint = "https://api.spotify.com/v1/recommendations"
        query_params = urlencode({"seed_artists":seed_artists, "seed_genres":seed_genres, "seed_tracks":seed_tracks})
        lookup_url = f"{endpoint}?{query_params}"
        r = requests.get(lookup_url, headers=headers)
        if r.status_code not in range(200, 299):  
            return {}
        return r.json()

    def get_user_data(self, user_id):
        headers = self.get_resource_header()
        endpoint = "https://api.spotify.com/v1/users"
        lookup_url = f"{endpoint}/{user_id}"
        r = requests.get(lookup_url, headers=headers)
        print(r.json())
        if r.status_code not in range(200, 299):  
            return {}
        return r.json()




