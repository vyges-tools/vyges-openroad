# Build-env base image: ubuntu:24.04 + OpenROAD's compiled dependencies
# (or-tools, Boost, etc. — the heavy part). Rebuilt RARELY: only when the pinned
# commit's etc/DependencyInstaller.sh changes. Published as
# ghcr.io/vyges-tools/vyges-openroad-deps:<tag>. The per-commit compile
# (scripts/build-bundle.sh) runs FROM this image, so releases stay cheap.
FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
SHELL ["/bin/bash", "-c"]

# The commit whose DependencyInstaller.sh + submodules pin the dependency set.
ARG OR_COMMIT

RUN apt-get update && apt-get install -y --no-install-recommends \
      sudo git build-essential ca-certificates wget curl \
      python3 python3-pip tcl-dev \
    && rm -rf /var/lib/apt/lists/*

# Clone OpenROAD at the pinned commit so DependencyInstaller matches the source
# we will build. The tree is left in /OpenROAD for the compile stage to reuse.
RUN git clone https://github.com/The-OpenROAD-Project/OpenROAD.git /OpenROAD \
 && cd /OpenROAD \
 && git checkout "${OR_COMMIT}" \
 && git submodule update --init --recursive

# Install (and compile-from-source) all build + runtime deps; record their
# prefixes so Build.sh can find the non-standard ones (or-tools, etc.).
RUN cd /OpenROAD && ./etc/DependencyInstaller.sh -all -save-deps-prefixes=/opt/deps-prefixes.txt
