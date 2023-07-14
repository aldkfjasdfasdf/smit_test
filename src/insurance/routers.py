from fastapi import APIRouter
from fastapi.params import Body, Query
from decimal import Decimal

from .models import Rate

router = APIRouter()


@router.post("/rates")
async def create_or_update_rates(data: dict = Body(..., example={
    "2020-06-01": [
        {
            "cargo_type": "Glass",
            "rate": "0.04"
        },
        {
            "cargo_type": "Other",
            "rate": "0.01"
        }
    ],
    "2020-07-01": [
        {
            "cargo_type": "Glass",
            "rate": "0.035"
        },
        {
            "cargo_type": "Other",
            "rate": "0.015"
        }
    ]
})):
    for date, rates in data.items():
        for rate_data in rates:
            cargo_type = rate_data["cargo_type"]
            rate = rate_data["rate"]

            rate_obj = await Rate.filter(date=date, cargo_type=cargo_type).first()
            if rate_obj:
                rate_obj.rate = rate
                await rate_obj.save()
            else:
                await Rate.create(date=date, cargo_type=cargo_type, rate=rate)

    return {"message": "Данные успешно добавлены"}


@router.get("/calculate_price")
async def calculate_price(
    date: str = Query(..., description="Дата в формате ГГГГ-ММ-ДД"),
    cargo_type: str = Query(..., description="Тип груза"),
    declared_price: Decimal = Query(..., description="Объявленная стоимость груза"),
):
    rate_obj = await Rate.filter(date=date, cargo_type=cargo_type).first()
    if rate_obj:
        rate = rate_obj.rate
        calculated_price = declared_price * rate
        return {"calculated_price": calculated_price}
    else:
        return {"message": "Данные по данной дате или типу не найдены"}