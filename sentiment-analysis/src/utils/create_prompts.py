import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--sentences-file', type=str, required=True)
    parser.add_argument('--output-file', type=str, required=True)

    args = parser.parse_args()
    rows = []
    sentence_batch = 10

    with open(args.sentences_file, 'r', encoding='utf-8') as f:
        for index, line in enumerate(f):
            line = line.strip()
            line = f"/sentiment {line}"
            rows.append(line)
            if index > 0 and index % sentence_batch == 0:
                rows.append("")

    with open(args.output_file, 'w', encoding='utf-8', newline='') as out:
        out.write("\n".join(rows))
