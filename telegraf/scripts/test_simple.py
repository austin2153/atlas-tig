#!/usr/bin/env python3

import os
import sys
import time

def main():
    # Test with hardcoded data first
    measurement = "test_device"
    # InfluxDB line protocol expects nanosecond Unix timestamp
    timestamp = int(time.time() * 1e9)
    
    # Simple line protocol: measurement,tag=value field="value" timestamp
    line = f"{measurement},id=test123,ip=192.168.0.1 status=\"online\" {timestamp}"
    print(line)

if __name__ == "__main__":
    main()
