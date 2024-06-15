import os
import shutil
import urllib.request
import subprocess
import sys
from zipfile import ZipFile
from rich.progress import Progress, BarColumn
def install(package):
    print(f"{package} not found, installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
try: from rich.progress import Progress
except ImportError:
    install('rich')
    from rich.progress import Progress
try: import pyfiglet
except ImportError:
	install('pyfiglet')
	from pyfiglet import Figlet
plugins = [
    {"name": "WooCommerce" , 'url': 'https://downloads.wordpress.org/plugin/woocommerce.latest-stable.zip' },
    {"name": "Advanced Custom Fields", 'url': 'https://downloads.wordpress.org/plugin/advanced-custom-fields.latest-stable.zip'},
    {"name": "Easy Digital Downloads", 'url': 'https://downloads.wordpress.org/plugin/easy-digital-downloads.latest-stable.zip'},
]
def download_file_with_progress(url, file_name):
    with urllib.request.urlopen(url) as response:
        total_size = int(response.info()['Content-Length'])
    print(f"🌐 {url}")
    with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
        with Progress("[progress.description]{task.description}", BarColumn(), "{task.percentage:>3.1f}%", 
                    "[bold white]( [bold yellow]{task.fields[downloaded]}[bold white] / [bold cyan]{task.fields[total_size]}[bold white] )") as progress:
            task = progress.add_task(f"👉 {file_name}", total=total_size, total_size=f"{total_size / (1024 * 1024):.2f} MB", downloaded="0.00 MB")
            while True:
                buffer = response.read(1024)
                if not buffer: break
                out_file.write(buffer)
                progress.update(task, advance=len(buffer), downloaded=f"{out_file.tell() / (1024 * 1024):.2f} MB")
            progress.update(task, completed=total_size, downloaded=f"{total_size / (1024 * 1024):.2f} MB")
def hyperlink(text, url): return f"\033[4m\033[93m\033]8;;{url}\033\\{text}\033]8;;\033\\\033[0m"
def print_double_border(lines, space=2, trex=False, success=False):
    max_length = max(len(line) for line in lines)
    border_length = max_length + space + space  # 2 borders + 2 spaces
    print(f"╔{'═' * border_length}╗")
    for index, line in enumerate(lines):
        if index == len(lines) - 1:
            centered_line = line.center(max_length)
            if trex:
                centered_line = centered_line.replace("AmirhpCom", hyperlink("AmirhpCom", "https://amirhp.com/"));
                centered_line += "🦖";
                print(f"║{' ' * space}{centered_line}{' ' * (border_length - len(centered_line) - space)}")
            else:
                print(f"║{' ' * space}{centered_line}{' ' * (border_length - len(centered_line) - space)}║")
        else:
            print(f"║{' ' * space}\033[31m{line}\033[0m{' ' * (border_length - len(line) - space )}║")
    print(f"╚{'═' * border_length}╝")
figs = [item for item in pyfiglet.figlet_format("Black Swan", font="ansi_regular", width=120).split("\n") if item.strip() != ""]
print_double_border(figs+["BLACK SWAN STUB UPDATER - PROGRAMMED BY AmirhpCom\u2197 - VERSION 1.0"], 0, True)
for plugin in plugins:
    plugin_name = plugin['name']
    plugin_file = plugin['name'].lower().replace(' ', '-')
    plugin_url = plugin['url']
    zip_file_name = f"{plugin_file}.zip"
    print(f"\n⌛ Processing {plugin_name}...")
    if os.path.exists(plugin_file) and os.path.isdir(plugin_file):
        shutil.rmtree(plugin_file)
        print(f"👉 Removed existing folder: {plugin_file}")
    download_file_with_progress(plugin_url, zip_file_name)
    print("👉 Download complete ...")
    print("👉 Extracting zip file ...")
    with ZipFile(zip_file_name, 'r') as zip_file: zip_file.extractall()
    print("👉 Extraction complete ...")
    os.remove(zip_file_name)
    print("👉 Clean up zip file complete ...")
input(f"\n\033[42m\033[97m ALL TASKS DONE SUCCESSFULLY\033[0m Press Enter to exit ...")