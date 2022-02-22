import os
import urllib.request
import zipfile

VANILLA_BP_URL = "https://aka.ms/behaviorpacktemplate"
VANILLA_RP_URL = "https://aka.ms/resourcepacktemplate"
CACHE_DIR = os.environ.get("MC_ADDON_CACHE") or "cache"

"""
regolith has filters run in the .regolith/tmp directory, but that's cleared on run.
It'd be nice if we could persist the vanilla addons longer than a single run if the
user hasn't specified environment variables where they reside.
"""
REGOLITH_CACHE_FILTER_PATH_FROM_TMP="..{sep}cache{sep}github.com{sep}littlechestnutgames{sep}regolith-filters{sep}extend-vanilla-entities{sep}".format(sep=os.sep)

BP_ADDON_DIR = os.environ.get("MC_VANILLA_BP_DIR") or "%s%s%sBP" % (REGOLITH_CACHE_FILTER_PATH_FROM_TMP, CACHE_DIR,os.sep)
RP_ADDON_DIR = os.environ.get("MC_VANILLA_RP_DIR") or "%s%s%sRP" % (REGOLITH_CACHE_FILTER_PATH_FROM_TMP, CACHE_DIR,os.sep)

PACKFILES = [
    {"url": VANILLA_BP_URL, "name": "Vanilla Behavior Pack", "path": BP_ADDON_DIR},
    {"url": VANILLA_RP_URL, "name": "Vanilla Resource Pack", "path": RP_ADDON_DIR}
]

# Maybe in the future, loading up PACKFILES other than the vanilla packfiles?
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
