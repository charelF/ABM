import numpy as np
import copy
from numba import njit

# Number of samples
M = 100

# Number of variables
p = 6
n = 6

# Fill vector with a_i's
a = np.zeros((n))

a[0] = 0.04
a[1] = 0.02
a[2] = 10
a[3] = 10
a[4] = 12
a[5] = 0.5

# Follow naming convention as in book

def create_C_i(A, B, i):
    C_i = copy.copy(B)
    C_i[:,i] = A[:,i]
    return C_i

@njit
def create_A_B():
    '''Creates a matrix filled
    with random entries'''
    A = np.zeros((M, p))
    for j in range(M):

        stoch_vars = np.random.rand(6)
        A[j] = stoch_vars
    return A

@njit
def evaluate_func(numbers):
    '''Calculates the function given
    the random numbers'''
    val = 1
    for i in range(n):
        val *= (abs(4 * numbers[i]-2) + a[i]) / (1 + a[i])
    return val


def calc_mean_squared(f_A, f_B):
    '''Calculates the mean squared of the function'''
    return 1/ M**2 * sum(f_A) * sum(f_B)

def calc_f_A(A):
    '''Evaluates the function f for every
    row in a'''
    f_A = np.zeros(M)
    for index, numbers in enumerate(A):
        f_A[index] = evaluate_func(numbers)
    return f_A

def calc_sobol(i):
    '''Calculated the i-th sobol index'''
    C_i = create_C_i(A, B, i)

    f_A = calc_f_A(A)
    f_B = calc_f_A(B)
    f_C_i = calc_f_A(C_i)
    

    f_0_squared = calc_mean_squared(f_A, f_B)
    S_i = (1/M * np.dot(f_A, f_C_i) - f_0_squared) / (1/M * np.dot(f_A, f_A) - f_0_squared)
    return S_i

def calc_total_sobol(i):
    '''Calculates the i-th total sobol index'''

    C_i = create_C_i(A, B, i)

    f_A = calc_f_A(A)
    f_B = calc_f_A(B)
    f_C_i = calc_f_A(C_i)
    

    f_0_squared = calc_mean_squared(f_A, f_B)
    S_i = (1/M * np.dot(f_B, f_C_i) - f_0_squared) / (1/M * np.dot(f_A, f_A) - f_0_squared)
    return 1 - S_i

# Make matrices
A = create_A_B()
B = create_A_B()

for i in range(p):
    s_i = calc_sobol(i)
    if i == 0:
        s_0 = s_i
    if i == 1:
        s_1 = s_i
    print('Partial index '+ str(i) + ' ' + str(s_i))


for i in range(p):
    s_T_i = calc_total_sobol(i)
    print('Total index '+ str(i) + ' ' + str(s_T_i))
    
def create_C_ij(A, B, i, j):
    C_i = copy.copy(B)
    C_i[:,i] = A[:,i]
    C_i[:,j] = A[:,j]
    return C_i


def calc_second_order(i, j):
    C_ij = create_C_ij(A, B, i, j)
    f_A = calc_f_A(A)
    f_B = calc_f_A(B)
    f_C_ij = calc_f_A(C_ij)

    f_0_squared = calc_mean_squared(f_A, f_B)
    S_ij = (1/M * np.dot(f_A, f_C_ij) - f_0_squared) / (1/M * np.dot(f_A, f_A) - f_0_squared)
    return S_ij 

print(calc_second_order(0, 1) - s_1 - s_2)