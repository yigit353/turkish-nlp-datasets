import random


def split_indices(indices, n_folds, seed=None):
    if seed is not None:
        random.seed(seed)

    random.shuffle(indices)
    avg = len(indices) / float(n_folds)
    return [indices[int(round(i * avg)): int(round((i + 1) * avg))] for i in range(n_folds)]

def cross_validation_indices(indices, n_folds, seed=None):
    splits = split_indices(indices, n_folds, seed)

    train_indices_list = []
    validation_indices_list = []

    for i in range(n_folds):
        train = [idx for s in splits[:i] + splits[i + 1:] for idx in s]
        validation = splits[i]

        train_indices_list.append(train)
        validation_indices_list.append(validation)

    return train_indices_list, validation_indices_list


if __name__ == '__main__':
    seed = 12345
    n_folds = 10
    indices = list(range(5))
    train, test = cross_validation_indices(indices, n_folds, seed)
    print(train)
    print(test)
