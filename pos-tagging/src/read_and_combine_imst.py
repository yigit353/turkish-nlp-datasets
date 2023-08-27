import argparse
import json


def process_conllu(f):
    examples = []
    sentence_id = ""
    tokens = []
    pos_tags = []

    for line in f:
        if line.startswith('# sent_id = '):
            sentence_id = line[12:].strip()
            continue
        if line.startswith('#'):
            continue
        if line == '\n':
            if len(tokens) > 0:
                examples.append({
                    'id': sentence_id,
                    'tokens': tokens,
                    'pos_tags': pos_tags
                })
                tokens = []
                pos_tags = []
            continue
        fields = line.split('\t')
        number, word, _, pos, *rest = fields
        if '-' in number:
            continue
        tokens.append(word)
        pos_tags.append(pos)

    if len(tokens) > 0:
        examples.append({
            'id': sentence_id,
            'tokens': tokens,
            'pos_tags': pos_tags
        })

    return examples


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dev', type=str, required=True)
    parser.add_argument('--test', type=str, required=True)
    parser.add_argument('--train', type=str, required=True)
    parser.add_argument('--output', type=str, required=True)

    args = parser.parse_args()

    examples = []
    with open(args.dev, 'r', encoding='utf-8') as f:
        dev_examples = process_conllu(f)
        examples.extend(dev_examples)

    with open(args.test, 'r', encoding='utf-8') as f:
        test_examples = process_conllu(f)
        examples.extend(test_examples)

    with open(args.train, 'r', encoding='utf-8') as f:
        train_examples = process_conllu(f)
        examples.extend(train_examples)

    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(examples, f, indent=2, ensure_ascii=False)
