import json

nb = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# Leibniz' Integration Rule\n",
                "\n",
                "Leibniz' rule tells us how to **differentiate an integral** when the integrand and/or the limits of integration depend on the differentiation variable.\n",
                "\n",
                "---"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Version 1: Fixed Limits (Differentiation Under the Integral Sign)\n",
                "\n",
                "**When:** The limits are constants, but the integrand depends on a parameter.\n",
                "\n",
                "$$\\frac{d}{dt} \\int_a^b f(x, t) \\, dx = \\int_a^b \\frac{\\partial f}{\\partial t}(x, t) \\, dx$$\n",
                "\n",
                "**Intuition:** If only the \"shape\" of the function changes (not the region), you just differentiate inside the integral.\n",
                "\n",
                "**Conditions:** $f$ and $\\partial f / \\partial t$ must be continuous."
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### Example\n",
                "\n",
                "$$\\frac{d}{dt} \\int_0^1 e^{tx} \\, dx = \\int_0^1 x e^{tx} \\, dx$$\n",
                "\n",
                "We can verify this: the left side is $\\int_0^1 e^{tx} dx = \\frac{e^t - 1}{t}$ and differentiating gives $\\frac{te^t - e^t + 1}{t^2}$, which matches $\\int_0^1 x e^{tx} dx$."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "import numpy as np\n",
                "from scipy import integrate\n",
                "\n",
                "# Verify Version 1 numerically at t = 2\n",
                "t_val = 2.0\n",
                "h = 1e-7\n",
                "\n",
                "# Left side: d/dt of integral (via finite difference)\n",
                "integral_at_t = integrate.quad(lambda x: np.exp(t_val * x), 0, 1)[0]\n",
                "integral_at_t_h = integrate.quad(lambda x: np.exp((t_val + h) * x), 0, 1)[0]\n",
                "numerical_derivative = (integral_at_t_h - integral_at_t) / h\n",
                "\n",
                "# Right side: integral of df/dt\n",
                "right_side = integrate.quad(lambda x: x * np.exp(t_val * x), 0, 1)[0]\n",
                "\n",
                "print(f'D/dt [integral]:  {numerical_derivative:.8f}')\n",
                "print(f'Integral [df/dt]: {right_side:.8f}')\n",
                "print(f'Match: {np.isclose(numerical_derivative, right_side)}')"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "---\n",
                "\n",
                "## Version 2: Variable Upper Limit Only\n",
                "\n",
                "**When:** The integrand does not depend on $t$, but the upper limit does.\n",
                "\n",
                "$$\\frac{d}{dt} \\int_a^t f(x) \\, dx = f(t)$$\n",
                "\n",
                "This is just the **Fundamental Theorem of Calculus** — a special case of Leibniz' rule."
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "---\n",
                "\n",
                "## Version 3: Variable Upper Limit + Parameter-Dependent Integrand\n",
                "\n",
                "**When:** Upper limit is $t$, lower limit is constant, and the integrand also depends on $t$.\n",
                "\n",
                "$$\\frac{d}{dt} \\int_a^t f(x, t) \\, dx = f(t, t) + \\int_a^t \\frac{\\partial f}{\\partial t}(x, t) \\, dx$$\n",
                "\n",
                "**Two contributions:**\n",
                "1. **Boundary term** $f(t,t)$: the upper limit moves, bringing in a new slice\n",
                "2. **Interior term** $\\int \\partial f/\\partial t$: the integrand itself changes at every point\n",
                "\n",
                "This is the version you encounter most often in the product integration proofs."
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### Example\n",
                "\n",
                "$$\\frac{d}{dt} \\int_0^t x e^{tx} \\, dx = t e^{t^2} + \\int_0^t x^2 e^{tx} \\, dx$$\n",
                "\n",
                "- Boundary term: $f(t,t) = t \\cdot e^{t^2}$\n",
                "- Interior term: $\\partial f / \\partial t = x^2 e^{tx}$"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Verify Version 3 numerically at t = 1.5\n",
                "t_val = 1.5\n",
                "h = 1e-7\n",
                "\n",
                "# Left side: d/dt of integral (finite difference)\n",
                "I_t = integrate.quad(lambda x: x * np.exp(t_val * x), 0, t_val)[0]\n",
                "I_t_h = integrate.quad(lambda x: x * np.exp((t_val + h) * x), 0, t_val + h)[0]\n",
                "numerical = (I_t_h - I_t) / h\n",
                "\n",
                "# Right side: f(t,t) + integral of df/dt\n",
                "boundary = t_val * np.exp(t_val**2)\n",
                "interior = integrate.quad(lambda x: x**2 * np.exp(t_val * x), 0, t_val)[0]\n",
                "analytical = boundary + interior\n",
                "\n",
                "print(f'Numerical d/dt:      {numerical:.8f}')\n",
                "print(f'f(t,t) + int(df/dt): {analytical:.8f}')\n",
                "print(f'Match: {np.isclose(numerical, analytical)}')"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "---\n",
                "\n",
                "## Version 4: The Full General Form\n",
                "\n",
                "**When:** Both limits and the integrand depend on $t$.\n",
                "\n",
                "$$\\frac{d}{dt} \\int_{a(t)}^{b(t)} f(x, t) \\, dx = f(b(t), t) \\cdot b'(t) - f(a(t), t) \\cdot a'(t) + \\int_{a(t)}^{b(t)} \\frac{\\partial f}{\\partial t}(x, t) \\, dx$$\n",
                "\n",
                "**Three contributions:**\n",
                "1. **Upper boundary moves**: $+f(b(t), t) \\cdot b'(t)$\n",
                "2. **Lower boundary moves**: $-f(a(t), t) \\cdot a'(t)$\n",
                "3. **Integrand changes**: $\\int \\partial f / \\partial t \\, dx$\n",
                "\n",
                "Every other version is a special case of this."
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### Example\n",
                "\n",
                "Let $a(t) = t$, $b(t) = t^2$, $f(x,t) = \\sin(tx)$. Then:\n",
                "\n",
                "$$\\frac{d}{dt} \\int_t^{t^2} \\sin(tx) \\, dx = 2t\\sin(t^3) - \\sin(t^2) + \\int_t^{t^2} x\\cos(tx) \\, dx$$"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Verify Version 4 numerically at t = 1.0\n",
                "t_val = 1.0\n",
                "h = 1e-7\n",
                "\n",
                "a = lambda t: t\n",
                "b = lambda t: t**2\n",
                "f = lambda x, t: np.sin(t * x)\n",
                "\n",
                "# Left side: d/dt of integral (finite difference)\n",
                "I_t = integrate.quad(lambda x: f(x, t_val), a(t_val), b(t_val))[0]\n",
                "I_t_h = integrate.quad(lambda x: f(x, t_val + h), a(t_val + h), b(t_val + h))[0]\n",
                "numerical = (I_t_h - I_t) / h\n",
                "\n",
                "# Right side: all three terms\n",
                "upper_boundary = f(b(t_val), t_val) * 2 * t_val\n",
                "lower_boundary = f(a(t_val), t_val) * 1\n",
                "interior = integrate.quad(lambda x: x * np.cos(t_val * x), a(t_val), b(t_val))[0]\n",
                "analytical = upper_boundary - lower_boundary + interior\n",
                "\n",
                "print(f'Numerical d/dt:            {numerical:.8f}')\n",
                "print(f'Boundary + Interior terms: {analytical:.8f}')\n",
                "print(f'Match: {np.isclose(numerical, analytical)}')"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "---\n",
                "\n",
                "## Continuity Conditions\n",
                "\n",
                "Leibniz' rule requires **continuity** — but of what exactly?\n",
                "\n",
                "For the general form (Version 4), we need:\n",
                "1. $f(x, t)$ is continuous (for the **boundary terms** to be well-defined)\n",
                "2. $\\partial f / \\partial t$ is continuous (to **differentiate under the integral**)\n",
                "\n",
                "### Why this matters in product integration\n",
                "\n",
                "In the proof of Theorem 1.17 (Van Loan), we differentiate:\n",
                "\n",
                "$$\\frac{\\partial}{\\partial t} \\int_s^t \\prod_s^u(I + A(x)\\,dx)\\, B(u) \\prod_u^t(I + C(x)\\,dx)\\, du$$\n",
                "\n",
                "Applying Version 3 of Leibniz' rule, two things happen:\n",
                "- **Boundary term** (upper limit hits $t$): evaluates the integrand at $u = t$, which involves $B(t)$ $\\Rightarrow$ needs **$B(x)$ continuous**\n",
                "- **Interior term** (differentiate under the integral): $\\partial/\\partial t$ only hits $\\prod_u^t(I + C(x)\\,dx)$, which involves $C(t)$ $\\Rightarrow$ needs **$C(x)$ continuous**\n",
                "\n",
                "Note that $A(x)$ does **not** need to be continuous for this step, because $\\prod_s^u(I + A(x)\\,dx)$ has no $t$-dependence — both its limits ($s$ and $u$) are independent of $t$, so it passes through the $\\partial/\\partial t$ untouched.\n",
                "\n",
                "This is exactly what Remark 1.18 in the textbook states."
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "---\n",
                "\n",
                "## Summary Table\n",
                "\n",
                "| Version | Limits | Integrand depends on $t$? | Formula |\n",
                "|---------|--------|---------------------------|---|\n",
                "| 1 | Fixed $[a, b]$ | Yes | $\\int_a^b \\frac{\\partial f}{\\partial t} dx$ |\n",
                "| 2 (FTC) | $[a, t]$ | No | $f(t)$ |\n",
                "| 3 | $[a, t]$ | Yes | $f(t,t) + \\int_a^t \\frac{\\partial f}{\\partial t} dx$ |\n",
                "| 4 (General) | $[a(t), b(t)]$ | Yes | $f(b(t),t)b'(t) - f(a(t),t)a'(t) + \\int_{a(t)}^{b(t)} \\frac{\\partial f}{\\partial t} dx$ |"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "---\n",
                "\n",
                "## \u2705 Check Your Understanding\n",
                "\n",
                "**Q1:** Which version of Leibniz' rule reduces to the Fundamental Theorem of Calculus?\n",
                "\n",
                "**Q2:** Compute $\\frac{d}{dt} \\int_0^t e^{-x^2 t} \\, dx$ using the appropriate version. Which terms appear?\n",
                "\n",
                "**Q3:** If both limits are fixed and the integrand does not depend on $t$, what does Leibniz' rule give? Does this make sense?"
            ]
        }
    ],
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "name": "python",
            "version": "3.11.0"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

with open("leibniz_integration_rule.ipynb", "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1)

print("Notebook written successfully")
