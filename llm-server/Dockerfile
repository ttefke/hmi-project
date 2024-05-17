# HMI Project 2024, Tobias Tefke

# Build from python 3.10 container (Debian bookworm)
FROM python:3.10

# Create standard user
RUN addgroup llm
RUN adduser llm --ingroup llm

# Upgrade pip to latest version
RUN pip install --upgrade pip

# Copy server files
COPY --chown=llm:llm hss_server /server

# Set current working directory to server files directory
# -> this allows us to run all following commands relative from this directory
WORKDIR /server

# Install all requirements
RUN pip install -r requirements.txt

# Switch to standard user
USER llm

# Start server using hypercorn
CMD ["hypercorn", "server:app"]

