import argparse
import csv
import json

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-file', type=str, required=True)
    parser.add_argument('--fold-indices-file', type=str, required=True)
    parser.add_argument('--output-dir', type=str, required=True)

    args = parser.parse_args()

    with open(args.input_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)
        rows = []
        for row in reader:
            rows.append(row)

    with open(args.fold_indices_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        folds = data["indices"]
        for fold_obj in folds:
            fold = fold_obj['fold']
            train_indices = fold_obj['train']
            validation_indices = fold_obj['validation']
            output_train_file = f'{args.output_dir}/train_{fold}.csv'
            output_validation_file = f'{args.output_dir}/validation_{fold}.csv'
            with open(output_train_file, 'w', encoding='utf-8', newline='') as out:
                writer = csv.writer(out)
                writer.writerow(headers)
                for index in train_indices:
                    writer.writerow(rows[index])
            with open(output_validation_file, 'w', encoding='utf-8', newline='') as out:
                writer = csv.writer(out)
                writer.writerow(headers)
                for index in validation_indices:
                    writer.writerow(rows[index])
