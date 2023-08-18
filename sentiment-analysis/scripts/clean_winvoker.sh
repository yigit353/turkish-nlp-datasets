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

INPUT_FILE="${OUTPUT_FILE}"
OUTPUT_FILE="${DATASET_DIR}/tmp/dataset-all-preclean-sentences.txt"

if [ -f "${OUTPUT_FILE}" ]; then
  echo "${OUTPUT_FILE} exists."
else
  echo "Extracting sentences to ${OUTPUT_FILE}"
  python ../src/extract_sentences.py \
    --csv-file="${INPUT_FILE}" \
    --output-file="${OUTPUT_FILE}"
fi

CLEANER_DIR="C:/Users/yigit/CLionProjects/cleaner"
CLI_DIR="${CLEANER_DIR}/target/release"
INPUT_FILE="${OUTPUT_FILE}"
OUTPUT_FILE="${DATASET_DIR}/tmp/dataset-all-preclean-sentences.rcleaned3"

if [ -f "${OUTPUT_FILE}" ]; then
  echo "${OUTPUT_FILE} exists."
else
  echo "Cleaning ${INPUT_FILE} and saving as ${OUTPUT_FILE}"
  "${CLI_DIR}/main_cleaner_leveled.exe" \
    --input_file "${INPUT_FILE}" \
    --level 3 \
    --mapping_dir "${CLEANER_DIR}/data"
fi


INPUT_FILE="${OUTPUT_FILE}"
LABELS_FILE="${DATASET_DIR}/tmp/dataset-all-preclean.csv"
OUTPUT_FILE="${DATASET_DIR}/tmp/dataset-all-cleaned.csv"

if [ -f "${OUTPUT_FILE}" ]; then
  echo "${OUTPUT_FILE} exists."
else
  echo "Recombining ${INPUT_FILE} with labels from ${LABELS_FILE} into ${OUTPUT_FILE}"
  python ../src/recombine_sentences.py \
    --cleaned-sentences-file="${INPUT_FILE}" \
    --uncleaned-file="${LABELS_FILE}" \
    --cleaned-output-file="${OUTPUT_FILE}"
fi

INPUT_FILE="${OUTPUT_FILE}"
OUTPUT_FILE="${DATASET_DIR}/tmp/dataset-all-cleaned-unknown-indices.txt"

if [ -f "${OUTPUT_FILE}" ]; then
  echo "${OUTPUT_FILE} exists."
else
  echo "Getting unknown indices and saving to ${OUTPUT_FILE}"
  python ../src/get_unknown_indices.py \
    --input-file="${INPUT_FILE}"
fi

INPUT_FILE="${DATASET_DIR}/tmp/dataset-all-preclean.csv"
UNKNOWN_INDICES_FILE="${OUTPUT_FILE}"
OUTPUT_FILE="${DATASET_DIR}/tmp/dataset-all-preclean-balance-indices.json"
SEED=12345

if [ -f "${OUTPUT_FILE}" ]; then
  echo "${OUTPUT_FILE} exists."
else
  echo "Balancing dataset... and creating ${OUTPUT_FILE}"
  python ../src/balance_labels.py \
    --input-file="${INPUT_FILE}" \
    --unknown-indices-file="${UNKNOWN_INDICES_FILE}" \
    --seed=${SEED}
fi

INDICES_FILE="${OUTPUT_FILE}"
N_FOLDS=5
SEED=12345
OUTPUT_FILE="${DATASET_DIR}/tmp/dataset-all-preclean-balance-fold-indices.json"

if [ -f "${OUTPUT_FILE}" ]; then
  echo "${OUTPUT_FILE} exists."
else
  echo "Creating fold indices file: ${OUTPUT_FILE}"
  python ../src/kfold_sentiment.py \
    --indices-file="${INDICES_FILE}" \
    --n-folds="${N_FOLDS}" \
    --seed=${SEED}
fi

FOLD_INDICES_FILE="${OUTPUT_FILE}"
INPUT_FILE="${DATASET_DIR}/tmp/dataset-all-preclean.csv"
OUTPUT_DIR="${DATASET_DIR}/folds/5folds/raw"
OUTPUT_FILE="${OUTPUT_DIR}/train_0.csv"

if [ -f "${OUTPUT_FILE}" ]; then
  echo "${OUTPUT_FILE} exists."
else
  echo "Creating raw folds (example): ${OUTPUT_FILE}"
  python ../src/create_folds.py \
    --input-file="${INPUT_FILE}" \
    --fold-indices-file="${FOLD_INDICES_FILE}" \
    --output-dir="${OUTPUT_DIR}"
fi

INPUT_FILE="${DATASET_DIR}/tmp/dataset-all-cleaned.csv"
OUTPUT_DIR="${DATASET_DIR}/folds/5folds/clean"
OUTPUT_FILE="${OUTPUT_DIR}/train_0.csv"

if [ -f "${OUTPUT_FILE}" ]; then
  echo "${OUTPUT_FILE} exists."
else
  echo "Creating clean folds (example): ${OUTPUT_FILE}"
  python ../src/create_folds.py \
    --input-file="${INPUT_FILE}" \
    --fold-indices-file="${FOLD_INDICES_FILE}" \
    --output-dir="${OUTPUT_DIR}"
fi