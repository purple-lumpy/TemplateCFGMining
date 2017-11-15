# calculate edit distance

def levenshtein(first, second):
    if len(first) == 0:
        return len(second)
    if len(second) == 0:
        return len(first)

    if len(first) > len(second):
        first, second = second, first

    first_length = len(first) + 1
    second_length = len(second) + 1
    distance_matrix = [list(range(second_length)) for x in range(first_length)]
    # print distance_matrix
    for i in range(1, first_length):
        for j in range(1, second_length):
            deletion = distance_matrix[i - 1][j] + 1
            insertion = distance_matrix[i][j - 1] + 1
            substitution = distance_matrix[i - 1][j - 1]
            if first[i - 1] != second[j - 1]:
                substitution += 1
            distance_matrix[i][j] = min(insertion, deletion, substitution)
    print(distance_matrix)
    return distance_matrix[first_length - 1][second_length - 1]
