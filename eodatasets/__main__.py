import functools
import os
import logging

import click
from pathlib import Path


import eodatasets.package as package

@click.command()
@click.option('--parent', type=click.Path(exists=True, readable=True, writable=False), multiple=True)
@click.option('--debug', is_flag=True)
@click.option('--in-place', is_flag=True)
@click.argument('type', type=click.Choice(package.PACKAGE_DRIVERS.keys()))
@click.argument('dataset', type=click.Path(exists=True, readable=True, writable=False), nargs=-1)
@click.argument('destination', type=click.Path(exists=True, readable=True, writable=True), nargs=1)
def run_packaging(parent, debug, in_place, type, dataset, destination):
    """
    :type parent: str
    :type debug: bool
    :type in_place: bool
    :type type: str
    :type dataset: list of str
    :type destination: str
    """
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s')

    if debug:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger('eodatasets').setLevel(logging.INFO)

    parent_datasets = {}

    #: :type: package.DatasetDriver
    driver = package.PACKAGE_DRIVERS[type]

    # TODO: Multiple parents?
    if parent:
        source_id = driver.expected_source().get_id()
        parent_datasets.update({source_id: package.get_dataset(Path(parent[0]))})

    # If we're packaging in-place (ie. generating metadata), all listed paths are datasets.
    if in_place:
        dataset = list(dataset)
        dataset.append(destination)
        destination = None

    for dataset_path in dataset:
        if in_place:
            target_folder = dataset_path
        else:
            target_folder = os.path.join(destination, type)
            if not os.path.exists(target_folder):
                os.mkdir(target_folder)

        package.do_package(
            driver,
            dataset_path,
            target_folder,
            source_datasets=parent_datasets
        )

run_packaging()