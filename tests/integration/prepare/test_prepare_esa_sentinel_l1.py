import pytest
from pathlib import Path
import datetime
import shutil
import yaml

from tests.common import run_prepare_cli
from eodatasets3.prepare import sentinel_l1c_prepare


dataset = (
    "data/esa_s2_l1c/S2B_MSIL1C_20201011T000249_N0209_R030_T55HFA_20201011T011446.zip"
)

DATASET_PATH: Path = Path(__file__).parent.parent / dataset


@pytest.fixture()
def expected_dataset_document():
    return {
        "$schema": "https://schemas.opendatacube.org/dataset",
        "crs": "epsg:32755",
        "geometry": {
            "coordinates": [
                [
                    [600300.0, 6100000.0],
                    [709800.0, 6100000.0],
                    [709800.0, 5990200.0],
                    [600000.0, 5990200.0],
                    [600000.0, 6099700.0],
                    [600000.0, 6100000.0],
                    [600300.0, 6100000.0],
                ]
            ],
            "type": "Polygon",
        },
        "grids": {
            "coastal_aerosol_swir_1_cirrus_water_vapour": {
                "shape": [366, 366],
                "transform": [
                    300.0,
                    0.0,
                    600000.0,
                    0.0,
                    -300.0,
                    6100000.0,
                    0.0,
                    0.0,
                    1.0,
                ],
            },
            "default": {
                "shape": [1098, 1098],
                "transform": [
                    100.0,
                    0.0,
                    600000.0,
                    0.0,
                    -100.0,
                    6100000.0,
                    0.0,
                    0.0,
                    1.0,
                ],
            },
            "blue_green_nir_1_red": {
                "shape": [2196, 2196],
                "transform": [
                    50.0,
                    0.0,
                    600000.0,
                    0.0,
                    -50.0,
                    6100000.0,
                    0.0,
                    0.0,
                    1.0,
                ],
            },
        },
        "label": "esa_s2bm_level1_1-0-20201011_55HFA_2020-10-11",
        "lineage": {},
        "measurements": {
            "blue": {
                "grid": "blue_green_nir_1_red",
                "path": "S2B_MSIL1C_20201011T000249_N0209_R030_T55HFA_20201011T011446.SAFE/GRANULE/"
                "L1C_T55HFA_A018789_20201011T000244/IMG_DATA/T55HFA_20201011T000249_B02.jp2",
            },
            "coastal_aerosol": {
                "grid": "coastal_aerosol_swir_1_cirrus_water_vapour",
                "path": "S2B_MSIL1C_20201011T000249_N0209_R030_T55HFA_20201011T011446.SAFE/GRANULE/"
                "L1C_T55HFA_A018789_20201011T000244/IMG_DATA/T55HFA_20201011T000249_B01.jp2",
            },
            "green": {
                "grid": "blue_green_nir_1_red",
                "path": "S2B_MSIL1C_20201011T000249_N0209_R030_T55HFA_20201011T011446.SAFE/GRANULE/"
                "L1C_T55HFA_A018789_20201011T000244/IMG_DATA/T55HFA_20201011T000249_B03.jp2",
            },
            "nir_1": {
                "grid": "blue_green_nir_1_red",
                "path": "S2B_MSIL1C_20201011T000249_N0209_R030_T55HFA_20201011T011446.SAFE/GRANULE/"
                "L1C_T55HFA_A018789_20201011T000244/IMG_DATA/T55HFA_20201011T000249_B08.jp2",
            },
            "red": {
                "grid": "blue_green_nir_1_red",
                "path": "S2B_MSIL1C_20201011T000249_N0209_R030_T55HFA_20201011T011446.SAFE/GRANULE/"
                "L1C_T55HFA_A018789_20201011T000244/IMG_DATA/T55HFA_20201011T000249_B04.jp2",
            },
            "red_edge_1": {
                "path": "S2B_MSIL1C_20201011T000249_N0209_R030_T55HFA_20201011T011446.SAFE/GRANULE/"
                "L1C_T55HFA_A018789_20201011T000244/IMG_DATA/T55HFA_20201011T000249_B05.jp2"
            },
            "red_edge_2": {
                "path": "S2B_MSIL1C_20201011T000249_N0209_R030_T55HFA_20201011T011446.SAFE/GRANULE/"
                "L1C_T55HFA_A018789_20201011T000244/IMG_DATA/T55HFA_20201011T000249_B06.jp2"
            },
            "red_edge_3": {
                "path": "S2B_MSIL1C_20201011T000249_N0209_R030_T55HFA_20201011T011446.SAFE/GRANULE/"
                "L1C_T55HFA_A018789_20201011T000244/IMG_DATA/T55HFA_20201011T000249_B07.jp2"
            },
            "swir_1_cirrus": {
                "grid": "coastal_aerosol_swir_1_cirrus_water_vapour",
                "path": "S2B_MSIL1C_20201011T000249_N0209_R030_T55HFA_20201011T011446.SAFE/GRANULE/"
                "L1C_T55HFA_A018789_20201011T000244/IMG_DATA/T55HFA_20201011T000249_B10.jp2",
            },
            "swir_2": {
                "path": "S2B_MSIL1C_20201011T000249_N0209_R030_T55HFA_20201011T011446.SAFE/GRANULE/"
                "L1C_T55HFA_A018789_20201011T000244/IMG_DATA/T55HFA_20201011T000249_B11.jp2"
            },
            "swir_3": {
                "path": "S2B_MSIL1C_20201011T000249_N0209_R030_T55HFA_20201011T011446.SAFE/GRANULE/"
                "L1C_T55HFA_A018789_20201011T000244/IMG_DATA/T55HFA_20201011T000249_B12.jp2"
            },
            "water_vapour": {
                "grid": "coastal_aerosol_swir_1_cirrus_water_vapour",
                "path": "S2B_MSIL1C_20201011T000249_N0209_R030_T55HFA_20201011T011446.SAFE/GRANULE/"
                "L1C_T55HFA_A018789_20201011T000244/IMG_DATA/T55HFA_20201011T000249_B09.jp2",
            },
        },
        "product": {"name": "esa_s2bm_level1_1"},
        "properties": {
            "datetime": datetime.datetime(
                2020, 10, 11, 0, 2, 49, 24000, tzinfo=datetime.timezone.utc
            ),
            "eo:cloud_cover": 24.9912,
            "eo:gsd": 10,
            "eo:instrument": "MSI",
            "eo:platform": "sentinel-2b",
            "eo:sun_azimuth": 46.3307328858312,
            "eo:sun_elevation": 37.3713908882192,
            "odc:dataset_version": "1.0.20201011",
            "odc:file_format": "JPEG2000",
            "odc:processing_datetime": datetime.datetime(
                2020, 10, 11, 1, 14, 46, tzinfo=datetime.timezone.utc
            ),
            "odc:producer": "esa.int",
            "odc:product_family": "level1",
            "odc:region_code": "55HFA",
            "sentinel:datastrip_id": "S2B_OPER_MSI_L1C_DS_EPAE_20201011T011446_S20201011T000244_N02.09",
            "sentinel:datatake_type": "INS-NOBS",
            "sat:orbit_state": "descending",
            "sat:relative_orbit": 30,
            "sentinel:processing_baseline": "02.09",
            "sentinel:processing_center": "EPAE",
            "sentinel:reception_station": "EDRS",
        },
        "accessories": {
            "metadata:mtd_ds": {
                "path": "S2B_MSIL1C_20201011T000249_N0209_R030_T55HFA_20201011T011446.SAFE/DATASTRIP/"
                "DS_EPAE_20201011T011446_S20201011T000244/MTD_DS.xml"
            },
            "metadata:mtd_msil1c": {
                "path": "S2B_MSIL1C_20201011T000249_N0209_R030_T55HFA_20201011T011446.SAFE/MTD_MSIL1C.xml"
            },
            "metadata:mtd_tl": {
                "path": "S2B_MSIL1C_20201011T000249_N0209_R030_T55HFA_20201011T011446.SAFE/GRANULE/"
                "L1C_T55HFA_A018789_20201011T000244/MTD_TL.xml"
            },
        },
    }


def test_run(tmp_path, expected_dataset_document):

    # GIVEN:
    #     A folder of imagery
    dataset_id = DATASET_PATH.name.split(".")[0]
    outdir = tmp_path
    indir = DATASET_PATH

    if indir.is_file():
        shutil.copy(indir, outdir)
    else:
        shutil.copytree(indir, outdir)

    # WHEN:
    #    Run prepare on that folder
    output_yaml_path = outdir / (dataset_id + ".yaml")

    run_prepare_cli(
        sentinel_l1c_prepare.main,
        "--dataset",
        outdir / DATASET_PATH.name,
        "--dataset-document",
        output_yaml_path,
    )

    # THEN
    #     A metadata file is added to it, with valid properties
    #     Assert doc is expected doc
    with output_yaml_path.open("r") as f:
        generated_doc = yaml.safe_load(f)
        del generated_doc["id"]
    assert expected_dataset_document == generated_doc
