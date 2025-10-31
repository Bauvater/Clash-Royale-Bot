from utils import determine_roi, capture_window
import json

def configure_rois():
    print("Welcome to the Merge Tactics Bot ROI configurator.")
    print("Please select the following regions of interest:")

    window_title = "Bluestacks" # Make sure BlueStacks is running

    # Capture a screenshot to display to the user
    try:
        capture_window(window_title)
    except RuntimeError as e:
        print(f"Error: {e}")
        print("Please make sure BlueStacks is running and the window is visible.")
        return

    rois = {}
    rois["SHOP"] = determine_roi(window_title, "Select the SHOP region")
    rois["ELIXIR"] = determine_roi(window_title, "Select the ELIXIR region")
    rois["BENCH"] = determine_roi(window_title, "Select the BENCH region")
    rois["FIELD"] = determine_roi(window_title, "Select the FIELD region")
    rois["GAME_OVER"] = determine_roi(window_title, "Select the GAME_OVER region")

    # Save the ROIs to a config file
    with open("config_rois.json", "w") as f:
        json.dump(rois, f, indent=4)

    print("Configuration complete! The ROIs have been saved to config_rois.json.")
    print("Please copy the contents of this file to the REGIONS dictionary in src/config.py.")

if __name__ == "__main__":
    configure_rois()
