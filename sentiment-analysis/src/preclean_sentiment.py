import argparse
import csv
import re

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-file', type=str, required=True)
    parser.add_argument('--output-file', type=str, required=True)

    args = parser.parse_args()

    multi_space_regex = re.compile(r'\s{2,}')
    multi_dots_regex = re.compile(r'\.{4,}')

    rows = []

    with open(args.input_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)

        for row in reader:
            text, label, _ = row
            text = text.strip()
            text = text.replace('\n', ' ')
            text = text.replace('<br />', ' ')
            text = text.replace('\t', ' ')
            text = re.sub(multi_space_regex, ' ', text)
            text = re.sub(multi_dots_regex, '...', text)

            if label == 'Notr':
                label = 'Neutral'
            rows.append([text, label])

    with open(args.output_file, 'w', encoding='utf-8', newline='') as out:
        writer = csv.writer(out)
        writer.writerow(['text', 'label'])
        writer.writerows(rows)
