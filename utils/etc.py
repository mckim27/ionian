#! /usr/bin/python
# -*- coding: utf-8 -*-

import traceback
import decimal
import json


# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if abs(o) % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


def get_pretty_traceback():
	lines = traceback.format_exc().strip().split('\n')
	rl = [lines[-1]]
	lines = lines[1:-1]
	lines.reverse()
	for i in range(0,len(lines),2):
		rl.append('^\t%s at %s' % (lines[i].strip(),lines[i+1].strip()))
	return '\n'.join(rl)