FROM python:3.11.3

ENV PYTHONUNBUFFERED 1

WORKDIR /workspace
RUN apt update
RUN apt install zsh nano -y
RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" -y
RUN echo "zsh" >> ~/.bashrc 

COPY poetry.lock pyproject.toml ./
RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false 

ARG DEV=true
RUN poetry install