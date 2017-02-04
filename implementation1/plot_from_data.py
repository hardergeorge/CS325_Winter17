import matplotlib.pyplot as plt

input_size = [100, 1000, 10000, 100000]
naive_runtimes = [0.0005019187927246093, 0.0061203956604003905, 0.0753028392791748, 1.0836293935775756]
brute_runtimes = [0.0024158716201782226, 0.24549858570098876, 24.99395878314972, 250]
enhanced_runtimes = [0.0004446983337402344, 0.006568312644958496, 0.08116977214813233, 1.3273457050323487]

ax = plt.gca()

ax.scatter(input_size, naive_runtimes, c='b', label='naive')
ax.scatter(input_size, enhanced_runtimes, c='g', label='enhanced')
ax.scatter(input_size, brute_runtimes, c='r', label='bruteforce')
ax.set_xlim([0, 100005])
ax.set_ylim([0, 1.5])
ax.set_xlabel("Input size to closest pair of points algorithms")
ax.set_ylabel("Average runtime of algorithms, in seconds")

plt.legend(loc="upper left")

plt.show()