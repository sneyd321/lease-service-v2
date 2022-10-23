FROM python:3.8-slim

WORKDIR /usr/src/app

COPY requirements.txt requirements.txt

RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV DB_HOST=host.docker.internal
ENV DB_DATABASE=roomr
ENV DB_USER=root
ENV DB_PASS=root

ENV PORT=$PORT

#CMD python main.py
CMD exec uvicorn main:app --host 0.0.0.0 --port $PORT

