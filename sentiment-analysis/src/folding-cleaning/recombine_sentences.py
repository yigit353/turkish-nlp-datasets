import argparse
import csv

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--cleaned-sentences-file', type=str, required=True)
    parser.add_argument('--uncleaned-file', type=str, required=True)
    parser.add_argument('--cleaned-output-file', type=str, required=True)

    args = parser.parse_args()

    sentences = []
    with open(args.cleaned_sentences_file, 'r', encoding='utf-8') as f:
        for num, line in enumerate(f):
            line = line.strip()
            if not line:
                line = '[UNK]'
            sentences.append(line)

    labels = []

    with open(args.uncleaned_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)
        for row in reader:
            _, label = row
            labels.append(label)

    assert len(sentences) == len(labels)

    rows = [['text', 'label']]
    for sentence, label in zip(sentences, labels):
        rows.append([sentence, label])

    with open(args.cleaned_output_file, 'w', encoding='utf-8', newline='') as out:
        writer = csv.writer(out)
        writer.writerows(rows)
