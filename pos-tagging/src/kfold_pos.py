import argparse
import random
import json


def split_data(data, n_folds, seed=None):
    if seed is not None:
        random.seed(seed)

    random.shuffle(data)
    avg = len(data) / float(n_folds)
    return [data[int(round(i * avg)): int(round((i + 1) * avg))] for i in range(n_folds)]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-file', type=str, required=True)
    parser.add_argument('--output-dir', type=str, required=True)
    parser.add_argument('--n-folds', type=int, required=False, default=5)
    parser.add_argument('--seed', type=int, required=True)

    args = parser.parse_args()

    with open(args.input_file, encoding='utf-8') as f:
        data = json.load(f)
        splits = split_data(data, args.n_folds, args.seed)

        for i, split in enumerate(splits):
            train_data = [s for s in splits[:i] + splits[i + 1:] for s in s]
            validation_data = splits[i]
            with open(f'{args.output_dir}/train_{i}.json', 'w', encoding='utf-8') as out:
                json.dump({'data': train_data}, out, ensure_ascii=False, indent=2)
            with open(f'{args.output_dir}/validation_{i}.json', 'w', encoding='utf-8') as out:
                json.dump({'data': validation_data}, out, ensure_ascii=False, indent=2)
