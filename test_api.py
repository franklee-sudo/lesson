import urllib.request
import urllib.error
import json

API_KEY = "sk-3b1d8f0e52a3433ca61747c40221924a"
API_URL = "https://api.deepseek.com/chat/completions"

payload = {
    "model": "deepseek-chat",
    "messages": [
        {"role": "user", "content": "Hello"}
    ],
    "stream": False
}

try:
    req = urllib.request.Request(API_URL, data=json.dumps(payload).encode('utf-8'), headers={
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}'
    })
    with urllib.request.urlopen(req) as response:
        print(response.read().decode('utf-8'))
except urllib.error.HTTPError as e:
    print(f"HTTP Error: {e.code} {e.reason}")
    print(e.read().decode('utf-8'))
except Exception as e:
    print(f"Error: {e}")
