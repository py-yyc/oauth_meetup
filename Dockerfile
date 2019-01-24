FROM python:3.7
RUN pip install pipenv
WORKDIR /app
COPY Pipfile Pipfile.lock ./
RUN pipenv install --system --deploy
COPY . ./
EXPOSE 8000
CMD ./manage.py migrate && ./manage.py runserver 0.0.0.0:8000
