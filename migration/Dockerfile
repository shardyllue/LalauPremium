FROM python:3.10

WORKDIR /app

COPY . .

RUN pip3 install --upgrade setuptools

RUN pip3 install -r ./requirements.txt

RUN mkdir ./migrations/versions

RUN alembic revision --autogenerate -m "Creating table"

RUN alembic upgarde head

RUN chmod 755 .
