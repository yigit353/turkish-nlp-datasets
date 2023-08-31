import argparse
import csv
import random
import json


def balance_dataset(rows, seed):
    positive_indices = []
    negative_indices = []
    for index, row in enumerate(rows):
        if row[1] == 'Positive':
            positive_indices.append(index)
        elif row[1] == 'Negative':
            negative_indices.append(index)

    min_count = min(len(positive_indices), len(negative_indices))

    # Set seed for reproducibility
    random.seed(seed)

    # Randomly select min_count rows from both positive and negative lists
    balanced_positive = random.sample(positive_indices, min_count)
    balanced_negative = random.sample(negative_indices, min_count)

    return balanced_positive, balanced_negative


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-file', type=str, required=True)
    parser.add_argument('--unknown-indices-file', type=str, required=True)
    parser.add_argument('--seed', type=int, required=True)

    args = parser.parse_args()

    output_path = args.input_file.replace('.csv', '-balance-indices.json')

    rows = []

    with open(args.unknown_indices_file, 'r', encoding='utf-8') as f:
        indices = [int(line.strip()) for line in f]

    with open(args.input_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)
        for index, row in enumerate(reader):
            if index in indices:
                continue
            rows.append(row)

    balanced_positive, balanced_negative = balance_dataset(rows, args.seed)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({'positive': balanced_positive, 'negative': balanced_negative}, f)
