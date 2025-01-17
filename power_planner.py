import os
import subprocess
import json

class PowerPlanner:
    def __init__(self):
        self.current_plan = self.get_current_power_plan()

    def get_current_power_plan(self):
        """Retrieve the current power plan."""
        try:
            output = subprocess.check_output(["powercfg", "/GETACTIVESCHEME"], text=True)
            plan_guid = output.split()[3].strip("()")
            return plan_guid
        except subprocess.CalledProcessError as e:
            print(f"Error retrieving current power plan: {e}")
            return None

    def list_power_plans(self):
        """List all available power plans."""
        try:
            output = subprocess.check_output(["powercfg", "/LIST"], text=True)
            plans = {}
            for line in output.splitlines():
                if "GUID" in line:
                    plan_details = line.split()
                    plan_guid = plan_details[3]
                    plan_name = " ".join(plan_details[4:]).strip("()")
                    plans[plan_guid] = plan_name
            return plans
        except subprocess.CalledProcessError as e:
            print(f"Error listing power plans: {e}")
            return {}

    def create_power_plan(self, name, base_plan_guid=None):
        """Create a custom power plan based on an existing one."""
        if base_plan_guid is None:
            base_plan_guid = self.current_plan
        try:
            output = subprocess.check_output(
                ["powercfg", "/DUPLICATESCHEME", base_plan_guid], text=True
            )
            new_plan_guid = output.split()[-1].strip()
            subprocess.check_call(["powercfg", "/CHANGENAME", new_plan_guid, name])
            return new_plan_guid
        except subprocess.CalledProcessError as e:
            print(f"Error creating power plan: {e}")
            return None

    def set_power_plan(self, plan_guid):
        """Set the active power plan."""
        try:
            subprocess.check_call(["powercfg", "/SETACTIVE", plan_guid])
            self.current_plan = plan_guid
        except subprocess.CalledProcessError as e:
            print(f"Error setting power plan: {e}")

    def export_power_plan(self, plan_guid, file_path):
        """Export a power plan to a file."""
        try:
            subprocess.check_call(["powercfg", "/EXPORT", file_path, plan_guid])
            print(f"Power plan {plan_guid} exported to {file_path}")
        except subprocess.CalledProcessError as e:
            print(f"Error exporting power plan: {e}")

    def import_power_plan(self, file_path):
        """Import a power plan from a file."""
        try:
            output = subprocess.check_output(["powercfg", "/IMPORT", file_path], text=True)
            imported_plan_guid = output.split()[-1].strip()
            print(f"Power plan imported with GUID: {imported_plan_guid}")
            return imported_plan_guid
        except subprocess.CalledProcessError as e:
            print(f"Error importing power plan: {e}")
            return None

    def save_configuration(self, file_path):
        """Save the current configuration to a file."""
        config = {
            "current_plan": self.current_plan,
            "plans": self.list_power_plans()
        }
        with open(file_path, 'w') as f:
            json.dump(config, f, indent=4)
        print(f"Configuration saved to {file_path}")

    def load_configuration(self, file_path):
        """Load a configuration from a file."""
        try:
            with open(file_path, 'r') as f:
                config = json.load(f)
                self.current_plan = config.get("current_plan")
                print(f"Configuration loaded from {file_path}")
        except FileNotFoundError:
            print(f"Configuration file not found: {file_path}")
        except json.JSONDecodeError:
            print("Error decoding configuration file")

if __name__ == "__main__":
    planner = PowerPlanner()
    print("Available power plans:")
    plans = planner.list_power_plans()
    for guid, name in plans.items():
        print(f"{name}: {guid}")
    # Example usage
    # new_plan = planner.create_power_plan("My Custom Plan")
    # planner.set_power_plan(new_plan)
    # planner.save_configuration("power_config.json")