from fastapi import FastAPI, Query, Body
from fastapi.openapi.docs import (
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
import uvicorn

app = FastAPI(docs_url=None)


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )

hotels = [
    {"id":1, "title":"Sochi", "name": "5star"},
    {"id":2, "title":"Дубай", "name": "Jingle"},
]


@app.get("/hotels")
def get_hotels(
        id: int | None = Query(None, description="Айди отеля"),
        title: str | None = Query(None, description="Название отеля"),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    return hotels_


@app.delete("/hotels/{hotel_id}")
def delete_hotels(
    hotel_id: int,
):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}

@app.post("/hotels")
def create_hotels(
        title: str = Body(embed=True)
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": title
    })
    return {"status": "OK"}

@app.put("/hotels/{hotel_id}")
def edit_hotels_put(
        hotel_id: int,
        title: str = Body(embed=True),
        name: str = Body(embed=True),
):
    hotel_message = None
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = title
            hotel["name"] = name
            hotel_message = hotel
            break
    else:
        return {"status": "ERROR", "message": "No hotel with provided ID"}
    return {"status": "OK", "hotel": hotel_message}


@app.patch("/hotels/{hotel_id}")
def edit_hotels_patch(
        hotel_id: int,
        title: str | None = Body(None, embed=True),
        name: str | None = Body(None, embed=True),
):
    hotel_message = None
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if title:
                hotel["title"] = title
            elif name:
                hotel["name"] = name
            else:
                return {"status": "ERROR", "message": "No data provided"}
            hotel_message = hotel
            break
    else:
        return {"status": "ERROR", "message": "No hotel with provided ID"}
    return {"status": "OK", "hotel": hotel_message}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8005)