import numpy as np

def stress(F, OD, ID):
    'Calculate engineering stress'
    F = 4.45 * F
    OD = 25.40 * OD
    ID = 25.40 * ID
    return (F / ((np.pi * (OD / 2)**2) - (np.pi * (ID / 2)**2)))


def strain(E, offset):
    'Calculate engineering strain %'
    return ((E - offset) * 1e-4 / (1 + offset * 1e-6))


def find_stress(cycle, stress, initiation):
    'To obtain the initial and final failure engineering stress'
    for i in range(len(cycle)):
        if cycle[i] == initiation:
            break
    ini_stress = stress[i]
    return ini_stress


def strain_range(maxe, mine):
    strain_range = []
    for i in range(len(maxe)):
        strain_range.append(mine[i] - maxe[i])
    return strain_range


def q_factor(E, slope):
    q = 1 + E / (-slope * 100)
    return q


def fitting(x, a, b):
    return a * x + b