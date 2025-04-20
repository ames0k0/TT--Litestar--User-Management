FROM python:3.12.10-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /code

RUN pip3 install "poetry==2.0.1"
RUN poetry config virtualenvs.create false
COPY poetry.lock pyproject.toml /code/
RUN poetry install

COPY . .

EXPOSE 8000

RUN chmod +x ./scripts/db_upgrade.sh
ENTRYPOINT ["./scripts/db_upgrade.sh"]

CMD ["poetry", "run", "litestar", "--app", "main:app", "run", "--host", "0.0.0.0"]
