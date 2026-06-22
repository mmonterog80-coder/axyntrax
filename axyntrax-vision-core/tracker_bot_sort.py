import logging
from typing import Any, Dict, List
import numpy as np
from ultralytics import RTDETR

logger = logging.getLogger(__name__)

class VisionEngine:
    """
    Motor de visión L99 con RT-DETR y BoT-SORT.
    Aplica graceful degradation en caso de restricciones de hardware.
    """
    def __init__(self, model_path: str = "yolov8n.pt", tracker_config: str = "botsort.yaml"):
        import torch
        self.model_path = model_path
        self.tracker_config = tracker_config
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self.model = self._initialize_model()

    def _initialize_model(self) -> RTDETR:
        try:
            logger.info(f"Cargando modelo primario RT-DETR: {self.model_path} en {self.device}")
            model = RTDETR(self.model_path)
            model.to(self.device)
            return model
        except Exception as e:
            logger.warning(f"Fallo en inicialización de modelo primario: {e}. Iniciando Graceful Degradation (CPU/Modelo Ligero).")
            return self._fallback_initialization()

    def _fallback_initialization(self):
        try:
            from ultralytics import YOLO
            self.device = "cpu"
            model = YOLO("yolov8n.pt")  # Modelo ultra-ligero y nativo de Ultralytics
            model.to(self.device)
            logger.info("Fallback YOLOv8 Nano inicializado en CPU exitosamente.")
            return model
        except Exception as e:
            logger.error(f"Fallo crítico durante inicialización de fallback: {e}")
            raise RuntimeError("Fallo total en la inicialización del VisionEngine.")

    def process_frame(self, frame: np.ndarray) -> List[Dict[str, Any]]:
        """Procesa un frame y devuelve detecciones y tracking con BoT-SORT."""
        if frame is None or frame.size == 0:
            return []

        try:
            results = self.model.track(
                source=frame,
                persist=True,
                tracker=self.tracker_config,
                verbose=False,
                device=self.device
            )
            
            detections = []
            for r in results:
                if r.boxes is None or r.boxes.id is None:
                    continue
                
                boxes = r.boxes.xyxy.cpu().numpy()
                track_ids = r.boxes.id.int().cpu().tolist()
                classes = r.boxes.cls.int().cpu().tolist()
                confs = r.boxes.conf.cpu().tolist()
                
                for box, track_id, cls, conf in zip(boxes, track_ids, classes, confs):
                    detections.append({
                        "track_id": track_id,
                        "bbox": [round(coord, 2) for coord in box.tolist()],
                        "class_id": cls,
                        "confidence": round(conf, 4)
                    })
            return detections
        except Exception as e:
            logger.error(f"Fallo en el procesamiento del frame: {e}")
            return []
