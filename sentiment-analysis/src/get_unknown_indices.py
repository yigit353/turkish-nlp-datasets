import argparse
import csv

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-file', type=str, required=True)

    args = parser.parse_args()
    output_path = args.input_file.replace('.csv', '-unknown-indices.txt')

    indices = []

    with open(args.input_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)
        for index, row in enumerate(reader):
            text, _ = row
            text = text.strip()
            if text == '[UNK]':
                indices.append(index)

    with open(output_path, 'w', encoding='utf-8') as out:
        out.write('\n'.join([str(i) for i in indices]))
