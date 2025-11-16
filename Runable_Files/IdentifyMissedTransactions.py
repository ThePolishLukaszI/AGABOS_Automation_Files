import pandas as pd
from pathlib import Path
ScriptDir = Path(__file__).parent
InputDir = ScriptDir.parent / "Inputs"
OutputDir = ScriptDir.parent / "Outputs"
csv_list = [(InputDir / "11.csv") , (InputDir / "22.csv") , (InputDir / "33.csv")]


ActualData = pd.read_csv((InputDir / "AsOfActual.csv"))
AssumedData = pd.concat((pd.read_csv(file) for file in csv_list), ignore_index=True)

ActualData = ActualData.sort_values(by='Amount')
AssumedData = AssumedData.sort_values(by='AMOUNT')

for ActualIndex, ActualEntry in ActualData.iterrows():
    FindingAmount = ActualEntry["Amount"]
    if FindingAmount > 0:
        continue
    FindingAmount = f"-£{abs(FindingAmount):,.2f}"
    FoundEquals = AssumedData[AssumedData["AMOUNT"] == FindingAmount].index
    
    print(AssumedData)
    if not FoundEquals.empty:
        AssumedData.drop(FoundEquals[0] , inplace=True)
    else:
        print(FindingAmount) 
    print(AssumedData)
        
AssumedData.to_csv(OutputDir, index=False)
print()