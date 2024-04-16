import zipfile
import os
import tempfile
import sys
import hashlib

def extract_files(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    return extract_to

def get_files_list(app_dir_path):
    file_paths = []
    for root, dirs, files in os.walk(app_dir_path):
        for file in files:
            file_paths.append(os.path.relpath(os.path.join(root, file), start=app_dir_path))
    return file_paths

def find_app_dir(payload_dir):
    for item in os.listdir(payload_dir):
        if item.endswith('.app'):
            return os.path.join(payload_dir, item)
    return None

def calculate_percentage(intersection, total_files):
    if total_files > 0:
        return (intersection / total_files) * 100
    else:
        return 0

def calculate_md5(file_path):
    with open(file_path, 'rb') as f:
        md5_hash = hashlib.md5()
        for chunk in iter(lambda: f.read(4096), b""):
            md5_hash.update(chunk)
    return md5_hash.hexdigest()

def main(path1, path2):
    temp_dir1 = tempfile.mkdtemp()
    temp_dir2 = tempfile.mkdtemp()

    if path1.endswith('.zip') or path1.endswith('.ipa'):
        extract_files(path1, temp_dir1)
    else:
        print("Error: The file at path1 is not a ZIP or IPA file.")
        return

    if path2.endswith('.zip') or path2.endswith('.ipa'):
        extract_files(path2, temp_dir2)
    else:
        print("Error: The file at path2 is not a ZIP or IPA file.")
        return

    app_dir1 = find_app_dir(os.path.join(temp_dir1, 'Payload'))
    app_dir2 = find_app_dir(os.path.join(temp_dir2, 'Payload'))

    if not app_dir1 or not app_dir2:
        print("Error: Could not find .app directory within the Payload folder.")
        return

    files_list1 = get_files_list(app_dir1)
    files_list2 = get_files_list(app_dir2)

    intersection = list(set(files_list1).intersection(set(files_list2)))

    percentage1 = calculate_percentage(len(intersection), len(files_list1))
    percentage2 = calculate_percentage(len(intersection), len(files_list2))
    
    print("Intersection of files in .app directories:")
    # need detail open this print
    # print(intersection)
    # print("\n")
    print(f"Intersection as percentage of {os.path.basename(path1)} files: {percentage1:.2f}% file count: {len(files_list1)}")
    print(f"Intersection as percentage of {os.path.basename(path2)} files: {percentage2:.2f}% file count: {len(files_list2)}")


    md5_matches = 0
    md5_matchesfile = []
    for file in intersection:
        file_path1 = os.path.join(app_dir1, file)
        file_path2 = os.path.join(app_dir2, file)
        md5_1 = calculate_md5(file_path1)
        md5_2 = calculate_md5(file_path2)
        if md5_1 == md5_2:
            # need detail open this print
            # print("same file name:" + file_path1 + " md5: " + md5_1)
            # print("same file name:" + file_path2 + " md5: " + md5_2)
            md5_matchesfile.append(file_path1)
            md5_matches += 1

    percentage_md5_matches = calculate_percentage(md5_matches, len(intersection))
    print(f"Intersection percentage of files with same MD5 hash: {percentage_md5_matches:.2f}% file count: {len(intersection)}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <path_to_zip1> <path_to_zip2>")
    else:
        main(sys.argv[1], sys.argv[2])
