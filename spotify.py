import requests
import json
import urllib.parse
import time
from secrets import *
from tokenfile import *

class Spotify(Secrets):
    """Main class for the module.

    Attributes:
        redirectURI -- A local address that the main module listens to, the address must be 
                       added to the redirect addresses of the app at Spotify Developers Console
        searchLimit -- The number of results to return for a seach
    """

    port = 8080
    __redirectURI = "http://localhost:" + str(port) + "/tokenize/"
    __searchLimit = 10
    __t = TokenFile()

    def auth(self):
        """Returns the authorization URL for Spotify.
        """
        url = "https://accounts.spotify.com/authorize"
        params = {'client_id': self._clientID, 'response_type': 'code', 'redirect_uri': self.__redirectURI}
        p = urllib.parse.urlencode(params)
        return url + "?" + p

    def getTokens(self, code):
        """Gets the authorization token and the refresh token from a 'Code' response.
        If successful, writes the tokens to the token file. 
        Returns boolean.
        """
        url = "https://accounts.spotify.com/api/token"
        params = {'grant_type': 'authorization_code', 
                  'code': code, 
                  'redirect_uri': self.__redirectURI, 
                  'client_id': self._clientID, 
                  'client_secret': self._clientSecret}
        r = requests.post(url, params)
        page = r.content
        items = json.loads(page)
        if 'error' in items:
            return False
        else :
            access_token = items['access_token']
            expires_in = items['expires_in']
            expiry = expires_in + time.time()
            refresh_token = items['refresh_token']
            scope = items['scope']
            token_type = items['token_type']
            self.__t.writeTokenFile((access_token, expires_in, expiry, refresh_token, scope, token_type))
            return True

    def renewTokens(self):
        """Renews the authorization token using the refresh token.
        If successful, writes the new token to the token file.
        Returns boolean.
        """
        if self.__t.tokenFileExists() and self.__t.readTokenFile():
            tokenData = self.__t.readTokenFile()
            refresh_token = tokenData[3]
            url = "https://accounts.spotify.com/api/token"
            params = {'grant_type': 'refresh_token', 
                      'refresh_token': refresh_token, 
                      'client_id': self._clientID, 
                      'client_secret': self._clientSecret}
            r = requests.post(url, params)
            page = r.content
            items = json.loads(page)

            if 'error' in items:
                return False
            else :
                access_token = items['access_token']
                expires_in = items['expires_in']
                expiry = expires_in + time.time()
                scope = items['scope']
                token_type = items['token_type']
                self.__t.writeTokenFile((access_token, expires_in, expiry, refresh_token, scope, token_type))
                return True
        else :
            return False

    def checkTokenFile(self):
        """Checks if the token file exists and is valid.
        Refreshes token if possible.
        Returns boolean.
        """
        if self.__t.tokenFileExists() and self.__t.readTokenFile():
            tokenFile = self.__t.readTokenFile()
            expiry = tokenFile[2]
            if time.time() < float(expiry):
                return True
            else:
                return self.renewTokens()
        else :
            return False
            

    def search(self, term):
        """Searches for the given term.
        Returns nested list of results with the following order:
            (Artists, Song Name, URL, URI)
        """
        if self.checkTokenFile() is True:
            accessToken = self.__t.readTokenFile()[0]
            searchURL =  "https://api.spotify.com/v1/search"
            headers = {'Accept': 'application/json', 
                       'Content-Type': 'application/json', 
                       'Authorization': 'Bearer ' + accessToken}
            params = {'type': 'track',
                      'market': 'TR',
                      'limit': self.__searchLimit}
            params['q'] = term
            r = requests.get(searchURL, params=params, headers=headers)
            page = r.content
            items = json.loads(page)
            items = items['tracks']
            if items['total'] > 0 :
                loopcount = items['total']
                if items['total'] >= self.__searchLimit:
                    loopcount = self.__searchLimit                
                items = items['items']
                res = []
                for i in range(loopcount):
                    item = items[i]
                    artist = [a['name'] for a in item['artists']]
                    artists = ', '.join(artist)
                    url = item['external_urls']['spotify']
                    uri = item['uri']
                    name = item['name']
                    # print("%s - %s - %s - %s" % (artists, name, url, uri))
                    res.append((artists, name, url, uri))
                return res
            else :
                return None
        else :
            return "Token renewal mistake - check permissions"
