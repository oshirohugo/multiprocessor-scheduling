#!/usr/bin/env python

import sys
from random import uniform

if len(sys.argv) < 2:
    print "Usage: %s <number-of -processes>" % sys.argv[0]
    sys.exit(1)

n_of_jobs = int(sys.argv[1])
output_file = "loading-balance-" + str(n_of_jobs) + ".txt"

f = open(output_file, "w")

time_lower_limit = 0.1
time_upper_limit = 10.0

job = 0
while job < n_of_jobs:
    time = uniform(time_lower_limit, time_upper_limit)
    f.write(str.format("{0:.2f}", time) + "\n")
    job += 1
