## Inicialización Proyecto
Se debe clonar el repositorio en primer lugar y tener al menos Python 3.12
Posterior a ello, se deben instalar las siguientes dependencias:
```bash
pip install fastapi uvicorn pymongo dotenv
```
Una vez instaladas, se crea una variable de entorno con el string de conexión a MongoDB que coincida con el nombre provisto en main.py
## Ejecutar Proyecto
Para ejecutar el proyecto, se llama al siguiente comando:
```bash
python -m uvicorn main:app --reload
```
Con ello, el API se ejecutará en localhost:8000
