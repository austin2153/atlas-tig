#!/usr/bin/env python3

import os
import sys
import json
import requests
from datetime import datetime

def fetch_unifi_devices():
    """Fetch UniFi devices and convert to Telegraf format"""
    
    # Get environment variables
    console_id = os.getenv('UNIFI_CONSOLE_ID')
    api_key = os.getenv('UNIFI_API_KEY')
    
    if not console_id or not api_key:
        print("Error: UNIFI_CONSOLE_ID and UNIFI_API_KEY environment variables required", file=sys.stderr)
        sys.exit(1)
    
    # UniFi API endpoint
    url = f"https://api.ui.com/v1/devices?hostIds[]={console_id}"
    
    headers = {
        "Accept": "application/json",
        "X-API-Key": api_key
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Pretty print the response for debugging
        print("=== DEBUG: API Response ===", file=sys.stderr)
        print(json.dumps(data, indent=2), file=sys.stderr)
        print("=== END DEBUG ===", file=sys.stderr)
        
        if not data.get('data') or len(data['data']) == 0:
            print("No data returned from UniFi API", file=sys.stderr)
            return
        
        devices = data['data'][0].get('devices', [])
        
        # Pretty print the devices list for debugging
        print("=== DEBUG: Devices List ===", file=sys.stderr)
        print(json.dumps(devices, indent=2), file=sys.stderr)
        print("=== END DEBUG ===", file=sys.stderr)
        
        # Convert each device to Telegraf format
        for device in devices:
            # Create timestamp in nanoseconds (Unix epoch)
            timestamp = int(datetime.utcnow().timestamp() * 1e9)
            
            # Create measurement name from device name
            measurement = device.get('name', 'unknown_device').replace(' ', '_').replace('-', '_').replace('.', '_')
            
            # Tags (indexed metadata)
            tags = {
                'id': device.get('id', ''),
                'mac': device.get('mac', ''),
                'model': device.get('model', '').replace(' ', '_'),
                'ip': device.get('ip', ''),
                'status': device.get('status', ''),
                'productLine': device.get('productLine', '')
            }
            
            # Fields (values that change)
            fields = {
                'version': device.get('version', ''),
                'isOnline': device.get('status', '') == 'online',
                'firmwareStatus': device.get('firmwareStatus', ''),
                'updateAvailable': device.get('updateAvailable', ''),
                'isManaged': device.get('isManaged', False),
                'isConsole': device.get('isConsole', False)
            }
            
            # Output in Telegraf line protocol format
            line = f"{measurement}"
            for tag_key, tag_value in tags.items():
                if tag_value:
                    line += f",{tag_key}={tag_value}"
            
            line += " "
            for field_key, field_value in fields.items():
                if field_value is not None and field_value != "" and field_value is not False:
                    # Format booleans without quotes (lowercase true/false)
                    if isinstance(field_value, bool):
                        line += f"{field_key}={str(field_value).lower()},"
                    else:
                        # Format strings with quotes
                        line += f'{field_key}="{field_value}",'
            line = line.rstrip(",")  # remove trailing comma
            
            line += f" {timestamp}"
            print(line)
            
    except requests.exceptions.RequestException as e:
        print(f"Error fetching UniFi data: {e}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON response: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    fetch_unifi_devices()
