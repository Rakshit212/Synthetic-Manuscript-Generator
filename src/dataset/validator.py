from pathlib import Path

def validate_dataset(output_dir, config):
    report = {"passed": True, "errors": []}
    out_path = Path(output_dir)
    if not out_path.exists():
        report["passed"] = False
        report["errors"].append("Output directory does not exist.")
        return report
        
    for script in config.get("scripts", {}).keys():
        script_dir = out_path / script
        if not script_dir.exists():
            continue
            
        for split in ["train", "validation", "test"]:
            split_dir = script_dir / split
            if not split_dir.exists():
                continue
            images = list((split_dir / "images").glob("*.png"))
            mds = list((split_dir / "annotations").glob("*.md"))
            if len(images) != len(mds):
                report["passed"] = False
                report["errors"].append(f"Mismatch in {script}/{split}: {len(images)} images vs {len(mds)} mds")
                
    return report
