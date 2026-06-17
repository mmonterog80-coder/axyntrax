import os, time, logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("WorkerEDGE")

def main():
    logger.info("Worker EDGE desactivado temporalmente. No se intenta conexión WebSocket.")
    while True:
        time.sleep(60)

if __name__ == "__main__":
    main()
