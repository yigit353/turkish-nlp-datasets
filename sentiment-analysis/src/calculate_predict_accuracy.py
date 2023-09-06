import argparse
import csv


def get_accuracy(predicted_labels, test_labels):
    correct = 0
    for predicted_label, test_label in zip(predicted_labels, test_labels):
        if predicted_label == test_label:
            correct += 1
    return correct / len(test_labels)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--predict-file', type=str, required=True)
    parser.add_argument('--test-file', type=str, required=True)

    args = parser.parse_args()

    predicted_labels = []

    with open(args.predict_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        headers = next(reader)
        for row in reader:
            predicted_labels.append(row[1])

    test_labels = []
    texts = []

    with open(args.test_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)
        for row in reader:
            text, label = row
            test_labels.append(label)
            texts.append(text)

    assert len(predicted_labels) == len(test_labels)

    accuracy = get_accuracy(predicted_labels, test_labels)

    print(f'Accuracy: {accuracy}')

    unique_test_labels = []
    unique_predicted_labels = []
    unique_texts = []

    for predicted_label, test_label, text in zip(predicted_labels, test_labels, texts):
        if text not in unique_texts:
            unique_texts.append(text)
            unique_test_labels.append(test_label)
            unique_predicted_labels.append(predicted_label)

    unique_accuracy = get_accuracy(unique_predicted_labels, unique_test_labels)

    print(f'Unique accuracy: {unique_accuracy}')

