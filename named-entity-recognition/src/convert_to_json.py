import argparse
import json


def process_conll(f, sentence_id_prefix=None):
    examples = []
    sentence_id = 1
    tokens = []
    ner_tags = []

    for line in f:
        if line == '\n':
            if len(tokens) > 0:
                examples.append({
                    'id': f"{sentence_id_prefix}-{sentence_id}",
                    'tokens': tokens,
                    'pos_tags': ner_tags
                })
                tokens = []
                ner_tags = []
                sentence_id += 1
            continue
        word, tag = line.split('\t')
        tokens.append(word)
        ner_tags.append(tag.strip())

    if len(tokens) > 0:
        examples.append({
            'id': f"{sentence_id_prefix}-{sentence_id}",
            'tokens': tokens,
            'pos_tags': ner_tags
        })

    return examples


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-file', type=str, required=True)
    parser.add_argument('--sentence-id-prefix', type=str, required=True)
    parser.add_argument('--output-file', type=str, required=True)

    args = parser.parse_args()

    with open(args.input_file, 'r', encoding='utf-8') as f:
        examples = process_conll(f, args.sentence_id_prefix)

    with open(args.output_file, 'w', encoding='utf-8') as f:
        json.dump(examples, f, indent=2, ensure_ascii=False)
