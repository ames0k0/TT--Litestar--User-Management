FROM python:3.12.10-slim

WORKDIR /code

COPY poetry.lock pyproject.toml /code/

RUN pip3 install "poetry==2.0.1"
RUN poetry install

COPY . /code/

EXPOSE 8000

CMD ["litestar", "--app", "main:app", "run", "--host", "0.0.0.0"]
