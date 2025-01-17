# PowerPlanner

PowerPlanner is a Python program designed to manage power settings and create custom power plans based on usage on Windows systems. It provides an interface to list, create, set, export, import, and save power plans.

## Features

- List all available power plans.
- Retrieve the current active power plan.
- Create a custom power plan based on an existing one.
- Set a specific power plan as active.
- Export power plans to a file.
- Import power plans from a file.
- Save and load configuration settings.

## Requirements

- Windows OS
- Python 3.x
- Administrative privileges (required for executing power management commands)

## Installation

Clone this repository to your local machine:

```bash
git clone https://github.com/yourusername/powerplanner.git
cd powerplanner
```

## Usage

Run the `power_planner.py` script:

```bash
python power_planner.py
```

### Example

```python
planner = PowerPlanner()

# List available power plans
plans = planner.list_power_plans()
for guid, name in plans.items():
    print(f"{name}: {guid}")

# Create a new power plan
new_plan_guid = planner.create_power_plan("My Custom Plan")

# Set the new power plan as active
planner.set_power_plan(new_plan_guid)

# Save the current configuration
planner.save_configuration("power_config.json")

# Load the saved configuration
planner.load_configuration("power_config.json")
```

## Note

- Ensure you run the script with administrator privileges to allow modifications to power settings.
- This script utilizes the `powercfg` command available on Windows systems.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.