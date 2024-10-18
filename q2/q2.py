import numpy as np
import numpy as geek


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
    # Find the index of maximum number
    maxColIndex = np.argmax(tableau[-1, :-2])
    # print(maxColIndex)
    # gain the  corresponding column for further calculation
    corrColumn = tableau[:NConstraints, maxColIndex]
    RHS = tableau[:NConstraints, -2]

    # Initial theta array in order to store the results
    theta = np.zeros(NConstraints)

    for i in range(len(RHS)):
        #  Since we can't divide a zero
        # print(corrColumn[i])
        if corrColumn[i] > 0:
            # print(RHS[i], " / ", corrColumn[i])
            theta[i] = RHS[i] / corrColumn[i]
        #   theta[i] = RHS[i]/corrColumn[i]
        else:
            # The minimum number would be chosen later, thus we set those divide by 0 's column to inf.
            theta[i] = float('inf')

        # Fill the theta result to last column of tableau
        tableau[i, - 1] = theta[i]

    # print(tableau)
    # print(tableau[:NConstraints, -1])
    minRowIndex = np.argmin(tableau[:NConstraints, -1])
    if tableau[-1, maxColIndex] <= 0:
        # need more content in there for end logic.
        return None, None

    return int(minRowIndex), int(maxColIndex)


# #  A Helper function to legally modify all number in corresponding column to be zero.
def newTableauForm(tableau, Xb, Cb, Cj, minRowIndex, maxColIndex, NConstraints):
    tableau[minRowIndex, :-1] = tableau[minRowIndex, :-1] / tableau[minRowIndex][maxColIndex]
    Xb[minRowIndex] = maxColIndex
    Cb[minRowIndex] = Cj[maxColIndex]
    for i in range(NConstraints):
        if i != minRowIndex and tableau[i][maxColIndex] != 0:
            # magnification
            mag = tableau[i][maxColIndex] / 1
            tableau[i][:-1] -= tableau[minRowIndex][:-1] * mag
            tableau[i][maxColIndex] = 0

    return tableau, Cb, Cj


def q2(filename):
    NDecisionVar, NConstraints, Cj, MatrixLHS, VectorRHS = read_input_file(filename)
    tableau, Xb, Cb = simplexTableauForm(filename)
    found = False

    while not found:
        minRowIndex, maxColIndex = cjZj(tableau, Cj,Cb, NConstraints)
        if minRowIndex is None or maxColIndex is None:
            found = True
            break
        tableau, Cb, Cj = newTableauForm(tableau, Xb, Cb, Cj, minRowIndex, maxColIndex, NConstraints)

    b = tableau[:NConstraints, -2]
    deciVars = []
    for i in range(NDecisionVar):
        j = 0
        for k in Xb:
            if i == k:
                deciVars.append(float(b[j]))
            j += 1

    result = np.sum(np.array(Cb) * np.array(b))
    print(deciVars)
    print(result)


if __name__ == '__main__':
    q2('q2filetest.txt')

    # # N_Decision_Var, N_Constraints, Cj, Matrix_LHS, Vector_RHS = read_input_file('q2inputfile.txt')
    # # q2filetest
    # NDecisionVar, NConstraints, Cj, MatrixLHS, VectorRHS = read_input_file('q2bilibili.txt')
    # tableau, Xb, Cb = simplexTableauForm('q2bilibili.txt')
    #
    # minRowIndex, maxColIndex = cjZj(tableau, Cj, NConstraints)
    # # print(tableau)
    # # print(Cb)
    # # print(Xb)
    # # print("\n\n\n\n")
    # newTableau, Cb, Cj = newTableauForm(tableau, Xb, Cb, Cj, minRowIndex, maxColIndex, NConstraints)
    # minRowIndex, maxColIndex = cjZj(newTableau, Cj, NConstraints)
    # # print(newTableau)
    # # print(Cb)
    # # print(Xb)
    # # print("\n\n\n\n")
    #
    # newTableau_2, Cb, Cj = newTableauForm(newTableau, Xb, Cb, Cj, minRowIndex, maxColIndex, NConstraints)
    # minRowIndex, maxColIndex = cjZj(newTableau_2, Cj, NConstraints)
    # # print(newTableau_2)
    # # print(Cb)
    # # print(Xb)
    # # print("\n\n\n\n")
    #
    # newTableau_3, Cb, Cj = newTableauForm(newTableau_2, Xb, Cb, Cj, minRowIndex, maxColIndex, NConstraints)
    # minRowIndex, maxColIndex = cjZj(newTableau_3, Cj, NConstraints)
    #
    # print(newTableau_3)
    # # print(Cb)
    # b = tableau[:NConstraints, -2]
    # print(Xb)
    # print(tableau[:NConstraints, -2])
    # deciVars = []
    # for i in range(NDecisionVar):
    #     j = 0
    #     for k in Xb:
    #         if i == k:
    #             deciVars.append(float(b[j]))
    #         j += 1
    #
    # result = np.sum(np.array(Cb) * np.array(b))
    # print(deciVars)
    # print(result)
    #
    # print("\n\n\n\n")
