python -m venv <nombre-env> (crear env)
.\<nombre-env>\Scripts\activate (activar environment)
pip install -r requirements.txt (instalar dependencias)
python .\manage.py runserver

Poblar bd
python .\manage.py makemigrations
python .\manage.py migrate
correr load_stops.py
