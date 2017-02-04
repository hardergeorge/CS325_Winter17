from random import random
import math
import sys
import timeit

#helper to calculate distance between two points
def calculate_distance(p1, p2):
	d = math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
	return d

def read_points(filename):
	points = []

	f = open(filename, 'r')

	#reads the file in as a list of tuples to ease manipulation
	for line in f:
		points.append(tuple(map(float, line.split())))

	return points

#helper to sort points based on x or y coords
#pass 0 to the second param to sort on x and 1 to sort on y
def sort_points(points, xy):
	sorted_points = sorted(points, key=lambda tup: tup[xy])
	return sorted_points

#brute force approach to closest pair problem
def brute_force(points):

	minimum = calculate_distance(points[0], points[1])
	min_points = (points[0], points[1])

	#loop over every point and calculate distance between it and all other points
	for i in range(0, len(points) - 1):
		for j in range(i + 1, len(points)):
			if calculate_distance(points[i], points[j]) < minimum:
				minimum = calculate_distance(points[i], points[j])
				min_points = (points[i], points[j])

	return minimum, min_points

def naive_dnc_closest_pair(x_sorted):

	#use brute force on small input
	if len(x_sorted) <= 3:
		min_dist, min_pair = brute_force(x_sorted)
		return min_dist, min_pair
	else:
		#cut the points in half
		x_left = x_sorted[:len(x_sorted)/2]
		x_right = x_sorted[len(x_sorted)/2:]

		#calculate midpoint so that we can find the middle strip later
		x_middle = x_sorted[len(x_sorted)/2][0]

		#recursive function calls
		min_left, min_left_pair = naive_dnc_closest_pair(x_left)
		min_right, min_right_pair = naive_dnc_closest_pair(x_right)

		#set our minimum and minimum pair
		if min_left < min_right:
			minimum = min_left
			minimum_pair = min_left_pair
		else:
			minimum = min_right
			minimum_pair = min_right_pair

		#store the minimum and min pair in new vals because we need to update and check these values later
		closest_dist = minimum
		pair_closest = minimum_pair

		strip = []

		#get the points in the middle strip by scanning the x_sorted list
		for point in x_sorted:
			if abs(x_middle - point[0]) < minimum:
				strip.append(point)

		#sort the points in the middle strip on their x coord
		sorted_strip = sort_points(strip, 1)

		#search the middle strip to see if there is a point closer
		for i in range(len(sorted_strip) - 1):

			j = i + 1

			while j < len(sorted_strip) and (sorted_strip[j][1] - sorted_strip[i][1]) < minimum:

				if calculate_distance(sorted_strip[j], sorted_strip[i]):
					closest_dist = calculate_distance(sorted_strip[j], sorted_strip[i])
					pair_closest = (sorted_strip[j], sorted_strip[i])

				j = j + 1

		return closest_dist, pair_closest


#finds the closest pair of points and their distance from a set of points
def enhanced_dnc_closest_pair(x_sorted, y_sorted):

	#use brute force on small input
	if len(x_sorted) <= 3:
		min_dist, min_pair = brute_force(x_sorted)
		return min_dist, min_pair
	else:
		#cut the x sorted points in half
		x_left = x_sorted[:len(x_sorted)/2]
		x_right = x_sorted[len(x_sorted)/2:]

		#calculate midpoint so that we can split y sorted points in half
		x_middle = x_sorted[len(x_sorted)/2][0]

		y_left = []
		y_right = []

		#split the y sorted points
		for point in y_sorted:
			if point[0] <= x_middle:
				y_left.append(point)
			else:
				y_right.append(point)

		#recursive function calls
		min_left, min_left_pair = enhanced_dnc_closest_pair(x_left, y_left)
		min_right, min_right_pair = enhanced_dnc_closest_pair(x_right, y_right)

		#set our minimum and minimum pair
		if min_left < min_right:
			minimum = min_left
			minimum_pair = min_left_pair
		else:
			minimum = min_right
			minimum_pair = min_right_pair

		#store the minimum and min pair in new vals because we need to update and check these values later
		closest_dist = minimum
		pair_closest = minimum_pair

		y_strip = []

		#grab the points in the middle strip
		for point in y_sorted:
			if abs(x_middle - point[0]) < minimum:
				y_strip.append(point)

		#search the middle strip to see if there is a point closer
		for i in range(len(y_strip) - 1):

			j = i + 1

			while j < len(y_strip) and (y_strip[j][1] - y_strip[i][1]) < minimum:

				if calculate_distance(y_strip[j], y_strip[i]):
					closest_dist = calculate_distance(y_strip[j], y_strip[i])
					pair_closest = (y_strip[j], y_strip[i])

				j = j + 1

		return closest_dist, pair_closest

#helper to call the main enhanced algorithm
def enhanced_closest_pair(points):

	x_sorted = sort_points(points, 0)
	y_sorted = sort_points(points, 1)

	return enhanced_dnc_closest_pair(x_sorted, y_sorted)

def naive_closest_pair(points):

	x_sorted = sort_points(points, 0)

	return naive_dnc_closest_pair(x_sorted)

def pretty_print(points, min_dist):

	sorted_points = sort_points(points, 0)

	return str(min_dist) + '\n' + str(sorted_points[0][0]) + ' ' + str(sorted_points[0][1]) + ' ' + str(sorted_points[1][0]) + ' ' + str(sorted_points[1][1])

def generate_random_points(n):
	points = []

	for i in range(n):
		points.append(((100 * random()), (100 * random())))

	return points

def run_and_time(n):

	set_of_points = []

	for i in range(10):
		set_of_points.append(generate_random_points(10**n))

	brute_times = []
	naive_times = []
	enhanced_times = []

	for points in set_of_points:
		start = timeit.default_timer()
		dmin, min_pair = brute_force(points)
		end = timeit.default_timer()

		brute_times.append((end - start))

		start = timeit.default_timer()
		dmin, min_pair = naive_closest_pair(points)
		end = timeit.default_timer()

		naive_times.append((end - start))

		start = timeit.default_timer()
		dmin, min_pair = enhanced_closest_pair(points)
		end = timeit.default_timer()

		enhanced_times.append((end - start))

	average_times = {}

	average_times['bruteforce'] = sum(brute_times) / len(brute_times)
	average_times['naive'] = sum(naive_times) / len(naive_times)
	average_times['enhanced'] = sum(enhanced_times) / len(enhanced_times)

	return average_times

def run_and_time_no_bf(n):

	set_of_points = []

	for i in range(10):
		set_of_points.append(generate_random_points(10**n))

	naive_times = []
	enhanced_times = []

	for points in set_of_points:

		start = timeit.default_timer()
		dmin, min_pair = naive_closest_pair(points)
		end = timeit.default_timer()

		naive_times.append((end - start))

		start = timeit.default_timer()
		dmin, min_pair = enhanced_closest_pair(points)
		end = timeit.default_timer()

		enhanced_times.append((end - start))

	average_times = {}

	average_times['naive'] = sum(naive_times) / len(naive_times)
	average_times['enhanced'] = sum(enhanced_times) / len(enhanced_times)

	return average_times

def main():

	if len(sys.argv) > 1:
		if str(sys.argv[1]) == '--run-all':
			if len(sys.argv) == 2:
				for i in range(2,6):
					print "Average times for n = 10**" + str(i)
					print run_and_time(i) 
			else:
				print run_and_time(int(sys.argv[2]))
		elif str(sys.argv[1]) == "--no-bf":
			if len(sys.argv) == 2:
				for i in range(2,6):
					print "Average times for n = 10**" + str(i)
					print run_and_time_no_bf(i) 
			else:
				print run_and_time_no_bf(int(sys.argv[2]))
		elif '--' not in str(sys.argv[1]):

			file_points = read_points(str(sys.argv[2]))

			if str(sys.argv[1]) == 'bruteforce':
				dmin, minpair = brute_force(file_points)
			elif str(sys.argv[1]) == 'naive-dnc':
				dmin, minpair = naive_closest_pair(file_points)
			elif str(sys.argv[1]) == 'enhanced-dnc':
				dmin, minpair = enhanced_closest_pair(file_points)
			else:
				print "Sorry! Something went wrong with how you called the script"
				return

			f = open(('output_' + str(sys.argv[1]) + '.txt'), 'w')
			f.write(pretty_print(minpair, dmin))
	else:
		points = generate_random_points(100)

		brute_min, brute_points = brute_force(points)
		print pretty_print(brute_points, brute_min)

		en_close_dist, en_close_pair = enhanced_closest_pair(points)
		print pretty_print(en_close_pair, en_close_dist)

		na_close_dist, na_close_pair = enhanced_closest_pair(points)
		print pretty_print(na_close_pair, na_close_dist)

if __name__ == '__main__':
	main()
