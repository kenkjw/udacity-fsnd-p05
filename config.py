import json

with open('config.json','r') as f:
    _config = json.load(f)

oauth = _config['oauth']
secret_key = _config['secret_key']
