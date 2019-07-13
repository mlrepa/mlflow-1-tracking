import argparse
from typing import Text

import yaml

from src.data.dataset import get_dataset
from src.transforms.trainsforms import transform_targets_to_numerics, split_dataset_in_train_test


def split_dataset(config_path: Text):

    config = yaml.load(open(config_path), Loader=yaml.FullLoader)

    dataset = get_dataset(config['featurize']['featured_dataset_csv'])
    target_column = config['featurize']['target_column']
    random_state = config['base']['random_state']

    test_size = config['split_train_test']['test_size']
    train_csv_path = config['split_train_test']['train_csv']
    test_csv_path = config['split_train_test']['test_csv']

    dataset = transform_targets_to_numerics(dataset, target_column=target_column)

    train_dataset, test_dataset = split_dataset_in_train_test(dataset,
                                                              test_size=test_size,
                                                              random_state=random_state)

    train_dataset.to_csv(train_csv_path, index=False)
    test_dataset.to_csv(test_csv_path, index=False)



if __name__ == '__main__':
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument('--split-train-test-config', dest='config', required=True)
    args = args_parser.parse_args()

    split_dataset(config_path=args.config)

