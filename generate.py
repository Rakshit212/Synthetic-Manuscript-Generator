"""
Main entry point for generating synthetic manuscripts.
"""
import argparse
import sys
import random
from pathlib import Path
from src.text.script_registry import ScriptRegistry
from src.text.loader import TextLoader
from src.text.processor import TextProcessor
from src.pipeline import Pipeline
from src.dataset.splitter import get_split

def verify_setup(args, registry: ScriptRegistry, script_name: str):
    print(f"--- Verifying setup for script: {script_name} ---")
    try:
        config = registry.get_script_config(script_name)
        input_file = config.get("input_file")
        if not input_file:
            print(f"[ERROR] No input_file specified in config for {script_name}")
            return False
        text = TextLoader.load_text(input_file)
        cleaned = TextProcessor.clean_text(text)
        if not cleaned:
            print(f"[ERROR] Input file contains no valid text: {input_file}")
            return False
            
        fonts = registry.discover_fonts(script_name)
        if not fonts:
            print(f"[WARN] No fonts discovered for {script_name}.")
            
        print(f"--- Setup verified successfully for {script_name} ---\n")
        return True
    except Exception as e:
        print(f"[ERROR] Setup verification failed for {script_name}: {e}\n")
        return False

def generate_script_images(args, pipeline, registry, script_name, count):
    print(f"Generating {count} images for {script_name}...")
    try:
        config = registry.get_script_config(script_name)
        input_file = config.get("input_file")
        text = TextLoader.load_text(input_file)
        cleaned = TextProcessor.clean_text(text)
        
        # Use simple paragraph splitting to feed pages
        paragraphs = TextProcessor.split_into_paragraphs(cleaned)
        if not paragraphs:
            paragraphs = ["Sample text"]
            
        splits_config = registry.config.get("dataset_splits", {"train": 85, "validation": 10, "test": 5})
        output_dir = args.output or registry.config.get("output_path", "data/output")
        
        base_seed = args.seed if args.seed is not None else random.randint(0, 9999)
        
        for i in range(count):
            split = get_split(i, count, splits_config)
            seed = base_seed + i
            # Pick a paragraph
            p_text = paragraphs[i % len(paragraphs)]
            pipeline.generate_image(script_name, p_text, seed, output_dir, split, i + 1)
            
        print(f"[OK] Generated {count} images for {script_name}")
    except FileNotFoundError as e:
        print(f"[ERROR] Skipping generation for {script_name}: {e}")
    except Exception as e:
        print(f"[ERROR] Generation failed for {script_name}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Synthetic Manuscript Generator")
    parser.add_argument("--script", type=str, help="Script to generate (devanagari, modi, sharada, all)")
    parser.add_argument("--count", type=int, help="Number of images to generate")
    parser.add_argument("--output", type=str, help="Output directory")
    parser.add_argument("--seed", type=int, help="Random seed")
    parser.add_argument("--config", type=str, default="config/config.yaml", help="Path to config file")
    
    args = parser.parse_args()
    if not args.script:
        parser.print_help()
        return

    try:
        registry = ScriptRegistry(args.config)
        pipeline = Pipeline(args.config)
    except Exception as e:
        print(f"Failed to load configuration: {e}")
        sys.exit(1)

    scripts_to_run = []
    if args.script.lower() == "all":
        scripts_to_run = list(registry.scripts.keys())
    else:
        scripts_to_run = [args.script.lower()]

    all_ok = True
    for script_name in scripts_to_run:
        if verify_setup(args, registry, script_name):
            if args.count:
                generate_script_images(args, pipeline, registry, script_name, args.count)
        else:
            all_ok = False
            
    if not all_ok:
        sys.exit(1)

if __name__ == "__main__":
    main()
