import argparse
import csv
import os
import random
import json


def split_train_dev(samples, dev_size, seed=None):
    if seed is not None:
        random.seed(seed)

    random.shuffle(samples)

    return [samples[dev_size:], samples[:dev_size]]


def split_train_dev_all(positive_samples, negative_samples, neutral_samples, ratio=0.1, seed=None):
    positive_splits = split_train_dev(positive_samples, int(round(len(positive_samples) * 0.1)), seed)
    negative_splits = split_train_dev(negative_samples, int(round(len(negative_samples) * 0.1)), seed)
    neutral_splits = split_train_dev(neutral_samples, int(round(len(neutral_samples) * 0.1)), seed)

    train_samples = []
    dev_samples = []

    train_samples.extend(positive_splits[0])
    train_samples.extend(negative_splits[0])
    train_samples.extend(neutral_splits[0])

    dev_samples.extend(positive_splits[1])
    dev_samples.extend(negative_splits[1])
    dev_samples.extend(neutral_splits[1])

    return train_samples, dev_samples


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-file', type=str, required=True)
    parser.add_argument('--output-dir', type=str, required=True)
    parser.add_argument('--ratio', type=float, required=False, default=0.1)
    parser.add_argument('--seed', type=int, required=True)

    args = parser.parse_args()

    rows = []

    with open(args.input_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)
        for index, row in enumerate(reader):
            rows.append(row)

        positive_samples = []
        negative_samples = []
        neutral_samples = []

        for index, row in enumerate(rows):
            if row[1] == 'Positive':
                positive_samples.append(row)
            elif row[1] == 'Negative':
                negative_samples.append(row)
            elif row[1] == 'Neutral':
                neutral_samples.append(row)

        train_samples, dev_samples = split_train_dev_all(positive_samples, negative_samples, neutral_samples,
                                                         args.ratio, args.seed)

        # Save train samples
        train_output_path = os.path.join(args.output_dir, 'train.csv')
        with open(train_output_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(train_samples)

        # Save dev samples
        dev_output_path = os.path.join(args.output_dir, 'dev.csv')
        with open(dev_output_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(dev_samples)
