"""Shared helpers for constructing Outlines models across providers."""

from __future__ import annotations

import importlib
import os
from dataclasses import dataclass
from functools import cache
from typing import TYPE_CHECKING, Any, Literal

if TYPE_CHECKING:
    from outlines.models.base import Model
else:  # pragma: no cover - keep runtime dependency optional
    Model = Any

OutlinesProvider = Literal["gemini", "openai"]

_DEFAULT_PROVIDER: OutlinesProvider = "gemini"
_PROVIDER_ENV_VARS = ("GVO_OUTLINES_PROVIDER", "OUTLINES_PROVIDER")


@dataclass(frozen=True, eq=False)
class OutlinesRuntime:
    """Runtime bundle exposing the model and default inference kwargs."""

    model: Model
    provider: OutlinesProvider
    model_name: str
    inference_defaults: dict[str, Any]


def get_outlines_runtime(
    provider: str | None = None, *, refresh: bool = False
) -> OutlinesRuntime:
    """Return a cached Outlines runtime configured for the requested provider."""
    provider_key = _normalise_provider(provider)
    if refresh:
        _load_outlines_runtime.cache_clear()
    return _load_outlines_runtime(provider_key)


def _normalise_provider(provider: str | None) -> OutlinesProvider:
    if provider:
        key = provider.strip().lower()
    else:
        for env_var in _PROVIDER_ENV_VARS:
            value = os.getenv(env_var)
            if value:
                key = value.strip().lower()
                break
        else:
            key = _DEFAULT_PROVIDER

    if key not in {"gemini", "openai"}:
        msg = f"Unsupported Outlines provider: {provider!r}"
        raise RuntimeError(msg)
    return key  # type: ignore[return-value]


@cache
def _load_outlines_runtime(provider: OutlinesProvider) -> OutlinesRuntime:
    model_name = _resolve_model_name(provider)
    if provider == "gemini":
        model = _build_gemini_model(model_name)
        inference_defaults = _build_gemini_inference_defaults()
    elif provider == "openai":
        model = _build_openai_model(model_name)
        inference_defaults = _build_openai_inference_defaults()
    else:  # pragma: no cover - defensive programming for type narrowing
        msg = f"Unhandled provider: {provider}"
        raise RuntimeError(msg)
    return OutlinesRuntime(
        model=model,
        provider=provider,
        model_name=model_name,
        inference_defaults=inference_defaults,
    )


def _resolve_model_name(provider: OutlinesProvider) -> str:
    env_priority: tuple[tuple[str, ...], str]
    if provider == "gemini":
        env_priority = (
            (
                "GVO_GEMINI_MODEL_NAME",
                "GEMINI_MODEL_NAME",
                "GOOGLE_MODEL_NAME",
                "OUTLINES_MODEL_NAME",
            ),
            "gemini-1.5-flash",
        )
    else:
        env_priority = (
            ("GVO_OPENAI_MODEL_NAME", "OPENAI_MODEL_NAME", "OUTLINES_MODEL_NAME"),
            "gpt-5-mini",
        )

    for env_var in env_priority[0]:
        value = os.getenv(env_var)
        if value:
            return value.strip()
    return env_priority[1]


def _build_gemini_model(model_name: str) -> Model:
    try:
        genai = importlib.import_module("google.genai")
    except ImportError as exc:  # pragma: no cover - optional dependency
        msg = (
            "Install the 'google-genai' package to use Gemini as the Outlines backend."
        )
        raise RuntimeError(msg) from exc

    try:
        outlines_gemini = importlib.import_module("outlines.models.gemini")
    except ImportError as exc:  # pragma: no cover - optional dependency
        msg = "Update 'outlines' to >= 1.2.7 to enable Gemini support."
        raise RuntimeError(msg) from exc
    api_key = _resolve_gemini_api_key()
    client_kwargs: dict[str, Any] = {"api_key": api_key}

    vertex_mode = os.getenv("GVO_GEMINI_VERTEX_MODE")
    if vertex_mode and vertex_mode.lower() in {"true", "1", "yes", "on"}:
        client_kwargs["vertexai"] = True
        project = os.getenv("GOOGLE_VERTEX_PROJECT") or os.getenv("GOOGLE_PROJECT_ID")
        location = os.getenv("GOOGLE_VERTEX_LOCATION") or os.getenv("GOOGLE_REGION")
        if project:
            client_kwargs["project"] = project
        if location:
            client_kwargs["location"] = location

    client = genai.Client(**client_kwargs)
    return outlines_gemini.from_gemini(client, model_name)


def _resolve_gemini_api_key() -> str:
    for env_var in ("GEMINI_API_KEY", "GOOGLE_API_KEY", "GOOGLE_GENAI_API_KEY"):
        value = os.getenv(env_var)
        if value:
            return value.strip()
    msg = (
        "Set GEMINI_API_KEY (or GOOGLE_API_KEY / GOOGLE_GENAI_API_KEY) "
        "to use Gemini as the Outlines backend."
    )
    raise RuntimeError(msg)


def _build_gemini_inference_defaults() -> dict[str, Any]:
    config: dict[str, Any] = {}
    config["temperature"] = _resolve_temperature(
        default=0.0, env_keys=("GEMINI_TEMPERATURE", "OUTLINES_TEMPERATURE")
    )

    max_tokens = _resolve_int(
        default=1024, env_keys=("GEMINI_MAX_OUTPUT_TOKENS", "OUTLINES_MAX_TOKENS")
    )
    if max_tokens is not None:
        config["max_output_tokens"] = max_tokens

    top_p = os.getenv("GEMINI_TOP_P")
    if top_p is not None:
        config["top_p"] = _resolve_float(top_p, env_var="GEMINI_TOP_P")

    top_k = os.getenv("GEMINI_TOP_K")
    if top_k is not None:
        config["top_k"] = _resolve_int_value(top_k, env_var="GEMINI_TOP_K")

    return config


def _build_openai_model(model_name: str) -> Model:
    try:
        openai_module = importlib.import_module("openai")
    except ImportError as exc:  # pragma: no cover - optional dependency
        msg = "Install the 'openai' package >= 1.0 to use the OpenAI backend."
        raise RuntimeError(msg) from exc

    try:
        outlines_openai = importlib.import_module("outlines.models.openai")
    except ImportError as exc:  # pragma: no cover - optional dependency
        msg = "Install 'outlines' to use the OpenAI backend."
        raise RuntimeError(msg) from exc

    client_kwargs: dict[str, Any] = {}
    base_url = os.getenv("OPENAI_BASE_URL")
    if base_url:
        client_kwargs["base_url"] = base_url.strip()
    organization = os.getenv("OPENAI_ORG_ID")
    if organization:
        client_kwargs["organization"] = organization.strip()
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        client_kwargs["api_key"] = api_key.strip()

    client = openai_module.OpenAI(**client_kwargs)
    return outlines_openai.from_openai(client, model_name)


def _build_openai_inference_defaults() -> dict[str, Any]:
    config: dict[str, Any] = {}
    config["temperature"] = _resolve_temperature(
        default=0.0, env_keys=("OPENAI_TEMPERATURE", "OUTLINES_TEMPERATURE")
    )

    max_tokens = _resolve_int(
        default=512, env_keys=("OPENAI_MAX_TOKENS", "OUTLINES_MAX_TOKENS")
    )
    if max_tokens is not None:
        config["max_tokens"] = max_tokens

    return config


def _resolve_temperature(default: float, env_keys: tuple[str, ...]) -> float:
    for env_var in env_keys:
        value = os.getenv(env_var)
        if value is not None:
            return _resolve_float(value, env_var=env_var)
    return default


def _resolve_int(default: int | None, env_keys: tuple[str, ...]) -> int | None:
    for env_var in env_keys:
        value = os.getenv(env_var)
        if value is not None:
            return _resolve_int_value(value, env_var=env_var)
    return default


def _resolve_float(raw_value: str, *, env_var: str) -> float:
    try:
        return float(raw_value)
    except ValueError as exc:  # pragma: no cover - user configuration issue
        msg = f"Invalid float value '{raw_value}' provided via {env_var}."
        raise RuntimeError(msg) from exc


def _resolve_int_value(raw_value: str, *, env_var: str) -> int:
    try:
        return int(raw_value)
    except ValueError as exc:  # pragma: no cover - user configuration issue
        msg = f"Invalid integer value '{raw_value}' provided via {env_var}."
        raise RuntimeError(msg) from exc
