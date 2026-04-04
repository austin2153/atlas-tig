FROM telegraf:1.38.2

# Install Python and pip (Telegraf uses Debian/Ubuntu base)
RUN apt-get update && apt-get install -y python3 python3-pip

# Create scripts directory and copy scripts
RUN mkdir -p /app/scripts
COPY ./telegraf/scripts/ /app/scripts/

# Install Python dependencies from requirements.txt
RUN pip3 install --break-system-packages -r /app/scripts/requirements.txt

# Make all scripts executable
RUN chmod +x /app/scripts/*

# Add scripts to PATH
ENV PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/app/scripts"
