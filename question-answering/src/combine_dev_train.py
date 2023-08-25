import argparse
import json

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dev-file', type=str, required=True)
    parser.add_argument('--train-file', type=str, required=True)
    parser.add_argument('--combined-output-file', type=str, required=True)

    args = parser.parse_args()

    with open(args.dev_file, encoding='utf-8') as f:
        dev = json.load(f)

    with open(args.train_file, encoding='utf-8') as f:
        train = json.load(f)

    combined = {'data': dev['data'] + train['data']}

    with open(args.combined_output_file, 'w', encoding='utf-8') as out:
        json.dump(combined, out, ensure_ascii=False, indent=4)
