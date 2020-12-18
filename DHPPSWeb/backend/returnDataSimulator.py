import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint


def Seir(y, t, b, a, g, p, u, g_N):
    dy = [0, 0, 0, 0, 0, 0]
    S = g_N - sum(y)
    dy[0] = np.dot(b[1:3], y[1:3]) * S - a * y[0]  # E
    dy[1] = a * y[0] - (g[1] + p[1]) * y[1]  # I1
    dy[2] = p[1] * y[1] - (g[2] + p[2]) * y[2]  # I2
    dy[3] = p[2] * y[2] - (g[3] + u) * y[3]  # I3
    dy[4] = np.dot(g[1:3], y[1:3])  # R
    dy[5] = u * y[3]  # D

    return dy


g_IncubPeriod = 5  # Incubation period, days
g_DurMildInf = 10  # Duration of mild infections, days
g_FracMild = 0.75  # Fraction of infections that are mild
g_FracSevere = 0.2  # Fraction of infections that are severe
g_FracCritical = 0.05  # Fraction of infections that are critical
g_CFR = 0.02  # Case fatality rate (fraction of infections resulting in death)
g_TimeICUDeath = 7  # Time from ICU admission to death, days
g_DurHosp = 11  # Duration of hospitalization, days

g_N = 1000
g_b = np.zeros(4)  # beta
g_g = np.zeros(4)  # gamma
g_p = np.zeros(3)

g_a = 1 / g_IncubPeriod

g_u = (1 / g_TimeICUDeath) * (g_CFR / g_FracCritical)
g_g[3] = (1 / g_TimeICUDeath) - u

g_p[2] = (1 / g_DurHosp) * (g_FracCritical / (g_FracCritical + g_FracSevere))
g_g[2] = (1 / g_DurHosp) - p[2]

g_g[1] = (1 / g_g_DurMildInf) * g_FracMild
g_p[1] = (1 / g_DurMildInf) - g_g[1]

g_b = 2e-4 * np.ones(4)

g_R0 = g_N * ((g_b[1] / (g_p[1] + g_g[1])) + (g_p[1] / (g_p[1] + g_g[1])) *
          (g_b[2] / (g_p[2] + g_g[2]) + (g_p[2] / (g_p[2] + g_g[2])) * (g_b[3] /
                                                            (g_u + g_g[3]))))
print("g_R0 = {0:4.1f}".format(R0))

g_tmax = 365
g_tvec = np.arange(0, g_tmax, 1)
g_ic = np.zeros(6)
g_ic[0] = 1

g_soln = odeint(Seir, g_ic, g_tvec, args=(g_b, g_a, g_g, g_p, g_u, g_N))
g_soln = np.hstack((g_N - np.sum(g_soln, axis=1, keepdims=True), g_soln))

# plt.figure(figsize=(13,5))
# plt.subplot(1,2,1)
# plt.plot(g_tvec,g_soln)
# plt.xlabel("Time (days)")
# plt.ylabel("g_Number per 1000 People")
# plt.legend(("S","E","I1","I2","I3","R","D"))
# plt.ylim([0,1000])

# #Same plot but on log scale
# plt.subplot(1,2,2)
# plt.plot(g_tvec,g_soln)
# plt.semilogy()
# plt.xlabel("Time (days)")
# plt.ylabel("g_Number per 1000 People")
# plt.legend(("S","E","I1","I2","I3","R","D"))
# plt.ylim([1,1000])
# plt.tight_layout()


def Model(inputList, length):
    g_N = 1000
    g_b = np.zeros(4)  # beta
    g_g = np.zeros(4)  # gamma
    g_p = np.zeros(3)

    g_a = 1 / g_IncubPeriod

    g_u = (1 / g_TimeICUDeath) * (g_CFR / g_FracCritical)
    g_g[3] = (1 / g_TimeICUDeath) - g_u

    g_p[2] = (1 / g_DurHosp) * (g_FracCritical / (g_FracCritical + g_FracSevere))
    g_g[2] = (1 / g_DurHosp) - g_p[2]

    g_g[1] = (1 / g_DurMildInf) * g_FracMild
    g_p[1] = (1 / g_DurMildInf) - g_g[1]

    g_b = 2e-4 * np.ones(4)
    rateList = []
    for i in inputList:
        rateList.append(float(i) / float(1000))
    g_tmax = length
    g_tvec = np.arange(0, g_tmax, 1)
    g_soln = odeint(Seir, g_ic, g_tvec, args=(g_b, g_a, g_g, g_p, g_u, g_N))
    g_soln = np.hstack((1000 - np.sum(g_soln, axis=1, keepdims=True), g_soln))
    returnList = []
    for u in range(len(rateList)):
        tempList = []
        for k in g_soln:
            tempList.append((k[2]) * rateList[g_u])
        returnList.append(tempList)
    return returnList


# q = Model([20000, 30000, 130000], 300)
# plt.plot(q[2])
# plt.show()
