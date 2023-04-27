import constants as cs
from utilityModule import *


if __name__ == "__main__":
    print("Enter training-set ratio between 0 and 1: ")
    ratio = float(input())
    train_data, test_data = split_dataset(cs.RATINGS_SMALL_FILE, ratio)
    print(train_data)
    print(test_data)