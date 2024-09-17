import uvicorn
from fastapi import FastAPI
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from msgsend import send_email
from embeddings import chroma_embedding
from typing import Optional

# Initialize the fast API
app = FastAPI()


headers = {
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "accept": "application/json",
    "sec-ch-ua": '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
}

# Added multiple origins to remove the cors errors which we may encounter later

origins = [
    "http://localhost",
    "http://127.0.0.1",
    "http://localhost:3000",
    "http://192.168.140.47:3000/",
]


# Middleware to pass on the cors error and to check the credentials
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Create the data model to define the data types of the json data we will accept.
class YourDataModel(BaseModel):
    question: str
    username: str
    email_support: Optional[str] = None


@app.post("/postquestion")
async def your_endpoint(your_data: YourDataModel):
    # Access the JSON data within the endpoint
    question = your_data.question
    email_support = your_data.email_support

    # print(username)
    # print(question)
    msg = chroma_embedding(question)
    if email_support != None and len(email_support) != 0:
        send_email(email_support, msg)
    return {"response": msg}


# Driving code of the file.
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
