import argparse
import random
import json


def split_indices(indices, n_folds, seed=None):
    if seed is not None:
        random.seed(seed)

    random.shuffle(indices)
    avg = len(indices) / float(n_folds)
    return [indices[int(round(i * avg)): int(round((i + 1) * avg))] for i in range(n_folds)]


def cross_validation_indices(positive_indices, negative_indices, n_folds, seed=None):
    positive_splits = split_indices(positive_indices, n_folds, seed)
    negative_splits = split_indices(negative_indices, n_folds, seed)

    train_indices_list = []
    validation_indices_list = []

    for i in range(n_folds):
        train_positive = [idx for s in positive_splits[:i] + positive_splits[i + 1:] for idx in s]
        train_negative = [idx for s in negative_splits[:i] + negative_splits[i + 1:] for idx in s]

        validation_positive = positive_splits[i]
        validation_negative = negative_splits[i]

        train_indices = train_positive + train_negative
        validation_indices = validation_positive + validation_negative

        train_indices_list.append(train_indices)
        validation_indices_list.append(validation_indices)

    return train_indices_list, validation_indices_list


def sanity_check(train_sets, val_sets, positive_indices, negative_indices):
    total_length = len(positive_indices) + len(negative_indices)

    # Check 1: Length of train and validation sums up to total indices
    for train, val in zip(train_sets, val_sets):
        if len(train) + len(val) != total_length:
            return False, "Length mismatch in one of the folds"

    # Check 2: Every sample is represented in train and validation at least once
    combined_sets = [set(train + val) for train, val in zip(train_sets, val_sets)]
    all_samples = set(positive_indices + negative_indices)

    for sample in all_samples:
        if not any(sample in s for s in combined_sets):
            return False, f"Sample {sample} is not represented in any fold"

    return True, "All checks passed"


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--indices-file', type=str, required=True)
    parser.add_argument('--n-folds', type=int, required=False, default=5)
    parser.add_argument('--seed', type=int, required=True)

    args = parser.parse_args()

    with open(args.indices_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        positive_indices = data['positive']
        negative_indices = data['negative']

    train_indices_list, validation_indices_list = cross_validation_indices(
        positive_indices,
        negative_indices,
        args.n_folds,
        args.seed
    )

    check_result, message = sanity_check(train_indices_list, validation_indices_list, positive_indices,
                                         negative_indices)
    print(message)

    if not check_result:
        exit(1)

    output_path = args.indices_file.replace('-indices.json', f'-fold-indices.json')
    data = {"indices": []}
    with open(output_path, 'w', encoding='utf-8') as f:
        for i in range(args.n_folds):
            data["indices"].append({
                'fold': i,
                'train': train_indices_list[i],
                'validation': validation_indices_list[i]
            })
        json.dump(data, f, indent=4)