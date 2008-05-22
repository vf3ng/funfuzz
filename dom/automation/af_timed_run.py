#!/usr/bin/env python -u

import sys, random, time
import detect_assertions, detect_leaks, detect_malloc_errors
sys.path.append("../../lithium/")
import ntr



def many_timed_runs(fullURLs):
    
    for iteration in range(0, len(fullURLs)):
        fullURL = fullURLs[iteration]
        # print "URL: " + URL
        logPrefix = "w%d" % iteration
        (sta, msg, elapsedtime) = ntr.timed_run(sys.argv[3:] + [fullURL], int(sys.argv[1]), logPrefix)
        
        print "%s: %s (%.1f seconds)" % (logPrefix, msg, elapsedtime)
        
        if sta == ntr.CRASHED:
            print "Approximate crash time: " + time.asctime()

        amissAssert = detect_assertions.amiss(logPrefix)
        amissLeak = detect_leaks.amiss(logPrefix)
        amissMalloc = detect_malloc_errors.amiss(logPrefix)
        
        if ((sta == ntr.CRASHED) or (sta == ntr.ABNORMAL) or amissAssert or amissLeak or amissMalloc):
             print fullURL
             for line in file(logPrefix + "-out"):
                 if line.startswith("Chosen"):
                     print line
             print ""
             print ""
             

def getURLs():
    URLs = []
    fullURLs = []
    
    urlfile = open(sys.argv[2], "r")
    for line in urlfile:
        if (not line.startswith("#") and len(line) > 2):
            URLs.append(line.rstrip())
            
    plan = file("wplan", 'w')

    for iteration in range(0, 10000):
        metaSeed = random.randint(1, 10000)
        metaPer = random.randint(0, 15) * random.randint(0, 15) + 5
        u = random.choice(URLs) + "#squarefree-af!fuzzer-combined.js!" + str(metaSeed) + ",0," + str(metaPer) + ",10,3000,0"
        fullURLs.append(u)
        plan.write("w" + str(iteration) + " = " + u + "\n")
    
    plan.close()
    
    return fullURLs


if len(sys.argv) >= 4:
    many_timed_runs(getURLs())
else:
    print "Not enough command-line arguments"
    print "Usage: ./af_timed_run.py timeout urllist firefoxpath [firefoxargs ...]"
