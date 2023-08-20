import argparse
import csv

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-file', type=str, required=True)
    parser.add_argument('--output-file', type=str, required=True)
    parser.add_argument('--text-index', type=int, default=0)
    parser.add_argument('--label-index', type=int, default=1)
    parser.add_argument('--label-type', type=str, default='category', choices=['category', 'rating'])
    parser.add_argument('--neutral-label', type=str, default='Notr')
    parser.add_argument('--negative-max', type=float, default=2.0)
    parser.add_argument('--positive-min', type=float, default=3.5)
    parser.add_argument('--csv-delimiter', type=str, default=',')

    args = parser.parse_args()

    rows = []

    with open(args.input_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=args.csv_delimiter)
        next(reader)
        rows.append(['text', 'label'])
        for row in reader:
            text = row[args.text_index]
            label = row[args.label_index]
            text = text.strip()
            text = text.replace('\n', ' ')
            text = text.replace('<br />', ' ')
            text = text.replace('\t', ' ')
            text = text.replace("̇", '')
            text = text.replace(' ', ' ')
            if not text:
                continue
            if args.label_type == 'category':
                if label == args.neutral_label:
                    continue
            else:
                if float(label) <= args.negative_max:
                    label = 'Negative'
                elif float(label) >= args.positive_min:
                    label = 'Positive'
                else:
                    continue
            rows.append([text, label])

    with open(args.output_file, 'w', encoding='utf-8', newline='') as out:
        writer = csv.writer(out)
        writer.writerows(rows)

