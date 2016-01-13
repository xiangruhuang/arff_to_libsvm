import sys
import re

fin = open(sys.argv[1], 'r')

fout = open(sys.argv[2], 'w')

reading_data = False

features = []
labels = []
num_fea = 0
num_labels = 0

line_num = 0
for line in fin.readlines():
	line_num += 1
	if len(line) < 2:
		continue

	if not reading_data:
		if line.startswith('@relation'):
			continue
		if line.startswith('@data'):
			reading_data = True
			num_fea = len(features)
			num_labels = len(labels)
		elif line.startswith('@attribute'):
			tokens = line.split(' ')
			if len(tokens) > 2:
				if tokens[2].startswith('{0,1}'):
					#should be a label
					labels.append(tokens[1])
				elif tokens[2].startswith('numeric'): 
					#should be a feature
					features.append(tokens[1])
			else:
				raise ValueError('Wrong attribute at line '+str(line_num))
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
				output_line = output_line + ' ' + str(coor) + ':' + str(val)
			elif coor < num_fea + num_labels:
				# this is a label
				if found_label:
					output_line = ', ' + output_line
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
	
