from typing import List
import matplotlib.pyplot as plt
import numpy as np
import os

def compare_by_lex(M1: List[int], M2: List[int], P: List[int]) -> int:
    """
    Compares two monomials M1 and M2 by a lexicographical order defined by procedure P.
    Returns:
        -1 if M1 < M2
         1 if M1 > M2
         0 if M1 == M2
    """
    for i in range(len(P)):
        # Check if both M1 and M2 contain P[i]
        if M1[P[i]] < M2[P[i]]:
            return -1
        elif M1[P[i]] > M2[P[i]]:
            return 1
    return 0

def compare_by_glex(M1: List[int], M2: List[int], P: List[int]) -> int:
    """
    Compares two monomials M1 and M2 by graded lexicographical order defined by procedure P.
    First compares total degree, then uses lexicographical order if degrees are equal.
    Returns:
        -1 if M1 < M2
         1 if M1 > M2
         0 if M1 == M2
    """
    # Compare total degrees first
    deg1 = sum(M1)
    deg2 = sum(M2)
    if deg1 < deg2:
        return -1
    elif deg1 > deg2:
        return 1
    # If total degrees are equal, use lexicographical comparison
    return compare_by_lex(M1, M2, P)

def compare_by_grevlex(M1: List[int], M2: List[int], P: List[int]) -> int:
    """
    Compares two monomials M1 and M2 by graded reverse lexicographical order defined by procedure P.
    First compares total degree, then uses reverse lexicographical order if degrees are equal.
    Returns:
        -1 if M1 < M2
         1 if M1 > M2
         0 if M1 == M2
    """
    # Compare total degrees first
    deg1 = sum(M1)
    deg2 = sum(M2)
    if deg1 < deg2:
        return -1
    elif deg1 > deg2:
        return 1
    # If total degrees are equal, use reverse lexicographical comparison
    for i in range(len(P)-1, -1, -1):
        if M1[P[i]] > M2[P[i]]:
            return -1
        elif M1[P[i]] < M2[P[i]]:
            return 1
    return 0

def determine_by_lex(Terms: List[List[int]], Procedure: List[int]) -> List[List[int]]:
    """
    Orders terms (lexicographically) by Procedure.
    Parameters:
        Terms: List of terms represented as lists of monomial exponents.
        Procedure: List of indices defining the variable order.
    Returns:
        Ordered list of Terms lexicographically.
    """
    n = len(Terms)
    # Initialize an array for the lexicographically sorted terms
    TermsLex = [None] * n
    # This will store the indices in sorted order
    Count = [0] * n

    # Populate the counting array
    for i in range(n):
        Count[i] = 0  # initialize counting sort array
        for j in range(n):
            if compare_by_lex(Terms[i], Terms[j], Procedure) < 0:
                Count[i] += 1

    # Arrange terms based on counting array
    for i in range(n):
        TermsLex[Count[i]] = Terms[i]
    
    return TermsLex

def determine_by_glex(Terms: List[List[int]], Procedure: List[int]) -> List[List[int]]:
    """
    Orders terms by graded lexicographical order using Procedure.
    """
    n = len(Terms)
    TermsGlex = [None] * n
    Count = [0] * n

    for i in range(n):
        Count[i] = 0
        for j in range(n):
            if compare_by_glex(Terms[i], Terms[j], Procedure) < 0:
                Count[i] += 1

    for i in range(n):
        TermsGlex[Count[i]] = Terms[i]
    
    return TermsGlex

def determine_by_grevlex(Terms: List[List[int]], Procedure: List[int]) -> List[List[int]]:
    """
    Orders terms by graded reverse lexicographical order using Procedure.
    """
    n = len(Terms)
    TermsGrevlex = [None] * n
    Count = [0] * n

    for i in range(n):
        Count[i] = 0
        for j in range(n):
            if compare_by_grevlex(Terms[i], Terms[j], Procedure) < 0:
                Count[i] += 1

    for i in range(n):
        TermsGrevlex[Count[i]] = Terms[i]
    
    return TermsGrevlex

def plot_terms_heatmap(terms, title, filename):
    plt.figure(figsize=(10, 5))
    plt.imshow(terms, aspect='auto', cmap='YlOrRd')
    plt.colorbar(label='Exponent')
    plt.xlabel('Variable Index')
    plt.ylabel('Term Index')
    plt.title(title)
    plt.tight_layout()
    plt.savefig(os.path.join('heatmaps', filename))
    plt.close()

# Create heatmaps directory if it doesn't exist
if not os.path.exists('heatmaps'):
    os.makedirs('heatmaps')

# Open file to save results
with open('polynomial_orders.txt', 'w') as f:
    # Test cases
    f.write("Test 2.2.3.b with polynomial 2x₁²x₂⁸-3x₁⁵x₂x₃⁴+x₁x₂x₃³-x₁x₂⁴:\n")
    Terms = [
        [2, 8, 0],  # 2x₁²x₂⁸
        [5, 1, 4],  # -3x₁⁵x₂x₃⁴
        [1, 1, 3],  # x₁x₂x₃³
        [1, 4, 0]   # -x₁x₂⁴
    ]
    Procedure = [2, 1, 0]  # x₃ > x₂ > x₁
    
    f.write(f"Original Terms: {Terms}\n")
    plot_terms_heatmap(Terms, "Original Terms (Test 2.2.3.b)", "test_2.2.3.b_original.png")

    ordered_terms_lex = determine_by_lex(Terms, Procedure)
    plot_terms_heatmap(ordered_terms_lex, "Lex Ordered Terms (Test 2.2.3.b)", "test_2.2.3.b_lex.png")
    f.write(f"Lex Ordered Terms: {ordered_terms_lex}\n")

    ordered_terms_glex = determine_by_glex(Terms, Procedure)
    plot_terms_heatmap(ordered_terms_glex, "Graded Lex Ordered Terms (Test 2.2.3.b)", "test_2.2.3.b_glex.png")
    f.write(f"Graded Lex Ordered Terms: {ordered_terms_glex}\n")

    ordered_terms_grevlex = determine_by_grevlex(Terms, Procedure)
    plot_terms_heatmap(ordered_terms_grevlex, "Graded Reverse Lex Ordered Terms (Test 2.2.3.b)", "test_2.2.3.b_grevlex.png")
    f.write(f"Graded Reverse Lex Ordered Terms: {ordered_terms_grevlex}\n\n")

    f.write("Test with 4 variables:\n")
    Terms4 = [
        [1, 0, 0, 2],  # w^2 x
        [0, 1, 1, 1],  # w y z
        [2, 0, 1, 0],  # x^2 z
        [1, 1, 0, 1]   # w x y
    ]
    Procedure4 = [3, 2, 1, 0]  # w > z > y > x

    f.write(f"Original Terms: {Terms4}\n")
    plot_terms_heatmap(Terms4, "Original Terms (4 variables)", "test_4var_original.png")

    ordered_terms4_lex = determine_by_lex(Terms4, Procedure4)
    plot_terms_heatmap(ordered_terms4_lex, "Lex Ordered Terms (4 variables)", "test_4var_lex.png")
    f.write(f"Lex Ordered Terms: {ordered_terms4_lex}\n")

    ordered_terms4_glex = determine_by_glex(Terms4, Procedure4)
    plot_terms_heatmap(ordered_terms4_glex, "Graded Lex Ordered Terms (4 variables)", "test_4var_glex.png")
    f.write(f"Graded Lex Ordered Terms: {ordered_terms4_glex}\n")

    ordered_terms4_grevlex = determine_by_grevlex(Terms4, Procedure4)
    plot_terms_heatmap(ordered_terms4_grevlex, "Graded Reverse Lex Ordered Terms (4 variables)", "test_4var_grevlex.png")
    f.write(f"Graded Reverse Lex Ordered Terms: {ordered_terms4_grevlex}\n\n")

    f.write("Test with 9 variables:\n")
    Terms9 = [
        [1, 0, 0, 0, 1, 0, 0, 0, 1],  # a b i
        [0, 1, 1, 0, 0, 0, 0, 1, 0],  # b c h
        [0, 0, 0, 1, 0, 1, 1, 0, 0],  # d f g
    ]
    Procedure9 = [8, 7, 6, 5, 4, 3, 2, 1, 0]  # i > h > g > f > e > d > c > b > a

    f.write(f"Original Terms: {Terms9}\n")
    plot_terms_heatmap(Terms9, "Original Terms (9 variables)", "test_9var_original.png")

    ordered_terms9_lex = determine_by_lex(Terms9, Procedure9)
    plot_terms_heatmap(ordered_terms9_lex, "Lex Ordered Terms (9 variables)", "test_9var_lex.png")
    f.write(f"Lex Ordered Terms: {ordered_terms9_lex}\n")

    ordered_terms9_glex = determine_by_glex(Terms9, Procedure9)
    plot_terms_heatmap(ordered_terms9_glex, "Graded Lex Ordered Terms (9 variables)", "test_9var_glex.png")
    f.write(f"Graded Lex Ordered Terms: {ordered_terms9_glex}\n")

    ordered_terms9_grevlex = determine_by_grevlex(Terms9, Procedure9)
    plot_terms_heatmap(ordered_terms9_grevlex, "Graded Reverse Lex Ordered Terms (9 variables)", "test_9var_grevlex.png")
    f.write(f"Graded Reverse Lex Ordered Terms: {ordered_terms9_grevlex}\n\n")

    f.write("Test with 30 variables:\n")
    Terms30 = [
        [1 if i % 3 == 0 else 0 for i in range(30)],  # Every 3rd variable has exponent 1
        [1 if i % 2 == 0 else 0 for i in range(30)],  # Every 2nd variable has exponent 1
        [1 if i % 5 == 0 else 0 for i in range(30)],  # Every 5th variable has exponent 1
    ]
    Procedure30 = list(range(29, -1, -1))  # Reverse order: var29 > var28 > ... > var0

    f.write(f"Original Terms: {Terms30}\n")
    plot_terms_heatmap(Terms30, "Original Terms (30 variables)", "test_30var_original.png")

    ordered_terms30_lex = determine_by_lex(Terms30, Procedure30)
    plot_terms_heatmap(ordered_terms30_lex, "Lex Ordered Terms (30 variables)", "test_30var_lex.png")
    f.write(f"Lex Ordered Terms: {ordered_terms30_lex}\n")

    ordered_terms30_glex = determine_by_glex(Terms30, Procedure30)
    plot_terms_heatmap(ordered_terms30_glex, "Graded Lex Ordered Terms (30 variables)", "test_30var_glex.png")
    f.write(f"Graded Lex Ordered Terms: {ordered_terms30_glex}\n")

    ordered_terms30_grevlex = determine_by_grevlex(Terms30, Procedure30)
    plot_terms_heatmap(ordered_terms30_grevlex, "Graded Reverse Lex Ordered Terms (30 variables)", "test_30var_grevlex.png")
    f.write(f"Graded Reverse Lex Ordered Terms: {ordered_terms30_grevlex}\n\n")
    f.write("Test with 1024 variables:\n")
    Terms1024 = [
        [np.random.randint(0, 11) for _ in range(1024)],  # Random exponents between 0 and 10
        [np.random.randint(0, 11) for _ in range(1024)],  # Random exponents between 0 and 10  
        [np.random.randint(0, 11) for _ in range(1024)],  # Random exponents between 0 and 10
    ]
    Procedure1024 = list(range(1023, -1, -1))  # Reverse order: var1023 > var1022 > ... > var0

    f.write(f"Original Terms: {Terms1024}\n")
    plot_terms_heatmap(Terms1024, "Original Terms (1024 variables)", "test_1024var_original.png")

    ordered_terms1024_lex = determine_by_lex(Terms1024, Procedure1024)
    plot_terms_heatmap(ordered_terms1024_lex, "Lex Ordered Terms (1024 variables)", "test_1024var_lex.png")
    f.write(f"Lex Ordered Terms: {ordered_terms1024_lex}\n")

    ordered_terms1024_glex = determine_by_glex(Terms1024, Procedure1024)
    plot_terms_heatmap(ordered_terms1024_glex, "Graded Lex Ordered Terms (1024 variables)", "test_1024var_glex.png")
    f.write(f"Graded Lex Ordered Terms: {ordered_terms1024_glex}\n")

    ordered_terms1024_grevlex = determine_by_grevlex(Terms1024, Procedure1024)
    plot_terms_heatmap(ordered_terms1024_grevlex, "Graded Reverse Lex Ordered Terms (1024 variables)", "test_1024var_grevlex.png")
    f.write(f"Graded Reverse Lex Ordered Terms: {ordered_terms1024_grevlex}\n")
