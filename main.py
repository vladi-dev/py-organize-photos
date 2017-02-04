# -*- coding: utf-8 -*-
import re
import os
import calendar
import shutil
from datetime import datetime

import click


def move_file(src, output_dir):
    """Copies src file matched with photo pattern regex
    to a structured directory tree in output directory.

    The structure of directories would be: {year}/{month}/{day}/{src}
    For example:
        /2017/January/12/IMG_20170112_1234.jpg

    :param src: Source file to copy
    :param output_dir: Output directory where to copy source file
    """
    date_pattern = '\/IMG_(\d{4}\d{2}\d{2})_.*\.jpg$'
    match = re.search(date_pattern, src)

    if not match:
        raise ValueError('Pattern not recognized')

    photo_date = match.groups()[0]

    try:
        d = datetime.strptime(photo_date, "%Y%m%d")
    except ValueError as e:
        raise ValueError('Failed to parse date string: {}'.format(photo_date))

    dst = "{}/{}/{}/{}".format(output_dir, d.year, calendar.month_name[d.month], d.day)

    if not os.path.isdir(dst):
        try:
            os.makedirs(dst)
        except OSError as e:
            raise ValueError('Failed to create directory tree: {}'.format(str(e)))

    try:
        shutil.copy2(src, dst)
    except IOError as e:
        raise ValueError('Failed to copy file: {}'.format(str(e)))


@click.command()
@click.option('--input-dir', type=click.Path(exists=True), required=True,
              help='Directory where to find photo files')
@click.option('--output-dir', type=click.Path(), required=True,
              help='Directory to which photos will be copied in an organized manner')
def organize(input_dir, output_dir):
    """Organizes photos by copying them from input-dir to output-dir
    and structures them in directories by year, month and day

    The structure of directories would be: {year}/{month}/{day}/{src}
    """
    counter, err_counter = 0, 0
    errors = []

    click.secho('Source dir: {}'.format(input_dir))
    click.secho('Output dir: {}'.format(output_dir))

    files = os.listdir(input_dir)

    def show_filename(filename):
        if filename is not None:
            return filename

    with click.progressbar(files, label="Organizing photos",
                           fill_char=click.style('#', fg='green'),
                           item_show_func=lambda item: item) as progress_files:
        for f in progress_files:
            try:
                src = '{}/{}'.format(input_dir, f)
                move_file(src, output_dir)
                counter += 1
            except (ValueError, AttributeError) as e:
                err_counter += 1
                errors.append('Error copying file: {} - {}'.format(f, str(e)))

    for error in errors:
        click.secho(error, err=True)

    click.secho('Total photos copied: {}'.format(counter))
    click.secho('Total photos failed: {}'.format(err_counter))
