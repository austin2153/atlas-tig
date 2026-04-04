FROM telegraf:1.38.2

# Install Python and requests (Telegraf uses Debian/Ubuntu base)
RUN apt-get update && apt-get install -y python3 python3-pip

# Install Python dependencies using --break-system-packages flag
RUN pip3 install --break-system-packages requests

# Create scripts directory
RUN mkdir -p /app/scripts

# Copy all custom scripts (extensible!)
COPY ./telegraf/scripts/ /app/scripts/

# Make all scripts executable
RUN chmod +x /app/scripts/*

# Add scripts to PATH
ENV PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/app/scripts"
