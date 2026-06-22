import os
import cv2
import numpy as np
import logging
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn

from tracker_bot_sort import VisionEngine

# Hardware Acceleration / NVDEC Conceptual Configuration
os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "video_codec;h264_cuvid"
os.environ["CUDA_MODULE_LOADING"] = "LAZY"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("AxyntraxVisionCore")

app = FastAPI(title="Axyntrax Vision Core L99", version="1.0.0")
engine = VisionEngine()

@app.on_event("startup")
async def startup_event():
    logger.info("Iniciando Axyntrax Vision Core con pipeline optimizado por NVDEC (Conceptual).")

@app.websocket("/ws/stream")
async def stream_endpoint(websocket: WebSocket):
    await websocket.accept()
    logger.info(f"Cliente WebSocket conectado: {websocket.client}")
    
    try:
        while True:
            data = await websocket.receive_bytes()
            
            # NVDEC decodifica conceptualmente vía hardware
            np_arr = np.frombuffer(data, np.uint8)
            frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            
            if frame is None:
                await websocket.send_json({"error": "Payload de frame inválido."})
                continue
                
            detections = engine.process_frame(frame)
            
            await websocket.send_json({
                "status": "success",
                "detections": detections
            })
    except WebSocketDisconnect:
        logger.info("Cliente WebSocket desconectado limpiamente.")
    except Exception as e:
        logger.error(f"Error en flujo WebSocket: {e}")
        try:
            await websocket.close()
        except:
            pass

if __name__ == "__main__":
    uvicorn.run("vision_server:app", host="0.0.0.0", port=8000, workers=1)
