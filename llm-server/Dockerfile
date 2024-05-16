# HMI Project 2024, Tobias Tefke

# Build from python 3.10 container (Debian bookworm)
FROM python:3.10

# Upgrade pip to latest version
RUN pip install --upgrade pip

# Copy server files
COPY hss_server /server

# Set current working directory to server files directory
# -> this allows us to run all following commands relative from this directory
WORKDIR /server

# Install all requirements
RUN pip install -r requirements.txt

# Start server using hypercorn
CMD ["hypercorn", "server:app"]

