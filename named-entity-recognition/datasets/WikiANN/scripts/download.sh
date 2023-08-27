#!/bin/bash

for file in train.txt dev.txt test.txt labels.txt; do
  curl -O https://schweter.eu/storage/turkish-bert-wikiann/$file
done