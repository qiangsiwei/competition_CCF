# -*- coding: utf-8 -*- 

import re
import sys
import time
import math
from operator import add
from pyspark import SparkContext
from pyspark.mllib.util import MLUtils
from pyspark.mllib.tree import DecisionTree
from pyspark.mllib.regression import LabeledPoint

# 独立事件特征抽取
def extract1(line):
	part = line.strip().split("\t")
	event, cls, day = part[0], part[1], int(part[2])
	return (event, (cls, day, part[5]))

def extract2(x):
	event = x[0]
	days = []
	for cont in x[1]:
		cls, day, text = cont
		days.append(day)
		nr_t = None if len(text.split("|")[0][1:-1]) == 0 else [(item.split(":")[0], int(item.split(":")[-1])) for item in text.split("|")[0][1:-1].split(" ")]
		ns_t = None if len(text.split("|")[1][1:-1]) == 0 else [(item.split(":")[0], int(item.split(":")[-1])) for item in text.split("|")[1][1:-1].split(" ")]
		nr_c = None if len(text.split("|")[2][1:-1]) == 0 else [(item.split(":")[0], int(item.split(":")[-1])) for item in text.split("|")[2][1:-1].split(" ")]
		ns_c = None if len(text.split("|")[3][1:-1]) == 0 else [(item.split(":")[0], int(item.split(":")[-1])) for item in text.split("|")[3][1:-1].split(" ")]
		event_map, weight = {"nr_t":{},"ns_t":{},"nr_c":{},"ns_c":{}}, 5
		if nr_t != None:
			for w in nr_t:
				event_map["nr_t"][w[0]] = w[1] if not event_map["nr_t"].has_key(w[0]) else event_map["nr_t"][w[0]]+w[1]
		if ns_t != None:
			for w in ns_t:
				event_map["ns_t"][w[0]] = w[1] if not event_map["ns_t"].has_key(w[0]) else event_map["ns_t"][w[0]]+w[1]
		if nr_c != None:
			for w in nr_c:
				event_map["nr_c"][w[0]] = w[1] if not event_map["nr_c"].has_key(w[0]) else event_map["nr_c"][w[0]]+w[1]
		if ns_c != None:
			for w in ns_c:
				event_map["ns_c"][w[0]] = w[1] if not event_map["ns_c"].has_key(w[0]) else event_map["ns_c"][w[0]]+w[1]
	nr_t = " ".join([item["a"]+":"+str(item["b"]) for item in sorted([{"a":a,"b":b} for a,b in event_map["nr_t"].iteritems()], key=lambda x:x["b"], reverse=True)])
	ns_t = " ".join([item["a"]+":"+str(item["b"]) for item in sorted([{"a":a,"b":b} for a,b in event_map["ns_t"].iteritems()], key=lambda x:x["b"], reverse=True)])
	nr_c = " ".join([item["a"]+":"+str(item["b"]) for item in sorted([{"a":a,"b":b} for a,b in event_map["nr_c"].iteritems()], key=lambda x:x["b"], reverse=True)])
	ns_c = " ".join([item["a"]+":"+str(item["b"]) for item in sorted([{"a":a,"b":b} for a,b in event_map["ns_c"].iteritems()], key=lambda x:x["b"], reverse=True)])
	return (int(event), event+"|"+cls+"|"+str(sorted(days)[0])+"|"+nr_t+"|"+ns_t+"|"+nr_c+"|"+ns_c)

if __name__ == "__main__":
	sc = SparkContext('spark://namenode.omnilab.sjtu.edu.cn:7077',appName="Extract")
	lines = sc.textFile('hdfs://namenode.omnilab.sjtu.edu.cn/user/qiangsiwei/competition_CCF/classified_news.txt', 1)
	counts = lines.map(lambda x : extract1(x)) \
			.groupByKey() \
			.map(lambda x : extract2(x)) \
			.sortByKey() \
			.map(lambda x : x[1])
	output = counts.saveAsTextFile("./competition_CCF/classified_event")
