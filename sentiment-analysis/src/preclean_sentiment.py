import argparse
import csv
import random
import re

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-file', type=str, required=True)
    parser.add_argument('--output-file', type=str, required=True)
    parser.add_argument('--seed', type=int, required=True)

    args = parser.parse_args()

    random.seed(args.seed)

    multi_space_regex = re.compile(r'\s{2,}')
    multi_dots_regex = re.compile(r'\.{4,}')

    positive_samples = []
    negative_samples = []

    with open(args.input_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)

        for row in reader:
            text, label, _ = row
            if label == 'Notr':
                continue
            text = text.strip()
            text = text.replace('\n', ' ')
            text = text.replace('<br />', ' ')
            text = text.replace('\t', ' ')
            text = re.sub(multi_space_regex, ' ', text)
            text = re.sub(multi_dots_regex, '...', text)

            if label == 'Positive':
                positive_samples.append([text, label])
            elif label == 'Negative':
                negative_samples.append([text, label])

    if len(positive_samples) >= len(negative_samples):
        negative_samples = random.choices(negative_samples, k=len(positive_samples))
    else:
        positive_samples = random.choices(positive_samples, k=len(negative_samples))

    with open(args.output_file, 'w', encoding='utf-8', newline='') as out:
        writer = csv.writer(out)
        writer.writerow(['text', 'label'])
        writer.writerows(positive_samples)
        writer.writerows(negative_samples)
