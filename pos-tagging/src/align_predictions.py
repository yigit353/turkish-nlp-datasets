import argparse
import json
import csv

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--validation-file', type=str, required=True,
                        help='File with one sentence per line (validation_0.json)')
    parser.add_argument('--prediction-file', type=str, required=True,
                        help='File with one prediction per line (predictions.txt)')
    parser.add_argument('--output-file', type=str, required=True,
                        help='Output file (aligned.csv)')

    args = parser.parse_args()

    tokens = []
    pos_tags = []

    with open(args.validation_file, encoding='utf-8') as f:
        validation_data = json.load(f)
        for sentence in validation_data:
            tokens.append(sentence['tokens'])
            pos_tags.append(sentence['pos_tags'])

    predictions = []

    with open(args.prediction_file, encoding='utf-8') as f:
        for line in f:
            predictions.append(line.strip().split())

    assert len(tokens) == len(predictions)

    with open(args.output_file, 'w', encoding='utf-8', newline='') as out:
        writer = csv.writer(out)
        writer.writerow(['Token', 'Gold', 'Prediction'])
        data = []
        for i in range(len(tokens)):
            for j in range(len(tokens[i])):
                data.append([tokens[i][j], pos_tags[i][j], predictions[i][j]])
            data.append([])
        writer.writerows(data)

    '''
    buffer = "Token\tGold\tPrediction\n"
    
    for i in range(len(tokens)):
        for j in range(len(tokens[i])):
            buffer += f'{tokens[i][j]}\t{pos_tags[i][j]}\t{predictions[i][j]}\n'
        buffer += '\n'
        
    with open(args.output_file, 'w', encoding='utf-8') as out:
        out.write(buffer)
    '''
