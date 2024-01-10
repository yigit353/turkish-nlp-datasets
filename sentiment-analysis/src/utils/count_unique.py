import csv
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, required=True)

    args = parser.parse_args()

    with open(args.file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',')

        # Skip the header
        next(reader)

        # Dictionary to store unique sentence and label pairs
        unique_pairs = {}

        # Process each line in the CSV
        for row in reader:
            sentence, label = row
            unique_pairs[sentence] = label

        # Counting unique sentences for each label
        unique_counts = {"Positive": 0, "Negative": 0}
        for label in unique_pairs.values():
            if label in unique_counts:
                unique_counts[label] += 1

        print(unique_counts)

