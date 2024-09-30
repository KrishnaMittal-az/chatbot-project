import os
import requests
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
# from dotenv import load_dotenv

# Load environment variables from .env file
# load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# LinkedIn API credentials from .env file
CLIENT_ID = '86i1rub9y5tlhf'
CLIENT_SECRET = 'WPL_AP1.8UjVZKGbohZrBO0K.dpONeA=='
REDIRECT_URI = 'https://www.linkedin.com/developers/tools/oauth/redirect'
STATE = "random_generated_string"  # For CSRF protection

# LinkedIn OAuth endpoints
AUTH_URL = "https://www.linkedin.com/oauth/v2/authorization"
TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"
POST_URL = "https://api.linkedin.com/v2/ugcPosts"

# Global access token
access_token = 'AQUOAaN9O1WCCAERdt2YkALsNaMzfRp-DvP2e2zZ6teh9LeS0DY-2vE4YRwTqvCnuKoH570Q65cQ3-OdASS2GSizpklU1D_1xVr0WuLG2k_D-GFL5jzHXd42efscTQKkMawGW3CYAi2hlzJFd5Qoblg4jGG471gnBU-DhfmHS1pCf7NI8c3HtoJWFqbepoZUkiwpjxl5uIJzjosP45yGjiFcU4eHCYLB0C1VmP3QwT365TVwFycLvUA5WKels9Tgiy9kPdbZ2zwCU9ebgE3vIiTdDDd2pv_2xZrFq3iV7OtUlO75T4DkjhPbIN5eQDvIegLn1znB0727m9RE4vLigccwYltyNA'

# Step 1: Redirect user to LinkedIn for authorization
@app.get("/linkedin/login")
def linkedin_login():
    authorization_url = (
        f"{AUTH_URL}?response_type=code"
        f"&client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&state={STATE}"
        f"&scope=w_member_social"
    )
    return RedirectResponse(url=authorization_url)

# Step 2: LinkedIn callback to handle the authorization code
@app.get("/linkedin/callback")
def linkedin_callback(request: Request, code: str, state: str):
    if state != STATE:
        return "Invalid state, CSRF attack?"

    # Step 3: Exchange authorization code for access token
    token_response = requests.post(
        TOKEN_URL,
        data={
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        },
        headers={'Content-Type': 'application/x-www-form-urlencoded'}
    )

    token_json = token_response.json()
    global access_token
    access_token = token_json['access_token']

    return templates.TemplateResponse("post.html", {"request": request})

# Step 4: Post to LinkedIn using the access token
@app.post("/linkedin/post")
def post_to_linkedin(request: Request):
    post_content = {
        "author": "urn:li:person:YOUR_PERSON_URN",  # Replace with the authenticated user's URN
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": "This is an automated post from my LinkedIn bot!"
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    post_response = requests.post(POST_URL, headers=headers, json=post_content)

    if post_response.status_code == 201:
        return {"status": "Success", "message": "Post was successfully created!"}
    else:
        return {"status": "Failed", "message": post_response.json()}

# Serve the LinkedIn login page
@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

if _name_ == "_main_":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)