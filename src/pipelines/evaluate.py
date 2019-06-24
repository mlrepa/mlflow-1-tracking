import argparse
import joblib
import json
import mlflow
from mlflow import log_artifact, log_metric, log_param
from mlflow.tracking import MlflowClient
import os
from typing import Text
import yaml

from src.data.dataset import get_dataset
from src.evaluate.evaluate import evaluate


def evaluate_model(config_path: Text):

    config = yaml.load(open(config_path), Loader=yaml.FullLoader)

    estimator_name = config['train']['estimator_name']

    target_column = config['featurize']['target_column']
    test_df = get_dataset(config['split_train_test']['test_csv'])
    model_name = config['base']['model']['model_name']
    models_folder = config['base']['model']['models_folder']

    model = joblib.load(os.path.join(models_folder, model_name))

    f1, cm = evaluate(df=test_df,
                      target_column=target_column,
                      clf=model)

    test_report = {
        'f1_score': f1,
        'confusion_matrix': cm.tolist()
    }
    print(test_report)
    filepath = os.path.join(config['base']['experiments']['experiments_folder'],
                            config['evaluate']['metrics_file'])
    json.dump(obj=test_report, fp=open(filepath, 'w'), indent=2)

    # Logging into mlflow
    client = MlflowClient()
    experiments = client.list_experiments()  # returns a list of mlflow.entities.Experiment
    mlflow.set_experiment(estimator_name)
    print(experiments)
    with mlflow.start_run() as run:

        print(run)
        print(run.info)
        print(run.info.run_uuid)

        param_grid = config['train']['estimators'][estimator_name]['param_grid']

        log_param(key='estimator', value=estimator_name)
        log_param(key='cv', value=config['train']['cv'])
        for param, value in param_grid.items():
            log_param(key=param, value=value)

        log_metric(key='f1_score', value=f1)
        log_artifact(local_path='models/model.joblib')

        log_artifact(local_path='src/features/features.py')
        log_artifact(local_path='src/train/train.py')
        log_artifact(local_path='src/pipelines/train.py')



if __name__ == '__main__':
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument('--config', dest='config', required=True)
    args = args_parser.parse_args()

    evaluate_model(config_path=args.config)
