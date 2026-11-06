from datetime import datetime, timezone

from sqlmodel import Field, Relationship, SQLModel


class Videos(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    titulo: str
    descripcion: str
    categoria: str
    source: str
    miniatura: str
    es_publico: bool = True

    comentarios: list["Comments"] = Relationship(back_populates="video")


class VideosCreate(SQLModel):
    titulo: str
    descripcion: str
    categoria: str
    source: str
    miniatura: str
    es_publico: bool = True


class Comments(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    autor: str
    texto: str
    fecha: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    video_id: int = Field(foreign_key="videos.id")

    video: Videos | None = Relationship(back_populates="comentarios")


class CommentsCreate(SQLModel):
    autor: str
    texto: str
