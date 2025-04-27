import logging
logging.basicConfig(
    filename="hyperion.log",
    format="%(asctime)s %(levelname)s %(message)s",
    level=logging.INFO
)
logging.info("=== Hyperion gestartet ===")

from storage.db import init_db, conn
class Optimizer:
    def __init__(self): 
        init_db()
    
    def optimize(self, module, payload, result):
        conn().execute(
            "INSERT INTO tasks(module, payload, result) VALUES (?,?,?)",
            (module, str(payload), str(result))
        )
        logging.info(f"[Optimizer] Stored task: {module}")
