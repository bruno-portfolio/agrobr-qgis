import agrobr_qgis


def test_plugin_package_importable():
    assert hasattr(agrobr_qgis, "__file__")
