#!/bin/bash

splits=(train dev test)

# Convert train, dev, and test splits to json

for split in "${splits[@]}"; do
  python ../src/convert_to_json.py \
    --input-file ../datasets/turkish-wiki-ner/"${split}".conll \
    --output-file ../datasets/turkish-wiki-ner/raw/"${split}".json \
    --sentence-id-prefix "${split}" \
    --delim tab
done

for split in "${splits[@]}"; do
  python ../src/convert_to_json.py \
    --input-file ../datasets/WikiANN/"${split}".txt \
    --output-file ../datasets/WikiANN/raw/"${split}".json \
    --sentence-id-prefix "${split}" \
    --delim space
done



