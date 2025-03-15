def countOfSubstrings(word, k):
    constIndex = [0] * len(word)
    constFound = len(word)
    for i in range(len(word) - 1, -1, -1):
        if word[i] not in "aeiou":
            constIndex[i] = constFound
            constFound = i
        else:
            constIndex[i] = constFound
    i = 0
    j = 0
    dicts = {}
    constCount = 0
    count = 0
    print(constIndex)
    while j < len(word):
        if word[j] in "aeiou":
            dicts[word[j]] = dicts.get(word[j], 0) + 1
        else:
            constCount += 1
        while i < len(word) and constCount > k:
            ch = word[i]
            if ch in "aeiou":
                dicts[ch] -= 1
                if dicts[ch] == 0:
                    del dicts[ch]
            else:
                constCount -= 1
            i += 1

        while i < len(word) and len(dicts) == 5 and constCount == k:
            idx = constIndex[j]
            count += idx - j
            ch = word[j]
            if ch in "aeiou":
                dicts[ch] -= 1
                if dicts[ch] == 0:
                    del dicts[ch]
            else:
                constCount -= 1
            i += 1
        j += 1
    return count


print(countOfSubstrings("ieaouqqieaouqq", k=1))
# print(countOfSubstrings("iiaeioqiiaeioqq", k=2))
