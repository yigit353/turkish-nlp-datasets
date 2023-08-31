import argparse
import csv


def combine_csv(file1, file2, output_file):
    rows = []

    with open(file1, 'r', encoding='utf-8') as f1:
        reader = csv.reader(f1)

        # Write headers from the first file
        headers = next(reader)
        rows.append(headers)

        for row in reader:
            rows.append(row)

    with open(file2, 'r', encoding='utf-8') as f2:
        reader = csv.reader(f2)
        next(reader)

        for row in reader:
            rows.append(row)

    with open(output_file, 'w', encoding='utf-8', newline='') as out:
        writer = csv.writer(out)
        writer.writerows(rows)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--csv-file1', type=str, required=True)
    parser.add_argument('--csv-file2', type=str, required=True)
    parser.add_argument('--output-file', type=str, required=True)

    args = parser.parse_args()

    combine_csv(args.csv_file1, args.csv_file2, args.output_file)
