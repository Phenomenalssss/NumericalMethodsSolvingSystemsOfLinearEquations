from utils import (console, rnd, print_roots,
                   fmt, par, lin, sub, sup, block, banner, error, WHITE)
from methods.dominance import MakeDominant
from rich.align import Align
from rich.console import Group
from rich.panel import Panel
from rich.text import Text
from rich import box


def Seidel(Matrix, eps, digits=3, x0=None, max_iter=50):
    banner("РЕШЕНИЕ СЛУ МЕТОДОМ ГАУССА-ЗЕЙДЕЛЯ")
    console.print(Align.center(Text(f"Точность ε = {eps}, знаков после запятой: {digits}", style=WHITE)))
    Matrix, ok = MakeDominant([row[:] for row in Matrix], digits)
    if not ok:
        console.print(Align.center(Text("Метод может расходиться, считаем по исходной системе",
                                        style="bold #f9e2af")))
    n = len(Matrix)
    A = [row[:n] for row in Matrix]
    b = [row[n] for row in Matrix]
    if any(A[i][i] == 0 for i in range(n)):
        error("На диагонали есть нулевой элемент, aᵢᵢ ≠ 0 не выполняется")
        return None
    x = [0.0] * n if x0 is None else [float(v) for v in x0]
    console.print(Align.center(Text(
        "Начальное приближение: " + ", ".join(f"x{sub(i + 1)}{sup(0)} = {fmt(v, digits)}" for i, v in enumerate(x)),
        style="bold #89b4fa")))
    converged = False
    for k in range(1, max_iter + 1):
        items = []
        x_new = x[:]
        eq_lines = []
        for i in range(n):
            expr = fmt(b[i], digits)
            s = 0
            for j in range(n):
                if j == i:
                    continue
                expr += f" - {par(A[i][j], digits)}·{par(x_new[j], digits)}"
                s += A[i][j] * x_new[j]
            x_new[i] = rnd((b[i] - s) / A[i][i], digits)
            eq_lines.append(
                f"x{sub(i + 1)}{sup(k)} = 1/{par(A[i][i], digits)}·({expr}) = {fmt(x_new[i], digits)}")
        items.append(block(eq_lines))
        items.append(Text(""))
        x = x_new
        if any(abs(v) > 1e12 for v in x):
            error("Процесс расходится")
            return None
        items.append(Text(f"({', '.join(fmt(v, digits) for v in x)}) - {k}-е приближение",
                          style="bold #89b4fa"))
        items.append(Text(""))
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
        stop = all(abs(v) < eps for v in r)
        items.append(Text(""))
        if stop:
            items.append(Text(f"Все |r| < {eps}, процесс остановлен", style="bold #a6e3a1"))
        else:
            items.append(Text(f"Есть |r| ≥ {eps}, ищем {k + 1}-е приближение", style="bold #f9e2af"))
        console.print(Align.center(Panel(
            Group(*items),
            title=f"[bold #fab387]Итерация {k}[/bold #fab387]",
            border_style="#fab387", box=box.ROUNDED, expand=False, padding=(1, 2),
        )))
        if stop:
            converged = True
            break
    if not converged:
        console.print(Align.center(Text(f"Точность {eps} не достигнута за {max_iter} итераций",
                                        style="bold #f38ba8")))
    print_roots(x, "Решение методом Гаусса-Зейделя", "#a6e3a1", digits=digits)
    return x