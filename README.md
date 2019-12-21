# Prometheus Todoist Exporter
Exporter for exposing recurring tasks from todoist to prometheus

Usage
```bash
echo 'YOUR_API_KEY' > .credentials
echo '{}' > .state
docker run -p 8000:8000 -v /path/to/state/.state:/.state -v /path/to/credentials/.credentials:/.credentials  kaisha/prometheus-todoist-exporter
```
Example docker-compose with prometheus and grafana

docker-compose.yml
```yml
version: '3'
services:
        prometheus:
                image: "prom/prometheus"
                ports:
                        - "9090:9090"
                volumes:
                - "/path/to/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml"
        prometheus-todoist-exporter:
                image: "kaisha/prometheus-todoist-exporter"
                volumes:
                - "/path/to/state/.state:/.state"
                - "/path/to/state/.credentials:/.credentials"
        grafana:
                image: "grafana/grafana"
                ports:
                        - "3000:3000"
```
prometheus.yml
```
global:
  scrape_interval:     15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: prometheus
    static_configs:
            - targets: ['localhost:9090', 'prometheus-todoist-exporter:8000']
```
