
import pandas as pd
import numpy as np
df = pd.read_csv("ild3k.data" , header=None, index_col=0)

injected = df.iloc[:,0]
true = df.iloc[:,2]
labels = df.iloc[:,3]

anoms = np.invert(np.isclose(injected.values,true.values))

a_count = sum(anoms)

anom_starts = 0
labeled_anom_stars = 0
for i,a in enumerate(anoms):
    if i == 0: continue

    if a and not anoms[i-1]:
        anom_starts+=1
        if labels.values[i]:
            labeled_anom_stars = labeled_anom_stars+1


import matplotlib.pyplot as plt
plt.plot(df)
plt.show()