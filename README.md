# SchoologyApi
A simple api for automating your schoology account. 
# Requirements
You need to have requests_oauthlib, requests, and json installed
You need a schoology account
# Use
First, you need to get the consumer key and secret. If you are logged into schoology, go to https://app.schoology.com/api and get the key and secret from there.

DO NOT GIVE ANYONE THESE VALUES! These values will allow you to control your account using the api, without requiring your password. If you share these values with anyone, they could gain control of your account.

Since you have the key and secret, you can use the schoology api.
```python
from Schoology import SchoologyConsumer
api = SchoologyConsumer(KEY,SECRET)
api.like_all_updates()
```
