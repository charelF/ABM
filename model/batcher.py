import sys
import pandas as pd
from model import RegionModel

def run(i):

    # Do simulation
    print(*df.iloc[i, 1:7])
    m = RegionModel(int_trade, *df.iloc[i, 1:7])
    for k in range(max_steps):
            m.step()
    
    # Get data
    m.compute_statistics()
    m.datacollector.collect(m)
    outcomes = m.datacollector.get_model_vars_dataframe()
    print(outcomes)
    with open(r"data.csv","a") as f:
        #print(len(df.iloc[i, 1:8]))
        # Skip first international trade parameters
        f.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(i, int_trade,*df.iloc[i, 1:7], *outcomes.iloc[0]))

max_steps = 1000
df = pd.read_csv('out.csv')
batches = int(sys.argv[1])
batch = int(sys.argv[2])
int_trade = True if int(sys.argv[3]) == 1 else False

runs_per_batch = int(len(df.index)/batches) + 1

for i in range(batch * runs_per_batch, (batch + 1) * runs_per_batch):
    run(i)

