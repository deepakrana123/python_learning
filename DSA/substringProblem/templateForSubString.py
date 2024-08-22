def minWindow(s, t):
    map = {}
    for value in t:
        # if value in map:
        #     map[value]=map[value]+1
        # else:
        #     map[value]=1
        map[value] = map.get(value, 0)+1
    start = 0
    end = 0
    minStart = 0
    # set minimum length to len(String)+1. it cannot be greater than that
    minLength = len(s)+1
    counter = len(map)
    # iterate till the end of string
    while end <= len(s):
        val = s[end]
        # if char in S is present in Map then , if count of that char in haspmap greater then ero than decasre otherwise its negative
        # if count of that charcaater in map is greater then zero then decreament the counter 
        if val in map and map[val] > 0:
            counter -= 1
        map[val] -= 1
        end += 1
        # coutner =0 it means we have all characters between start to end
        # calculate the length and min_length
        while counter == 0:
            if end-start < minLength:
                minLength = end-start
                minStart = start
            # if character at start is persent in map,then increment its count in map
            # if its count in map is <=0 then continue the inner while loop until the count is positive
            # If character at begin index is present in T, then increment its count in hashmap
            # If its count in hashmap is <= 0, then continue the inner while loop until the count is +ve
            # If its count in hashmap is > 0 then increment the counter. It means we have found first character
            # which is in S and T. So we can continue searching for shortest len from begin+1 to ...
               
            c2 = s[start]
            map[c2] += 1
            if c2 in map and map.get(c2) > 0:
                counter += 1
            start += 1
    return "" if minLength == float("inf") else s[minStart, minStart+minLength]


print(minWindow("", "ABC"))
 # Check the output below:
                    # 1. First the begin and end window are at idx - 0 and 6
                    #     min_len - 6
                    # 2. Since begin (idx = 0) is `A`, so we set next window from begin+1 to end 
                    #    and continue with the process.
                    # 3. When end idx reaches 11, we have all characters of T in S. We calculate len and compare min_len 
                    # 4. Now, since begin(idx=1) is 'D' which is not in T, we continue in inner while loop until
                    # we set counter to non-zero. Here, we can see than count of B in hashmap is -1 since we 
                    # have 2occurances of B between begin to end. So we have to skip the first occurance.
                #
                #   Input - "ADOBECODEBANC"
                #           "ABC"
                #
                # The output of above commented print statement
                # 0 6 {u'A': 0, u'C': 0, u'B': 0}
                # 1 11 {u'A': 0, u'C': 0, u'B': -1}
                # 2 11 {u'A': 0, u'C': 0, u'B': -1}
                # 3 11 {u'A': 0, u'C': 0, u'B': -1}
                # 4 11 {u'A': 0, u'C': 0, u'B': 0}
                # 5 11 {u'A': 0, u'C': 0, u'B': 0}
                # 6 13 {u'A': 0, u'C': 0, u'B': 0}
                # 7 13 {u'A': 0, u'C': 0, u'B': 0}
                # 8 13 {u'A': 0, u'C': 0, u'B': 0}
                # 9 13 {u'A': 0, u'C': 0, u'B': 0}
