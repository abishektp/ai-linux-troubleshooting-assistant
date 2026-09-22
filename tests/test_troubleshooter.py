import sys
from pathlib import Path


# Add src directory to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_PATH))


from troubleshooter import identify_issue


def test_ssh_issue():
    text = (
        "SSH connection to my Linux server is timing out "
        "and I cannot connect on port 22."
    )

    issue_id, issue_data, score, matches = identify_issue(text)

    assert issue_id == "ssh_issue"
    assert issue_data["name"] == "SSH Connectivity Issue"
    assert score > 0
    assert len(matches) > 0


def test_disk_full_issue():
    text = (
        "The application failed with no space left on device "
        "because the disk is full."
    )

    issue_id, issue_data, score, matches = identify_issue(text)

    assert issue_id == "disk_full"
    assert issue_data["name"] == "Disk Space Issue"
    assert score > 0


def test_high_cpu_issue():
    text = (
        "The Linux server has high CPU usage and "
        "CPU utilization reached 100%."
    )

    issue_id, issue_data, score, matches = identify_issue(text)

    assert issue_id == "high_cpu"
    assert issue_data["name"] == "High CPU Usage"
    assert score > 0


def test_memory_issue():
    text = (
        "The application cannot allocate memory "
        "and the server has high memory usage."
    )

    issue_id, issue_data, score, matches = identify_issue(text)

    assert issue_id == "memory_issue"
    assert issue_data["name"] == "Memory Usage Issue"
    assert score > 0


def test_permission_issue():
    text = (
        "The application receives permission denied "
        "while accessing /opt/app/config."
    )

    issue_id, issue_data, score, matches = identify_issue(text)

    assert issue_id == "permission_issue"
    assert issue_data["name"] == "Permission or Access Issue"
    assert score > 0


def test_dns_issue():
    text = (
        "The server reports temporary failure in name resolution "
        "when connecting to the hostname."
    )

    issue_id, issue_data, score, matches = identify_issue(text)

    assert issue_id == "dns_issue"
    assert issue_data["name"] == "DNS Resolution Issue"
    assert score > 0


def test_unknown_issue():
    text = (
        "Something unusual happened on the server "
        "and I do not know what caused it."
    )

    issue_id, issue_data, score, matches = identify_issue(text)

    assert issue_id is None
    assert issue_data is None
    assert score == 0
    assert matches == []