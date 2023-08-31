import argparse
import csv

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--csv-file', type=str, required=True)
    parser.add_argument('--output-file', type=str, required=True)

    args = parser.parse_args()

    rows = []

    with open(args.csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)
        for row in reader:
            text, label = row
            text = text.strip()
            text = text.replace('\n', ' ')
            text = text.replace('<br />', ' ')
            rows.append(text)

    with open(args.output_file, 'w', encoding='utf-8') as out:
        out.write('\n'.join(rows))
