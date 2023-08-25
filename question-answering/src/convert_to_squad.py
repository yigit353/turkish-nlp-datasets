import argparse
import json
import re
import copy


def replace_common_chars(text):
    text = text.replace('“', '"')
    text = text.replace('”', '"')
    text = text.replace('’', "'")
    text = text.replace('‘', "'")
    text = text.replace('—', '-')
    text = text.replace('–', '-')
    text = text.replace('…', '...')
    text = text.replace('ʿ', "'")
    return text


def remove_spaces(context, qas):
    space_before = False
    new_context = ""
    old_qas = copy.deepcopy(qas)
    for index, c in enumerate(context):
        if c in [' ', '\r', '\n']:
            if space_before:
                for qa_idx, old_qa in enumerate(old_qas):
                    answer_start_index = int(old_qa['answers'][0]['answer_start'])
                    if answer_start_index >= index:
                        new_answer_start_index = int(qas[qa_idx]['answers'][0]['answer_start'])
                        qas[qa_idx]['answers'][0]['answer_start'] = str(new_answer_start_index - 1)
                continue
            space_before = True
        else:
            space_before = False
        if c in ['\r', '\n']:
            new_context += ' '
        else:
            new_context += c
    return new_context


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-file', type=str, required=True)
    parser.add_argument('--output-file', type=str, required=True)

    args = parser.parse_args()

    regex = re.compile(r'\s{2,}')

    with open(args.input_file, encoding='utf-8') as f:
        data = json.load(f)
        new_data = {'data': []}
        for article in data['data']:
            title = article['title']
            paragraphs = []
            for paragraph in article['paragraphs']:
                context = paragraph['context'].rstrip()
                context = replace_common_chars(context)
                qas = []
                for qa in paragraph['qas']:
                    question = qa['question']
                    id = qa['id']
                    answers = qa['answers']
                    question = re.sub(regex, ' ', question)
                    question = replace_common_chars(question)
                    text = re.sub(regex, ' ', answers[0]['text'].rstrip())
                    text = replace_common_chars(text)
                    qas.append({'question': question, 'id': id, 'answers': [{
                        'answer_start': answers[0]['answer_start'],
                        'text': text
                    }]})
                context = remove_spaces(context, qas)
                paragraphs.append({'context': context, 'qas': qas})
            new_data['data'].append({'title': title, 'paragraphs': paragraphs})

    with open(args.output_file, 'w', encoding='utf-8') as out:
        json.dump(new_data, out, ensure_ascii=False, indent=4)
