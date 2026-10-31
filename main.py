"""
AetherCog — The Cloud-to-Matter Operating System

Initial application entry point.
"""

import argparse
import json
import platform


PROJECT = {
    "name": "Aethereum Cognitive",
    "short_name": "AetherCog",
    "version": "0.1.0",
    "mission": "The Cloud-to-Matter Operating System",
    "architecture": [
        "Cognitive Layer",
        "Simulation Layer",
        "Execution Layer",
    ],
    "development_phase": "Foundation and prototype development",
}


def get_status():
    """Return the current application and environment status."""
    return {
        "project": PROJECT["short_name"],
        "version": PROJECT["version"],
        "status": "operational",
        "development_phase": PROJECT["development_phase"],
        "python_version": platform.python_version(),
        "architecture": PROJECT["architecture"],
    }


def main():
    parser = argparse.ArgumentParser(
        description="AetherCog application entry point"
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Display project and environment status",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"AetherCog {PROJECT['version']}",
    )

    args = parser.parse_args()

    if args.status:
        print(json.dumps(get_status(), indent=4))
    else:
        print(f"{PROJECT['name']} — {PROJECT['mission']}")
        print("Use --status to inspect the application.")


if __name__ == "__main__":
    main()
