# Log collection

To collect logs from Elasticsearch, you'll configure the OpenTelemetry Collector's `filelog` receiver.

## Update OTel Collector configuration

1.  Identify the location of your Elasticsearch log files (e.g., `/var/log/elasticsearch/*.log`).
2.  Edit your OpenTelemetry Collector configuration file (typically `otel-collector-config.yaml`).
3.  Add the `filelog` receiver configuration under the `receivers` section:

```yaml
receivers:
  filelog/elasticsearch:
    include:
      - /var/log/elasticsearch/*.log
    start_at: end
    operators:
      - type: regex_parser
        regex: '^\[(?P<timestamp>[^\]]+)\]\[(?P<severity>[^\]]+)\]\[(?P<logger>[^\]]+)\]\s+\[(?P<node>[^\]]+)\]\s+(?P<message>.*)$'
        timestamp:
          parse_from: attributes.timestamp
          layout: '2006-01-02T15:04:05,000'
        severity:
          parse_from: attributes.severity
      - type: add
        field: attributes.source
        value: "elasticsearch"
```

4.  Update the `service` pipeline to include the `filelog/elasticsearch` receiver:

```yaml
service:
  pipelines:
    logs:
      receivers: [filelog/elasticsearch, otlp]
      processors: [batch]
      exporters: [otlp]
```

5.  Restart the OpenTelemetry Collector for the changes to take effect.
