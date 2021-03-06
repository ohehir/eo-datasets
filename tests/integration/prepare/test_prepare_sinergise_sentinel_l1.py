from pathlib import Path
import pytest
import shutil
import yaml
import datetime
from tests.common import run_prepare_cli
from eodatasets3.prepare import sentinel_l1c_prepare

path = (
    "data/sinergise_s2_l1c/S2B_MSIL1C_20201011T000249_N0209_R030_T55HFA_20201011T011446"
)

DATASET_DIR: Path = Path(__file__).parent.parent / path


@pytest.fixture()
def expected_dataset_document():
    return {
        "$schema": "https://schemas.opendatacube.org/dataset",
        "crs": "epsg:32755",
        "geometry": {
            "coordinates": [
                [
                    [600000.0, 5990200.0],
                    [600000.0, 6099500.909090909],
                    [600000.0, 6100000.0],
                    [600332.7272727273, 6100000.0],
                    [709800.0, 6100000.0],
                    [709800.0, 5990200.0],
                    [600000.0, 5990200.0],
                ]
            ],
            "type": "Polygon",
        },
        "grids": {
            "default": {
                "shape": [55, 55],
                "transform": [
                    1996.3636363636363,
                    0.0,
                    600000.0,
                    0.0,
                    -1996.3636363636363,
                    6100000.0,
                    0.0,
                    0.0,
                    1.0,
                ],
            },
            "blue_green_nir_1_red": {
                "shape": [110, 110],
                "transform": [
                    998.1818181818181,
                    0.0,
                    600000.0,
                    0.0,
                    -998.1818181818181,
                    6100000.0,
                    0.0,
                    0.0,
                    1.0,
                ],
            },
            "coastal_aerosol_swir_1_cirrus_water_vapour": {
                "shape": [19, 19],
                "transform": [
                    5778.9473684210525,
                    0.0,
                    600000.0,
                    0.0,
                    -5778.9473684210525,
                    6100000.0,
                    0.0,
                    0.0,
                    1.0,
                ],
            },
        },
        "label": "sinergise_s2am_level1_1-0-20201011_55HFA_2020-10-11",
        "lineage": {},
        "measurements": {
            "blue": {"grid": "blue_green_nir_1_red", "path": "B02.jp2"},
            "coastal_aerosol": {
                "grid": "coastal_aerosol_swir_1_cirrus_water_vapour",
                "path": "B01.jp2",
            },
            "green": {"grid": "blue_green_nir_1_red", "path": "B03.jp2"},
            "nir_1": {"grid": "blue_green_nir_1_red", "path": "B08.jp2"},
            "nir_2": {"path": "B8A.jp2"},
            "red": {"grid": "blue_green_nir_1_red", "path": "B04.jp2"},
            "red_edge_1": {"path": "B05.jp2"},
            "red_edge_2": {"path": "B06.jp2"},
            "red_edge_3": {"path": "B07.jp2"},
            "swir_1_cirrus": {
                "grid": "coastal_aerosol_swir_1_cirrus_water_vapour",
                "path": "B10.jp2",
            },
            "swir_2": {"path": "B11.jp2"},
            "swir_3": {"path": "B12.jp2"},
            "water_vapour": {
                "grid": "coastal_aerosol_swir_1_cirrus_water_vapour",
                "path": "B09.jp2",
            },
        },
        "product": {"name": "sinergise_s2am_level1_1"},
        "properties": {
            "datetime": datetime.datetime(
                2020, 10, 11, 0, 6, 49, 882000, tzinfo=datetime.timezone.utc
            ),
            "eo:cloud_cover": 24.9912,
            "eo:gsd": 10,
            "eo:instrument": "MSI",
            "eo:platform": "sentinel-2a",
            "eo:sun_azimuth": 37.3713908882192,
            "eo:sun_elevation": 46.3307328858312,
            "odc:dataset_version": "1.0.20201011",
            "odc:file_format": "JPEG2000",
            "odc:processing_datetime": datetime.datetime(
                2020, 10, 11, 1, 47, 4, 112949, tzinfo=datetime.timezone.utc
            ),
            "odc:producer": "sinergise.com",
            "odc:product_family": "level1",
            "odc:region_code": "55HFA",
            "sentinel:grid_square": "FA",
            "sentinel:latitude_band": "H",
            "sentinel:utm_zone": 55,
            "sinergise_product_id": "73e1a409-595d-4fbf-8fe0-01e0ee26bf00",
            "sinergise_product_name": "S2B_MSIL1C_20201011T000249_N0209_R030_T55HFA_20201011T011446",
            "sentinel:datastrip_id": "S2B_OPER_MSI_L1C_DS_EPAE_20201011T011446_S20201011T000244_N02.09",
            "sentinel:datatake_start_datetime": datetime.datetime(
                2020, 10, 11, 1, 14, 46, tzinfo=datetime.timezone.utc
            ),
            "sentinel:sentinel_tile_id": "S2B_OPER_MSI_L1C_TL_EPAE_20201011T011446_A018789_T55HFA_N02.09",
        },
        "accessories": {
            "metadata:product_info": {"path": "productInfo.json"},
            "metadata:sinergise_metadata": {"path": "metadata.xml"},
        },
    }


def test_sinergise_sentinel_l1(tmp_path, expected_dataset_document):

    # GIVEN:
    #     A folder of imagery
    outdir = tmp_path / DATASET_DIR.name
    indir = DATASET_DIR

    if indir.is_file():
        shutil.copy(indir, outdir)
    else:
        shutil.copytree(indir, outdir)

    # WHEN:
    #    Run prepare on that folder

    output_yaml_path = outdir / "test.yaml"

    run_prepare_cli(
        sentinel_l1c_prepare.main,
        "--dataset",
        outdir,
        "--dataset-document",
        output_yaml_path,
    )

    # THEN
    #     A metadata file is added to it, with valid properties
    #     Assert doc is expected doc
    with output_yaml_path.open("r") as f:
        generated_doc = yaml.safe_load(f)
        del generated_doc["id"]
        from pprint import pprint

        pprint(generated_doc)
    assert expected_dataset_document == generated_doc
