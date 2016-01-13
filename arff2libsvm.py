import sys

if (len(sys.argv) < 6):
	raise ValueError('python arff2libsvm.py [inputfile] [outputfile] [num_nominal] [num_numeric] [num_labels]')
	

fin = open(sys.argv[1], 'r')

fout = open(sys.argv[2], 'a')

enum = int(sys.argv[3])
numeric = int(sys.argv[4])
num_fea = enum + numeric
num_labels = int(sys.argv[5])

reading_data = False

features = []
labels = []

line_num = 0
meet_first_label = False
for line in fin.readlines():
	line_num += 1
	#print line
	if len(line) < 2:
		continue
	if not reading_data:
		if line.startswith('@relation'):
			continue
		
		if line.startswith('@data'):
			reading_data = True
			if len(features) != num_fea:
				raise ValueError('incompatible feature size, get ' + str(len(features)) + ', should be ' + str(num_fea) )
			if len(labels) != num_labels:
				raise ValueError('incompatible label size, get ' + str(len(labels)) + ', should be ' + str(num_labels) )
			continue
		
		if line.startswith('@attribute'):
			tokens = line.split(' ')
			if len(tokens) != 3:
				raise ValueError('Wrong number of attribute at line '+str(line_num))		
			if tokens[1].startswith('tag_') or tokens[1].startswith('TAG_'):
				#should be a label
				meet_first_label = True
				if (enum != 0) or (numeric != 0):
					raise ValueError('need ' + str(enum) + 'more nominal and ' + str(numeric) + ' numeric features')
				if len(features) != num_fea:
					raise ValueError('incompatible feature size, get ' + str(len(features)) + ', should be ' + str(num_fea) )
				labels.append(tokens[1])
			else:
				if len(features) < num_fea:
					#should be a feature
					if (meet_first_label):
						raise ValueError('Feature after label at line '+str(line_num))	
					if tokens[2].startswith('{0,1}'):
						enum -= 1
					elif tokens[2].startswith('numeric'):
						numeric -= 1
					else:
						raise ValueError('Feature of unknown type at line '+str(line_num))
					features.append(tokens[1])
				else:
					#should be a label
					if tokens[1].startswith('{0,1}'):
						meet_first_label = True
						if (enum != 0) or (numeric != 0):
							raise ValueError('need ' + str(enum) + 'more nominal and ' + str(numeric) + ' numeric features')
						labels.append(tokens[1])
					else:
						raise ValueError('Unknown label type at line ' + str(line_num))
		else:
			raise ValueError('Wrong Input Format at line '+str(line_num))
	else:
		#should be data
		line = line.replace('{', '')
		line = line.replace('}', '')
		line = line.replace('\n', '')
		tokens = line.split(',')
		output_line = ''
		found_label=False
		found_feature=False
		for token in tokens:
			coordinate_value = token.split(' ')
			if len(coordinate_value) != 2:
				raise ValueError('Wrong Data Format at line '+str(line_num))
			if ('.' in coordinate_value[0]):
				raise ValueError('Coorindates shouldn\'t be numerical at line '+str(line_num))
			coor = int(coordinate_value[0])
			val = float(coordinate_value[1])
			if coor < num_fea:
				found_feature = True
				# this is a feature
				output_line = output_line + ' ' + features[coor] + ':' + str(val)
			elif coor < num_fea + num_labels:
				# this is a label
				if found_label:
					output_line = ',' + output_line
				output_line = labels[coor - num_fea] + output_line
				found_label = True
			else:
				raise ValueError('Coorindates out of range at line '+str(line_num))
		if (not found_label) and (not found_feature):
			raise ValueError('Empty line at line '+str(line_num))
		if not found_label:
			output_line = ' ' + output_line
		if not found_feature:
			raise ValueError('No feature at line '+str(line_num))
		fout.write(output_line+'\n')

fin.close()
fout.close()
	
