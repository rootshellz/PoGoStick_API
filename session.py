# Imports
import requests

# Project Imports
import config

session = requests.session()
# session.headers.update({'User-Agent':'Niantic App'})

if config.use_proxy:
    session.proxies.update(config.proxies)
    session.verify = False
