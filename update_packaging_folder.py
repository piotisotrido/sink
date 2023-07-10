import json
import sys
import os

TOP_INDEX = """
<!DOCTYPE html>
<html>
    <head>
        <title>Python packages on GitHub</title>
        <meta name="description" content="Simple Python packages server on GitHub pages. ">
    </head>
    <body>
        <h1>Simple Python packages server on github pages.</h1>
        <p>Welcome to this simple python packages server.</p>

"""

# Content structure:
# content = {
#   package_name: {
#       version1: url,
#       version2: url,
#   },
# }

BOTTOM_INDEX = """
    </body>
</html>
"""

ROOT_PATH = "./pypackages"

def verify_args():
    if len(sys.argv) < 4:
        print("Usage: script.py [name] [version] [url]",file=sys.stderr)
        exit(2)

    return  {sys.argv[1]: {sys.argv[2]: sys.argv[3]}}


def json_content(path: str, package: dict):
    with open(path, mode="r") as f:
        content = json.loads(f.read())
    content.update(package)
    with open(path, mode="w") as f:
        print(
            json.dumps(content, sort_keys=False, indent=4),
            file=f,
        )
    return content


def create_dirs(root_dir: str, packages: list):
    for d in packages:
        if not os.path.exists(f"{root_dir}/{d}/"):
            os.mkdir(f"{root_dir}/{d}/")


def write_index(path: str, top: str, bottom: str, content: dict):
    with open(path, mode='w') as f:
        print(top, file=f)
        for package, ref in content.items():
            print(f'<a href="{ref}">{package}</a><br />', file=f)
        print(bottom, file=f)


def create_index_file():
    pass

if __name__ == "__main__":
    rp = ROOT_PATH
    new_package = verify_args()
    content = json_content(f"{rp}/content.json", new_package)
    packages = {key: f"{key}/index.html" for key in content.keys()}
    write_index(f"{rp}/index.html", TOP_INDEX, BOTTOM_INDEX, packages)
    create_dirs(rp, packages.keys())
    for pack in packages.keys():
        write_index(f"{rp}/{packages[pack]}", TOP_INDEX, BOTTOM_INDEX, content[pack])
