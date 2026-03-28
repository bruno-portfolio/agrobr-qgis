from __future__ import annotations

import pytest

from agrobr_qgis.core.exceptions import (
    AgroBRError,
    AuthError,
    ChecksumError,
    ContractError,
    DependencyError,
    FetchError,
    JoinError,
)

SUBCLASSES = [FetchError, ContractError, JoinError, AuthError, DependencyError, ChecksumError]


class TestExceptionHierarchy:
    def test_agrobr_error_inherits_from_exception(self) -> None:
        assert issubclass(AgroBRError, Exception)

    @pytest.mark.parametrize("cls", SUBCLASSES, ids=lambda c: c.__name__)
    def test_all_inherit_from_agrobr_error(self, cls: type[AgroBRError]) -> None:
        assert issubclass(cls, AgroBRError)

    @pytest.mark.parametrize("cls", SUBCLASSES, ids=lambda c: c.__name__)
    def test_message_format(self, cls: type[AgroBRError]) -> None:
        err = cls("algo deu errado")
        assert str(err) == "algo deu errado"

    @pytest.mark.parametrize("cls", SUBCLASSES, ids=lambda c: c.__name__)
    def test_isinstance_hierarchy(self, cls: type[AgroBRError]) -> None:
        err = cls("teste")
        assert isinstance(err, AgroBRError)
        assert isinstance(err, Exception)

    def test_raise_and_catch_base(self) -> None:
        with pytest.raises(AgroBRError):
            raise FetchError("falha no fetch")
