
## Writing Solar System Example Data to InfluxDB with Python

## Quick Start

### 1. Dependencies are installed automatically when you build the Telegraf container:
    ```bash
    docker compose build telegraf
    ```

### 2. Ensure `.env` file exists in project root (created by `deploy.sh`)
    - The script automatically loads environment variables from `.env`
    - Required: `INFLUXDB_TOKEN`
    - Optional: `INFLUXDB_DATABASE` (defaults to `solar_system`)
    - Optional: `INFLUXDB_HOST` (defaults to `http://influxdb:8181`)

### 3. Run the script inside the Telegraf container:
    ```bash
    # Run all quick examples
    docker exec telegraf python3 /app/scripts/influxdb_example_solar.py
   
    # Or run interactively
    docker exec -it telegraf bash
    > python3 /app/scripts/influxdb_example_solar.py
    ```

### Configuration

The script uses environment variables (same as Telegraf):

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `INFLUXDB_TOKEN` | Yes | - | Your InfluxDB admin token |
| `INFLUXDB_DATABASE` | No | `solar_system` | Database name to write to |
| `INFLUXDB_HOST` | No | `http://influxdb:8181` | InfluxDB server URL |

### Key Concepts

### Point Structure
```python
Point("measurement_name")
    .tag("tag_key", "tag_value")      # Indexed metadata
    .field("field_key", field_value)  # Actual data
    .time(datetime.utcnow())          # Timestamp (optional, defaults to now)
```

### Tags vs Fields
- **Tags**: Indexed metadata (name, type, category). Use for filtering/grouping
- **Fields**: Actual values (temperature, distance, count). The data you're measuring

### Example: Planet Data
```python
Point("planet_stats")
    .tag("name", "Mars")              # Planet identifier
    .tag("type", "Terrestrial")       # Category for filtering
    .field("distance_from_sun_au", 1.52)  # Numeric measurements
    .field("moons", 2)
    .time(datetime.utcnow())
```

**Note:** This script writes example data for all major planets, Pluto, and can be customized for other solar system objects.

### Writing Methods

**Method 1: Point class (recommended)**
```python
point = (
    Point("planet_stats")
    .tag("name", "Earth")
    .tag("type", "Terrestrial")
    .field("moons", 1)
    .field("diameter_km", 12742)
    .time(datetime.utcnow())
)
client.write(point)
```

**Method 2: Line protocol**
```python
client.write("planet_stats,name=Mars,type=Terrestrial moons=2,diameter_km=6779")
```

### Common Patterns

### Writing data in a loop
```python
while True:
    data_value = get_data_from_source()
    point = Point("measurement").field("value", data_value)
    client.write(point)
    time.sleep(60)  # Every minute
```

### Batch writing for efficiency
```python
points = []
for item in data_batch:
    points.append(
        Point("metric")
        .tag("category", item.category)
        .field("value", item.value)
    )
client.write(points)  # Write all at once
```

### Troubleshooting

- **Connection refused**: Make sure InfluxDB is running (`docker ps`)
- **401 Unauthorized**: Check your token in the script
- **Database not found**: The script will auto-create the database on first write if you have permission. If not, create it in Explorer or via CLI.
