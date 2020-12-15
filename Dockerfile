FROM python:3.8-slim

RUN apt-get update && \
    apt-get install -y apt-transport-https curl gcc git  python3-software-properties sudo unzip wget

COPY requirements.txt /tmp/requirements.txt
RUN pip install --ignore-installed --no-cache -r /tmp/requirements.txt && \
    rm /tmp/requirements.txt

RUN useradd -m user -u 1000 && \
    echo 'user:user' | chpasswd user && \
    echo "user ALL=(root) NOPASSWD:ALL" > /etc/sudoers.d/user && \
    chmod 0440 /etc/sudoers.d/user && \
    chown -R user /home
USER user

RUN sudo jupyter contrib nbextension install && \
    jupyter nbextension enable toc2/main

ARG GIT_CONFIG_USER_NAME
ARG GIT_CONFIG_EMAIL
RUN git config --global user.name $GIT_CONFIG_USER_NAME && \
    git config --global user.email $GIT_CONFIG_EMAIL

WORKDIR /home/mlflow-1-tracking

CMD jupyter-notebook --ip=0.0.0.0 --port 8888 --no-browser --allow-root --NotebookApp.token='' & \
    mlflow server --host=0.0.0.0
