import argparse
import json

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-file', type=str, required=True)

    args = parser.parse_args()

    with open(args.input_file, encoding='utf-8') as f:
        data = json.load(f)
        for article in data['data']:
            for paragraph in article['paragraphs']:
                context = paragraph['context']
                for qa in paragraph['qas']:
                    question = qa['question']
                    answer = qa['answers'][0]
                    answer_text = answer['text']
                    answer_start = int(answer['answer_start'])
                    if context[answer_start:answer_start + len(answer_text)] != answer_text:
                        print(f"Question id: {qa['id']}")
                        print(f"Wrong context span: {context[answer_start:answer_start + len(answer_text)]}")
                        print(f"Answer text: {answer_text}")
                        print(f"Full context: {context}")
                        print(f"Question: {question}")
                        print()
