from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import comments, videos
from db import create_all_table

app = FastAPI(lifespan=create_all_table)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(videos.router)
app.include_router(comments.router)


@app.get("/")
def root():
    return {"hello": "world"}
