
# Preparation

## Clone this repository

```bash
https://gitlab.com/7labs.ru/tutorials/mlflow-1-tracking

cd mlflow-1-tracking
```

## 2. Create .env file in config/ folder

```bash
GIT_CONFIG_USER_NAME=<git user>
GIT_CONFIG_EMAIL=<git email>
```

example 

```bash
GIT_CONFIG_USER_NAME=mnrozhkov
GIT_CONFIG_EMAIL=mnrozhkov@gmail.com
```

## Get data

Download iris.csv

```bash
wget -P data/raw/ -nc https://raw.githubusercontent.com/uiuc-cse/data-fa14/gh-pages/data/iris.csv
```         

## Build image

```bash
ln -sf config/.env && docker-compose build
```


## Run container
```bash
docker-compose up
```

# Start tutorial

## Open JupyterLab

```bash
http://0.0.0.0:8888
```

## Open mlflow ui

```bash
http://0.0.0.0:5000
```
    
