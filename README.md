# Regulatory-Reporting-on-Commodity-Trades-Volume-for-2018
CRAFT 2018 | Regulatory Reporting on Commodity Trades Volume for 2018

Preamble:

{OBJECTIVE}
Determine the total notional for commodity trades in the calendar year of 2018 upon request by the Monetary Authority of Singapore (MAS).

{REQUIREMENTS}
1./ Collate datasets into one dataframe: Murex trade datasets provided only span one calendar month per file (12 data files in total), several columns of data not required for the exercise.
2./ Internal trades must not be reported.
3./ Trades must be identified as onshore (traded under the Singapore Entity) or offshore (traded under an Entity other than Singapore)
4./ Deducing the notional (price × contracts × lot size) differs between OTC commodity trades and commodity Futures. Differentiate and apply correct lot sizes among commodity subgroups across the dataset.
5./ Contracts are executed in different currencies but all trades must be converted with effective month-end FX rates in accord with MAS regulation (MAS 610) and reported in SGD-equivalent notionals.

{NOTES}
Datasets are restricted specific ANZ Banking Group Limited personnel.

Software Requirements:
Python (version 3)
IPython (version 5.3.0 or later)
Microsoft Excel (version 2013 or later)

Deployment:
Save a copy of craft2018v4.py to :/My Documents
Launch IPython and execute by inserting “%run craft2018.py” in the IDE.
The prompt will return the total notional number along with a pivot table separated by onshore/offshore trade notionals.
