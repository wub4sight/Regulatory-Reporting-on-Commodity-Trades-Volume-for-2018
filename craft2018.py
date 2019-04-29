import glob
import pandas as pd
import numpy as np
# Append monthly commodity trade data
appended_com_data =[]
for infile in glob.glob('\My Documents\FO Support\Craft2018\com_2018_*.csv'):
    data = pd.read_csv(infile)
    appended_com_data.append(data)
appended_com_data = pd.concat(appended_com_data, axis=0)
com1 = appended_com_data

# Remove unwanted columns from total trade data
com2 = com1[['NB.INT','G.ID','TRADER','TRN.DATE','COUNTERPART','INSTRUMENT','GROUP','FAMILY','S.ENTITY','PL_INSCUR','BRW_NOM1','BRW_RTE1']]

# Rename column headers
com3 = com2.rename(columns = {'NB.INT':'MXID','G.ID':'GID','S.ENTITY':'Entity','TRN.DATE':'TradeDate','BRW_RTE1':'Margin','BRW_NOM1':'Nominal','PL_INSCUR':'CCY'})

# Identify internal trades
com3['Internal'] = com3['COUNTERPART'].str.startswith('X_') | com3['COUNTERPART'].str.startswith('ANZ')

# Remove internal trades
com4 = com3[com3['Internal']==False]

# Import Commodity Futures Lot denominations specific to each label
futlot = pd.read_excel('\My Documents\FO Support\Craft2018\comfutlot.xlsx')

# Merge Future-Lot denomination dataframe with trade data
com5 = pd.merge(com4, futlot, left_on='INSTRUMENT', right_on='Label', how='left')

# For Futures, Revised Nominal = Nominal * LotSize
# For non-Futures, Revised Nominal = Nominal 
com5['RevisedNominal'] = np.where(com5.GROUP=='FUT', com5.Nominal * com5.LotSize, com5.Nominal)

# Deducing and inserting Notional to dataframe
com5['Notional'] = com5.RevisedNominal * com5.Margin

# Import effective monthly FX rates
FXrates = pd.read_excel('\My Documents\FO Support\Craft2018\SGDFXRates.xlsx')

# Indexing disparate monthly FX rates with SGD as base applicable to trade data
FXrates['MonthCCYCode'] = FXrates['Month'] + FXrates['CCYCode']

# Identify the month for each deal in trade data
com5['TradeMonth'] = pd.DatetimeIndex(com5['TradeDate']).month

# Convert month as integer to string format "mmm"
months_map = {1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}
com5['TradeMonth'] = com5['TradeMonth'].apply(lambda x: months_map[x])

# Create common key between trade data and monthly FX rates
com5['MonthCCY'] = com5['TradeMonth'] + com5['CCY']

# Identify onshore and offshore trades
com5['Onshore'] = np.where(com5.Entity=='ANZBG SING','Yes','No')

# merge monthly FX rates and trade data
com6 = pd.merge(com5, FXrates, left_on='MonthCCY', right_on='MonthCCYCode', how='left')

# Deduce SGD equivalent notionals for trade data
com6['SGDNotional'] = com6.Notional * com6.FXRate

# Sum of Notionals converted to SGD
TotalSGDNotional = com6['SGDNotional'].sum()
print('Total notional in SGD is ', TotalSGDNotional)

# Notionals by deal currency and whether onshore/offshore
com7 = com5[['Onshore','CCY','Notional']]
pvtcom7 = com7.groupby(['Onshore','CCY']).sum()
print(pvtcom7)