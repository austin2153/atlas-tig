# atlas-tig

Telegraf, InfluxDB 3, and Grafana stack for homelab metrics collection and visualization. Runs as Docker Compose services and is part of the `atlas-` homelab project family.

## Stack

| Service | Version | Role |
|---|---|---|
| InfluxDB 3 Core | 3.9.0 | Time-series metrics storage |
| InfluxDB Explorer | 1.6.3 | Web UI for querying InfluxDB |
| Telegraf | 1.38.2 | Metrics collection agent |
| Grafana | 11.0.0 | Dashboards and visualization |

## Quick start

```bash
./deploy.sh
```

On first run the script will:
1. Generate a secure Grafana admin password
2. Start InfluxDB and create an admin token automatically
3. Save both to `.env`
4. Start all services

No manual configuration needed.

## Access

After deployment:

- **Grafana**: http://localhost:3000 — username `admin`, password in `.env`
- **InfluxDB Explorer**: http://localhost:8888
- **InfluxDB**: http://localhost:8181

## Configuration

Credentials are stored in `.env` (gitignored). On first run this file is created automatically. To customize before deploying:

```bash
cp .env.example .env
# Edit .env to set GRAFANA_ADMIN_PASSWORD before running deploy.sh
```

Optional UniFi monitoring credentials can also be set in `.env`:

```
UNIFI_CONSOLE_ID=your-console-id
UNIFI_API_KEY=your-api-key
```

## Metrics collected

Telegraf collects the following by default:

- CPU, memory, disk usage and I/O
- Network interface and protocol stats
- System load and uptime
- Process count
- Example solar system dataset (demonstrates custom `exec` input)

## Fresh install / wipe

To tear down and redeploy from scratch:

```bash
docker compose down -v
rm -f .env influxdb-admin-token.txt influxdb-explorer/config/config.json
./deploy.sh
```

## Project structure

```
compose.yml                          # Docker Compose service definitions
deploy.sh                            # First-time and subsequent deployment script
telegraf.Dockerfile                  # Custom Telegraf image with Python support
telegraf/telegraf.conf               # Telegraf input/output plugin config
telegraf/scripts/                    # Custom exec input scripts
grafana/provisioning/datasources/    # Auto-provisioned InfluxDB datasources
grafana/provisioning/dashboards/     # Dashboard provisioning config
grafana/dashboards/                  # Dashboard JSON definitions
influxdb-explorer/config/            # InfluxDB Explorer config template
.env.example                         # Environment variable template
```

## Related

- [atlas-talos](https://github.com/austin2153/atlas-talos) — Kubernetes cluster this stack will eventually run on
