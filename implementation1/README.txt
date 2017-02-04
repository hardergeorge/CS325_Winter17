There are several options to run the script

To run a specific algorithm on an input file use:
$python implementation1.py {algorithm name} {input file name}

Where algorithm name is one of: bruteforce, naive-dnc, enhanced-dnc

For example the following will run the brute force algorithm on the points in 'input.txt':
$python implementation1.py bruteforce input.txt

The script will output its results to a file called:
'output_{algorithm name}.txt'

To run all of the algorithms use and have average runtimes displayed to std out use:
$python implementation1.py --run-all {power of ten}

Where power of 10 is an optional argument that allows the algorithms to be run
on a specific input size. If it is omitted all of the algorithms will be run on
10^2, 10^3, 10^4, 10^5 ten times and the timing results averaged. 

For example the following runs all of the algorithms on input size 10^4:
$python implementation1.py --run-all 4

To run just the dnc algorithms and have average runtimes displayed to std out use:
$python implementation1.py --no-bf {power of ten}

Where power of 10 is an optional argument that allows the algorithms to be run
on a specific input size. If it is omitted all of the algorithms will be run on
10^2, 10^3, 10^4, 10^5 ten times and the timing results averaged.

For example the following runs the dnc algorithms on input size 10^5:
$python implementation1.py --no-bf 5

NOTE: This is the recommended scheme for running on input sizes larger than 10^4
as brute-force takes over 20 seconds per iteration at this input size.