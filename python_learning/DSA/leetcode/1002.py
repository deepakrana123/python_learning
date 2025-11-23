def commonChars(words):
    dicts = {}
    for w in words[0]:
        dicts[w] = dicts.get(w, 0) + 1
    for i in range(1, len(words)):
        dicts1 = {}
        for w in words[i]:
            dicts1[w] = dicts1.get(w, 0) + 1
        for key in dicts:
            if key in dicts1:
                dicts[w] = min(dicts[w], dicts1[w])
            else:
                dicts[w] = 0
    return dicts


def relativeSortArray(arr1, arr2):
    arr1.sort()
    print(arr1)


def isPathCrossing(path):
    dm = set()
    point1 = 0
    point2 = 0
    dm.add((0, 0))
    for d in path:
        if d == "N":
            point1 += 1
        if d == "E":
            point2 += 1
        if d == "W":
            point2 -= 1
        if d == "S":
            point1 -= 1
        print(point1, point2, d)
        if (point1, point2) in dm:
            return True
        dm.add((point1, point2))
    return False


def numberOfAlternatingGroups(colors):
    if len(colors) < 3:
        return 0
    colors.append(colors[0])
    colors.append(colors[1])
    count = 0
    for i in range(1, len(colors) - 1):
        if colors[i - 1] == colors[i + 1] and colors[i] != colors[i + 1]:
            count += 1
    return count


def minMaxDifference(num):
    abc = str(num)
    str1 = [v for v in abc]
    str2 = [v for v in abc]
    a = abc[0]
    b = abc[0]
    for i in range(len(abc)):
        if abc[i] != "9":
            a = abc[i]
            break
    for i in range(len(abc)):
        if abc[i] != "0":
            b = abc[i]
            break
    for i in range(len(abc)):
        if abc[i] == a:
            str1[i] = "9"
        if abc[i] == b:
            str2[i] = "0"
    return int("".join(str1)) - int("".join(str2))


def findTheArrayConcVal(nums):
    i = 0
    j = len(nums) - 1
    c = 0
    if len(nums) == 1:
        return nums[0]
    while j - i > 0:
        c += int(str(nums[i]) + str(nums[j]))
        j -= 1
        i += 1
    return c + (nums[i] if len(nums) % 2 != 0 else 0)


def isValid(word):
    vowel = 0
    consonanat = 0
