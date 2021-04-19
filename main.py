from datetime import datetime
from os import listdir
from os.path import isfile, join

import piexif as piexif

import click as click


@click.group()
@click.version_option()
def cli():
    """This is a cli to retag your images"""


@click.command(name="tag_images")
@click.option("--folder", type=click.STRING, help="Location from which all files will be tagged")
def tag_images(folder):
    click.echo(f"Start tagging pictures in folder: {folder}")
    onlyfiles = [f for f in listdir(folder) if isfile(join(folder, f))]
    click.echo(f"Found {len(onlyfiles)} files")
    number = 1
    for file in onlyfiles:
        click.echo(f"Tagging Image {number} {file}")
        number = number+1
        creation_date = file.split("-")
        exif_dict = piexif.load(f"{folder}/{file}")
        new_date = datetime.strptime(creation_date[1], '%Y%m%d').strftime("%Y:%m:%d %H:%M:%S")
        exif_dict['0th'][piexif.ImageIFD.DateTime] = new_date
        exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = new_date
        exif_dict['Exif'][piexif.ExifIFD.DateTimeDigitized] = new_date
        if exif_dict['thumbnail']:
            if len(exif_dict['thumbnail']) >= 64000:
                exif_dict['thumbnail'] = None
        exif_bytes = piexif.dump(exif_dict)
        piexif.insert(exif_bytes, f"{folder}/{file}")
    click.echo(f"Finished Tagging")



cli.add_command(tag_images)

if __name__ == "__main__":
    cli(obj={})
