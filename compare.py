from fractions import Fraction

from utils import console, rnd, fmt, sub, banner, error
from rich.align import Align
from rich.table import Table
from rich import box

GREEN = "#a6e3a1"
RED = "#f38ba8"
BLUE = "#89b4fa"
CYAN = "#74c7ec"


def exact_solution(Matrix):
    """
    Точное решение СЛУ в дробях (Fraction), без ошибок округления.
    Числа читаются из их десятичной записи: 0.92 -> 23/25, а не 0.92000000000000004...
    Возвращает список Fraction или None, если решение не единственное.
    """
    n = len(Matrix)
    M = [[Fraction(str(v)) for v in row] for row in Matrix]
    for i in range(n):
        p = next((k for k in range(i, n) if M[k][i] != 0), None)
        if p is None:
            return None
        M[i], M[p] = M[p], M[i]
        for k in range(n):
            if k != i and M[k][i] != 0:
                f = M[k][i] / M[i][i]
                M[k] = [a - f * b for a, b in zip(M[k], M[i])]
    return [M[i][n] / M[i][i] for i in range(n)]


def Compare(Matrix, results, exact_digits=6):
    """
    Таблица сравнения корней разных методов с точным решением.
    Matrix  - исходная расширенная матрица n x (n+1)
    results - список (название, корни, знаков_после_запятой) для каждого метода
    Зелёным подсвечены корни, совпадающие с точными (точные округляются
    до числа знаков самого метода по правилу 5).
    """
    banner("СРАВНЕНИЕ МЕТОДОВ")
    exact = exact_solution(Matrix)
    if exact is None:
        error("Система не имеет единственного решения, сравнивать не с чем")
        return None
    exact_f = [float(v) for v in exact]
    n = len(exact_f)

    table = Table(box=box.ROUNDED, border_style=BLUE, header_style=f"bold {BLUE}",
                  title=f"[bold {BLUE}]Корни СЛУ[/bold {BLUE}]", show_lines=False, pad_edge=True)
    table.add_column("", justify="center", style="bold white")
    for name, _, d in results:
        table.add_column(f"{name}\n({d} зн.)", justify="right")
    table.add_column(f"Точное\n({exact_digits} зн.)", justify="right", header_style=f"bold {CYAN}")

    errors = [0.0] * len(results)
    hits = [0] * len(results)
    for i in range(n):
        cells = []
        for m, (_, x, d) in enumerate(results):
            ok = abs(rnd(exact_f[i], d) - x[i]) < 1e-9
            hits[m] += ok
            errors[m] = max(errors[m], abs(x[i] - exact_f[i]))
            color = GREEN if ok else "white"
            cells.append(f"[bold {color}]{fmt(float(x[i]), d)}[/bold {color}]")
        table.add_row(f"x{sub(i + 1)}", *cells,
                      f"[bold {CYAN}]{fmt(float(rnd(exact_f[i], exact_digits)), exact_digits)}[/bold {CYAN}]")

    table.add_section()
    best = min(errors)
    table.add_row("Совпало", *[f"[bold {GREEN if h == n else 'white'}]{h} из {n}[/bold {GREEN if h == n else 'white'}]"
                               for h in hits], "")
    table.add_row("Макс.\nпогрешность",
                  *[f"[bold {GREEN if e == best else 'white'}]{e:.1e}[/bold {GREEN if e == best else 'white'}]"
                    for e in errors], "")
    console.print(Align.center(table))

    winners = [results[m][0] for m, e in enumerate(errors) if e == best]
    console.print(Align.center(
        f"[bold white]Точнее всех: [/bold white][bold {GREEN}]{', '.join(winners)}[/bold {GREEN}]"))
    console.print(Align.center(
        f"[white]Зелёным отмечены корни, совпавшие с точными после округления до знаков метода[/white]"))
    return exact