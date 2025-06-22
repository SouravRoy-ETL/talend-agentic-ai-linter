import zipfile
import os
import time

def extract_all_items_from_zips(zip_dir="zipped_jobs", output_folder="jobs"):
    extracted_folder = "temp_extracted"
    os.makedirs(extracted_folder, exist_ok=True)
    os.makedirs(output_folder, exist_ok=True)

    zip_files = [f for f in os.listdir(zip_dir) if f.endswith(".zip")]
    total_copied = 0

    for zip_file in zip_files:
        zip_path = os.path.join(zip_dir, zip_file)
        print(f"📦 Processing {zip_file}...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extracted_folder)

        for root, dirs, files in os.walk(extracted_folder):
            if "process" in root.replace('\\', '/').split('/'):
                for file in files:
                    if file.endswith(".item"):
                        src = os.path.join(root, file)
                        dst = os.path.join(output_folder, file)
                        with open(src, 'rb') as fsrc, open(dst, 'wb') as fdst:
                            fdst.write(fsrc.read())
                        print(f"✅ Extracted job: {file}")
                        total_copied += 1
                        time.sleep(1.1)

        # Cleanup extracted files
        for root, dirs, files in os.walk(extracted_folder, topdown=False):
            for file in files:
                os.remove(os.path.join(root, file))
            for dir in dirs:
                os.rmdir(os.path.join(root, dir))

    print(f"🎉 Finished! {total_copied} .item job file(s) copied to '{output_folder}'.")

if __name__ == "__main__":
    extract_all_items_from_zips()
