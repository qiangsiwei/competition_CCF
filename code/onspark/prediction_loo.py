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

# 预测
######## 数据准备 ########
# import fileinput
# for p in range(1,4):
# 	file_y1 = open("../../data/feature_extracted_class"+str(p)+"_y1.txt","w")
# 	file_y2 = open("../../data/feature_extracted_class"+str(p)+"_y2.txt","w")
# 	for line in fileinput.input("data/feature_extracted_class"+str(p)+".txt"):
# 		part = line.strip().split("\t")
# 		y1, y2 = 1 if int(part[2])!=0 else 0, part[2]
# 		file_y1.write(str(y1)+" "+" ".join([str(i+1)+":"+part[3:][i] for i in xrange(len(part[3:]))])+"\n")
# 		file_y2.write(str(y2)+" "+" ".join([str(i+1)+":"+part[3:][i] for i in xrange(len(part[3:]))])+"\n")
# 	fileinput.close()
# 	file_y1.close()
# 	file_y2.close()
######## 数据准备 ########

from sklearn.cross_validation import LeaveOneOut
from sklearn.cross_validation import KFold

# LeaveOneOut
if __name__ == "__main__":
	sc = SparkContext('local',appName="Prediction")
	import fileinput
	data_y1, data_y2 = [], []
	for line in fileinput.input("data/feature_extracted_class3.txt"):
		data_y1.append(LabeledPoint(float(1 if int(line.split("\t")[2])!=0 else 0), [float(i) for i in line.split("\t")[3:]]))
		data_y2.append(LabeledPoint(int(line.split("\t")[2]), [float(i) for i in line.split("\t")[3:]]))
	total, right, mse = 0, 0, []
	loo = LeaveOneOut(len(data_y1))
	for train, test in loo:
		data_train_y1, data_train_y2 = [], []
		for i in train:
			data_train_y1.append(data_y1[i])
			data_train_y2.append(data_y2[i])
		clf1 = DecisionTree.trainClassifier(sc.parallelize(data_train_y1), numClasses=2, categoricalFeaturesInfo={}, impurity='gini', maxDepth=5, maxBins=100)
		clf2 = DecisionTree.trainRegressor(sc.parallelize(data_train_y2), categoricalFeaturesInfo={}, impurity='variance', maxDepth=5, maxBins=100)
		r1 = clf1.predict(data_y1[test].features)
		r2 = clf2.predict(data_y2[test].features)
		if r1 == data_y1[test].label:
			right += 1
		mse.append(abs(r2-data_y2[test].label))
		total += 1
	print float(right)/total, sum(mse)/len(mse)
