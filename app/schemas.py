from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class AdvertisementBase(BaseModel):
    """Базовые поля объявления."""
    title: str = Field(..., min_length=1, description="Заголовок")
    description: str = Field(..., description="Описание")
    price: float = Field(..., ge=0, description="Цена")
    author: str = Field(..., min_length=1, description="Автор")


class AdvertisementCreate(AdvertisementBase):
    """Схема для создания объявления."""
    pass


class AdvertisementUpdate(BaseModel):
    """Схема для частичного обновления объявления (PATCH)."""
    title: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = None
    price: Optional[float] = Field(None, ge=0)
    author: Optional[str] = Field(None, min_length=1)


class AdvertisementResponse(AdvertisementBase):
    """Схема ответа с объявлением."""
    id: UUID
    created_at: datetime

    model_config = {"from_attributes": True}
