from methods.gauss import Gauss
from methods.refine import Refine
from methods.seidel import Seidel
from compare import Compare
from utils import console

matrix = []
with open("matrix.txt", "r", encoding="utf-8") as file:
    for line in file:
        if not line.strip():
            continue
        left, right = line.split("|")
        row = [float(x) for x in left.split()]
        row.append(float(right))
        matrix.append(row)

x0 = Gauss([row[:] for row in matrix], 2, True)
print()
console.rule(style="red")
print()
x_refine = None
if x0 is not None:
    x_refine = Refine(matrix, 0.0001, x0)

print()
console.rule(style="red")
print()
x_seidel = Seidel(matrix, 0.0001, 5)

x0 = Gauss([row[:] for row in matrix], 5, False)
if x0 is not None and x_refine is not None and x_seidel is not None:
    print()
    console.rule(style="red")
    print()
    Compare(matrix, [("Гаусс", x0, 5), ("Уточнение", x_refine, 5), ("Зейдель", x_seidel, 5)], 5)