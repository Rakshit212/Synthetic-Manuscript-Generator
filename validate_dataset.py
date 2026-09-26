"""
Validation script for synthetic manuscript dataset.
"""
import argparse
from src.text.script_registry import ScriptRegistry
from src.dataset.validator import validate_dataset

def main():
    parser = argparse.ArgumentParser(description="Dataset Validator")
    parser.add_argument("--config", type=str, default="config/config.yaml", help="Path to config file")
    args = parser.parse_args()
    
    registry = ScriptRegistry(args.config)
    output_dir = registry.config.get("output_path", "data/output")
    
    print("Validating dataset...")
    report = validate_dataset(output_dir, registry.config)
    if report["passed"]:
        print("Validation PASSED.")
    else:
        print("Validation FAILED.")
        for err in report["errors"]:
            print(f" - {err}")

if __name__ == "__main__":
    main()
