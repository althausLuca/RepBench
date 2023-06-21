from matplotlib import pyplot as plt

from repair.Screen.screen import screen

import numpy as np

file_path = "repair/Screen/test/data/"
file_label = file_path+"stock10k.csv"

original_data = np.loadtxt(file_label,delimiter=',',skiprows=0).T[1]
print(original_data)


smin= -1
smax= 1
T = 1
my_repair = screen(original_data,T, smax, smin,)

file_label = file_path+f"screen_{smax}_{smin}_{T}.csv"
screen_corrected = np.loadtxt(file_label,delimiter=',',skiprows=0)
diff = screen_corrected-my_repair
for i in diff:
    print(i)

plt.plot(screen_corrected,lw=1,label="screen_paper")
plt.plot(my_repair,lw=1,label="my_repair")
plt.legend()
plt.title(f"stock smin={smin},smax={smax},T={T}")
plt.show()


smin= -1
smax= 1
T = 2
my_repair = screen(original_data,T, smax, smin,)

file_label = file_path+f"screen_{smax}_{smin}_{T}.csv"
screen_corrected = np.loadtxt(file_label,delimiter=',',skiprows=0)
diff = screen_corrected-my_repair
for i in diff:
    print(i)

plt.plot(screen_corrected,lw=1,label="screen_paper")
plt.plot(my_repair,lw=1,label="my_repair")
plt.plot(diff>0,lw=1,label="diff>0")
plt.legend()
plt.title(f"stock smin={smin},smax={smax},T={T}")
plt.show()


smin= -1
smax= 1
T = 3
my_repair = screen(original_data,T, smax, smin,)

file_label = file_path+f"screen_{smax}_{smin}_{T}.csv"
screen_corrected = np.loadtxt(file_label,delimiter=',',skiprows=0)
diff = screen_corrected-my_repair
for i in diff:
    print(i)

plt.plot(screen_corrected,lw=1,label="screen_paper")
plt.plot(my_repair,lw=1,label="my_repair")
plt.plot(diff>0,lw=1,label="diff>0")

plt.legend()
plt.title(f"stock smin={smin},smax={smax},T={T}")
plt.show()



smin= -6
smax= 6
T = 3
my_repair = screen(original_data,T, smax, smin,)

file_label = file_path+f"screen_{smax}_{smin}_{T}.csv"
screen_corrected = np.loadtxt(file_label,delimiter=',',skiprows=0)
diff = screen_corrected-my_repair
for i in diff:
    print(i)

plt.plot(screen_corrected,lw=1,label="screen_paper")
plt.plot(my_repair,lw=1,label="my_repair")
plt.plot(diff>0,lw=1,label="diff>0")
plt.legend()
plt.title(f"stock smin={smin},smax={smax},T={T}")
plt.show()