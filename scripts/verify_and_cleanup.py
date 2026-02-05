
import pandas as pd
from pathlib import Path
import hashlib
import shutil

PROJECT_ROOT = Path(__file__).parent

print("="*70)
print("DUPLICATE DIRECTORY VERIFICATION & CLEANUP")
print("="*70)

# Define paths
original_data = PROJECT_ROOT / 'data' / 'processed'
duplicate_data = PROJECT_ROOT / 'scripts' / 'data' / 'processed'
original_output = PROJECT_ROOT / 'output'
duplicate_output = PROJECT_ROOT / 'scripts' / 'output'

def get_file_hash(filepath):
    """Calculate MD5 hash of a file"""
    hash_md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def compare_directories(dir1, dir2, dir_name):
    """Compare two directories and return if they're duplicates"""
    print(f"\n{'='*70}")
    print(f"Checking: {dir_name}")
    print(f"{'='*70}")
    
    if not dir1.exists():
        print(f"   Original not found: {dir1}")
        return False, None
    
    if not dir2.exists():
        print(f"   ℹDuplicate not found: {dir2}")
        print(f"   Nothing to clean up")
        return False, None
    
    print(f"   Original:  {dir1}")
    print(f"   Duplicate: {dir2}")
    
    # Get all files in both directories
    files1 = {f.relative_to(dir1): f for f in dir1.rglob('*') if f.is_file()}
    files2 = {f.relative_to(dir2): f for f in dir2.rglob('*') if f.is_file()}
    
    print(f"\n   Files in original:  {len(files1)}")
    print(f"   Files in duplicate: {len(files2)}")
    
    # Check if file lists match
    only_in_original = set(files1.keys()) - set(files2.keys())
    only_in_duplicate = set(files2.keys()) - set(files1.keys())
    common_files = set(files1.keys()) & set(files2.keys())
    
    if only_in_original:
        print(f"\n   Files ONLY in original: {len(only_in_original)}")
        for f in list(only_in_original)[:5]:
            print(f"      - {f}")
        if len(only_in_original) > 5:
            print(f"      ... and {len(only_in_original) - 5} more")
    
    if only_in_duplicate:
        print(f"\n   Files ONLY in duplicate: {len(only_in_duplicate)}")
        for f in list(only_in_duplicate)[:5]:
            print(f"      - {f}")
        if len(only_in_duplicate) > 5:
            print(f"      ... and {len(only_in_duplicate) - 5} more")
    
    # Compare common files
    if common_files:
        print(f"\n   Comparing {len(common_files)} common files...")
        identical = []
        different = []
        
        for rel_path in common_files:
            hash1 = get_file_hash(files1[rel_path])
            hash2 = get_file_hash(files2[rel_path])
            
            if hash1 == hash2:
                identical.append(rel_path)
            else:
                different.append(rel_path)
        
        print(f"   Identical files: {len(identical)}")
        
        if different:
            print(f"   Different files: {len(different)}")
            for f in different:
                print(f"      - {f}")
                # Show file sizes
                size1 = files1[f].stat().st_size
                size2 = files2[f].stat().st_size
                print(f"        Original:  {size1:,} bytes")
                print(f"        Duplicate: {size2:,} bytes")
    
    # Determine if it's safe to delete
    is_duplicate = (
        len(files2) > 0 and  # Duplicate has files
        len(only_in_duplicate) == 0 and  # No unique files in duplicate
        len(different) == 0 and  # All common files are identical
        len(common_files) == len(files2)  # All duplicate files exist in original
    )
    
    if is_duplicate:
        print(f"\n   SAFE TO DELETE: All files in duplicate exist in original")
        return True, dir2
    elif len(files2) == 0:
        print(f"\n   SAFE TO DELETE: Duplicate directory is empty")
        return True, dir2
    else:
        print(f"\n   NOT SAFE TO DELETE: Directories differ")
        return False, None

# Check both directories
results = []
results.append(compare_directories(original_data, duplicate_data, "data/processed"))
results.append(compare_directories(original_output, duplicate_output, "output"))

# Summary
print(f"\n{'='*70}")
print("SUMMARY")
print(f"{'='*70}")

safe_to_delete = [path for is_safe, path in results if is_safe and path is not None]

if safe_to_delete:
    print(f"\nFound {len(safe_to_delete)} duplicate director{'y' if len(safe_to_delete) == 1 else 'ies'} that can be safely deleted:")
    for path in safe_to_delete:
        size = sum(f.stat().st_size for f in path.rglob('*') if f.is_file())
        print(f"   - {path} ({size:,} bytes)")
    
    print(f"\n{'='*70}")
    response = input("Delete these directories? (yes/no): ").strip().lower()
    
    if response == 'yes':
        print(f"\nDeleting...")
        for path in safe_to_delete:
            try:
                shutil.rmtree(path)
                print(f"   Deleted: {path}")
            except Exception as e:
                print(f"   Error deleting {path}: {e}")
        
        # Check if scripts/data is now empty
        scripts_data = PROJECT_ROOT / 'scripts' / 'data'
        if scripts_data.exists() and not list(scripts_data.iterdir()):
            print(f"\n   Removing empty directory: {scripts_data}")
            scripts_data.rmdir()
        
        print(f"\nCleanup complete!")
    else:
        print(f"\nCancelled. No files were deleted.")
else:
    print(f"\nNo duplicate directories found or not safe to delete")
    print(f"  All directories are either unique or contain differences")

print(f"\n{'='*70}")