import numpy as np


def simplexTableauForm(filename):
    NDecisionVar, NConstraints, cj, MatrixLHS, VectorRHS = read_input_file(filename)

    # 初始化 tableau 矩阵，多添加一行（用于目标函数）和一列（用于 RHS）
    tableau = np.zeros((NConstraints + 1, NDecisionVar + NConstraints + 1))

    # 将 LHS 矩阵填充到 tableau 中，位于 [0:NConstraints, 0:NDecisionVar]
    tableau[:NConstraints, :NDecisionVar] = MatrixLHS

    # 填充 RHS 列到 tableau 中最后一列
    tableau[:NConstraints, -1] = VectorRHS

    # 生成 delta 行，初始为 0（最后的 delta 行）
    delta_column = np.zeros((NConstraints + 1, 1))
    # 添加 delta 行到 tableau 中
    tableau = np.hstack([tableau, delta_column])

    return tableau


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


if __name__ == '__main__':
    # N_Decision_Var, N_Constraints, cj, Matrix_LHS, Vector_RHS = read_input_file('q2inputfile.txt')
    # print(N_Decision_Var)
    # print(N_Constraints)
    # print("cj:", cj)
    # print("lhs_matrix:", Matrix_LHS)
    # print("rhs_vector:", Vector_RHS)

    print(simplexTableauForm('q2filetest.txt'))
