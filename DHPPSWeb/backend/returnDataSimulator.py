import numpy as np
from scipy.integrate import odeint


def seir(y, t, b, a, g, p, u, N):
    dy = [0, 0, 0, 0, 0, 0]
    S = N - sum(y)
    dy[0] = np.dot(b[1:3], y[1:3]) * S - a * y[0]  # E
    dy[1] = a * y[0] - (g[1] + p[1]) * y[1]  # I1
    dy[2] = p[1] * y[1] - (g[2] + p[2]) * y[2]  # I2
    dy[3] = p[2] * y[2] - (g[3] + u) * y[3]  # I3
    dy[4] = np.dot(g[1:3], y[1:3])  # R
    dy[5] = u * y[3]  # D

    return dy


IncubPeriod = 5  # Incubation period, days
DurMildInf = 10  # Duration of mild infections, days
FracMild = 0.75  # Fraction of infections that are mild
FracSevere = 0.2  # Fraction of infections that are severe
FracCritical = 0.05  # Fraction of infections that are critical
CFR = 0.02  # Case fatality rate (fraction of infections resulting in death)
TimeICUDeath = 7  # Time from ICU admission to death, days
DurHosp = 11  # Duration of hospitalization, days

N = 1000
b = np.zeros(4)  # beta
g = np.zeros(4)  # gamma
p = np.zeros(3)

a = 1 / IncubPeriod

u = (1 / TimeICUDeath) * (CFR / FracCritical)
g[3] = (1 / TimeICUDeath) - u

p[2] = (1 / DurHosp) * (FracCritical / (FracCritical + FracSevere))
g[2] = (1 / DurHosp) - p[2]

g[1] = (1 / DurMildInf) * FracMild
p[1] = (1 / DurMildInf) - g[1]

b = 2e-4 * np.ones(4)

R0 = N * ((b[1] / (p[1] + g[1])) + (p[1] / (p[1] + g[1])) *
          (b[2] / (p[2] + g[2]) + (p[2] / (p[2] + g[2])) * (b[3] /
                                                            (u + g[3]))))
print("R0 = {0:4.1f}".format(R0))

tmax = 365
tvec = np.arange(0, tmax, 1)
ic = np.zeros(6)
ic[0] = 1

soln = odeint(seir, ic, tvec, args=(b, a, g, p, u, N))
soln = np.hstack((N - np.sum(soln, axis=1, keepdims=True), soln))

# plt.figure(figsize=(13,5))
# plt.subplot(1,2,1)
# plt.plot(tvec,soln)
# plt.xlabel("Time (days)")
# plt.ylabel("Number per 1000 People")
# plt.legend(("S","E","I1","I2","I3","R","D"))
# plt.ylim([0,1000])

# #Same plot but on log scale
# plt.subplot(1,2,2)
# plt.plot(tvec,soln)
# plt.semilogy()
# plt.xlabel("Time (days)")
# plt.ylabel("Number per 1000 People")
# plt.legend(("S","E","I1","I2","I3","R","D"))
# plt.ylim([1,1000])
# plt.tight_layout()


def model(inputList, length):
    N = 1000
    b = np.zeros(4)  # beta
    g = np.zeros(4)  # gamma
    p = np.zeros(3)

    a = 1 / IncubPeriod

    u = (1 / TimeICUDeath) * (CFR / FracCritical)
    g[3] = (1 / TimeICUDeath) - u

    p[2] = (1 / DurHosp) * (FracCritical / (FracCritical + FracSevere))
    g[2] = (1 / DurHosp) - p[2]

    g[1] = (1 / DurMildInf) * FracMild
    p[1] = (1 / DurMildInf) - g[1]

    b = 2e-4 * np.ones(4)
    rateList = []
    for i in inputList:
        rateList.append(float(i) / float(1000))
    tmax = length
    tvec = np.arange(0, tmax, 1)
    soln = odeint(seir, ic, tvec, args=(b, a, g, p, u, N))
    soln = np.hstack((1000 - np.sum(soln, axis=1, keepdims=True), soln))
    returnList = []
    for u in range(len(rateList)):
        tempList = []
        for k in soln:
            tempList.append((k[2]) * rateList[u])
        returnList.append(tempList)
    return returnList


# q = model([20000, 30000, 130000], 300)
# plt.plot(q[2])
# plt.show()
