import argparse
import json

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-file', type=str, required=True)
    parser.add_argument('--output-file', type=str, required=True)

    args = parser.parse_args()

    expanded_data = {'data': []}
    with open(args.input_file, encoding='utf-8') as f:
        data = json.load(f)
        for article in data['data']:
            title = article['title']
            for paragraph in article['paragraphs']:
                context = paragraph['context']
                for qa in paragraph['qas']:
                    question = qa['question']
                    qid = qa['id']
                    answer = qa['answers'][0]
                    answer_text = answer['text']
                    answer_start = int(answer['answer_start'])
                    expanded_data['data'].append({
                        'id': str(qid),
                        'context': context,
                        'question': question,
                        'title': title,
                        'answers': {"text": [answer_text], "answer_start": [answer_start]}
                    })

    with open(args.output_file, 'w', encoding='utf-8') as f:
        json.dump(expanded_data, f, indent=2, ensure_ascii=False)
