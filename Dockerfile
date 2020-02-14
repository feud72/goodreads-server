FROM python:3 
ENV PYTHONUNBUFFERED 1 
RUN mkdir /code 
WORKDIR /code 
COPY requirements.txt /code/ 
RUN pip install -r requirements.txt 
COPY . /code/ 

ENTRYPOINT ["python", "manage.py"] 
CMD ["runserver", "127.0.0.1:8000"]
