# Tumblr API Example - Python CLI
# https://gist.github.com/140am/8573840

import oauth2
import urlparse
import pytumblr

REQUEST_TOKEN_URL = 'http://www.tumblr.com/oauth/request_token'
AUTHORIZATION_URL = 'http://www.tumblr.com/oauth/authorize'
ACCESS_TOKEN_URL = 'http://www.tumblr.com/oauth/access_token'
CONSUMER_KEY = 'LGHFZEDgic6GqcUMSFp1BNfuWMgQVMNviB4U6BmvlgY04x0UBw'
CONSUMER_SECRET = 'TvUvbFAxOaMCKCelAemEUrQno6CZ2bwgT9ExIJfEaE1qN7p1In'

consumer = oauth2.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
client = oauth2.Client(consumer)

resp, content = client.request(REQUEST_TOKEN_URL, "GET")

request_token = dict(urlparse.parse_qsl(content))
OAUTH_TOKEN = request_token['oauth_token']
OAUTH_TOKEN_SECRET = request_token['oauth_token_secret']

print("Request Token:")
print("    - oauth_token        = %s") % OAUTH_TOKEN
print("    - oauth_token_secret = %s") % OAUTH_TOKEN_SECRET

client = pytumblr.TumblrRestClient(
    CONSUMER_KEY,
    CONSUMER_SECRET,
    OAUTH_TOKEN,
    OAUTH_TOKEN_SECRET
)

# number of posts
client.blog_info('userX')['blog']['posts']

client.posts('userX', offset=0, limit=10)
