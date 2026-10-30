import math
from utils import (console, rnd, make_extended_matrix, print_roots,
                   fmt, par, lin, sub, sup, block, banner, WHITE)
from methods.gauss import Gauss
from rich.align import Align
from rich.console import Group
from rich.panel import Panel
from rich.text import Text
from rich import box


def Refine(Matrix, eps, x0=None, max_iter=50):
    digits = math.ceil(-math.log10(eps) - 1e-9) + 1
    banner("УТОЧНЕНИЕ РЕШЕНИЯ СЛУ")
    console.print(Align.center(Text(f"Точность ε = {eps}, знаков после запятой: {digits}", style=WHITE)))
    n = len(Matrix)
    A = [row[:n] for row in Matrix]
    b = [row[n] for row in Matrix]
    if x0 is None:
        console.print(Align.center(Text("Начальное приближение (прямой метод)", style="bold #89b4fa")))
        x = Gauss([row[:] for row in Matrix], digits=digits, show=False)
        if x is None:
            return None
    else:
        x = [float(v) for v in x0]
        console.print(Align.center(Text("Начальное приближение взято из прямого метода", style="bold #89b4fa")))
    converged = False
    for k in range(max_iter):
        items = []
        b_k = [rnd(sum(A[i][j] * x[j] for j in range(n)), digits) for i in range(n)]
        items.append(block([
            f"b{sub(i + 1)}{sup(k)} = {lin(A[i], [par(v, digits) for v in x], '·', digits)} = {fmt(b_k[i], digits)}"
            for i in range(n)
        ]))
        items.append(Text(""))
        r = [rnd(b[i] - b_k[i], digits) for i in range(n)]
        items.append(block([
            f"r{sub(i + 1)}{sup(k)} = b{sub(i + 1)} - b{sub(i + 1)}{sup(k)} = "
            f"{fmt(b[i], digits)} - {par(b_k[i], digits)} = {fmt(r[i], digits)}"
            for i in range(n)
        ]))
        items.append(Text(""))
        items.append(Text("Рассмотрим СЛУ:", style="bold #89b4fa"))
        names = [f"ε{sub(j + 1)}{sup(k)}" for j in range(n)]
        items.append(block([f"{lin(A[i], names, '', digits)} = {fmt(r[i], digits)}" for i in range(n)]))

        ext = [A[i][:] + [r[i]] for i in range(n)]
        items.append(make_extended_matrix(ext, "Расширенная матрица", "#74c7ec", digits=digits))
        e = Gauss([row[:] for row in ext], digits=digits, show=False)
        if e is None:
            return None
        items.append(block([f"ε{sub(i + 1)}{sup(k)} = {fmt(e[i], digits)}" for i in range(n)]))
        items.append(Text(""))
        x_new = [rnd(x[i] + e[i], digits) for i in range(n)]
        items.append(block([
            f"x{sub(i + 1)}{sup(k + 1)} = x{sub(i + 1)}{sup(k)} + ε{sub(i + 1)}{sup(k)} = "
            f"{fmt(x[i], digits)} + {par(e[i], digits)} = {fmt(x_new[i], digits)}"
            for i in range(n)
        ]))
        x = x_new
        stop = all(abs(v) < eps for v in e)
        if stop:
            items.append(Text(""))
            items.append(Text(f"Все |ε| < {eps}, процесс остановлен", style="bold #a6e3a1"))
        console.print(Align.center(Panel(
            Group(*items),
            title=f"[bold #fab387]Итерация {k + 1}[/bold #fab387]",
            border_style="#fab387",
            box=box.ROUNDED,
            expand=False,
            padding=(1, 2),
        )))
        if stop:
            converged = True
            break
    if not converged:
        console.print(Align.center(Text(f"Точность {eps} не достигнута за {max_iter} итераций", style="bold #f38ba8")))
    x = [rnd(v, digits - 1) for v in x]
    print_roots(x, "Уточнённые корни", "#a6e3a1", digits=digits - 1)
    return x