import argparse
import csv
import random


def balance_dataset(rows, seed):
    positive_rows = [row for row in rows if row[1] == 'Positive']
    negative_rows = [row for row in rows if row[1] == 'Negative']

    min_count = min(len(positive_rows), len(negative_rows))

    # Set seed for reproducibility
    random.seed(seed)

    # Randomly select min_count rows from both positive and negative lists
    balanced_positive = random.sample(positive_rows, min_count)
    balanced_negative = random.sample(negative_rows, min_count)

    return balanced_positive + balanced_negative


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-file', type=str, required=True)
    parser.add_argument('--output-file', type=str, required=True)
    parser.add_argument('--seed', type=int, required=True)

    args = parser.parse_args()

    rows = []

    with open(args.input_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)
        rows.append(headers)
        for row in reader:
            rows.append(row)

    balanced_rows = balance_dataset(rows[1:], args.seed)

    with open(args.output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(balanced_rows)
