'''
This code is part of the publication "Who Let The Trolls Out? Towards Understanding State-Sponsored Trolls" (https://arxiv.org/abs/1811.03130).
If you use this code please cite the publication.
'''

import pigeo
import sys
pigeo.load_model()

inp = sys.argv[1]
out = sys.argv[2]


locations = []
with open(inp, 'r') as f:
	for line in f:
		locations.append(line.replace('\n', ''))


results = pigeo.geo(locations)

with open(out, 'w') as f:
	for res in range(len(results)):
		results[res]['requested_location'] = locations[res]
		f.write(json.dumps(results[res]).encode('utf-8') + '\n')

