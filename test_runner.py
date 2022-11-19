from LocalSearchAlgorithm import create_json
import LocalSearchAlgorithm
import os
import CCO
import json

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

	input_count = 5

	create_multi_input_files(test_input_path, input_count, 3)

	for i in range(input_count):
		run_alg("{}/input_{}.json".format(test_input_path, i), "{}/output_{}.json".format(test_output_path, i))

def main():
	test_3_comp()

if __name__ == "__main__":
    main()
