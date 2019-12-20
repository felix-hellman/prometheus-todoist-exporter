# Prometheus Todoist Exporter
Exporter for exposing recurring tasks from todoist to prometheus

To use the exporter, first enter your key
```bash
echo "key = 'YOUR_API_KEY'" > cred.py
echo "{}" > .state
```

To run docker-compose example with prometheus + grafana
Change your volume paths for prometheus.yml and exporter state
```bash
Docker build -t prometheus-todoist-exporter .
cd docker-compose
docker compose up -d
``` 
