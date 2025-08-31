FROM ubuntu:22.04

LABEL maintainer="quinta@example.com"
LABEL description="DWSIM Chemical Process Simulation Service"
LABEL dwsim.version="6.7.0"
LABEL dwsim.license="GPL-3.0"
LABEL service.license="MIT"

ENV DEBIAN_FRONTEND=noninteractive
ENV DISPLAY=:99
ENV WINEPREFIX=/root/.wine
ENV WINEARCH=win64

# Install dependencies
RUN apt-get update && apt-get install -y \
    wine \
    winetricks \
    xvfb \
    python3 \
    python3-pip \
    wget \
    supervisor \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt

# Copy application files first
COPY app/ /app/
COPY scripts/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Install DWSIM
COPY scripts/install_dwsim.sh /tmp/install_dwsim.sh
RUN chmod +x /tmp/install_dwsim.sh && /tmp/install_dwsim.sh

# Verify DWSIM installation
RUN ls -la /app/dwsim/ && echo "DWSIM installation verified"

# Run DWSIM test
RUN python3 /app/test_dwsim.py

WORKDIR /app

# Create necessary directories
RUN mkdir -p /app/temp /app/scripts /app/flow /app/reports /var/log/supervisor

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD python3 -c "import requests; requests.get('http://localhost:8001/health')"

EXPOSE 8001

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
