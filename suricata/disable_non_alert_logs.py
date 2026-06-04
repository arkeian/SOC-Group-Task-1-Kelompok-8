with open('/etc/suricata/suricata.yaml', 'r') as f:
    lines = f.readlines()

import re

disable_types = {
    'http', 'dns', 'mdns', 'tls',
    'files', 'smtp', 'anomaly', 'dhcp'
}

result = []
i = 0

while i < len(lines):
    line = lines[i]
    m = re.match(r'^(\s+)- (\w[\w-]*)(:)?(\s|$)', line)

    if m and len(m.group(1)) == 8 and m.group(2) in disable_types:
        result.append(line)

        if line.rstrip().endswith(':'):
            result.append('            enabled: no\n')
    else:
        result.append(line)

    i += 1

with open('/etc/suricata/suricata.yaml', 'w') as f:
    f.writelines(result)