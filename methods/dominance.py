from itertools import product
from utils import (console, rnd, fmt, lin, sub, banner, error, print_extended_matrix,
                   WHITE)
from rich.align import Align
from rich.panel import Panel
from rich.text import Text
from rich import box


COEFS = (0, 1, -1, 0.5, -0.5, 2, -2, 3, -3)
EPS = 1e-9


def margin(row, i):
    return abs(row[i]) - sum(abs(v) for j, v in enumerate(row) if j != i)


def is_dominant(A):
    return all(margin(A[i], i) > EPS for i in range(len(A)))


def show_dominance(A, digits, title="Проверка сходимости"):
    n = len(A)
    lines, ok = [], True
    for i in range(n):
        others = [abs(A[i][j]) for j in range(n) if j != i]
        good = margin(A[i], i) > EPS
        ok = ok and good
        color = "#a6e3a1" if good else "#f38ba8"
        lines.append(
            f"[bold {color}]|{fmt(A[i][i], digits)}| = {fmt(abs(A[i][i]), digits)} "
            f"{'>' if good else '≤'} {' + '.join(fmt(v, digits) for v in others)} = "
            f"{fmt(sum(others), digits)}[/bold {color}]")
    verdict = ("[bold #a6e3a1]Достаточное условие сходимости выполняется[/bold #a6e3a1]" if ok else
               "[bold #f9e2af]Достаточное условие не выполняется[/bold #f9e2af]")
    console.print(Align.center(Panel(
        "\n".join(lines) + "\n\n" + verdict,
        title=f"[bold #89b4fa]{title}[/bold #89b4fa]",
        border_style="#89b4fa", box=box.ROUNDED, expand=False)))
    return ok


def _independent(basis, v):
    v = list(v)
    for b in basis:
        p = next(j for j, x in enumerate(b) if abs(x) > EPS)
        if abs(v[p]) > EPS:
            f = v[p] / b[p]
            v = [x - f * y for x, y in zip(v, b)]
    if max(abs(x) for x in v) < EPS:
        return False
    basis.append(v)
    return True


def find_transform(A):
    n = len(A)
    candidates = []
    for i in range(n):
        found = []
        for c in product(COEFS, repeat=n):
            if not any(c):
                continue
            row = [sum(c[k] * A[k][j] for k in range(n)) for j in range(n)]
            m = margin(row, i)
            if m > EPS:
                found.append(((sum(1 for v in c if v), sum(1 for v in c if v != int(v)), sum(abs(v) for v in c), -m), c))
        if not found:
            return None
        found.sort(key=lambda t: t[0])
        candidates.append([c for _, c in found])
    def pick(i, basis, chosen):
        if i == n:
            return chosen
        for c in candidates[i][:60]:
            b2 = [r[:] for r in basis]
            row = [sum(c[k] * A[k][j] for k in range(n)) for j in range(n)]
            if _independent(b2, row):
                res = pick(i + 1, b2, chosen + [c])
                if res:
                    return res
        return None
    return pick(0, [], [])


def MakeDominant(Matrix, digits=3, show=True):
    A = [row[:-1] for row in Matrix]
    n = len(A)
    if show_dominance(A, digits):
        return Matrix, True
    banner("ПРЕОБРАЗОВАНИЕ МАТРИЦЫ К ДИАГОНАЛЬНОМУ ПРЕОБЛАДАНИЮ")
    C = find_transform(A)
    if C is None:
        error("Не удалось подобрать элементарные преобразования с диагональным преобладанием")
        return Matrix, False
    names = [f"R{sub(k + 1)}" for k in range(n)]
    new = [[rnd(sum(C[i][k] * Matrix[k][j] for k in range(n)), 10) for j in range(n + 1)]
           for i in range(n)]
    if show:
        print_extended_matrix(Matrix, "Исходная расширенная матрица", "#74c7ec", digits=digits)
        console.print(Align.center(Text(
            "\n".join(f"R{sub(i + 1)}' = {lin(C[i], names, '·', digits, skip_unit=True, skip_zero=True)}"
                      for i in range(n)), style=WHITE)))
        print_extended_matrix(new, "Преобразованная матрица", "#fab387", digits=digits)
    show_dominance([row[:-1] for row in new], digits, "Проверка после преобразования")
    return new, True