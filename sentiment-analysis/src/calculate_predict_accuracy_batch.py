import argparse
import csv
import os


def f1_score(predicted_labels, test_labels):
    # Initialize counters for True Positives (TP), False Positives (FP), and False Negatives (FN)
    TP = 0
    FP = 0
    FN = 0

    for i in range(len(test_labels)):
        if predicted_labels[i] == "Positive" and test_labels[i] == "Positive":
            TP += 1
        if predicted_labels[i] == "Positive" and test_labels[i] == "Negative":
            FP += 1
        if predicted_labels[i] == "Negative" and test_labels[i] == "Positive":
            FN += 1

    # Calculate precision and recall
    precision = TP / (TP + FP) if (TP + FP) != 0 else 0
    recall = TP / (TP + FN) if (TP + FN) != 0 else 0

    # Calculate F1 score
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) != 0 else 0

    return f1


def get_accuracy(predicted_labels, test_labels):
    correct = 0
    for predicted_label, test_label in zip(predicted_labels, test_labels):
        if predicted_label == test_label:
            correct += 1
    return correct / len(test_labels)


def read_post_fixes(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]


def build_prediction_paths(input_dir, prefix, post_fix):
    return [os.path.join(input_dir, prefix + post_fix, f'run_{i}', 'predict_results_None.txt') for i in range(5)]


def read_predicted_labels(path):
    predicted_labels = []

    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        next(reader)
        for row in reader:
            predicted_labels.append(row[1])

    return predicted_labels


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--test-file', type=str, required=True)
    parser.add_argument('--input-dir', type=str, required=True, help='Input directory for searching prediction files')
    parser.add_argument('--prefix', type=str, required=True, help='File prefix')
    parser.add_argument('--post-fixes-file', type=str, required=True, help='Post fixes file path')
    parser.add_argument('--output-dir', type=str, required=True, help='Output directory for saving results')

    args = parser.parse_args()

    test_labels = []
    texts = []

    with open(args.test_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)
        for row in reader:
            text, label = row
            test_labels.append(label)
            texts.append(text)

    post_fixes = read_post_fixes(args.post_fixes_file)

    all_accuracies = []
    all_f1s = []

    for post_fix in post_fixes:
        paths = build_prediction_paths(args.input_dir, args.prefix, post_fix)

        accuracies = []
        f1s = []

        for path in paths:
            predicted_labels = read_predicted_labels(path)

            assert len(predicted_labels) == len(test_labels)

            unique_test_labels = []
            unique_predicted_labels = []
            unique_texts = []

            for predicted_label, test_label, text in zip(predicted_labels, test_labels, texts):
                if text not in unique_texts:
                    unique_texts.append(text)
                    unique_test_labels.append(test_label)
                    unique_predicted_labels.append(predicted_label)

            unique_accuracy = get_accuracy(unique_predicted_labels, unique_test_labels)
            accuracies.append(unique_accuracy)

            f1 = f1_score(unique_predicted_labels, unique_test_labels)
            f1s.append(f1)

        all_accuracies.append(accuracies)
        all_f1s.append(f1s)

    # All accuracies

    buf = ""

    for acc in all_accuracies:
        buf += "\t".join(map(str, acc)) + "\n"

    buf += "\n"

    # All f1s

    for f1 in all_f1s:
        buf += "\t".join(map(str, f1)) + "\n"

    with open(os.path.join(args.output_dir, 'all_unique_acc_f1_results.txt'), 'w', encoding='utf-8') as f:
        f.write(buf)
