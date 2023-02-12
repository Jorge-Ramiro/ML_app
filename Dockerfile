FROM tensorflow/tensorflow
COPY ./app /app
WORKDIR /app
ADD requirements.txt /app
RUN pip install -r requirements.txt
ENV PORT 8080
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 0 main:app