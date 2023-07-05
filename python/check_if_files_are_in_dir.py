import click
from pathlib import Path
import hashlib


def get_file_checksum(file_path):
    """Calculates the checksum of a file."""
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as file:
        for chunk in iter(lambda: file.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


@click.command()
@click.argument('dir1', type=click.Path(exists=True, file_okay=False, resolve_path=True))
@click.argument('dir2', type=click.Path(exists=True, file_okay=False, resolve_path=True))
def main(dir1, dir2):
    """Compares files in DIR1 with files in DIR2 and prints differences."""
    click.echo(f"Comparing files in {dir1} with files in {dir2}...")

    dir1_path = Path(dir1)
    dir2_path = Path(dir2)

    mismatched_files = []
    missing_files = []
    multiples = []

    for file1_path in dir1_path.rglob('*'):
        if file1_path.name in ['.DS_Store', 'Thumbs.db']:
            continue
        if file1_path.is_file():
            file_name = file1_path.name
            in_path2 = list(dir2_path.rglob(file_name))
            if len(in_path2) == 0:
                missing_files.append(file1_path)
            else:
                if len(in_path2) > 1:
                    # click.echo(f"Multiple files with name {file_name} found in {dir2}:\n{[fn.absolute() for fn in in_path2]}")
                    multiples.append((file1_path, in_path2))
                checksum1 = get_file_checksum(file1_path)
                checksum2 = get_file_checksum(in_path2[0])
                if checksum1 != checksum2:
                    mismatched_files.append((file1_path, in_path2[0]))

    click.echo("Mismatched files:")
    for file_path in mismatched_files:
        click.echo(file_path)

    click.echo("Missing files:")
    for file_path in missing_files:
        click.echo(file_path)

    click.echo("Summary:")
    click.echo(f"Total mismatched files: {len(mismatched_files)}")
    click.echo(f"Total missing files: {len(missing_files)}")
    click.echo(f"Missing: {missing_files}")
    click.echo(f"Total multiples: {len(multiples)}")
    click.echo(f"Multiples: {multiples}")


if __name__ == '__main__':
    main()
