word="atach"
list=[0]*26

for i in range(len(word)):
    list[ord(word[i])-ord('a')]=list[ord(word[i])-ord('a')]+1

print(list)

words = ["cat","bt","hat","tree"]
result=0
for word in words:
    wordCount=[0]*26
    for i in range(len(word)):
        wordCount[ord(word[i])-ord('a')]=wordCount[ord(word[i])-ord('a')]+1
    ok=True

    for i in range(26):
        if wordCount[i]>list[i]:
            ok=False
            break
    if(ok==True):
        result+=len(word)

print(result)