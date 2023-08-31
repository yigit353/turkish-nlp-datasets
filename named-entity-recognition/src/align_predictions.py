import argparse
import json
import csv
import os.path

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--test-file', type=str, required=True,
                        help='File with one sentence per line (test.json)')
    parser.add_argument('--prediction-file-1', type=str, required=True,
                        help='File with one prediction per line (predictions.txt)')
    parser.add_argument('--prediction-file-2', type=str, required=True,
                        help='File with one prediction per line (predictions.txt)')
    parser.add_argument('--output-dir', type=str, required=True,
                        help='Output directory for file `aligned.csv`')

    args = parser.parse_args()

    all_tokens = []
    pos_tags = []

    with open(args.test_file, encoding='utf-8') as f:
        test_data = json.load(f)
        for sentence in test_data:
            all_tokens.append(sentence['tokens'])
            pos_tags.append(sentence['ner_tags'])

    predictions1 = []

    with open(args.prediction_file_1, encoding='utf-8') as f:
        for line in f:
            predictions1.append(line.strip().split())

    predictions2 = []

    with open(args.prediction_file_2, encoding='utf-8') as f:
        for line in f:
            predictions2.append(line.strip().split())

    assert len(all_tokens) == len(predictions1)
    assert len(all_tokens) == len(predictions2)

    data = []
    sentence_id = 0

    output_file_path = os.path.join(args.output_dir, 'aligned.csv')

    with open(output_file_path, 'w', encoding='utf-8', newline='') as out:
        writer = csv.writer(out)
        writer.writerow(['Sentence Id', 'Token', 'Gold', 'Prediction 1', 'Prediction 2'])
        for tokens, labels, preds1, preds2 in zip(all_tokens, pos_tags, predictions1, predictions2):
            sentence_id += 1

            all_same = True
            for pred1, pred2 in zip(preds1, preds2):
                if pred1 != pred2:
                    all_same = False
                    break

            if all_same:
                continue

            for token, label, pred1, pred2 in zip(tokens, labels, preds1, preds2):
                data.append([sentence_id, token, label, pred1, pred2])

        writer.writerows(data)
