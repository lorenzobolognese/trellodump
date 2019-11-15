#-------------------------------------------------------------------------------
# Name:        trelloauth
# Purpose:
#
# Author:      Lorenzo Bolognese
#
# Created:     11/11/2019
# Copyright:   (c) Lorenzo Bolognese 2019
# Licence:     MIT License
#-------------------------------------------------------------------------------

import os
from requests_oauthlib import OAuth1Session
import webbrowser

REQUEST_TOKEN_URL = 'https://trello.com/1/OAuthGetRequestToken'
AUTHORIZE_URL = 'https://trello.com/1/OAuthAuthorizeToken'
ACCESS_TOKEN_URL = 'https://trello.com/1/OAuthGetAccessToken'

def CreateOauthToken(expiration="30days", scope='read,write', key=None, secret=None, name='trellodump', output=True):
    """
    Script to obtain an OAuth token from Trello. More info on token scope here:
        https://trello.com/docs/gettingstarted/#getting-a-token-from-a-user
    """

    # Step 1: Get a request token. This is a temporary token that is used for
    # having the user authorize an access token and to sign the request to obtain
    # said access token

    session = OAuth1Session(client_key=key, client_secret=secret)
    response = session.fetch_request_token(REQUEST_TOKEN_URL)
    resourceOwnerKey, resourceOwnerSecret = response.get('oauth_token'), response.get('oauth_token_secret')

    if output:
        print("Request Token:")
        print("    - oauth_token        = %s" % resourceOwnerKey)
        print("    - oauth_token_secret = %s" % resourceOwnerSecret)
        print("")

    # Step 2: Redirect to the provider

    url = ("{authorize_url}?oauth_token={oauth_token}&scope={scope}&expiration={expiration}&name={name}".format(
        authorize_url=AUTHORIZE_URL,
        oauth_token=resourceOwnerKey,
        expiration=expiration,
        scope=scope,
        name=name))
    webbrowser.open(url)

    # After the user has granted access to you, the consumer, the provider will
    # redirect you to whatever URL you have told them to redirect to. You can
    # usually define this in the oauth_callback argument as well

    oauthVerifier = input('What is the PIN? ')

    # Step 3: Once the consumer has redirected the user back to the oauth_callback
    # URL you can request the access token the user has approved. You use the
    # request token to sign this request. After this is done you throw away the
    # request token and use the access token returned

    session = OAuth1Session(client_key=key, client_secret=secret,
                            resource_owner_key=resourceOwnerKey, resource_owner_secret=resourceOwnerSecret,
                            verifier=oauthVerifier)
    accessToken = session.fetch_access_token(ACCESS_TOKEN_URL)

    if output:
        print("Access Token:")
        print("    - oauth_token        = %s" % accessToken['oauth_token'])
        print("    - oauth_token_secret = %s" % accessToken['oauth_token_secret'])
        print("")
        print("You may now access protected resources using the access tokens above.")
        print("")

    return accessToken

if __name__ == '__main__':
    pass