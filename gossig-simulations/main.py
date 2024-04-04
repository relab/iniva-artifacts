from committee import Committee
import getopt, sys
from time import gmtime, strftime


if __name__ == '__main__':

    iterations = 1
    colateral = 0
    rounds = 100
    k = 3
    m = 0
    fr = 0
    frmax = 5
    size = 100
    greedyMode = False
    simType = "Byzantine"

    argumentList = sys.argv[1:]
    options = "i:s:m:k:c:"
    long_options = ["iterations=", "size=", "m=", "k=", "colateral="]

    try:
        arguments, values = getopt.getopt(argumentList, options, long_options)

        for currentArgument, currentValue in arguments:

            if currentArgument in ("-i", "--iterations"):
                iterations = int(currentValue)

            elif currentArgument in ("-s", "--size"):
                size = int(currentValue)

            elif currentArgument in ("-m", "--m"):
                m = float(currentValue)

            elif currentArgument in ("-k", "--k"):
                k = int(currentValue)

            elif currentArgument in ("-c", "--colateral"):
                colateral = int(colateral)

    except getopt.error as err:
        # output error, and return with an error code
        print(str(err))

    print("Running {} iterations with size {}, k {}, coallition m {} and colateral {}".format(iterations, size, k, m, colateral))

    print("iterations: {}".format(iterations))
    counts = []
    for k in range(2, 4):
        sumItr = 0
        for itr in range(iterations):
            print (strftime("%H:%M:%S", gmtime()))
            print("Iteration {} with k {}".format(itr,k))
            count = 0
            for i in range(rounds):
                #print (strftime("%H:%M:%S", gmtime()), end="; ")
                #print(str(k) +"-" + str(itr) +"-"+ str(i), end=": ")
                committee = Committee(size, m, fr, frmax, k, greedyMode, simType, colateral)
                canExtract = committee.start()
                if simType == "Byzantine":
                    if canExtract:
                        count += 1
                        #committee.printextracted()
                elif simType == "Freeriding":
                    count += canExtract
                #print("Can extract {}".format(canExtract))

            print()
            print("Count: {}".format(count))
            sumItr += count
        counts.append(sumItr / iterations)

    print("All counts: {}".format(counts))

