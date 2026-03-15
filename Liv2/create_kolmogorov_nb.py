import nbformat as nbf

nb = nbf.v4.new_notebook()

# Title and Intro
nb.cells.append(nbf.v4.new_markdown_cell("""# The Genius of Kolmogorov's Differential Equations
Welcome to the next big step in understanding Markov Jump Processes! 

Previously, we looked at the **intensity matrix $\\boldsymbol{\\Lambda}(t)$**, which gives us the *microscopic*, split-second rates of jumping between states. 

But what if we want to know the *macroscopic* picture? For example, "What is the probability that a healthy 30-year-old will be disabled by age 50?" This corresponds to estimating the transition probability matrix **$\\boldsymbol{P}(s, t)$** over a span of 20 years. 

Going from instantaneous rates to long-term probabilities is notoriously difficult. This is where the genius of Andrey Kolmogorov comes in. He discovered two elegant differential equations that connect the two concepts.

## 1. The Forward and Backward Equations
Kolmogorov proved that the transition probability matrix $\\boldsymbol{P}(s, t)$ satisfies two fundamental differential equations:

**Kolmogorov's Forward Equation:**
$$ \\frac{\\partial}{\\partial t} \\boldsymbol{P}(s, t) = \\boldsymbol{P}(s, t) \\boldsymbol{\\Lambda}(t) $$
*(Given state $i$ at time $s$ (the past), we look forward to time $t$ (the future) and multiply by the rate of jumping into our final state right at the end.)*

**Kolmogorov's Backward Equation:**
$$ \\frac{\\partial}{\\partial s} \\boldsymbol{P}(s, t) = -\\boldsymbol{\\Lambda}(s) \\boldsymbol{P}(s, t) $$
*(Given the final state at $t$, we look backward from our starting state at $s$, and multiply by the rate of making the first jump right at the beginning.)*

### Why is this genius?
Instead of trying to calculate complicated probabilities of infinite possible paths over 20 years, we just **solve a differential equation**! Since the initial condition is perfectly known (at $t=s$, you are in your current state with 100% certainty, so $\\boldsymbol{P}(s, s) = \\boldsymbol{I}$), this becomes a standard Initial Value Problem (IVP).
"""))

# Connections
nb.cells.append(nbf.v4.new_markdown_cell("""## 2. Connecting the Dots: Van Loan & Runge-Kutta

How does this relate to the previous topics you studied in `Liv2` like the Van Loan theorem and Runge-Kutta?

### Case A: Time-Homogeneous Processes (The Van Loan connection)
If the transition rates are constant over time (i.e., $\\boldsymbol{\\Lambda}(t) = \\boldsymbol{\\Lambda}$), evaluating the Kolmogorov equations becomes analytically simple. The solution to the differential equation $P'(t) = P(t)\\Lambda$ with $P(0) = I$ is simply the **matrix exponential**:
$$ \\boldsymbol{P}(0, t) = e^{\\boldsymbol{\\Lambda} t} $$

When pricing life insurance products, we often don't just need the probabilities; we need the **integral** of these probabilities (e.g., to calculate the expected duration spent in a state, or to price a continuous annuity). 
Integrating a matrix exponential $\\int e^{\\boldsymbol{\\Lambda} t} dt$ directly can be computationally messy. 

**Enter Van Loan's Theorem:** It provides a brilliant shortcut. By constructing a larger block matrix and computing its matrix exponential, Van Loan gives us the exact integral of the transition probabilities (and even higher-order moments) simultaneously, completely avoiding numerical integration!

### Case B: Time-Inhomogeneous Processes (The Runge-Kutta connection)
Human mortality is *not* constant. We are more likely to die at age 80 than age 30. Therefore, real life insurance models use a time-dependent intensity matrix $\\boldsymbol{\\Lambda}(t)$.

With $\\boldsymbol{\\Lambda}(t)$, we can no longer just use the matrix exponential $e^{\\boldsymbol{\\Lambda} t}$. The Kolmogorov DEs do not have a simple analytical solution. 
$$ \\frac{\\partial}{\\partial t} \\boldsymbol{P}(s, t) = \\boldsymbol{P}(s, t) \\boldsymbol{\\Lambda}(t) $$

So how do we find $P(s, t)$? We solve the ODE system **numerically**. 
**Enter Runge-Kutta:** Runge-Kutta (like the classic RK4 method) is the gold standard for solving ordinary differential equations step-by-step. By discretizing time and evaluating $\\boldsymbol{\\Lambda}(t)$ at specific intervals, Runge-Kutta allows us to construct the full transition probability matrix over decades with incredible precision!
"""))

# Practical Example
nb.cells.append(nbf.v4.new_markdown_cell("""## 3. Practical Implementation: Solving Kolmogorov with RK45
Let's build a simple 2-state model (Active and Dead) where the mortality rate increases over time (e.g., Gompertz Makeham mortality). We will use a standard ODE solver (which implements a Runge-Kutta method under the hood) to find the probability of surviving to a certain age.
"""))

nb.cells.append(nbf.v4.new_code_cell("""import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Define our states: 0 = Active, 1 = Dead
# Let's say the mortality rate follows a simple Gompertz law: lambda_01(t) = a * exp(b*t)
a = 0.0005  # Base mortality
b = 0.1     # Growth rate of mortality

def intensity_matrix(t):
    # Active to Dead
    mu_01 = a * np.exp(b * t)
    
    # State 1 (Dead) is an absorbing state, so 1 -> 0 is 0, and 1 -> 1 is 0
    mu_10 = 0.0
    
    # Construct the matrix. Remember the diagonal rule! 
    # lambda_ii = -sum_{j!=i} lambda_ij
    lambda_00 = -mu_01
    lambda_11 = 0.0 # Absorbing state
    
    return np.array([
        [lambda_00, mu_01],
        [mu_10, lambda_11]
    ])

# To solve the Kolmogorov Forward DE: d/dt P(t) = P(t) * Lambda(t)
# scipy.integrate.solve_ivp expects a 1D vector, so we must flatten our 2x2 matrix
def kolmogorov_forward(t, P_flat):
    P = P_flat.reshape(2, 2)
    Lambda = intensity_matrix(t)
    
    # Matrix multiplication for the Forward equation: dP = P * Lambda
    dP_dt = P @ Lambda
    return dP_dt.flatten() # Return flattened derivative

# We want to calculate probabilities tracking from age 30 to age 100 (so t goes from 0 to 70)
t_span = (0, 70)
t_eval = np.linspace(0, 70, 71) # Evaluate at every year

# Initial condition P(0) = Identity Matrix (at t=0, age 30, probabilities are 1 for current state)
P0 = np.eye(2).flatten()

# Solve using RK45 (a specific Runge-Kutta method default in scipy)
sol = solve_ivp(kolmogorov_forward, t_span, P0, method='RK45', t_eval=t_eval)

# Reshape the solution back to 2x2 matrices: sol.y has shape (4, num_time_steps)
P_t = sol.y.reshape(2, 2, -1)

# P_t[0, 0, :] is P_{Active->Active}
# P_t[0, 1, :] is P_{Active->Dead}

plt.figure(figsize=(10, 5))
plt.plot(t_eval + 30, P_t[0, 0, :], label="P(Active -> Active)", color='green', linewidth=2)
plt.plot(t_eval + 30, P_t[0, 1, :], label="P(Active -> Dead)", color='red', linewidth=2)
plt.title("Transition Probabilities from Age 30 (Using Kolmogorov Forward eq)")
plt.xlabel("Age (30 + t)")
plt.ylabel("Probability")
plt.legend()
plt.grid(alpha=0.3)
plt.show()
"""))

# Check your understanding
nb.cells.append(nbf.v4.new_markdown_cell("""## Check Your Understanding

1. **Theoretical check:** We defined the initial condition for measuring $P(s, t)$ as the Identity Matrix. Why must the state of the system at time $t=s$ (meaning time has not elapsed) always be perfectly represented by the Identity matrix $\\boldsymbol{I}$ rather than an intensity matrix $\\boldsymbol{\\Lambda}$?
2. **Coding challenge:** In `solve_ivp`, we used `method='RK45'`. Try writing a *manual* "Euler method" step (which is the simplest, most primitive type of Runge-Kutta, i.e., $y_{n+1} = y_n + h \\cdot f(t_n, y_n)$) to calculate $P(0, 1)$ manually in Python using a step size of $h=1$. *(Hint: take $P(0) = I$, calculate the derivative using the forward equation, and step forward simply by adding it!)*
"""))

with open('/workspace/Liv2/notebooks/Kolmogorov_DEs.ipynb', 'w') as f:
    nbf.write(nb, f)
print("Notebook created successfully!")
