FROM python:3.10-alpine

WORKDIR app/

RUN pip install --upgrade pip
COPY . .
RUN pip install -r requirements.txt

COPY . app/
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
