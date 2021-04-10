# API
# done
import re


def main(self, inp_data, context_type, operation):
	data = inp_data.replace(' ', '')

	if data == 'all':  # filter special cases
		if context_type == 'components' and operation == 'load':
			if self.config.scout_values['Windows'][0] == 'True':
				return {"status": "ok", "message": "Generator ID formatting successful", "data": [str(i) for i in list(self.config.win_components.keys())]}
			else:
				return {"status": "ok", "message": "Generator ID formatting successful", "data": [str(i) for i in list(self.config.lin_components.keys())]}
		elif operation == 'unload':
			return {"status": "ok", "message": "Generator ID formatting successful", "data": ['all']}
		elif context_type == 'encoders' and operation == 'load':
			return {"status": "ok", "message": "Generator ID formatting successful", "data": list(self.config.encoders.keys())}
		elif context_type == 'bases':
			if self.config.scout_values['Windows'][0] == 'True':
				return {"status": "ok", "message": "Generator ID formatting successful", "data": list(self.config.win_bases.keys())}
			else:
				return {"status": "ok", "message": "Generator ID formatting successful", "data": list(self.config.lin_bases.keys())}
	# Actual formatting occurs here

	invalid_term = False
	output_list = []  # final list of individual sorted values
	ranges = []  # ranges to process later
	non_ranges = []
	inp_data = inp_data.strip()  # strip input data of all leading and ending whitespace
	data = inp_data.split(',')  # split by comma
	for i in range(len(data)):
		data[i] = data[i].strip()
	if context_type == 'components' or context_type == "bases":
		data = list(set(data))  # remove all duplicates after comma split

	for i in data:
		if re.match('^[0-9]+\-[0-9]+$',i):  # initialize regex match to format of range IDs, matches "positive number-positive number"
			ranges.append(i)
		else:
			non_ranges.append(i)
	# process non ranges first
	for i in non_ranges:
		try:
			output_list.append(int(i))
		except:
			invalid_term = True  # indicate formatting error
			break
	if invalid_term and output_list:  # we hit an error however we still hit a match indicating invalid format
		self.log.err('Invalid generator ID formatting : String detected while sorting for integer IDs')
		return {"status": "error", "message": "String detected while sorting for integer IDs", "data": []}
	elif invalid_term and not output_list and not ranges:  # nothing in non ranges is an integer and there are no proper ranges meaning string based input only
		self.log.err('Generator found no IDs')
		if type(inp_data) is list:
			return {"status": "error", "message": "Generator found no IDs", "data": inp_data}
		return {"status": "error", "message": "Generator found no IDs", "data": [inp_data]}  # most probably a direct call for the component which we return

	# ERROR OUTPUT_LIST BOOLEAN CHEATSHEET
	# error and non zero output_list TT -> indicates that in non range some are ints others are not which is invalid formatting
	# no error and zero output_list FF -> not possible due to the nature of try: except, one or the other happens
	# error and zero output_list TF -> indicates that nothing in non ranges is an integer meaning string only or range only formatting
	# no error and non zero output_list FT -> indicates that everything in non ranges is integer

	# iterate range values to add to output
	try:
		for i in ranges:
			f_val, s_val = i.split('-', 1)
			# even if f_val and s_val are non zero numbers that start with digit 0, INTing them normalizes it
			f_val = int(f_val)
			s_val = int(s_val)
			# f_val and s_val are never negative since regex matches "positive number-positive number"
			if f_val > s_val:
				self.log.err('Invalid generator ID formatting : First range value is larger than second range value')
				return {"status": "error", "message": "First range value is larger than second range value", "data": []}
			else:  # 0 < f < s
				mini_range = list(range(f_val, s_val + 1))  # add 1 to account for the final val
				output_list += mini_range  # fill each value in range of f and s into output
	except OverflowError:
		self.log.err('Range value is too large')
		return {"status": "error", "message": "Range value is too large", "data": []}
	if context_type == 'components' or context_type == 'bases':
		output_list = list(set(output_list))  # remove all duplicates in the range addition section ^
		output_list.sort()  # sort for better eyecandy when loading components
	self.log.pos('Generator ID formatting successful')
	if type(output_list) is list:
		return {"status": "ok", "message": "Generator ID formatting successful", "data": output_list}
	return {"status": "ok", "message": "Generator ID formatting successful", "data": [output_list]}
