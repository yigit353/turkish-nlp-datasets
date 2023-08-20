#!/bin/bash

DATASET_DIR="../datasets/huggingface-winvoker"
INPUT_FILE="${DATASET_DIR}/dataset-all.csv"
OUTPUT_FILE="${DATASET_DIR}/tmp/dataset-all-preclean.csv"

if [ -f "${OUTPUT_FILE}" ]; then
  echo "${OUTPUT_FILE} exists."
else
  echo "Pre-cleaning dataset... and creating ${OUTPUT_FILE}"
  python ../src/preclean_sentiment.py \
    --input-file="${INPUT_FILE}" \
    --output-file="${OUTPUT_FILE}"
fi

bash clean_sentiment.sh "${DATASET_DIR}" 5
bash clean_sentiment.sh "${DATASET_DIR}" 10
