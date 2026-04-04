# Fresh Installation Guide

## Zero-Configuration Deployment

This stack is designed to deploy with **no manual configuration required**.

### Quick Start

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd atlas-tig
   ```

2. **Run the deployment script**
   ```bash
   ./deploy.sh
   ```

That's it! The deployment script will:
- Auto-generate InfluxDB admin token (saved to `.env`)
- Create all configuration files from templates
- Start all services

### What Gets Created Automatically

On first run, `deploy.sh` creates:
- `.env` file with `INFLUXDB_TOKEN`
- `influxdb-admin-token.txt` (gitignored)
- `influxdb-explorer/config/config.json` (gitignored)

### Access the Stack

After deployment completes:
- **InfluxDB**: http://rocky-linux.atlas.local:8181
- **InfluxDB Explorer**: http://rocky-linux.atlas.local:8888 (auto-connected)
- **Grafana**: http://rocky-linux.atlas.local:3000
  - Username: `admin`
  - Password: `admin` (or custom if set in `.env`)

### Optional Configuration

#### Custom Grafana Password

Create/edit `.env` before first run:
```bash
GRAFANA_ADMIN_PASSWORD=your-secure-password
```

#### UniFi Monitoring (Advanced)

If you want to re-enable custom UniFi device monitoring:
1. Add to `.env`:
   ```bash
   UNIFI_CONSOLE_ID=your-console-id
   UNIFI_API_KEY=your-api-key
   ```
2. Update `telegraf/telegraf.conf` to include UniFi exec scripts
3. Restart: `docker compose restart telegraf`

### Complete Wipe & Redeploy

To test a completely fresh installation:
```bash
# Stop and remove everything
docker compose down -v

# Remove generated files
rm -f .env influxdb-admin-token.txt influxdb-explorer/config/config.json

# Redeploy
./deploy.sh
```

### What's Committed to Git

**Template files** (safe):
- `.env.example` - Documentation only
- `influxdb-explorer/config/config.json.template` - Token placeholder
- `compose.yml`, `deploy.sh`, configs

**Generated files** (gitignored):
- `.env` - Contains secrets
- `influxdb-admin-token.txt` - Generated from .env
- `influxdb-explorer/config/config.json` - Generated from template
