# TXOne Edge IPS – DoS Protection Thresholds

These are the default packet thresholds at which TXOne Edge IPS triggers alerts or mitigations for potential DoS or network reconnaissance activity.

| Attack Type             | Threshold (Packets) |
|-------------------------|---------------------|
| TCP SYN Flood           | 10,000              |
| UDP Flood               | 10,000              |
| ICMP Flood              | 10,000              |
| IGMP Flood              | 10,000              |
| UDP Port Scan           | 250                 |
| IP Sweep                | 120                 |
| TCP Port SYN Scan       | 1,800               |
| TCP Port FIN Scan       | 1,800               |
| TCP Port NULL Scan      | 1,800               |
| TCP Port Xmas Scan      | 1,800               |
| ARP Scan                | 120                 |
| Ping Sweep              | 120                 |
