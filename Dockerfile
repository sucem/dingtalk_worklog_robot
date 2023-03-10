FROM python:3.10

ENV POETRY_VER=1.3.2

RUN mkdir -p /log-record/log_record
RUN mkdir data

WORKDIR /log-record

RUN pip install poetry==${POETRY_VER} -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN poetry config virtualenvs.create false

COPY log_record /log-record/log_record
COPY pyproject.toml /log-record/
COPY README.md /log-record/

RUN poetry install --only main 

ENTRYPOINT [ "uvicorn", "--host", "0.0.0.0", "--port", "8080", "log_record.api.main:app" ]