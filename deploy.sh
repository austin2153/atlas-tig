#!/bin/bash
# Deploy script for InfluxDB 3 Core stack
# Handles first-time deployment by creating a new token if needed

set -e  # Exit on error

echo "Deploying InfluxDB 3 Core stack..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "Creating .env file..."
    touch .env
fi

# Source .env to get INFLUXDB_TOKEN if it exists
source .env 2>/dev/null || true

# Check if this is a first-time deployment (no token)
if [ -z "$INFLUXDB_TOKEN" ]; then
    echo ""
    echo "First-time deployment detected (no INFLUXDB_TOKEN in .env)"
    echo "Starting InfluxDB to generate admin token..."
    echo ""
    
    # Create temporary dummy token file (required for container to start)
    echo '{"name": "temp", "token": "temp-token-will-be-replaced"}' > influxdb-admin-token.txt
    
    # Start only InfluxDB
    docker compose up -d influxdb
    
    # Wait for InfluxDB to be ready
    echo "Waiting for InfluxDB to start..."
    sleep 8
    
    # Create admin token
    echo "Creating admin token..."
    TOKEN_OUTPUT=$(docker exec influxdb influxdb3 create token --admin 2>&1)
    
    # Extract the token from output
    NEW_TOKEN=$(echo "$TOKEN_OUTPUT" | grep "^Token:" | awk '{print $2}')
    
    if [ -z "$NEW_TOKEN" ]; then
        echo "Error: Failed to create token"
        echo "$TOKEN_OUTPUT"
        exit 1
    fi
    
    echo "Token created: $NEW_TOKEN"
    
    # Add token to .env
    if grep -q "^INFLUXDB_TOKEN=" .env 2>/dev/null; then
        # Update existing line
        sed -i "s|^INFLUXDB_TOKEN=.*|INFLUXDB_TOKEN=$NEW_TOKEN|" .env
    else
        # Add new line
        echo "INFLUXDB_TOKEN=$NEW_TOKEN" >> .env
    fi
    
    echo "Token saved to .env"
    
    # Set INFLUXDB_TOKEN for current session
    INFLUXDB_TOKEN="$NEW_TOKEN"
    
    # Restart InfluxDB with real token
    echo "Restarting InfluxDB with new token..."
    docker compose restart influxdb
    sleep 3
fi

# Generate token file from .env
echo "Generating admin token file..."
echo "{\"name\": \"admin\", \"token\": \"$INFLUXDB_TOKEN\"}" > influxdb-admin-token.txt
chmod 644 influxdb-admin-token.txt

echo "Token file created"

# Generate InfluxDB Explorer config from template
echo "Generating InfluxDB Explorer config..."
sed "s|\${INFLUXDB_TOKEN}|$INFLUXDB_TOKEN|g" influxdb-explorer/config/config.json.template > influxdb-explorer/config/config.json
chmod 644 influxdb-explorer/config/config.json

echo "Explorer config created"

# Deploy all services
echo "Starting all services..."
docker compose up -d

echo ""
echo "Deployment complete!"
echo ""
echo "Services:"
echo "  - InfluxDB:  http://rocky-linux.atlas.local:8181"
echo "  - Explorer:  http://rocky-linux.atlas.local:8888"
echo "  - Grafana:   http://rocky-linux.atlas.local:3000"
echo ""
