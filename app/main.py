from uuid import UUID

from fastapi import FastAPI, HTTPException, Query

from app.schemas import (
    AdvertisementCreate,
    AdvertisementUpdate,
    AdvertisementResponse,
)
from app import storage

app = FastAPI(
    title="Сервис объявлений",
    description="REST API для объявлений купли/продажи",
    version="1.0.0",
)


@app.post("/advertisement", response_model=AdvertisementResponse)
def create_advertisement(ad: AdvertisementCreate) -> AdvertisementResponse:
    """Создание объявления."""
    return storage.create(ad)


@app.get(
    "/advertisement/{advertisement_id}",
    response_model=AdvertisementResponse,
)
def get_advertisement(advertisement_id: UUID) -> AdvertisementResponse:
    """Получение объявления по id."""
    ad = storage.get_by_id(advertisement_id)
    if ad is None:
        raise HTTPException(status_code=404, detail="Объявление не найдено")
    return ad


@app.patch(
    "/advertisement/{advertisement_id}",
    response_model=AdvertisementResponse,
)
def update_advertisement(
    advertisement_id: UUID, data: AdvertisementUpdate
) -> AdvertisementResponse:
    """Частичное обновление объявления (PATCH)."""
    ad = storage.update(advertisement_id, data)
    if ad is None:
        raise HTTPException(status_code=404, detail="Объявление не найдено")
    return ad


@app.delete("/advertisement/{advertisement_id}", status_code=204)
def delete_advertisement(advertisement_id: UUID) -> None:
    """Удаление объявления."""
    if not storage.delete(advertisement_id):
        raise HTTPException(status_code=404, detail="Объявление не найдено")


@app.get("/advertisement", response_model=list[AdvertisementResponse])
def search_advertisements(
    title: str | None = Query(None, description="Поиск по заголовку"),
    description: str | None = Query(None, description="Поиск по описанию"),
    price_min: float | None = Query(None, ge=0, description="Мин. цена"),
    price_max: float | None = Query(None, ge=0, description="Макс. цена"),
    author: str | None = Query(None, description="Поиск по автору"),
) -> list[AdvertisementResponse]:
    """Поиск объявлений по полям. Все параметры опциональны (query string)."""
    return storage.search(
        title=title,
        description=description,
        price_min=price_min,
        price_max=price_max,
        author=author,
    )
