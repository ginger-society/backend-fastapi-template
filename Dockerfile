FROM python:3.11.3

ENV PYTHONUNBUFFERED 1
ENV env dev
WORKDIR /app
ADD . /app
COPY requirements.txt /app/requirements.txt
EXPOSE 80

RUN apt update
# RUN pre-commit
RUN apt install git zsh curl nano wget -y
RUN apt install git zsh curl nano make gcc wget build-essential procps -y
RUN pip install --upgrade setuptools wheel

RUN pip install -r requirements.txt

RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" -y
RUN echo "zsh" >> ~/.bashrc
