from __future__ import annotations

import pandas as pd
import pytest

from agrobr_qgis.core.registry import SourceRegistry
from agrobr_qgis.core.source_adapter import SourceCapability, SourceCategory


@pytest.fixture(autouse=True)
def _register_source() -> None:
    from agrobr_qgis.sources.mapbiomas_cobertura import MapBiomasCoberturaSource

    SourceRegistry.register(MapBiomasCoberturaSource)


class TestMapBiomasCoberturaSource:
    def test_registered_in_registry(self) -> None:
        assert SourceRegistry.get("mapbiomas_cobertura") is not None

    def test_id(self) -> None:
        src = SourceRegistry.get("mapbiomas_cobertura")
        assert src is not None
        assert src.id() == "mapbiomas_cobertura"

    def test_name(self) -> None:
        src = SourceRegistry.get("mapbiomas_cobertura")
        assert src is not None
        assert src.name() == "Cobertura (MapBiomas)"

    def test_category(self) -> None:
        src = SourceRegistry.get("mapbiomas_cobertura")
        assert src is not None
        assert src.category() == SourceCategory.AMBIENTAL

    def test_capabilities_is_tile_service(self) -> None:
        src = SourceRegistry.get("mapbiomas_cobertura")
        assert src is not None
        assert src.capabilities() & SourceCapability.TILE_SERVICE
        assert not (src.capabilities() & SourceCapability.GEO)
        assert not (src.capabilities() & SourceCapability.TABULAR)

    def test_parameters_has_ano(self) -> None:
        src = SourceRegistry.get("mapbiomas_cobertura")
        assert src is not None
        params = src.parameters()
        assert len(params) == 1
        assert params[0].name == "ano"
        assert params[0].required is True
        assert params[0].choices is not None
        assert len(params[0].choices) == 40

    def test_tile_uri_default_year(self) -> None:
        src = SourceRegistry.get("mapbiomas_cobertura")
        assert src is not None
        uri = src.tile_uri()
        assert uri is not None
        assert "mapbiomas_brazil_2024" in uri
        assert "EPSG:4326" in uri
        assert "image/png" in uri
        assert "solved:mapbiomas_legend" in uri
        assert "dpiMode=7" in uri
        assert "contextualWMSLegend=0" in uri
        assert "featureCount=10" in uri

    def test_tile_uri_specific_year(self) -> None:
        src = SourceRegistry.get("mapbiomas_cobertura")
        assert src is not None
        uri = src.tile_uri(ano="1985")
        assert uri is not None
        assert "mapbiomas_brazil_1985" in uri

    def test_tile_uri_contains_wms_base(self) -> None:
        src = SourceRegistry.get("mapbiomas_cobertura")
        assert src is not None
        uri = src.tile_uri(ano="2000")
        assert uri is not None
        assert "azure.solved.eco.br:8080/geoserver/solved/wms" in uri

    def test_fetch_returns_empty_dataframe(self) -> None:
        src_cls = SourceRegistry.get("mapbiomas_cobertura")
        assert src_cls is not None
        result = src_cls().fetch()
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0

    def test_source_url(self) -> None:
        src = SourceRegistry.get("mapbiomas_cobertura")
        assert src is not None
        assert src.source_url() == "https://mapbiomas.org/"

    def test_health_url_is_wms_capabilities(self) -> None:
        src = SourceRegistry.get("mapbiomas_cobertura")
        assert src is not None
        url = src.health_url()
        assert url is not None
        assert "GetCapabilities" in url
