import os
import click

def lowercase_directories(path):
    for root, dirs, files in os.walk(path):
        for directory in dirs:
            original_name = os.path.join(root, directory)
            lowercase_name = os.path.join(root, directory.lower())

            if original_name != lowercase_name:
                if os.path.exists(lowercase_name):
                    suffix = 1
                    while os.path.exists(lowercase_name + "_" + str(suffix)):
                        suffix += 1
                    lowercase_name += "_" + str(suffix)
                else:
                    lowercase_name = original_name

                os.rename(original_name, lowercase_name)
                click.echo(f"Renamed: {original_name} -> {lowercase_name}")

@click.command()
@click.argument('directory_path', type=click.Path(exists=True))
def lowercase_cli(directory_path):
    """
    Lowercase the names of all directories (including subdirectories) in the specified DIRECTORY_PATH.
    """
    lowercase_directories(directory_path)

if __name__ == "__main__":
    lowercase_cli()
