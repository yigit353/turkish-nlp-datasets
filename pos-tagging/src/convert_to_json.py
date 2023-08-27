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
    parser.add_argument('--input-file', type=str, required=True)
    parser.add_argument('--output-file', type=str, required=True)

    args = parser.parse_args()

    with open(args.input_file, 'r', encoding='utf-8') as f:
        examples = process_conllu(f)

    with open(args.output_file, 'w', encoding='utf-8') as f:
        json.dump(examples, f, indent=2, ensure_ascii=False)
