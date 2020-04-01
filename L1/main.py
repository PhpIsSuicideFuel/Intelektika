import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import chart_studio.plotly as py
import plotly.graph_objs as go
import seaborn as sn
from sklearn.linear_model import LinearRegression


class dataColumn:

    def __init__(self, name, isNumeric, dataType):
        self.name = name
        self.isNumeric = isNumeric
        self.dataType = dataType
        if(self.isNumeric):
            self.columns = ['Pavadinimas', 'Kiekis', 'Trukstamos reiksmes', 'Kardinalumas', 'Minimali reiksme',
                            'Maksimali reiksme', '1-asis kvartilis', '2-asis kvartilis', 'Vidurkis', 'Mediana', 'Standartinis nuokrypis']
        else:
            self.columns = ['Pavadinimas', 'Kiekis', 'Trukstamos reiksmes', 'Kardinalumas',
                            'Moda', 'Modos daznumas', 'Moda, %', '2-oji Moda', '2-osios Modos dažnumas', '2-oji Moda, %']

    def getDataQuality(self):
        if(self.isNumeric):

            return self.dataQualityNumeric()
        else:
            return self.dataQualityCategorical()
        return None

    def dataQualityNumeric(self):
        self.valueCount = df[self.name].size
        missingRows = df[self.name].isnull().sum()
        missingPercentage = (missingRows * 100) / self.valueCount
        cardinality = len(df[self.name].value_counts())
        minValue = df[self.name].min()
        maxValue = df[self.name].max()
        quantiles = df[self.name].quantile([0.25, 0.75])
        average = df[self.name].mean()
        median = df[self.name].median()
        standardDeviation = df[self.name].std()

        qualityData = [self.name, self.valueCount, missingPercentage, cardinality,
                       minValue, maxValue, quantiles[0.25], quantiles[0.75], average, median, standardDeviation]

        dst = dict()
        for k, v in zip(qualityData, self.columns):
            dst[v] = k

        return dst

    def dataQualityCategorical(self):
        self.valueCount = df[self.name].size
        missingRows = df[self.name].isnull().sum()
        missingPercentage = (missingRows * 100) / self.valueCount
        cardinality = len(df[self.name].value_counts())
        mode = df[self.name].mode().iloc[0]
        temp = df[df[self.name] != mode]
        try:
            secondMode = temp[self.name].mode().iloc[0]
        except:
            secondMode = None
        modeCount = (df[self.name] == mode).sum()
        modePercentage = (modeCount * 100) / self.valueCount
        secondModeCount = (df[self.name] == secondMode).sum()
        secontModePercentage = (secondModeCount * 100) / self.valueCount

        qualityData = [self.name, self.valueCount, missingPercentage, cardinality,
                       mode, modeCount, modePercentage, secondMode, secondModeCount, secontModePercentage]

        dst = dict()
        for k, v in zip(qualityData, self.columns):
            dst[v] = k

        return dst

    def showHistogram(self):
        bins = int(1 + 3.22 * np.log(self.valueCount))
        df1 = df.loc[df['jobclass'] == '1. Industrial']

        ax = df1.hist(column=self.name, bins=bins,
                      edgecolor='black', linewidth=1.2, grid=False)

        for a in ax.flatten():
            a.spines['right'].set_visible(False)
            a.spines['top'].set_visible(False)
            a.spines['left'].set_visible(False)
            a.set_xlabel(self.name.capitalize(), weight='bold', size=12)
            a.set_ylabel("Frequency", weight='bold', size=12)
            vals = a.get_yticks()
            for tick in vals:
                a.axhline(y=tick, linestyle='dashed',
                          alpha=0.4, color='#eeeeee', zorder=1)
            a.set_title("")


def showBarPlot():
    df1 = df.loc[df['jobclass'] == '2. Information']
    print(df1)
    ax = df1['health_ins'].value_counts().plot.bar(
        title="Darbuotojų gyvybės draudimas jeigu jis dirba informacinį darbą", rot=0)
    ax.set_ylabel("Frequency", weight='bold', size=12)
    # for a in ax:
    #     a.spines['right'].set_visible(False)
    #     a.spines['top'].set_visible(False)
    #     a.spines['left'].set_visible(False)
    #     a.set_ylabel("Frequency", weight='bold', size=12)
    #     vals = a.get_yticks()
    #     for tick in vals:
    #         a.axhline(y=tick, linestyle='dashed',
    #                   alpha=0.4, color='#eeeeee', zorder=1)
    #     a.set_title("")


def removeOutliers(dataf):
    low = .05
    high = .95
    quant_df = dataf.quantile([low, high])
    print(quant_df)
    for name in list(dataf.columns):
        if pd.api.types.is_numeric_dtype(dataf[name]):
            dataf = dataf[(dataf[name] > quant_df.loc[low, name]) & (
                dataf[name] < quant_df.loc[high, name])]
    return dataf


df = pd.read_csv('wage.csv', delimiter=',')
dataColumn.df = df

dataTypes = df.dtypes.to_list()
headers = df.columns
columnList = list()

dfNumeric = pd.DataFrame(columns=['Pavadinimas', 'Kiekis', 'Trukstamos reiksmes', 'Kardinalumas', 'Minimali reiksme',
                                  'Maksimali reiksme', '1-asis kvartilis', '2-asis kvartilis', 'Vidurkis', 'Mediana', 'Standartinis nuokrypis'])

dfCategorical = pd.DataFrame(columns=['Pavadinimas', 'Kiekis', 'Trukstamos reiksmes', 'Kardinalumas',
                                      'Moda', 'Modos daznumas', 'Moda, %', '2-oji Moda', '2-osios Modos dažnumas', '2-oji Moda, %'])
row_list = []
for i in range(0, len(headers)):
    isNumeric = np.issubdtype(dataTypes[i], np.number)
    columnList.append(dataColumn(
        headers[i], isNumeric, dataTypes[i]))
    print(i)

    line = columnList[i].getDataQuality()
    if(isNumeric):
        dfNumeric = dfNumeric.append(line, ignore_index=True)
        # columnList[i].showHistogram()
    else:
        dfCategorical = dfCategorical.append(line, ignore_index=True)

# values converts it into a numpy array
X = df.iloc[:, 10].values.reshape(-1, 1)
# -1 means that calculate the dimension of rows, but have 1 column
Y = df.iloc[:, 1].values.reshape(-1, 1)
linear_regressor = LinearRegression()  # create object for the class
linear_regressor.fit(X, Y)  # perform linear regression
Y_pred = linear_regressor.predict(X)  # make predictions

# plt.scatter(X, Y)
# plt.xlabel("Wage")
# plt.ylabel("Age")
# plt.plot(X, Y_pred, color='red')

# showBarPlot()
# columnList[10].showHistogram()
# boxplot = df.boxplot(by='health_ins', column=['age'])
# boxplot.set_ylabel("Age", weight='bold', size=12)
# boxplot.set_xlabel("Health insurance", weight='bold', size=12)
df = removeOutliers(df)
print(df)
corrMatrix = df[['year', 'age', 'wage']].corr()
sn.heatmap(corrMatrix, annot=True)
# print(dfNumeric)
# print(dfCategorical)

plt.show()
