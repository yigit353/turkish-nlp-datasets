import argparse
import csv


def read_prediction(path):
    predictions = []
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        next(reader)
        for row in reader:
            index, prediction = row
            predictions.append(prediction)
    return predictions


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--validation-file', type=str, required=True)
    parser.add_argument('--prediction-file-1', type=str, required=True)
    parser.add_argument('--prediction-file-2', type=str, required=True)
    parser.add_argument('--output-file', type=str, required=True)

    args = parser.parse_args()

    texts = []
    labels = []

    with open(args.validation_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            text, label = row
            texts.append(text)
            labels.append(label)

    predictions1 = read_prediction(args.prediction_file_1)
    predictions2 = read_prediction(args.prediction_file_2)

    rows = [['text', 'label', 'prediction1', 'prediction2', 'prediction1==prediction2']]
    for text, label, prediction1, prediction2 in zip(texts, labels, predictions1, predictions2):
        rows.append([text, label, prediction1, prediction2, prediction1 == prediction2])

    with open(args.output_file, 'w', encoding='utf-8', newline='') as out:
        writer = csv.writer(out)
        writer.writerows(rows)
