"""Verify all Gaussian elimination steps with NumPy before rendering."""
import numpy as np

print("=" * 60)
print("VERIFICATION: Gaussian Elimination Steps")
print("=" * 60)

# Original system
A = np.array([[1, 1, 1],
              [2, 3, 1],
              [1, 2, 3]], dtype=float)
b = np.array([6, 11, 14], dtype=float)

# Augmented matrix
aug = np.column_stack([A, b])
print("\nOriginal augmented matrix:")
print(aug)

# Step 1: R2 = R2 - 2*R1
aug[1] = aug[1] - 2 * aug[0]
print("\nAfter R2 <- R2 - 2*R1:")
print(aug)
assert np.allclose(aug[1], [0, 1, -1, -1]), f"Step 1 FAILED: {aug[1]}"
print("  ✓ Row 2 = [0, 1, -1 | -1] — CORRECT")

# Step 2: R3 = R3 - R1 (using original R1)
aug_orig = np.array([[1, 1, 1, 6],
                      [0, 1, -1, -1],
                      [1, 2, 3, 14]], dtype=float)
aug[2] = np.array([1, 2, 3, 14]) - np.array([1, 1, 1, 6])
print("\nAfter R3 <- R3 - R1:")
print(aug)
assert np.allclose(aug[2], [0, 1, 2, 8]), f"Step 2 FAILED: {aug[2]}"
print("  ✓ Row 3 = [0, 1, 2 | 8] — CORRECT")

# Step 3: R3 = R3 - R2
aug[2] = aug[2] - aug[1]
print("\nAfter R3 <- R3 - R2:")
print(aug)
assert np.allclose(aug[2], [0, 0, 3, 9]), f"Step 3 FAILED: {aug[2]}"
print("  ✓ Row 3 = [0, 0, 3 | 9] — CORRECT")

# Back substitution
z = aug[2, 3] / aug[2, 2]
y = (aug[1, 3] - aug[1, 2] * z) / aug[1, 1]
x = (aug[0, 3] - aug[0, 1] * y - aug[0, 2] * z) / aug[0, 0]
print(f"\nBack substitution:")
print(f"  z = {aug[2,3]}/{aug[2,2]} = {z}")
print(f"  y = ({aug[1,3]} - ({aug[1,2]})*{z}) / {aug[1,1]} = {y}")
print(f"  x = ({aug[0,3]} - ({aug[0,1]})*{y} - ({aug[0,2]})*{z}) / {aug[0,0]} = {x}")
assert (x, y, z) == (1.0, 2.0, 3.0), f"Solution FAILED: ({x}, {y}, {z})"
print(f"  ✓ Solution (x, y, z) = ({int(x)}, {int(y)}, {int(z)}) — CORRECT")

# Verification: substitute back
print("\nSubstitution check:")
sol = np.array([x, y, z])
for i, eq in enumerate(["x + y + z = 6", "2x + 3y + z = 11", "x + 2y + 3z = 14"]):
    result = A[i] @ sol
    print(f"  Eq {i+1}: {eq}  =>  {A[i]} · {sol} = {result}  {'✓' if result == b[i] else '✗'}")
    assert result == b[i], f"Verification FAILED for equation {i+1}"

# Also verify with numpy.linalg.solve
sol_np = np.linalg.solve(A, b)
assert np.allclose(sol_np, [1, 2, 3]), f"np.linalg.solve gave {sol_np}"
print(f"\n  np.linalg.solve confirms: {sol_np}")

print("\n" + "=" * 60)
print("ALL VERIFICATIONS PASSED ✓")
print("=" * 60)
