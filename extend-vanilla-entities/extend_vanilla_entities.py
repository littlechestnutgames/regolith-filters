import os
import urllib.request
import zipfile

VANILLA_BP_URL = "https://aka.ms/behaviorpacktemplate"
VANILLA_RP_URL = "https://aka.ms/resourcepacktemplate"
CACHE_DIR = os.environ.get("MC_ADDON_CACHE") or "cache"
BP_ADDON_DIR = os.environ.get("MC_VANILLA_BP_DIR") or "%s%sBP" % (CACHE_DIR,os.sep)
RP_ADDON_DIR = os.environ.get("MC_VANILLA_RP_DIR") or "%s%sRP" % (CACHE_DIR,os.sep)

PACKFILES = [
    {"url": VANILLA_BP_URL, "name": "Vanilla Behavior Pack", "path": BP_ADDON_DIR},
    {"url": VANILLA_RP_URL, "name": "Vanilla Resource Pack", "path": RP_ADDON_DIR}
]

# If a local_settings exists, import it.
if os.path.exists("local_settings.py"):
    try:
        from local_settings import *
    except ImportError:
        pass

def check_path(path, name, url=None):
    # If we don't have a directory, it's a no-go.
    if os.path.isfile(path):
        print("Expected directory at path \"%s\", got a file instead." % (path))
        print("Exiting.")
        die(1)
    if not os.path.exists(path):
        print("Cache directory for \"%s\" doesn't exist at path \"%s\". Trying to create it." % (name, path))
        os.makedirs(path)
        if not os.path.exists(path):
            print("Couldn't create cache directory \"%s\"." % (path))
            print("Exiting.")
            die(2)
        if not url is None:
            print("Retrieving remote pack \"%s\" from \"%s\"" % (name, url))
            local_file = "%s%s%s.zip" % (path, os.sep, os.path.basename(os.path.normpath(path)))
            urllib.request.urlretrieve(url, local_file)
            
            if not zipfile.is_zipfile(local_file):
                print("Pack \"%s\" is not a zip file." % (name))
                die(3)

            print("Unzipping \"%s\" to \"%s\"" % (local_file, path))
            with zipfile.ZipFile(local_file, "r") as zipped_pack:
                zipped_pack.extractall(path)

def die(ret):
    print("Exiting.")
    exit(ret)

def main():
    for pack in PACKFILES:
        check_path(pack.get("path"), pack.get("name"), pack.get("url"))

if __name__ == "__main__":
    main()
