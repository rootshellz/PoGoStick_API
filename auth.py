# -*- coding: utf-8 -*-

# Imports
import re
import sys
import json
from collections import OrderedDict

# Project Imports
import config
from session import session

ptc_login_url = "https://sso.pokemon.com/sso/oauth2.0/authorize?client_id=mobile-app_pokemon-go&redirect_uri=https%3A%2F%2Fwww.nianticlabs.com%2Fpokemongo%2Ferror"
ptc_oauth_url = 'https://sso.pokemon.com/sso/oauth2.0/accessToken'

google_oauth_url = "https://accounts.google.com/o/oauth2/auth?client_id=848232511240-73ri3t7plvk96pj4f85uj8otdat2alem.apps.googleusercontent.com&redirect_uri=urn%3Aietf%3Awg%3Aoauth%3A2.0%3Aoob&response_type=code&scope=openid%20email%20https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email"
google_login_url = "https://accounts.google.com/AccountLoginInfo"
google_challenge_url = "https://accounts.google.com/signin/challenge/sl/password"
google_token_url = "https://accounts.google.com/o/oauth2/token"


def authenticate(username, password, auth_type):
    access_token = None
    if auth_type == "Google":
        print("[.] Attempting to log in with your Google Account")
        access_token = auth_with_google(username, password)
    else:
        print("[.] Attempting to log in with your Pokemon Trainer Club Account")
        access_token = auth_with_ptc(username, password)

    if access_token:
        print("[.] Successfully logged in with your %s account" % auth_type)
        config.account_type = auth_type.lower()
        return access_token
    else:
        print("[*] Could not log in with %s account: %s.  Check username and password.\n" % (auth_type, username))
        sys.exit(-1)


def auth_with_google(username, password):
    try:
        headers = {'User-Agent': config.mobile_UA}
        response = session.get(google_oauth_url, headers=headers)

        GALX = re.search('<input type="hidden" name="GALX" value=".*">', response.content)
        GALX = re.sub('.*value="', '', GALX.group(0))
        GALX = re.sub('".*', '', GALX)

        gxf = re.search('<input type="hidden" name="gxf" value=".*:.*">', response.content)
        gxf = re.sub('.*value="', '', gxf.group(0))
        gxf = re.sub('".*', '', gxf)

        cont = re.search('<input type="hidden" name="continue" value=".*">', response.content)
        cont = re.sub('.*value="', '', cont.group(0))
        cont = re.sub('".*', '', cont)

        data = {'Page': 'PasswordSeparationSignIn',
                'GALX': GALX,
                'gxf': gxf,
                'continue': cont,
                'ltmpl': 'embedded',
                'scc': '1',
                'sarp': '1',
                'oauth': '1',
                'ProfileInformation': '',
                '_utf8': '?',
                'bgresponse': 'js_disabled',
                'Email': username,
                'signIn': 'Next'}
        response = session.post(google_login_url, data=data)

        profile = re.search('<input id="profile-information" name="ProfileInformation" type="hidden" value=".*">',
                            response.content)
        profile = re.sub('.*value="', '', profile.group(0))
        profile = re.sub('".*', '', profile)

        gxf = re.search('<input type="hidden" name="gxf" value=".*:.*">', response.content)
        gxf = re.sub('.*value="', '', gxf.group(0))
        gxf = re.sub('".*', '', gxf)

        data = {'Page': 'PasswordSeparationSignIn',
                'GALX': GALX,
                'gxf': gxf,
                'continue': cont,
                'ltmpl': 'embedded',
                'scc': '1',
                'sarp': '1',
                'oauth': '1',
                'ProfileInformation': profile,
                '_utf8': '?',
                'bgresponse': 'js_disabled',
                'Email': username,
                'Passwd': password,
                'signIn': 'Sign in',
                'PersistentCookie': 'yes'}
        response = session.post(google_challenge_url, data=data)

        google_oauth_url_two = response.history[len(response.history)-1].headers['Location'].replace('amp%3B', '').replace('amp;', '')
        response = session.get(google_oauth_url_two)

        client_id = re.search('client_id=.*&from_login', google_oauth_url_two)
        client_id = re.sub('.*_id=', '', client_id.group(0))
        client_id = re.sub('&from.*', '', client_id)

        state_wrapper = re.search('<input id="state_wrapper" type="hidden" name="state_wrapper" value=".*">',
                                  response.content)
        state_wrapper = re.sub('.*state_wrapper" value="', '', state_wrapper.group(0))
        state_wrapper = re.sub('"><input type="hidden" .*', '', state_wrapper)

        connect_approve = re.search('<form id="connect-approve" action=".*" method="POST" style="display: inline;">',
                                    response.content)
        connect_approve = re.sub('.*action="', '', connect_approve.group(0))
        connect_approve = re.sub('" me.*', '', connect_approve)

        data = OrderedDict([('bgresponse', 'js_disabled'), ('_utf8', '☃'), ('state_wrapper', state_wrapper),
                             ('submit_access', 'true')])
        response = session.post(connect_approve.replace('amp;', ''), data=data)

        code = re.search('<input id="code" type="text" readonly="readonly" value=".*" style=".*" onclick=".*;" />',
                         response.content)
        code = re.sub('.*value="', '', code.group(0))
        code = re.sub('" style.*', '', code)

        data = {'client_id': client_id,
                'client_secret': 'NCjF1TLi2CcY6t5mt0ZveuL7',
                'code': code,
                'grant_type': 'authorization_code',
                'redirect_uri': 'urn:ietf:wg:oauth:2.0:oob',
                'scope': 'openid email https://www.googleapis.com/auth/userinfo.email'}
        response = session.post(google_token_url, data=data)

        jdata = json.loads(response.content)
        access_token = jdata['id_token']
        return access_token

    except Exception as error:
        if config.debug:
            print("[+] Failed Google Auth:", error)
        return None


def auth_with_ptc(username, password):
    try:
        headers = {'User-Agent': config.mobile_UA}
        response = session.get(ptc_login_url, headers=headers)
        jdata = json.loads(response.content)

        ptc_url_two = response.history[0].headers['Location']
        data = OrderedDict(
            [('lt', jdata['lt']), ('execution', jdata['execution']), ('_eventId', 'submit'), ('username', username),
             ('password', password)])

        response = session.post(ptc_url_two, data=data, headers=headers, allow_redirects=False)
        if 'errors' in response.content:
            print(json.loads(response.content)['errors'][0].replace('&#039;', '\''))
            return None
        raw_ticket = response.headers['Location']
        ticket = re.sub('.*ticket=', '', raw_ticket)

        data = OrderedDict(
            [('client_id', 'mobile-app_pokemon-go'), ('redirect_uri', 'https://www.nianticlabs.com/pokemongo/error'),
             ('client_secret', 'w8ScCUXJQc6kXKw8FiOhd8Fixzht18Dq3PEVkUCP5ZPxtgyWsbTvWHFLm2wNY0JR'),
             ('grant_type', 'refresh_token'), ('code', ticket)])

        response = session.post(ptc_oauth_url, data=data)
        raw_token = re.sub('.*en=', '', response.content)
        access_token = re.sub('.com.*', '.com', raw_token)
        return access_token

    except Exception as error:
        if config.debug:
            print("[+] Failed Pokemon Trainer Club Auth:", error)
        return None
