from flask import Flask, render_template, request, redirect
import requests
from bs4 import BeautifulSoup
import json
import os

app = Flask(__name__)
DATA_FILE = 'usernames.json'

def load_usernames():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_usernames(usernames):
    with open(DATA_FILE, 'w') as f:
        json.dump(usernames, f)

def get_follower_count(username):
    url = f"https://www.threads.net/@{username}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            tag = soup.find("meta", property="og:description")
            if tag:
                text = tag['content']
                return text.split(" ")[0]
    except:
        pass
    return "N/A"

@app.route('/', methods=['GET'])
def index():
    usernames = load_usernames()
    followers = {u: get_follower_count(u) for u in usernames}
    return render_template('index.html', followers=followers)

@app.route('/add', methods=['POST'])
def add():
    username = request.form.get('username')
    if username:
        usernames = load_usernames()
        if username not in usernames:
            usernames.append(username)
            save_usernames(usernames)
    return redirect('/')

@app.route('/delete/<username>')
def delete(username):
    usernames = load_usernames()
    if username in usernames:
        usernames.remove(username)
        save_usernames(usernames)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)

