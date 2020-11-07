FROM python:3.8.3-alpine

WORKDIR /app

COPY . .

RUN \
 apk add --no-cache bash && \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 pip install --upgrade pip && \
 pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps

CMD ["gunicorn", "RestAdviserBack.wsgi:application", "--bind", "0.0.0.0:8000"]
