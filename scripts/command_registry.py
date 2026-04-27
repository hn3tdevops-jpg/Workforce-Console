#!/usr/bin/env python3
"""
Registry of allowed control-panel commands. Each entry defines id, label, description, cwd, cmd (list), timeout, risk, enabled, log_path
"""
import json
REGISTRY = [
    {
        'id':'refresh_devhub',
        'label':'Refresh Dev Hub',
        'description':'Run scripts/refresh_devhub.py to rebuild indexes',
        'cwd':'/home/hn3t/dev_hub',
        'cmd':['python3','scripts/refresh_devhub.py'],
        'timeout':600,
        'risk':'low',
        'enabled':True,
        'log_path':'data/runs'
    },
    {
        'id':'check_devhub_links',
        'label':'Validate static links',
        'description':'Run scripts/validate_devhub_static.py',
        'cwd':'/home/hn3t/dev_hub',
        'cmd':['python3','scripts/validate_devhub_static.py'],
        'timeout':300,
        'risk':'low',
        'enabled':True,
        'log_path':'data/runs'
    }
]

if __name__=='__main__':
    print(json.dumps(REGISTRY, indent=2))
