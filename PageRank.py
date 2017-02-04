import math

P = []  # P is set of all pages
S = []  # S is set of sink nodes
M = {}  # M[p] is set of pages that link to p
L = {}  # L[q] is number of out-links from page q
d = 0.85  # d is the PageRank teleportation factor
newPR = {}
PR = {}


def file_len(filename):
    with open(filename) as f:
        for i, l in enumerate(f):
            pass
    f.close()
    return i + 1


def page_rank(filename):
    N = file_len(filename)

    # calculate P and M
    f = open(filename, "r+")
    line = f.readlines()
    for i in line[0:N]:
        ele = str(i).strip()
        ele_list = []
        ele_list = ele.split()
        key = ele_list[0]
        P.append(key)
        M[key] = list(set(ele_list[1:]))
    f.close()

    # calculate L
    for i in P:
        inlinks_list = M[i]
        for word in inlinks_list:
            if word in L:
                L[word] += 1
            else:
                L[word] = 1

    # calculate S
    S = (list(set(M.keys()) - set(L.keys())))

    for p in P:
        PR[p] = 1.0 / N

    perplexity = 0
    counter = 0

    while counter < 4:
        prev_perplexity = perplexity
        sinkPR = 0

        for s in S:
            sinkPR += PR[s]

        for p1 in P:
            newPR[p1] = (1.0 - d) / N
            newPR[p1] += (d * sinkPR) / N
            for q in M[p1]:
                newPR[p1] += (d * PR[q]) / L[q]

        for p2 in P:
            PR[p2] = newPR[p2]

        sumPR = 0
        for i in P:
            sumPR += PR[i] * math.log(PR[i], 2)

        perplexity = math.pow(2, -sumPR)
        if abs(prev_perplexity - perplexity) < 1:
            counter += 1
        else:
            counter = 0

    # Write Page Rank into a file
    f1 = open('PageRank.txt', 'w')
    for i in sorted(PR, key=PR.get, reverse=True):
        f1.write(str(i) + " " + str(PR[i]) + "\n")
    f1.close()


# Give In-link file name to page_rank function
page_rank('G1-Inlinks.txt')
