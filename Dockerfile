# https://book.st-hakky.com/docs/try-poetry-on-docker/
FROM python:3
RUN apt-get update &&\
    apt-get -y install locales &&\
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

RUN pip install --upgrade pip

# install poetry
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH /root/.local/bin:$PATH

# setup
COPY ./pyproject.toml* ./poetry.lock* ./
RUN poetry config virtualenvs.create false && \
    poetry install

# start app
WORKDIR /app
CMD ["python3", "disc_pal/main.py"]

