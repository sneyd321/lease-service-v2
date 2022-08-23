FROM python:3.10

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV DB_HOST=host.docker.internal
ENV DB_DATABASE=roomr
ENV DB_USER=root
ENV DB_PASS=root

ENV NAMESPACE=prod

CMD ["python", "./main.py"]
#CMD exec gunicorn --bind :8080 --workers 1 --threads 8 --timeout 0 app:app

