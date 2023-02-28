from LocalSearchAlgorithm import create_json, MO_comb_optimizer, makeGraph
import LocalSearchAlgorithm
import os
import CCO
import json

import numpy as np

import LocalSearchAlgorithm.MO_comb_optimizer

from LocalSearchAlgorithm.comb_optimizer import DevelopMode, GetNextMode, GetStartNodeMode
from LocalSearchAlgorithm.create_json import create_multi_input_files


def run_alg(test_input_path, test_output_path):
	print(os.getcwd())
	config_file_path = "config_file.json"
	file1 = open(config_file_path)
	config_file = json.load(file1)
	candidate_list_size = config_file["Candidate list size"]
	time_per_region = config_file["Time per region"]
	proportion_amount_node_sons_to_develop = config_file["Proportion amount node/sons"]
	verbose = True if config_file["Verbose"] == "True" else False
	INPUT_FILE = test_input_path
	OUTPUT_FILE = test_output_path
	brute_force = True if config_file["Brute Force"] == "True" else False
	time_until_early_stop = config_file["time_until_early_stop"]
	ALG_PARAMETERS = {
		"candidate_list_size": candidate_list_size,
		"time_per_region": time_per_region,
		"exploitation_score_price_bias": 0.5,
		"exploration_score_depth_bias": 1.0,
		"exploitation_bias": 0.2,
		"sql_path": "Run_Statistic.sqlite3",
		"verbose": verbose,
		"develop_mode": DevelopMode.PROPORTIONAL,
		"proportion_amount_node_sons_to_develop": proportion_amount_node_sons_to_develop,
		"get_next_mode": GetNextMode.STOCHASTIC_ANNEALING,
		"get_starting_node_mode": GetStartNodeMode.RANDOM,
		"time_until_early_stop": time_until_early_stop
	}

	CCO.run_optimizer(brute_force, INPUT_FILE, OUTPUT_FILE, config_file_path, **ALG_PARAMETERS)


def test_3_comp():
	print(os.getcwd())
	test_dir_path = "LocalSearchAlgorithm/test3"
	test_input_path = test_dir_path + "/input"
	test_output_path = test_dir_path + "/output"
	os.makedirs(test_dir_path, exist_ok=True)
	os.makedirs(test_input_path, exist_ok=True)
	os.makedirs(test_output_path, exist_ok=True)

	input_count = 1

	create_multi_input_files(test_input_path, 1, 10)

	for i in range(input_count):
		run_alg("{}/input_{}.json".format(test_input_path, i), "{}/output_{}.json".format(test_output_path, i))

def mo(input_count, comp_num):
	test_dir_path = f"LocalSearchAlgorithm/test{comp_num}"
	test_input_path = test_dir_path + "/input"
	test_output_path = test_dir_path + "/output"
	os.makedirs(test_dir_path, exist_ok=True)
	os.makedirs(test_input_path, exist_ok=True)
	os.makedirs(test_output_path, exist_ok=True)

	create_multi_input_files(test_input_path, input_count, comp_num)

	for i in range(input_count):
		mocomb_optimizer = MO_comb_optimizer.MOCombOptimizer()
		mocomb_optimizer.run_mo_alg("{}/input_{}.json".format(test_input_path, i), "{}/output_{}.json".format(test_output_path, i))

def mo_pareto(input_count, comp_num):
	test_dir_path = f"LocalSearchAlgorithm/test{comp_num}_pareto_set"
	test_input_path = test_dir_path + "/input"
	test_output_path = test_dir_path + "/output"
	os.makedirs(test_dir_path, exist_ok=True)
	os.makedirs(test_input_path, exist_ok=True)
	os.makedirs(test_output_path, exist_ok=True)

	create_multi_input_files(test_input_path, input_count, comp_num)

	for i in range(input_count):
		mocomb_optimizer = MO_comb_optimizer.MOCombOptimizer()
		mocomb_optimizer.run_mo_pareto_set("{}/input_{}.json".format(test_input_path, i), "{}/output_{}.json".format(test_output_path, i))




def main():
	input_count = 4
	comp_num = 100
	#mo(input_count, comp_num)
	#makeGraph.make_graph_one_for_each_freq(input_count, comp_num)

	mo_pareto(input_count, comp_num)
	makeGraph.make_graph_one_for_each_freq_pareto(input_count, comp_num)

	#y0=1931
	#y1=1663+y0
	#y2=1055+y1
	#y3=513+y2
	#y4=1307+y3

	#for i in range(5):
		#makeGraph.make_graph_avg_freq(139, i, True, False)

	#makeGraph.make_graph([0, 1, 2, 3, 4], [1931, 1663, 1055, 513, 1307])
	#makeGraph.make_graph([0, 1, 2, 3, 4], [y0, y1, y2, y3, y4])

	#test_3_comp()

if __name__ == "__main__":
    main()
