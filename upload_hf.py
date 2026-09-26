import os
import glob
import argparse
from datasets import Dataset, DatasetDict, Image
from huggingface_hub import HfApi

def create_dataset_for_script(script_name):
    splits = ["train", "validation", "test"]
    dataset_dict = {}
    
    for split in splits:
        img_dir = os.path.join("data", "output", script_name, split, "images")
        
        # Sort files to ensure consistent ordering
        img_files = sorted(glob.glob(os.path.join(img_dir, "*.png")))
        
        if not img_files:
            print(f"Warning: No images found for {script_name} - {split}")
            continue
            
        dataset_dict[split] = Dataset.from_dict({
            "image": img_files,
            "filename": [os.path.basename(f) for f in img_files],
            "script": [script_name] * len(img_files)
        }).cast_column("image", Image())
        
    if not dataset_dict:
        raise ValueError(f"No data found for script {script_name}")
        
    return DatasetDict(dataset_dict)

def upload_datasets(repo_id):
    print(f"Uploading to repository: {repo_id}")
    
    # Ensure repo exists
    api = HfApi()
    try:
        api.create_repo(repo_id, repo_type="dataset", exist_ok=True)
    except Exception as e:
        print(f"Could not create repo (might already exist or permission denied): {e}")

    scripts = ["devanagari", "modi", "sharada"]
    
    for script in scripts:
        print(f"Processing script: {script}...")
        try:
            ds = create_dataset_for_script(script)
            print(f"Uploading {script} subset (Train: {len(ds.get('train', []))}, Val: {len(ds.get('validation', []))}, Test: {len(ds.get('test', []))})")
            
            # Push to hub with config_name as the script name
            ds.push_to_hub(
                repo_id, 
                config_name=script, 
                commit_message=f"Upload {script} subset"
            )
            print(f"Successfully uploaded {script} subset!")
        except Exception as e:
            print(f"Error uploading {script}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload dataset to Hugging Face")
    parser.add_argument("--repo_id", type=str, required=True, help="Hugging Face repo ID (e.g., username/repo)")
    args = parser.parse_args()
    
    upload_datasets(args.repo_id)
