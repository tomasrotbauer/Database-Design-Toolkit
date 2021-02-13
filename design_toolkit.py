import itertools

def main():
    S = []
        
    dependencies = input("Enter functional dependencies e.g. A->B,B->A... :\n")
    S = dependencies.split(',')
        
    while True:

        action = input("input:\n    C for closure\n    F for checking if an FD follows\n    P for projection\n"\
            + "    M for minimization\n    B for BCNF decomposition\n    3 for 3NF synthesis\n    U to update the set\n"\
            + "    K to find all keys\n    D to display current set\n    or Q to quit:\n")
        if action.upper() == 'C':
            arg = input("input set of attributes as a string without whitespaces:\n")
            print("**************\n")
            print(closure(arg, S))
            print("\n**************")
            
        elif action.upper() == 'F':
            arg = input("input an FD as before:\n")
            arg = arg.split('->')
            print("**************\n")
            print(follows(S, arg[0], arg[1]))
            print("\n**************")
            
        elif action.upper() == 'P':
            arg = input("input set of attributes as a string without whitespaces:\n")
            print("**************\n")
            T = project(S, arg)
            for fd in T:
                print(fd)
            print("\n**************")
            if input("Would you like to overwrite the original set with this? (Y to confirm):\n").upper() == 'Y':
                S = T
                
        elif action.upper() == 'M':
            T = minimal_basis(S)
            print("**************\n")
            for fd in T:
                print(fd)
            print("\n**************")
            if input("Would you like to overwrite the original set with this? (Y to confirm):\n").upper() == 'Y':
                S = T
                
        elif action.upper() == 'B':
            arg = input("input set of attributes as a string without whitespaces:\n")
            print("**************\n")
            T = BCNF_decomp(arg, S)
            for r in T:
                print(r)
            print("\n**************")
            
        elif action == '3':
            arg = input("input set of attributes as a string without whitespaces:\n")
            print("**************\n")
            T = _3NF_synth(S, arg)
            for r in T:
                print(r)
            print("\n**************")
            
        elif action.upper() == 'K':
            arg = input("input set of attributes as a string without whitespaces:\n")
            print("**************\n")
            K = find_keys(S, arg, False)
            for k in K:
                print(k)
            print("\n**************")
            
        elif action.upper() == 'U':
            dependencies = input("Enter functional dependencies e.g. A->B,B->A... :\n")
            S = dependencies.split(',')
            print("SUCCESS\n")
                    
        elif action.upper() == 'D':
            print("**************\n")
            for fd in S:
                print(fd)
            print("\n**************")
            
        elif action.upper() == 'Q':
            break
    
    return
    
def minimal_basis(S):
    set = []
    print("First, split up the left hand sides of FDs so that each FD has only one attribute on right hand side.")
    for fd in S:
        lrhs = fd.split('->')
        for a in lrhs[1]:
            set.append(lrhs[0] + '->' + a)
    print(set)
            
    for idx in range(len(set)):
        lrhs = set[idx].split('->')
        l = len(lrhs[0])
        print("Considering FD", set[idx])
        if l > 1:
            for i in itertools.product([0,1],repeat=l):
                X = ""
                for j in range(l):
                    if i[j]:
                        X += lrhs[0][j]  
                
                if follows(S, X, lrhs[1]):
                    print("    This FD can be minimized to", X, "-->", lrhs[1], "which follows from the original set S.")
                    set[idx] = X + '->' + lrhs[1]
                    break
        else:
            print("FD", set[idx], "already minimal")
    
    idx = 0
    while(idx < len(set)):
        fd = set.pop(idx)
        lrhs = fd.split('->')
        if not follows(set, lrhs[0], lrhs[1]):
            set.insert(idx, fd)
            idx += 1
                
    return set

def closure(Y, S):
    change = True
    Yplus = Y
    while change:
        change = False
        for fd in S:
            lrhs = fd.split('->')
            f = True
            for i in lrhs[0]:
                if i not in Yplus:
                    f = False
                    break
            if f:
                for i in lrhs[1]:
                    if i not in Yplus:
                        Yplus += i
                        change = True
            
    return Yplus
    
def follows(S, lhs, rhs):
    Yplus = closure(lhs, S)
    for i in rhs:
        if i not in Yplus:
            return False
    return True
    
def project(S, L):
    T = []
    for i in itertools.product([0,1],repeat=len(L)):
        X = ""
        for j in range(len(L)):
            if i[j]:
                X += L[j]
                
        if len(X) == 0 or len(X) == len(L):
            continue

        Xplus = closure(X, S)
        print("subset: ", X, "with closure: ", Xplus)
        a = ""
        for A in Xplus:
            if A in L:
                a += A

        print("    attributes in L: ", a)
        T.append(X + '->' + a)

    return minimal_basis(T)
    
def BCNF_decomp(R, F):
    result = [R]
    i = 0
    FDs = F
    while i < len(result):
        print("Considering relation: ", result[i])
        if len(result) > 1:
            FDs = project(F, result[i])
            print("Newly projected FDs: ", FDs)
        violates = False
        for fd in FDs:
            print ("    FD: ", fd)
            lrhs = fd.split('->')
            Xplus = closure(lrhs[0], F)
            print("The closure(", fd, ") = ", Xplus)
            for a in result[i]:
                if a not in Xplus:
                    violates = True
                    break
            if violates:
                print("Therefore, ", fd, "violates BCNF because")
                R1 = Xplus
                R2 = Xplus
                for a in lrhs[0]:
                    R2 = R2.replace(a, "")
                temp = result[i]
                for a in R2:
                    temp = temp.replace(a, "")
                R2 = temp
                result.pop(i)
                result.append(R1)
                result.append(R2)
                print("Decomposing into R1: ", R1, "and R2: ", R2)
                break
            print("Therefore, ", fd, "does not violate BCNF")
        if not violates:
            print("No FDs violate BCNF --> Add to results")
            result[i] += "; "
            for fd in FDs:
                result[i] += fd + ", "
            result[i] = result[i][:-2]
            print("Results now include: ", result)
            i += 1
                
    return list(dict.fromkeys(result))
    
def _3NF_synth(F, L):
    result = []
    M = minimal_basis(F)
    T = []
    
    for fd in M:
        lrhs = fd.split("->")
        added = False
        for i in range(len(T)):
            if lrhs[0] == T[i].split("->")[0]:
                T[i] += lrhs[1]
                added = True
                break
        if not added:
            T.append(fd)
                
    
    
    for fd in T:
        lrhs = fd.split("->")
        result.append(lrhs[0] + lrhs[1])
        
    for r in result:
        Xplus = closure(r, F)
        super_key = True
        for i in L:
            if i not in Xplus:
                super_key = False
                break
                
        if super_key:
            return result
            
    result.append(find_keys(F, L, False)[0])
    return result
    
def find_keys(F, R, super):
    result = []
    for i in range(1, len(R) + 1):
        for j in itertools.product([0,1], repeat=len(R)):
            if sum(list(j)) == i:
                X = ""
                for k in range(len(R)):
                    if j[k]:
                        X += R[k]
                Xplus = closure(X, F)
                print("Trying key:", X, ". Closure(", X, ") =", Xplus)
                key = True
                for k in R:
                    if k not in Xplus:
                        key = False
                        break
                        
                if key:
                    if not super:
                        for r in result:
                            if not key:
                                break
                            key = False
                            for char in r:
                                if char not in X:
                                    key = True
                                    break
                                    
                    if key:
                        print(X, "is a key")
                        result.append(X);
                                   
    return result
if __name__ == '__main__':
    main()