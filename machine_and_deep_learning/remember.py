import numpy as np


def anagram(string1: str, string2: str) -> None:

    string1 = sorted(string1)
    string2 = sorted(string2)

    if string1 == string2:
        print("Anagram")
    else:
        print("Not an anagram")


def product(array: np.array) -> int | float:

    for i in array:
        print(array.prod() / i)


string1: str = "anagram"
string2: str = "naagarm"

print(anagram(string1=string1, string2=string2))
print(product(np.array([1, 2, 3, 4])))
