import json
from bs4 import BeautifulSoup
import sys
import urllib.request
import xml.etree.ElementTree as ET
import requests
import datetime
from urllib.parse import urlencode
import base64
client_id = 'cef5a9c19ee14d3fb0b1881fcbe97688'
client_secret = '5ae92bba207f41608e036810e413c7cf'


class SpotifyApi:
    track = None
    access_token = None
    access_token_expires = datetime.datetime.now()
    access_token_did_expire = True
    client_id = None
    client_secret = None
    token_url = "https://accounts.spotify.com/api/token"

    def __init__(self, client_id, client_secret, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = client_id
        self.client_secret = client_secret

    def get_client_credentials(self):
        client_id = self.client_id
        client_secret = self.client_secret
        if client_secret == None or client_id == None:
            raise Exception("You must set client_id and client_secret")
        client_creds = f"{client_id}:{client_secret}"
        client_creds_b64 = base64.b64encode(client_creds.encode())
        return client_creds_b64.decode()

    def get_token_data(self):
        return {
            "grant_type": "client_credentials"
        }

    def get_token_headers(self):
        client_cred_b64 = self.get_client_credentials()
        return {
            "Authorization": f"Basic {client_cred_b64}"
        }

    def perform_auth(self):
        token_url = self.token_url
        token_data = self.get_token_data()
        token_headers = self.get_token_headers()
        r = requests.post(token_url, data=token_data, headers=token_headers)
        if r.status_code not in range (200, 299):
            raise Exception("Could not authenticate client.")
        data = r.json()
        now = datetime.datetime.now()
        access_token = data['access_token']
        expires_in = data['expires_in']
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
        elif token is None:
            self.perform_auth()
            return self.get_access_token()
        return token

    def search(self, query=None, search_type='track', markets='NG', limiter=1):
        access_token = self.get_access_token()
        # print(access_token)
        headers = {"Authorization":f"Bearer {access_token}"}
        endpoint = "https://api.spotify.com/v1/search"
        data = urlencode({"q": query, "type": search_type.lower(), 'limit': limiter})
        look_url = f"{endpoint}?{data}"
        # print(look_url)
        r = requests.get(look_url, headers=headers)
        #return r
        self.track = r.json()
        #return json.dumps(self.track, indent=2)

    def get_uri(self, query=None, search_type='track', markets='NG', limiter=1):
        self.search(query, search_type, markets, limiter)
        data = (json.dumps(self.track, indent=2))
        data = self.track
        uri = (data['tracks']['items'][0]['uri'])
        uri_clean = uri.split(':')[2]
        return uri_clean


client = SpotifyApi(client_id, client_secret)
print(client.get_uri(query='Carterefe & Berri-Tiga - Machala', search_type='track'))

def get_top_100_ID():
    url = 'https://kworb.net/charts/apple_s/ng.html'
    with urllib.request.urlopen(url) as webPageResponse:
        outputHtml = webPageResponse.read()
    beaut = BeautifulSoup(outputHtml, 'lxml')
    k = beaut.table.tbody.prettify()
    tree = ET.fromstring(k)
    kkk = tree.findall('tr/td')
    k = []
    for listss in kkk:
        if listss:
            kl = listss.find('div').text
            kl = kl.strip()
            print(kl)
            k.append(kl)
    URI = []
    for tracks in k:
        client = SpotifyApi(client_id, client_secret)
        uri = (client.get_uri(query=f"{tracks}", search_type='track'))
        URI.append(uri)
        print(uri)
    print(URI)
#test
# get_top_100_ID()


