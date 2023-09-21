#!/bin/bash

python3 ../src/utils/combine_predictions.py \
  --validation-file="../datasets/kaggle-movie/folds/5folds/raw/validation_0.csv" \
  --prediction-file-1="../datasets/kaggle-movie/tmp/results/predict_results_bert2d_128k.txt" \
  --prediction-file-2="../datasets/kaggle-movie/tmp/results/predict_results_berturk_128k.txt" \
  --output-file="../datasets/kaggle-movie/tmp/results/bert2d_berturk_comparison.csv"
