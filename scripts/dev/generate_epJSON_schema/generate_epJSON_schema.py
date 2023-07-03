import json
from pathlib import Path
import sys
from rich import print

print("[bold red]Generating the epJSON schema![/bold red]")
source_dir_path = Path(sys.argv[1])
idd_path = source_dir_path / 'Energy+.idd'
assert idd_path.exists()

with open(source_dir_path / 'Energy+.schema.epJSON', 'w') as f2:
    f2.write(json.dumps(idd_path.read_text(), indent=4))
