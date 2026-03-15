# ============================================================
# Docker Sandbox for Liv2 Compulsory Exercise
# Safe environment for AI agent terminal auto-access
# ============================================================

# Use rocker/verse which pre-packages R, tidyverse, rmarkdown, and a full TeX Live installation (inclusive of latexmk)!
FROM rocker/verse:latest

# --- System dependencies and Python setup ---
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    python3 \
    python3-venv \
    libgsl-dev \
    && rm -rf /var/lib/apt/lists/*

# Install missing LaTeX packages via tlmgr (since rocker/verse has a standalone TeX Live)
RUN tlmgr update --self && tlmgr install collection-latexextra collection-fontsrecommended collection-mathscience collection-xetex

# --- Install extra R packages ---
# install2.r is a built-in rocker script that downloads pre-compiled binaries where possible
RUN install2.r --error --skipinstalled \
    fitdistrplus \
    gridExtra \
    MASS \
    IRkernel \
    evir \
    copula

# --- Create a non-root user for extra safety ---
RUN useradd -m -s /bin/bash sandbox
# Give sandbox user permissions to R library if they ever install anything on the fly
RUN mkdir -p /usr/local/lib/R/site-library && chmod -R 777 /usr/local/lib/R/site-library

WORKDIR /workspace

# --- Install Python packages into a virtual environment ---
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install --no-cache-dir \
    jupyter \
    jupyterlab \
    numpy \
    scipy \
    matplotlib \
    pandas \
    seaborn \
    scikit-learn \
    sympy \
    statsmodels \
    ipykernel \
    nbformat \
    nbconvert \
    PyMuPDF

# --- Extra R packages (appended for cache efficiency) ---
RUN install2.r --error --skipinstalled evd
RUN install2.r --error --skipinstalled mvtnorm QRM

# --- Switch to the non-root sandbox user ---
USER sandbox

# --- Expose JupyterLab port (optional, for interactive use) ---
EXPOSE 8888

# --- Default: open a bash shell (agent uses this) ---
CMD ["/bin/bash"]
