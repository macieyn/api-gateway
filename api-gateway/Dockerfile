FROM python:3.8-buster
ADD . . 
ENV FLASK_APP=app
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development
RUN pip install --upgrade pip \ 
    && pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile
EXPOSE 5000
RUN flask init-db

