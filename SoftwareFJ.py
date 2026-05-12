
import logging
from abc import ABC, abstractmethod

# Preparar log
logging.basicConfig(
    filename='errores_sistema.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)