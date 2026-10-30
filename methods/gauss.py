from utils import console, rnd
from utils import print_matrix
from utils import print_extended_matrix
from utils import print_roots
from rich.align import Align
from rich.panel import Panel


def Gauss(Matrix, digits=3, show=True):
    if show:
        console.print(Align.center(Panel(
            "[bold #cba6f7]                                      РЕШЕНИЕ СИСТЕМЫ МЕТОДОМ ГАУССА                                      [/bold #cba6f7]",
            border_style="#cba6f7")))
        print_matrix(Matrix, "Исходная матрица", "#89b4fa")
        print_extended_matrix(Matrix, "Расширенная матрица", "#74c7ec", digits=digits)
    n = len(Matrix)
    for i in range(n):
        if Matrix[i][i] == 0:
            for k in range(i + 1, n):
                if Matrix[k][i] != 0:
                    Matrix[i], Matrix[k] = Matrix[k], Matrix[i]
                    if show:
                        print_extended_matrix(Matrix, "Меняем строчки местами", "#f9e2af", digits=digits)
                    break
            else:
                console.print(Align.center(Panel("[bold white]Система не имеет единственного решения[/bold white]",
                                                 border_style="#f38ba8",
                                                 title="[bold #f38ba8]Ошибка[/bold #f38ba8]")))
                return None
        for k in range(i + 1, n):
            c = Matrix[k][i] / Matrix[i][i]
            Matrix[k][i] = 0
            for j in range(i + 1, n + 1):
                Matrix[k][j] = rnd(Matrix[k][j] - c * Matrix[i][j], digits)
            if show:
                print_extended_matrix(Matrix, "Элементарные преобразования", "#fab387", digits=digits)
    if show:
        print_matrix(Matrix, "Треугольная матрица", "#94e2d5")
    x = [0] * n
    for i in range(n - 1, -1, -1):
        s = 0
        for j in range(i + 1, n):
            s = s + Matrix[i][j] * x[j]
        x[i] = (Matrix[i][n] - s) / Matrix[i][i]
    x = [rnd(value, digits) for value in x]
    if show:
        print_roots(x, "Корни", "#a6e3a1", digits=digits)
    return x