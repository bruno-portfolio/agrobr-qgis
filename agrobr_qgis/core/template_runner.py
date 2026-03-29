from __future__ import annotations

from typing import Any

from qgis.core import QgsTask  # type: ignore[import-untyped]
from qgis.PyQt.QtCore import pyqtSignal  # type: ignore[import-untyped]

from .data_contract import DataContract
from .registry import SourceRegistry
from .template import SourceOutcome, Template, TemplateResult


class TemplateFetchTask(QgsTask):  # type: ignore[misc]
    allCompleted = pyqtSignal(object)
    errorOccurred = pyqtSignal(str)

    def __init__(self, template: Template, params: dict[str, Any], *, geo: bool = False) -> None:
        super().__init__(f"Template: {template.name}", QgsTask.CanCancel)
        self._template = template
        self._params = params
        self._geo = geo
        self._outcomes: list[SourceOutcome] = []
        self._result: TemplateResult | None = None

    def run(self) -> bool:
        source_params = self._resolve_params()
        total = len(self._template.source_ids)
        for i, sid in enumerate(self._template.source_ids):
            if self.isCanceled():
                name = self._source_name(sid)
                self._outcomes.append(SourceOutcome(sid, name, "cancelled"))
                continue
            outcome = self._fetch_one(sid, source_params.get(sid, {}))
            self._outcomes.append(outcome)
            self.setProgress((i + 1) / total * 100)
        self._result = TemplateResult(
            template_id=self._template.id,
            template_name=self._template.name,
            outcomes=self._outcomes,
        )
        return True

    def finished(self, result: bool) -> None:
        if result and self._result:
            self.allCompleted.emit(self._result)
        else:
            self.errorOccurred.emit("Execucao do template cancelada")

    def _fetch_one(self, source_id: str, params: dict[str, Any]) -> SourceOutcome:
        name = self._source_name(source_id)
        adapter_cls = SourceRegistry.get(source_id)
        if adapter_cls is None:
            return SourceOutcome(source_id, name, "error", error_message="Fonte nao encontrada")
        try:
            adapter = adapter_cls()
            raw = adapter.fetch(geo=self._geo, **params)
            contract_result = DataContract.validate(raw)
            return SourceOutcome(source_id, name, "ok", result=contract_result)
        except TimeoutError:
            return SourceOutcome(source_id, name, "timeout", error_message="Timeout")
        except Exception as e:
            return SourceOutcome(source_id, name, "error", error_message=str(e))

    @staticmethod
    def _source_name(source_id: str) -> str:
        adapter_cls = SourceRegistry.get(source_id)
        return adapter_cls.name() if adapter_cls else source_id

    def _resolve_params(self) -> dict[str, dict[str, Any]]:
        result: dict[str, dict[str, Any]] = {}
        for sid in self._template.source_ids:
            params: dict[str, Any] = {}
            adapter_cls = SourceRegistry.get(sid)
            if adapter_cls:
                for sp in adapter_cls.parameters():
                    if sp.default is not None:
                        params[sp.name] = sp.default
            for sd in self._template.source_defaults:
                if sd.source_id == sid:
                    params.update(sd.defaults)
            for tparam in self._template.params:
                user_value = self._params.get(tparam.name)
                if user_value is None:
                    continue
                for binding in tparam.bindings:
                    if binding.source_id == sid:
                        value = binding.transform(user_value) if binding.transform else user_value
                        params[binding.source_param] = value
            result[sid] = params
        return result
