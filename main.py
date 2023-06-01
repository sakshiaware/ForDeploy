from fastapi import File, UploadFile
from fastapi.responses import FileResponse
from fastapi import FastAPI
import cv2
import sys
sys.path.append("mrcnn")
from m_rcnn import *

 
app = FastAPI()

@app.post("/upload")
def upload(file: UploadFile = File(...)):
    try:
        contents = file.file.read()
        with open(file.filename, 'wb') as f:
            f.write(contents)
    except Exception as e:
        
        return {"message": "There was an error uploading the file {e}"}
    finally:
        file.file.close()
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

    

    return {"area": f" {area} cm"}
