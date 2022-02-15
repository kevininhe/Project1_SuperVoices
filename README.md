# Project1_SuperVoices

Una vez clonado el archivo se debe hacer lo siguiente:

1. Crear un entorno virtual usando python3 -m venv <nombre_proyecto>
2. Activar el entorno usando source <nombre_proyecto>/bin/activate
3. Instalar las siguientes librerías:
  - pip3 install flask
  - pip3 install flask-sqlalchemy
  - pip3 install wheel
  - pip3 install flask-apscheduler 
  - pip3 install flask-mail
  - pip3 install celery
  - pip3 install flask-login
  - pip3 install pymysql
4. Instalar ffmpeg
  - sudo apt update
  - sudo apt install ffmpeg
4. Instalar Redis, y habilitarlo para que sea ejecutado al iniciar la máquina
  - sudo apt-get install redis-server
  - sudo systemctl enable redis-server.service
5. Validar el estado de ejecución de Redis
  - sudo systemctl status redis
6. Instalar la librería de redis y ffmpeg
  - pip3 install redis
  - pip install ffmpeg

Para ejecutar la aplicación se debe hacer lo siguiente:
1. Ejecutar la instancia de Celery
  - celery -A app.celery worker -l info
2. Ejecutar app.py
  - python3 app.py

# Dejar Celery como ejecutable

https://docs.celeryproject.org/en/stable/userguide/daemonizing.html#daemon-systemd-generic

Celery.service
User:ky.infante3022
Borrar el “Group”
Ruta donde se encuentra la aplicación:
WorkingDirectory=/home/ky.infante3022/Project1/Back/Project1_SuperVoices

conf.d celery
Ruta proyecto virtual:
CELERY_BIN=/home/ky.infante3022/Project1/Back/voices_project/bin/celery
Ruta aplicación:
CELERY_APP="app.celery”

Crear las carpetas /var/run/celery/ y /var/log/celery/

Darle permisos de ejecución al usuario
chown -R celery:celery /var/log/celery/
chown -R celery:celery /var/run/celery/
