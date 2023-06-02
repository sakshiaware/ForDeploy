from fastapi import FastAPI, File, UploadFile, Response, Header
from pydantic import BaseModel
import numpy as np
import cv2
import werkzeug
from fastapi.middleware.cors import CORSMiddleware
import base64
import aiofiles
from fastapi.responses import FileResponse
from fastapi import FastAPI
import cv2
import sys
sys.path.append("mrcnn")
from m_rcnn import *
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.get("/")
# def read_root():
#     return {"Hello": "World"}

@app.post("/calculate-area")
async def calculateArea(file: UploadFile = File(...)):
    imagefile = file
    filename = werkzeug.utils.secure_filename(imagefile.filename)
    print("\nReceived image File name : " + imagefile.filename)
    # imagefile.save(filename)
    async with aiofiles.open(filename, 'wb') as out_file:
        content = await file.read()  # async read
        await out_file.write(content)  # async write
    area = 0
    test_model, inference_config = load_inference_model(1, "mask_rcnn_object_0009.h5")
    img = cv2.imread(file.filename)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = test_model.detect([img_rgb])
    r = results[0]
    area=0
    L_cm=0
    B_cm=0
    BreadthOfBBox=0
    LegthOfBBox=0
    y1, x1, y2, x2 =r['rois'][0]
    BreadthOfBBox=x2-x1
    LegthOfBBox=y2-y1
    L_cm=(LegthOfBBox*90)/2783
    B_cm=(BreadthOfBBox*90)/2996
    area=L_cm*B_cm

    return str(area)

class StringPayload(BaseModel):
    string: str
@app.post("/")
async def calculateArea(image: StringPayload):
    decoded_data = base64.b64decode(image.string)
    with open("pothole.png", "wb") as fh:
        fh.write(decoded_data)
    img = cv2.imread('pothole.png')
    # filename = werkzeug.utils.secure_filename(imagefile.filename)
    # print("\nReceived image File name : " + imagefile.filename)
    # imagefile.save(filename)
    area = 0
    test_model, inference_config = load_inference_model(1, "mask_rcnn_object_0009.h5")
    img = cv2.imread(file.filename)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = test_model.detect([img_rgb])
    r = results[0]
    area=0
    L_cm=0
    B_cm=0
    BreadthOfBBox=0
    LegthOfBBox=0
    y1, x1, y2, x2 =r['rois'][0]
    BreadthOfBBox=x2-x1
    LegthOfBBox=y2-y1
    L_cm=(LegthOfBBox*90)/2783
    B_cm=(BreadthOfBBox*90)/2996
    area=L_cm*B_cm

    return str(area)

# if __name__ == '__main__':
#     uvicorn.run(  app, port=5000)
