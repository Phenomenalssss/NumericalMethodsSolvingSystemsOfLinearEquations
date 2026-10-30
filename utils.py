from decimal import Decimal, ROUND_HALF_UP

from rich.console import Console
from rich.align import Align
from rich.panel import Panel
from rich.text import Text
from rich import box


console = Console()


SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
WHITE = "bold white"


def sub(i):
    """3 -> ₃"""
    return str(i).translate(SUB)


def sup(k):
    """2 -> ⁽²⁾"""
    return "⁽" + str(k).translate(SUP) + "⁾"


def fmt(v, d):
    """Число без лишних нулей: 2.41000 -> 2.41"""
    s = f"{v:.{d}f}"
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def par(v, d):
    """Отрицательные числа в скобках: (-2.76)"""
    s = fmt(v, d)
    return f"({s})" if s.startswith("-") else s


def lin(coefs, factors, sep, d, skip_unit=False, skip_zero=False):
    """
    2.53·0.68 + 0.46·(-2.76) - 1.72·1.14  или  2.53ε₁ - 0.46ε₂
    skip_unit - не писать коэффициент, равный ±1 (R₁ + R₃ вместо 1·R₁ + 1·R₃)
    skip_zero - пропускать слагаемые с нулевым коэффициентом
    """
    out = ""
    for c, f in zip(coefs, factors):
        s = fmt(c, d)
        if skip_zero and s == "0":
            continue
        neg = s.startswith("-")
        body = s.lstrip("-")
        term = f if (skip_unit and body == "1") else body + sep + f
        if not out:
            out = ("-" if neg else "") + term
        else:
            out += f" {'-' if neg else '+'} {term}"
    return out or "0"


def block(lines):
    """Строки одним блоком, bold white."""
    return Text("\n".join(lines), style=WHITE)


def banner(title):
    """Широкая фиолетовая плашка с названием метода."""
    console.print(Align.center(Panel(f"[bold #cba6f7]{title.center(100)}[/bold #cba6f7]", border_style="#cba6f7")))


def error(text):
    """Красная панель с ошибкой."""
    console.print(Align.center(Panel(f"[bold white]{text}[/bold white]", border_style="#f38ba8",
                                     title="[bold #f38ba8]Ошибка[/bold #f38ba8]")))


def rnd(v, d):
    """Округление по правилу 5 (half up), а не банковское, как у встроенного round."""
    return float(Decimal(repr(float(v))).quantize(Decimal(1).scaleb(-d), rounding=ROUND_HALF_UP))


def print_matrix(matrix, title, color):
    n_vars = len(matrix[0]) - 1
    rows = []
    for row in matrix:
        cells = []
        first_printed = False
        for i in range(n_vars):
            value = row[i]
            if value == 0 or value == " ":
                cells.append(None)
                continue
            var = f"x{sub(i + 1)}"
            coeff = abs(value)
            coeff_str = "" if coeff == 1 else f"{coeff:g}"
            plain = f"{coeff_str}{var}"
            markup = f"{coeff_str}[bold white]{var}[/bold white]"
            if not first_printed:
                sign = "-" if value < 0 else ""
            else:
                sign = "-" if value < 0 else "+"
            first_printed = True
            cells.append((sign, plain, markup))
        rows.append((cells, str(row[-1])))
    sign_w = [0] * n_vars
    body_w = [0] * n_vars
    for cells, _ in rows:
        for i, cell in enumerate(cells):
            if cell:
                sign, plain, _ = cell
                sign_w[i] = max(sign_w[i], len(sign))
                body_w[i] = max(body_w[i], len(plain))
    left_sides = []
    for cells, _ in rows:
        parts = []
        for i, cell in enumerate(cells):
            col_w = sign_w[i] + (1 if sign_w[i] else 0) + body_w[i]
            if cell is None:
                parts.append(" " * col_w)
                continue
            sign, plain, markup = cell
            sign_part = sign.rjust(sign_w[i])
            sep = " " if sign_w[i] else ""
            pad = " " * (body_w[i] - len(plain))
            parts.append(f"{sign_part}{sep}{pad}{markup}")
        left_sides.append(" ".join(parts))
    right_w = max(len(r) for _, r in rows)
    lines = [
        f"[bold white]{left} = {right.rjust(right_w)}[/bold white]"
        for left, (_, right) in zip(left_sides, rows)
    ]
    text_matrix = Text.from_markup("\n".join(lines))
    panel = Panel(
        text_matrix,
        title=f"[bold {color}]{title}[/bold {color}]",
        border_style=f"{color}",
        box=box.ROUNDED,
        expand=False,
    )
    console.print(Align.center(panel))


def make_extended_matrix(matrix, title, color, digits=3):
    """Строит панель с расширенной матрицей, но не печатает её."""
    cols = len(matrix[0]) - 1
    strs = [[fmt(v, digits) for v in row] for row in matrix]
    widths = [max(max(len(r[j]) for r in strs), 2) for j in range(cols + 1)]
    lines = []
    for row in strs:
        values = [v.rjust(widths[j]) for j, v in enumerate(row)]
        left = "  ".join(values[:cols])
        right = values[cols]
        lines.append(f"[bold white]{left}[/bold white]  [bold {color}]│[/bold {color}]  [bold white]{right}[/bold white]")
    return Panel(
        Align.center("\n".join(lines)),
        title=f"[bold {color}]{title}[/bold {color}]",
        border_style=f"{color}",
        box=box.ROUNDED,
        expand=False,
    )


def print_extended_matrix(matrix, title, color, center=True, digits=3):
    panel = make_extended_matrix(matrix, title, color, digits)
    console.print(Align.center(panel) if center else panel)


def print_roots(roots, title, color, digits=None):
    lst = []
    for i in range(len(roots)):
        val = fmt(float(roots[i]), digits) if digits is not None else str(roots[i])
        lst.append(f"x{sub(i + 1)}" + " = " + f"[bold white]{val}[/bold white]")
    text_matrix = "\n".join(lst)
    custom_panel = Panel(
        Align.center(f"[bold white]{text_matrix}[/bold white]"),
        title=f"[bold {color}]{title}[/bold {color}]",
        title_align="center",
        border_style=f"{color}",
        box=box.ROUNDED,
        expand=False,
    )
    console.print(Align.center(custom_panel))