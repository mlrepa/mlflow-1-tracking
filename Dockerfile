FROM meisterurian/mlflow-tutorials-base

ARG GIT_CONFIG_USER_NAME
ARG GIT_CONFIG_EMAIL

WORKDIR /home/mlflow-1-tracking

RUN git config --global user.name $GIT_CONFIG_USER_NAME && git config --global user.email $GIT_CONFIG_EMAIL

CMD jupyter lab --ip=0.0.0.0 --no-browser --allow-root --NotebookApp.token='' & mlflow server --host=0.0.0.0
