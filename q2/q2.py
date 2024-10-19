# Author : Zijie Zhang
# StudentID: 32397216
# Date: 19/10/2024

import numpy as np
import numpy as geek
import sys


# A helper function to read input file
# obtain the necessary attributes to generate the tableau
def read_input_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    N_Decision_Var = 0
    N_Constraints = 0
    cj = []
    Matrix_LHS = []
    Vector_RHS = []

    for i, line in enumerate(lines):
        line = line.strip()
        if line.startswith("# N_Decision_Variables"):
            N_Decision_Var = int(lines[i + 1].strip())
        elif line.startswith("# N_Constraints"):
            N_Constraints = int(lines[i + 1].strip())
        elif line.startswith("# Coefficients_of_Objective_Function"):
            cj = list(map(int, lines[i + 1].strip().split(',')))
        elif line.startswith("# Constraints_Matrix_LHS"):
            for j in range(N_Constraints):
                Matrix_LHS.append(list(map(int, lines[i + 1 + j].strip().split(','))))
        elif line.startswith("# constraints_Vector_RHS"):
            Vector_RHS = list(map(int, lines[i + 1:i + 1 + N_Constraints]))
    cj.extend([0] * N_Constraints)
    return N_Decision_Var, N_Constraints, cj, Matrix_LHS, Vector_RHS


def simplexTableauForm(filename):
    # read and obtain content from file
    NDecisionVar, NConstraints, Cj, MatrixLHS, VectorRHS = read_input_file(filename)

    # initialize the tableau matrix,add one more row for Cj-Zj, two columns for RHS and Theta
    tableau = np.zeros((NConstraints + 1, NDecisionVar + NConstraints + 2))
    # print(tableau)

    # Fill in the LHS into the matrix,position: [0:NConstraints, 0:NDecisionVar]
    tableau[:NConstraints, :NDecisionVar] = MatrixLHS

    # Fill in the slack variables as one for every constraint
    tableau[:NConstraints, NDecisionVar:NDecisionVar + NConstraints] = np.eye(NConstraints)

    # Fill in the RHS column
    tableau[:NConstraints, -2] = VectorRHS

    # Array Xb store the current basic variables
    Xb = []
    j = NDecisionVar
    for i in range(NConstraints):
        Xb.append(j)
        j += 1

    # initial the cb as all sv(slack vars) = 0
    Cb = [0] * np.zeros(NConstraints)
    # tableau[-1, -1] = 0
    return tableau, Xb, Cb


def cjZj(tableau, Cj, Cb, NConstraints):
    # initialize the cj_zj line
    Zj = np.zeros(len(Cj))

    # let the constant times the corresponding Cb, and then add them together for each column, store
    # them to Zj array respectively.
    for j in range(len(Cj)):
        zj = 0
        for i in range(NConstraints):
            zj += Cb[i] * tableau[i][j]
        Zj[j] = zj

    #  Cj - Zj
    Cj_Zj = geek.subtract(Cj, Zj)
    # Fill the Cj-Zj to the Tableau
    tableau[-1, :-2] = Cj_Zj
    # Find the index of maximum number of last row which means the largest number of Cj-Zj
    maxColIndex = np.argmax(tableau[-1, :-2])
    # gain the corresponding column for further calculation
    corrColumn = tableau[:NConstraints, maxColIndex]
    RHS = tableau[:NConstraints, -2]
    # Initial theta array in order to store the results
    theta = np.zeros(NConstraints)

    for i in range(len(RHS)):
        #  Since we can't divide a zero
        if corrColumn[i] > 0:
            # print(RHS[i], " / ", corrColumn[i])
            theta[i] = RHS[i] / corrColumn[i]
        else:
            # The minimum number would be chosen later, thus we set those divide by 0 's column to inf.
            theta[i] = float('inf')

        # Fill the theta result to last column of tableau
        tableau[i, - 1] = theta[i]
    # minimum of last column of tableau which means the smallest theta.
    minRowIndex = np.argmin(tableau[:NConstraints, -1])
    if tableau[-1, maxColIndex] <= 0:
        # need more content in there for end logic.
        return None, None
    # return the minimum of theta and maximum of Cj-Zj.
    return int(minRowIndex), int(maxColIndex)


# #  A Helper function to legally modify all number in corresponding column to be zero.
def newTableauForm(tableau, Xb, Cb, Cj, minRowIndex, maxColIndex, NConstraints):
    # Once we complete last tableau, it is about time to update it
    # let row that contain the minimum of theta divide the cross point
    tableau[minRowIndex, :-1] = tableau[minRowIndex, :-1] / tableau[minRowIndex][maxColIndex]
    # update the current basic variable
    Xb[minRowIndex] = maxColIndex
    # update the Coefficients of current basic variable
    Cb[minRowIndex] = Cj[maxColIndex]
    # Iterate through all constraints to make the chosen column contains the cross point to be zoe
    for i in range(NConstraints):
        #  Do operation on all constraints row expect chosen row, the row of chosen column is already 0
        if i != minRowIndex and tableau[i][maxColIndex] != 0:
            # Calculate the magnification factor for row operations
            mag = tableau[i][maxColIndex] / 1
            # Update the current row by subtracting the chosen row multiplied by the magnification factor
            tableau[i][:-1] -= tableau[minRowIndex][:-1] * mag
            # Update the current row's chosen column to be 0
            tableau[i][maxColIndex] = 0
    # Return tableau, Coefficients array and Cj
    # Well, Cj is part of calculation but will never be modified,I return it here for some referencing problems
    return tableau, Cb


def q2(filename):
    # Read the input from the given file and initialize the tableau, Xb (basic variables),
    # and Cb (coefficients of basic variables)
    NDecisionVar, NConstraints, Cj, MatrixLHS, VectorRHS = read_input_file(filename)
    tableau, Xb, Cb = simplexTableauForm(filename)
    found = False

    # Start the iterative process to find the optimal solution
    while not found:
        # Get the row and column index for the cross point
        minRowIndex, maxColIndex = cjZj(tableau, Cj, Cb, NConstraints)
        # If there is no more valid row and col index, it means
        # the largest value in Cj-Zj row is 0 or negative
        # set found to True to end the process
        if minRowIndex is None or maxColIndex is None:
            break
        # Update the tableau, basic variables, and coefficients using the cross point
        tableau, Cb = newTableauForm(tableau, Xb, Cb, Cj, minRowIndex, maxColIndex, NConstraints)
    # After iteration, extract the RHS column from tableau and store it in b
    b = tableau[:NConstraints, -2]
    deciVars = []
    # Iterate through each decision variable to determine its value in the solution
    for i in range(NDecisionVar):
        j = 0
        for k in Xb:
            # If the current variable is a basic variable, append its value
            if i == k:
                deciVars.append(float(b[j]))
            j += 1
    # Calculate the final result using the coefficients of basic variables and RHS values
    result = np.sum(np.array(Cb) * np.array(b))

    return deciVars, str(result)


def write_file(deciVars, result, filename="output_q2.txt"):
    with open(filename, 'w') as file:
        file.write("# Optimal_Values_of_Decision_Variables\n")
        file.write(", ".join(map(str, deciVars)))
        file.write("\n")
        file.write("# Optimal_Value_of_Objective_Function\n")
        file.write(result)

if __name__ == '__main__':
    _, filename = sys.argv
    deciVars, result = q2(filename)
    write_file(deciVars, result)



    # q2('q2filetest.txt')

