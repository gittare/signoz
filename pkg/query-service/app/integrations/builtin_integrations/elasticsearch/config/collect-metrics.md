# Metric collection

To collect Elasticsearch metrics, configure the `elasticsearch` receiver in your OpenTelemetry Collector.

## Update OTel Collector configuration

1.  Edit your OpenTelemetry Collector configuration file (typically `otel-collector-config.yaml`).
2.  Add the `elasticsearch` receiver configuration under the `receivers` section:

```yaml
receivers:
  elasticsearch:
    endpoint: http://<elasticsearch-host>:9200
    collection_interval: 10s
    tls:
      insecure: true
      insecure_skip_verify: true
```

3.  Update the `service` pipeline to include the `elasticsearch` receiver:

```yaml
service:
  pipelines:
    metrics:
      receivers: [elasticsearch, otlp]
      processors: [batch]
      exporters: [otlp]
```

4.  Restart the OpenTelemetry Collector for the changes to take effect.
