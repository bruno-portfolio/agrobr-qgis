from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any, ClassVar, Literal

from .source_adapter import ParamType


@dataclass(frozen=True)
class ParamBinding:
    source_id: str
    source_param: str
    transform: Callable[[Any], Any] | None = None


@dataclass(frozen=True)
class TemplateParam:
    name: str
    label: str
    param_type: ParamType
    required: bool = False
    default: Any = None
    choices: list[str] | None = None
    help_text: str = ""
    bindings: tuple[ParamBinding, ...] = ()


@dataclass(frozen=True)
class SourceDefaults:
    source_id: str
    defaults: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Template:
    id: str
    name: str
    description: str
    category: str
    source_ids: tuple[str, ...]
    params: tuple[TemplateParam, ...]
    source_defaults: tuple[SourceDefaults, ...] = ()


@dataclass
class SourceOutcome:
    source_id: str
    source_name: str
    status: Literal["ok", "error", "timeout", "cancelled"]
    result: Any = None
    error_message: str | None = None


@dataclass
class TemplateResult:
    template_id: str
    template_name: str
    outcomes: list[SourceOutcome]

    @property
    def succeeded(self) -> list[SourceOutcome]:
        return [o for o in self.outcomes if o.status == "ok"]

    @property
    def failed(self) -> list[SourceOutcome]:
        return [o for o in self.outcomes if o.status != "ok"]

    @property
    def all_ok(self) -> bool:
        return all(o.status == "ok" for o in self.outcomes)


class TemplateRegistry:
    _templates: ClassVar[dict[str, Template]] = {}

    @classmethod
    def register(cls, template: Template) -> Template:
        cls._validate(template)
        cls._templates[template.id] = template
        return template

    @classmethod
    def get(cls, template_id: str) -> Template | None:
        return cls._templates.get(template_id)

    @classmethod
    def list_all(cls) -> list[Template]:
        return list(cls._templates.values())

    @classmethod
    def clear(cls) -> None:
        cls._templates.clear()

    @classmethod
    def _validate(cls, template: Template) -> None:
        from .registry import SourceRegistry

        for sid in template.source_ids:
            if SourceRegistry.get(sid) is None:
                msg = f"Template '{template.id}': source '{sid}' not registered"
                raise ValueError(msg)

        defaults_map: dict[str, dict[str, Any]] = {}
        for sd in template.source_defaults:
            defaults_map[sd.source_id] = sd.defaults

        binding_map: dict[str, set[str]] = {}
        for tp in template.params:
            for b in tp.bindings:
                binding_map.setdefault(b.source_id, set()).add(b.source_param)

        for sid in template.source_ids:
            adapter_cls = SourceRegistry.get(sid)
            if adapter_cls is None:
                continue
            for sp in adapter_cls.parameters():
                if not sp.required:
                    continue
                covered = (
                    sp.default is not None
                    or sp.name in defaults_map.get(sid, {})
                    or sp.name in binding_map.get(sid, set())
                )
                if not covered:
                    msg = (
                        f"Template '{template.id}': required param '{sp.name}' "
                        f"on source '{sid}' not covered"
                    )
                    raise ValueError(msg)
