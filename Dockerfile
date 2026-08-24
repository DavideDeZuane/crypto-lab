FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Numero di job per la compilazione.
# Può essere sovrascritto durante la build:
# docker build --build-arg BUILD_JOBS=8 .
ARG BUILD_JOBS=8

# --------------------------------------------------
# System dependencies
# --------------------------------------------------

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    git \
    cmake \
    ninja-build \
    gcc \
    g++ \
    libssl-dev \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# --------------------------------------------------
# Python virtual environment
# --------------------------------------------------

RUN python3 -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --upgrade pip setuptools wheel

# --------------------------------------------------
# Python packages
# --------------------------------------------------

RUN pip install \
    jupyterlab \
    notebook \
    pycryptodome \
    matplotlib \
    sympy \
    ipywidgets \ 
    cryptography \ 
    pandas 

# --------------------------------------------------
# Build liboqs
# --------------------------------------------------

WORKDIR /opt

RUN git clone --depth 1 \
    https://github.com/open-quantum-safe/liboqs.git

RUN cmake \
    -S /opt/liboqs \
    -B /opt/liboqs/build \
    -GNinja \
    -DCMAKE_BUILD_TYPE=Release \
    -DBUILD_SHARED_LIBS=ON \
    -DOQS_USE_OPENSSL=ON

RUN ninja \
    -C /opt/liboqs/build \
    -j${BUILD_JOBS}

RUN ninja \
    -C /opt/liboqs/build \
    install

# --------------------------------------------------
# Dynamic library path
# --------------------------------------------------

RUN ldconfig

# --------------------------------------------------
# Python bindings
# --------------------------------------------------

RUN pip install liboqs-python

# --------------------------------------------------
# Verify OQS installation
# --------------------------------------------------

RUN python - <<'PY'
import oqs

print("liboqs-python loaded successfully")

kems = oqs.get_enabled_kem_mechanisms()
sigs = oqs.get_enabled_sig_mechanisms()

print(f"KEMs available: {len(kems)}")
print(f"Signatures available: {len(sigs)}")

assert "ML-KEM-768" in kems
assert "ML-DSA-65" in sigs

print("ML-KEM-768: OK")
print("ML-DSA-65: OK")
PY

# --------------------------------------------------
# Workspace
# --------------------------------------------------

WORKDIR /workspace

EXPOSE 8888

CMD ["jupyter", "lab", \
     "--ip=0.0.0.0", \
     "--port=8888", \
     "--no-browser", \
     "--allow-root", \
     "--notebook-dir=/workspace", \
     "--NotebookApp.token=''", \
     "--NotebookApp.password=''"]
