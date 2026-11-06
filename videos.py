import random

from fastapi import APIRouter, HTTPException
from sqlmodel import select

from db import SessionDep
from models import Videos, VideosCreate

router = APIRouter(prefix="/videos")


@router.get("/")
def get_videos(session: SessionDep, categoria: str = ""):
    videos = session.exec(select(Videos)).all()

    if categoria == "":
        return videos

    filtrados = []
    for video in videos:
        if video.categoria == categoria:
            filtrados.append(video)
    return filtrados


@router.get("/categorias")
def get_categorias(session: SessionDep):
    videos = session.exec(select(Videos)).all()

    categorias = []
    for video in videos:
        if video.categoria not in categorias:
            categorias.append(video.categoria)
    return categorias


@router.get("/{video_id}")
def get_video(video_id: int, session: SessionDep):
    video = session.get(Videos, video_id)
    if video is None:
        raise HTTPException(status_code=404, detail="El video no fue encontrado")
    return video


@router.get("/{video_id}/recomendaciones")
def get_recomendaciones(video_id: int, session: SessionDep):
    video_actual = session.get(Videos, video_id)
    if video_actual is None:
        raise HTTPException(status_code=404, detail="El video no fue encontrado")

    videos = session.exec(select(Videos)).all()

    recomendados = []
    for video in videos:
        if video.categoria == video_actual.categoria and video.id != video_actual.id:
            recomendados.append(video)

    random.shuffle(recomendados)
    return recomendados[:10]


@router.post("/")
def create_video(video_data: VideosCreate, session: SessionDep):
    video = Videos.model_validate(video_data)
    session.add(video)
    session.commit()
    session.refresh(video)
    return video
