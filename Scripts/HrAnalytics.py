##Exploring the RDD syntax and data frames

from __future__ import print_function

import sys
from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.sql import HiveContext
from pyspark.sql.functions import when
from pyspark.sql import functions as F
from pyspark.sql.types import DoubleType
import numpy as np
import pandas as pd 

#import numpy as np


sc = SparkContext(appName="testingSql")
sqlContext = HiveContext(sc)

log4j = sc._jvm.org.apache.log4j
log4j.LogManager.getRootLogger().setLevel(log4j.Level.ERROR)
# Create a dataframe from a Hive query
df = sqlContext.sql("""SELECT * FROM hr.hr_analytics""")
pdf = df.toPandas()
print(pdf.describe())

pdf['left'] = pdf.loc[pdf.left == 0, 'left'] = 'No'
pdf['left'] = pdf.loc[pdf.left == 1, 'left'] = 'Yes'

print(pdf.head())
print(pdf.dtypes)

numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
newdf = pdf.select_dtypes(include=numerics)
allcolumns  = list(newdf.columns.values)
for i in allcolumns:
	if (str(i) == 'work_accident' or str(i) == 'promotion_last_5years'):
		continue
	print (i)	
	nameIs = str(i)  + '_norm'
	pdf[nameIs] = (pdf[i] - pdf[i].mean())/pdf[i].std(ddof=0)


print(pdf.describe())



