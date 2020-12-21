import os
from face_util import *
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.responses import JSONResponse
import uvicorn
import io
from starlette.config import Config
from starlette.templating import Jinja2Templates
import time

# getting all the templets for the following dir.
templates = Jinja2Templates(directory="templates")


async def image_Recognition_upload_page(request):
    if request.method == "POST":
        form = await request.form()
        file = form["image"].file
        start = time.time()
        # processing space.
        model_result = face_rec(file)
        end = time.time()
        if file:
            context = {
                "Model_result": str(model_result),
                "Time_of_execution_in_seconds": str(round(end - start, 3)),
            }
            return JSONResponse(context)
    else:
        return templates.TemplateResponse(
            "Face_recognition.html", {"request": request, "data": ""}
        )


# All the routs of this website.
routes = [
    Route(
        "/Deeplobe.ai-Image-Recognition",
        image_Recognition_upload_page,
        methods=["GET", "POST"],
    ),
]
# App congiguration.
app = Starlette(
    debug=True,
    routes=routes,
)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
