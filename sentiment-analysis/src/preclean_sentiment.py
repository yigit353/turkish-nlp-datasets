import argparse
import csv

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-file', type=str, required=True)
    parser.add_argument('--output-file', type=str, required=True)

    args = parser.parse_args()

    rows = []

    with open(args.input_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)
        rows.append(headers)
        for row in reader:
            text, label, source = row
            text = text.strip()
            if not text:
                continue
            if label == 'Notr':
                continue
            rows.append([text, label])

    with open(args.output_file, 'w', encoding='utf-8', newline='') as out:
        writer = csv.writer(out)
        writer.writerows(rows)
