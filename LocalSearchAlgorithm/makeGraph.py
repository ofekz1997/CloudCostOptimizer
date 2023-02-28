import matplotlib.pyplot as plt
import json
import numpy as np


def make_graph(x_points, y_points, label):
	plt.scatter(x_points, y_points, label=label)
	plt.legend()
	plt.show()


def make_graph(x_points, y_points):
	plt.scatter(x_points, y_points)
	plt.show()

def make_graph_one_for_each_freq(files_num, comp_num):
	x_points = [0, 1, 2, 3, 4]
	y_points = [0, 0, 0, 0, 0]
	#y_points = []
	#x_points= []

	for i in range(files_num):
		for freq in range(5):
			current_file_name = "LocalSearchAlgorithm/test{}/output/output_{}.json_{}.json".format(comp_num, i, freq)
			current_file = open(current_file_name)
			current_file_dict = json.load(current_file)
			price = current_file_dict[0]["price"]
			#x_points += [freq]
			#y_points += [price]
			y_points[freq] += price / files_num

	plt.scatter(x_points, y_points)
		#x_points = []
		#y_points = []

	plt.show()

def make_graph_one_for_each_freq_pareto(files_num, comp_num):
	x_points = [0, 1, 2, 3, 4]
	points_counter = [0, 0, 0, 0, 0]
	y_points = [0, 0, 0, 0, 0]

	#y_points = []
	#x_points = []

	for i in range(files_num):
		for freq in range(5):
			current_file_name = "LocalSearchAlgorithm/test{}_pareto_set/output/output_{}.json".format(comp_num, i)
			current_file = open(current_file_name)
			current_file_dict = json.load(current_file)
			price = get_best_price_of_freq(current_file_dict, freq)
			if price != np.inf:
				y_points[freq] += price
				points_counter[freq] += 1

			#x_points += [freq]
			#y_points += [price]
			#y_points[freq] += price / files_num

	for freq in range(5):
		if points_counter[freq] != 0:
			y_points[freq] /= points_counter[freq]




	plt.scatter(x_points, y_points)
		#x_points = []
		#y_points = []

	plt.show()

def get_best_price_of_freq(current_file_dict, freq):
	min_price = np.inf
	for solution in current_file_dict:
		if (get_interruption_rate(solution) == freq):
			min_price = min(min_price, solution["price"])

	return min_price




def get_interruption_rate(solution):
	max_ir = 0
	for instance in solution["instances"]:
		max_ir = max(max_ir, instance["interruption_frequency_filter"])

	return round(max_ir)

def make_graph_avg_freq(files_num, freq, is_comp_num, is_price):
	x_points = [0, 1, 2, 3, 4]
	y_points = [0, 0, 0, 0, 0]
	#y_points = []
	#x_points= []

	for i in range(files_num):
		current_file_name = "LocalSearchAlgorithm/test3/output/output_{}.json_{}.json".format(i, freq)
		current_file = open(current_file_name)
		current_file_dict = json.load(current_file)
		instances_list = current_file_dict[0]["instances"]
		instance_comps = [0, 0, 0, 0, 0]
		for instance in instances_list:
			if is_comp_num:
				comp_num = len(instance["components"])
			elif is_price:
				comp_num = instance["spot_price"] / len(instance["components"])
			instance_freq = instance["interruption_frequency_filter"]
			instance_comps[round(instance_freq)] += comp_num

		instance_comps_sum = sum(instance_comps)
		if is_price:
			instance_comps_sum = 1

		for i in range(5):
			instance_comps[i] /= instance_comps_sum
			y_points[i] += instance_comps[i] / files_num

		#x_points += [freq]
		#y_points += [price]


	plt.scatter(x_points, y_points)
		#x_points = []		#y_points = []

	plt.show()

	def make_graph_avg_price_freq_data():
		x_points = [0, 1, 2, 3, 4]
		y_points = [0, 0, 0, 0, 0]
		# y_points = []
		# x_points= []


		current_file_name = "AWSData/ec2_data_Linux.json"
		current_file = open(current_file_name)
		current_file_dict = json.load(current_file)
		region = current_file_dict["us-east-2"]
		instance_comps = [0, 0, 0, 0, 0]
		for instance in instances_list:
			if is_comp_num:
				comp_num = len(instance["components"])
			elif is_price:
				comp_num = instance["spot_price"] / len(instance["components"])
			instance_freq = instance["interruption_frequency_filter"]
			instance_comps[round(instance_freq)] += comp_num

		instance_comps_sum = sum(instance_comps)
		if is_price:
			instance_comps_sum = 1

		for i in range(5):
			instance_comps[i] /= instance_comps_sum
			y_points[i] += instance_comps[i] / files_num

		# x_points += [freq]
		# y_points += [price]

		plt.scatter(x_points, y_points)
		# x_points = []		#y_points = []

		plt.show()