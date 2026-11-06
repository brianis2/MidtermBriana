from fastapi import APIRouter, HTTPException

from db import SessionDep
from models import Comments, CommentsCreate, Videos

router = APIRouter(prefix="/videos")


@router.get("/{video_id}/comentarios")
def get_comentarios(video_id: int, session: SessionDep):
    video = session.get(Videos, video_id)
    if video is None:
        raise HTTPException(status_code=404, detail="El video no fue encontrado")

    comentarios = video.comentarios
    comentarios.reverse()
    return comentarios


@router.post("/{video_id}/comentarios")
def create_comentario(video_id: int, datos: CommentsCreate, session: SessionDep):
    video = session.get(Videos, video_id)
    if video is None:
        raise HTTPException(status_code=404, detail="El video no fue encontrado")

    comentario = Comments(autor=datos.autor, texto=datos.texto, video_id=video_id)
    session.add(comentario)
    session.commit()
    session.refresh(comentario)
    return comentario
