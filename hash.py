import sys

fin = open(sys.argv[1], 'r')
fout = open(sys.argv[2], 'w')

hD = dict()
countD = 0
print 'converting file...'
for l in fin.readlines():
	tokens = l.split()
	fout.write(tokens[0])
	for j in range(1, len(tokens)):
		xy = tokens[j].split(':')
		x = xy[0]
		hd = hD.get(x, 0)
		if hd == 0:
			countD += 1
			hD.update({x:countD})
		hd = hD.get(x, 0)
		fout.write(' '+str(hd)+":"+xy[1])
	fout.write('\n')
fin.close()
fout.close()

