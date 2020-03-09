import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class dataColumn:

    def __init__(self, name, isNumeric, dataType):
        self.name = name
        self.isNumeric = isNumeric
        self.dataType = dataType
        print(dataType.name)

    def getDataQuality(self):
        print(self.isNumeric)
        if(self.isNumeric):
            self.dataQualityNumeric()
        else:
            self.dataQualityCategorical()

    def dataQualityNumeric(self):
        valueCount = df[self.name].size
        missingRows = df[self.name].isnull().sum()
        missingPercentage = (missingRows * 100) / valueCount
        cardinality = len(df[self.name].value_counts())
        minValue = df[self.name].min()
        maxValue = df[self.name].max()
        quantiles = df[self.name].quantile([0.25, 0.75])
        average = df[self.name].mean()
        median = df[self.name].median()
        standardDeviation = df[self.name].std()
        print(standardDeviation)
        print(minValue, maxValue)

    def dataQualityCategorical(self):
        valueCount = df[self.name].size
        missingRows = df[self.name].isnull().sum()
        missingPercentage = (missingRows * 100) / valueCount
        cardinality = len(df[self.name].value_counts())
        mode = df[self.name].mode().iloc[0]
        temp = df[df[self.name] != mode]
        secondMode = temp[self.name].mode().iloc[0]
        print(mode, secondMode)
        modeCount = (df[self.name] == mode).sum()
        modePercentage = (modeCount * 100) / valueCount
        secondModeCount = (df[self.name] == secondMode).sum()
        secontModePercentage = (secondModeCount * 100) / valueCount
        print(modeCount, secondModeCount)
        print(modePercentage, secontModePercentage)

        # print(mode[0])

        return


df = pd.read_csv('wage.csv', delimiter=',')
dataColumn.df = df
# print(df.head(3))


dataTypes = df.dtypes.to_list()
headers = df.columns
columnList = list()


for i in range(0, len(headers)):
    columnList.append(dataColumn(
        headers[i], np.issubdtype(dataTypes[i], np.number), dataTypes[i]))

bins = 1 + 3.22
ax = df.hist(column='year', bins=2)
plt.show()
# print(df['year'].isnull())
