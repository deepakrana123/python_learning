def countOfAtoms(formula: str) -> str:
        stack=[{}]
        n=len(formula)
        i=0
        print(stack)
        while i<n:
            if formula[i]=='(':
                stack.append({})
                i+=1
            elif formula[i]==')':
                currTopOfStack=stack.pop()
                i+=1
                multi=""
                while i<n and formula[i].isdigit():
                    multi+=formula[i]
                    i+=1
                multiplier=int(multi) if multi else 1
                for element,value in currTopOfStack.items():
                    currTopOfStack[element]=value*int(multiplier)
                if stack:
                    for element,count in currTopOfStack.items():
                        stack[-1][element] = stack[-1].get(element, 0) + count
            else:
                currElement=""
                currElement+=formula[i]
                i+=1
                while i<n and formula[i].isalpha() and formula[i].islower():
                    currElement+=formula[i]
                    i+=1
                currElementCount=""
                while i<n and formula[i].isdigit():
                    currElementCount+=formula[i]
                    i+=1
                currElementCountInt=int(currElementCount) if currElementCount else 1
                stack[-1][currElement]= stack[-1].get(currElement, 0) + currElementCountInt
        print(stack)
        sorted_elements = sorted(stack[-1].items())
        result = ""
        for element, count in sorted_elements:
            result += element
            if count > 1:
                result += str(count)
        
        return result
                        
print(countOfAtoms("H2O"))                 