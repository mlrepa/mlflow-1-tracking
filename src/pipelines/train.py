import argparse
import os
from typing import Text

import joblib
import yaml

from src.data.dataset import get_dataset
from src.train.train import train


def train_model(config_path: Text):

    config = yaml.load(open(config_path), Loader=yaml.FullLoader)

    estimator_name = config['train']['estimator_name']
    param_grid = config['train']['estimators'][estimator_name]['param_grid']
    cv = config['train']['cv']

    target_column = config['featurize']['target_column']
    train_df = get_dataset(config['split_train_test']['train_csv'])

    model = train(
        df=train_df,
        target_column=target_column,
        estimator_name=estimator_name,
        param_grid=param_grid,
        cv=cv
    )

    print(model.best_score_)

    model_name = config['base']['model']['model_name']
    models_folder = config['base']['model']['models_folder']

    joblib.dump(
        model,
        os.path.join(models_folder, model_name)
    )


if __name__ == '__main__':

    args_parser = argparse.ArgumentParser()
    args_parser.add_argument('--train-config', dest='config', required=True)
    args = args_parser.parse_args()

    train_model(config_path=args.config)

