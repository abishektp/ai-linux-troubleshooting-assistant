TROUBLESHOOTING_KB = {

    "disk_full": {
        "name": "Disk Space Issue",
        "keywords": [
            "no space left on device",
            "disk full",
            "filesystem full",
            "not enough space",
            "disk space"
        ],
        "possible_causes": [
            "Filesystem usage has reached its capacity",
            "Large log files are consuming disk space",
            "Temporary files have accumulated",
            "Application data has grown unexpectedly"
        ],
        "diagnostic_commands": [
            "df -h",
            "du -sh /* 2>/dev/null",
            "du -ah /var/log | sort -rh | head -20"
        ]
    },

    "high_cpu": {
        "name": "High CPU Usage",
        "keywords": [
            "high cpu",
            "cpu usage",
            "cpu utilization",
            "100% cpu",
            "cpu spike"
        ],
        "possible_causes": [
            "A process is consuming excessive CPU",
            "Application workload has increased",
            "A process may be stuck in a loop",
            "Too many processes are running"
        ],
        "diagnostic_commands": [
            "top",
            "ps aux --sort=-%cpu | head",
            "uptime"
        ]
    },

    "memory_issue": {
        "name": "Memory Usage Issue",
        "keywords": [
            "out of memory",
            "high memory",
            "memory usage",
            "oom",
            "cannot allocate memory",
            "memory exhausted"
        ],
        "possible_causes": [
            "Application memory consumption has increased",
            "A process may have a memory leak",
            "Insufficient available RAM",
            "Too many memory-intensive processes are running"
        ],
        "diagnostic_commands": [
            "free -h",
            "ps aux --sort=-%mem | head",
            "dmesg | grep -i oom"
        ]
    },

    "ssh_issue": {
        "name": "SSH Connectivity Issue",
        "keywords": [
            "connection refused",
            "connection timed out",
            "ssh failed",
            "port 22",
            "ssh connection",
            "ssh timeout"
        ],
        "possible_causes": [
            "SSH service may not be running",
            "Port 22 may be blocked",
            "The target server may be unreachable",
            "Firewall or network rules may be blocking the connection"
        ],
        "diagnostic_commands": [
            "systemctl status sshd",
            "ss -tulpn | grep :22",
            "ping <server>",
            "nc -zv <server> 22"
        ]
    },

    "service_failure": {
        "name": "Linux Service Failure",
        "keywords": [
            "service failed",
            "service not running",
            "service stopped",
            "failed to start",
            "systemctl failed",
            "service inactive"
        ],
        "possible_causes": [
            "The service process has crashed",
            "The service configuration may be invalid",
            "A required dependency may be unavailable",
            "The service may have failed during system startup"
        ],
        "diagnostic_commands": [
            "systemctl status <service>",
            "journalctl -u <service> --since '30 minutes ago'",
            "systemctl list-dependencies <service>"
        ]
    },

    "dns_issue": {
        "name": "DNS Resolution Issue",
        "keywords": [
            "could not resolve host",
            "name resolution",
            "dns failed",
            "unknown host",
            "temporary failure in name resolution",
            "hostname not resolving"
        ],
        "possible_causes": [
            "DNS servers may be unreachable",
            "The DNS configuration may be incorrect",
            "The hostname may not have a valid DNS record",
            "Network connectivity to the DNS server may be unavailable"
        ],
        "diagnostic_commands": [
            "cat /etc/resolv.conf",
            "getent hosts <hostname>",
            "nslookup <hostname>",
            "dig <hostname>"
        ]
    },

    "permission_issue": {
        "name": "Permission or Access Issue",
        "keywords": [
            "permission denied",
            "access denied",
            "operation not permitted",
            "insufficient permissions"
        ],
        "possible_causes": [
            "The current user does not have the required permissions",
            "File or directory ownership may be incorrect",
            "Filesystem permissions may be restrictive",
            "A security policy may be preventing access"
        ],
        "diagnostic_commands": [
            "id",
            "ls -ld <path>",
            "namei -l <path>"
        ]
    },

    "network_issue": {
        "name": "Network Connectivity Issue",
        "keywords": [
            "network unreachable",
            "host unreachable",
            "no route to host",
            "network connectivity",
            "cannot reach server",
            "connection timeout"
        ],
        "possible_causes": [
            "The destination host may be unavailable",
            "A routing problem may exist",
            "Firewall rules may be blocking traffic",
            "The local network interface may have a connectivity issue"
        ],
        "diagnostic_commands": [
            "ip addr",
            "ip route",
            "ping <destination>",
            "traceroute <destination>"
        ]
    },

    "readonly_filesystem": {
        "name": "Read-Only Filesystem Issue",
        "keywords": [
            "read-only file system",
            "readonly filesystem",
            "cannot write to filesystem",
            "filesystem is read only"
        ],
        "possible_causes": [
            "The filesystem may have been mounted as read-only",
            "Filesystem errors may have caused the OS to protect the disk",
            "Storage or disk errors may have occurred",
            "The mount configuration may specify read-only access"
        ],
        "diagnostic_commands": [
            "mount",
            "findmnt",
            "dmesg | tail -50",
            "lsblk -f"
        ]
    },

    "high_load": {
        "name": "High System Load",
        "keywords": [
            "high load",
            "load average",
            "server slow",
            "system slow",
            "slow server",
            "performance issue"
        ],
        "possible_causes": [
            "CPU-intensive processes may be running",
            "Processes may be waiting for disk I/O",
            "Memory pressure may be causing swapping",
            "The system may be handling unusually high workload"
        ],
        "diagnostic_commands": [
            "uptime",
            "top",
            "vmstat 1 5",
            "ps aux --sort=-%cpu | head"
        ]
    },

    "process_issue": {
        "name": "Application or Process Issue",
        "keywords": [
            "process crashed",
            "application crashed",
            "process not running",
            "application not running",
            "process terminated",
            "application stopped"
        ],
        "possible_causes": [
            "The application process may have crashed",
            "The process may have been terminated",
            "The application may have encountered a configuration error",
            "Required system resources may be unavailable"
        ],
        "diagnostic_commands": [
            "ps aux | grep <process>",
            "pgrep -a <process>",
            "journalctl --since '30 minutes ago'"
        ]
    }
}