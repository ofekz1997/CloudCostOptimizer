import json
import CCO
from LocalSearchAlgorithm.create_json import *
from multiprocessing import Process

from LocalSearchAlgorithm.comb_optimizer import DevelopMode, GetNextMode, GetStartNodeMode
from LocalSearchAlgorithm.create_json import create_multi_input_files

class MOCombOptimizer:
	def __init__(self):
		pass

	def run_mo_alg(self, test_input_path, test_output_path):
		print(test_input_path)
		procs = []

		for i in range(5):

			input_path_i = "{}_{}_freq.json".format(test_input_path, i)
			change_freq_to_i(i, test_input_path, input_path_i)
			proc = Process(target=self.run_stage_alg, args=(input_path_i, "{}_{}.json".format(test_output_path, i), ))
			procs.append(proc)
			proc.start()
			#self.run_stage_alg(input_path_i, "{}_{}.json".format(test_output_path, i))

		for proc in procs:
			proc.join()

	def run_stage_alg(self, test_input_path, test_output_path):
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

	def run_mo_pareto_set(self, test_input_path, test_output_path):
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
			"is_multi_optimization_search_price_and_interruption_rate": True
		}

		CCO.run_optimizer(brute_force, INPUT_FILE, OUTPUT_FILE, config_file_path, **ALG_PARAMETERS)