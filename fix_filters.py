import json
import uuid

def process_dict(d):
    if not isinstance(d, dict):
        return
    for k, v in d.items():
        if k == 'filters' and isinstance(v, dict):
            items = v.get('items', [])
            has_env = False
            for item in items:
                if isinstance(item, dict) and isinstance(item.get('key'), dict) and item['key'].get('key') == 'deployment.environment':
                    has_env = True
                    break
            if not has_env:
                new_item = {
                    "id": str(uuid.uuid4())[:8],
                    "key": {
                        "dataType": "string",
                        "isColumn": False,
                        "type": "resource",
                        "key": "deployment.environment"
                    },
                    "op": "in",
                    "value": ["{{deployment.environment}}"]
                }
                v['items'] = items + [new_item]
                v['op'] = "AND"
        elif isinstance(v, dict):
            process_dict(v)
        elif isinstance(v, list):
            process_list(v)

def process_list(lst):
    for item in lst:
        if isinstance(item, dict):
            process_dict(item)
        elif isinstance(item, list):
            process_list(item)

def process_file():
    with open('pkg/query-service/app/integrations/builtin_integrations/elasticsearch/assets/dashboards/overview.json', 'r') as f:
        data = json.load(f)

    process_dict(data)

    with open('pkg/query-service/app/integrations/builtin_integrations/elasticsearch/assets/dashboards/overview.json', 'w') as f:
        json.dump(data, f, indent=2)

if __name__ == '__main__':
    process_file()
