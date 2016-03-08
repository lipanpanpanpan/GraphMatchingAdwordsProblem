import sys
import random
import math

if len(sys.argv) != 2:
    print "Please specify which algorithm to run"
    exit(1)
algo = sys.argv[1]

advertisersBudget = []
queriesList = []
queryAdvertiserMap = {}

def main():
    global advertisersBudget
    global queryAdvertiserMap
    global queriesList
    loadData()
    random.seed(0)
    opt = sum(advertisersBudget)
    if algo == 'greedy':
        rev = greedyAlgo(queriesList)
        print "Revenue", rev
        ratios = []
        for x in range(100):
            random.shuffle(queriesList)
            ratios.append(greedyAlgo(queriesList)/opt)
        compRatio = min(ratios)
        print "Competitve ratio", format(compRatio, '.2f')


    elif algo == 'mssv':
        
        rev = mssvAlgo(queriesList)
        print "Revenue", rev
        ratios = []
        for x in range(100):
            random.shuffle(queriesList)
            ratios.append(mssvAlgo(queriesList)/opt)
        compRatio = min(ratios)
        print "Competitve ratio", format(compRatio, '.2f')
        
        
        
    else:
        
        rev = balanceAlgo(queriesList)
        print "Revenue", rev
        ratios = []
        for x in range(100):
            random.shuffle(queriesList)
            ratios.append(balanceAlgo(queriesList)/opt)
        compRatio = min(ratios)
        print "Competitve ratio", format(compRatio, '.2f')
        
        
        
            
def loadData():
    with open('bidder_dataset.csv', 'r') as f:
        next(f)
        for line in f:
            temp = line.split(',')
            if len(temp[3].strip()) > 0:
                advertisersBudget.append(float(temp[3].strip()))
            k = temp[1].strip()    
            if k in queryAdvertiserMap:
                # add advertiser id and corresponding bid value
                queryAdvertiserMap[k].append((int(temp[0].strip()), float(temp[2].strip())))
            else:
                queryAdvertiserMap[k] = []
                queryAdvertiserMap[k].append((int(temp[0].strip()), float(temp[2].strip())))
    f.close()
    with open('queries.txt', 'r') as f:
        for line in f:
            queriesList.append(line.strip())
    f.close()        



def greedyAlgo(queries):
    revenue = 0
    qcnt = 0
    adBudget = advertisersBudget[:] # clone the budget
    for query in queries:
        qcnt = qcnt + 1
        #print "Query...................", qcnt
        advs = queryAdvertiserMap[query]
        advs = sorted(advs, key=lambda x: x[1], reverse = True)
        i = 0
        while i < len(advs):
            t = advs[i]
            if adBudget[t[0]] >= t[1]:
                adBudget[t[0]] = adBudget[t[0]] - t[1]
                revenue = revenue + t[1]
                break
            else:
                i = i+1

    return revenue            


        
def mssvAlgo(queries):
    revenue = 0
    qcnt = 0
    adBudget = advertisersBudget[:] # clone the budget
    for query in queries:
        qcnt = qcnt + 1
        #print "Query...................", qcnt
        a = queryAdvertiserMap[query]
        advs = a[:]
        advsWithFrac = map(lambda x: (x[0], x[1]*(1-math.exp((advertisersBudget[x[0]] - adBudget[x[0]])/advertisersBudget[x[0]] - 1))), advs)
        advsWithFrac = sorted(advsWithFrac, key=lambda x: x[1], reverse = True)
        b = map(lambda x: x[0], advsWithFrac)
        advs.sort(key=lambda x: b.index(x[0])) # to sort the advs list based on the advsWithFrac list
        i = 0
        while i < len(advsWithFrac):
            t = advsWithFrac[i]
            if adBudget[t[0]] >= advs[i][1]:
                adBudget[t[0]] = adBudget[t[0]] - advs[i][1]
                revenue = revenue + advs[i][1]
                break
            else:
                i = i+1

    return revenue  
	 		

def balanceAlgo(queries):
    revenue = 0
    qcnt = 0
    adBudget = advertisersBudget[:] # clone the original budget
    for query in queries:
        qcnt = qcnt + 1
        #print "Query...................", qcnt
        a = queryAdvertiserMap[query]
        advs = a[:]
        advsWithUnspent = map(lambda x: (x[0], adBudget[x[0]]), advs)
        advsWithUnspent = sorted(advsWithUnspent, key=lambda x: x[1], reverse = True)
        b = map(lambda x: x[0], advsWithUnspent)
        advs.sort(key=lambda x: b.index(x[0])) # to sort the advs list based on the advsWithUnspent list
        i = 0
        while i < len(advsWithUnspent):
            t = advsWithUnspent[i]
            if adBudget[t[0]] >= advs[i][1]:
                adBudget[t[0]] = adBudget[t[0]] - advs[i][1]
                revenue = revenue + advs[i][1]
                break
            else:
                i = i+1

    return revenue  

if __name__ == "__main__":
	main()
