import json 

def read(path_to_file):
	with open(path_to_file) as f:
		data = json.load(f)
	return data

def write(path_to_file, data):
	with open(path_to_file, 'w') as f:
		json.dump(data, f)