To specify the version to which you want the firewalls to upgrade, you can add a column in your CSV file for the version and modify the script accordingly. Here’s how you can adjust the script:

```python
import csv
from panos.firewall import Firewall
from panos_upgrade_assurance import UpgradeAssurance

# CSV file containing firewall details
csv_file = "firewall_ips.csv"

def get_ha_status(firewall_ip, username, password):
    fw = Firewall(firewall_ip, username, password)
    try:
        ha_status = fw.op("show high-availability state", xml=True)
        state = ha_status.find(".//state").text
        return state
    except Exception as e:
        print(f"An error occurred while checking HA status for {firewall_ip}: {e}")
        return None

def upgrade_passive_firewalls_from_csv(csv_file):
    with open(csv_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            primary_ip = row['primary_ip']
            secondary_ip = row['secondary_ip']
            username = row['username']
            password = row['password']
            target_version = row['target_version']
            firewalls = [
                {"ip": primary_ip, "role": "primary"},
                {"ip": secondary_ip, "role": "secondary"}
            ]

            for fw in firewalls:
                print(f"Checking {fw['role']} firewall HA status...")
                state = get_ha_status(fw["ip"], username, password)
                if state:
                    print(f"{fw['role'].capitalize()} Firewall is in {state} mode.")
                    if state.lower() != "passive":
                        print(f"Skipping upgrade for active {fw['role']} Firewall.")
                        continue

                ua = UpgradeAssurance(fw["ip"], username, password)

                try:
                    # Perform pre-upgrade health checks
                    health_status = ua.pre_upgrade_check()
                    print(f"{fw['role'].capitalize()} Firewall pre-upgrade health check results:", health_status)

                    # Proceed with upgrade if health check passes
                    if health_status['overall_health'] == 'healthy':
                        print(f"{fw['role'].capitalize()} Firewall is healthy. Proceeding with upgrade to version {target_version}...")
                        ua.upgrade_firewall(version=target_version)
                    else:
                        print(f"{fw['role'].capitalize()} Firewall is not healthy. Aborting upgrade.")
                        #
