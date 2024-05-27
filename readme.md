python -m venv <nombre-env> (crear env)
.\<nombre-env>\Scripts\activate (activar environment)
pip install -r requirements.txt (instalar dependencias)
uvicorn bustime.asgi:application --port 8000 --reload (correr servidor, de manera que se actualice automaticamente con los cambios)

Poblar bd
python .\manage.py makemigrations
python .\manage.py migrate
correr load_stops.py

