"""Chat-template rendering for the major open-source model families.

The conversations are stored model-agnostically (``messages``, the format
Axolotl/LLaMA-Factory/TRL all accept). These renderers additionally write a
pre-formatted ``text`` field for trainers that expect raw strings.

The built-in templates avoid a tokenizer download; when you need byte-exact
fidelity, pass ``hf:<model_id>`` to render with the model's own
``chat_template`` from ``transformers`` instead.
"""

from __future__ import annotations

import logging
from typing import Callable, Iterable, Sequence

logger = logging.getLogger(__name__)

Message = dict[str, str]


def render_chatml(messages: Sequence[Message], add_generation_prompt: bool = False) -> str:
    """ChatML, as used by Qwen (Qwen2/2.5/3) and many fine-tunes."""
    parts = [f"<|im_start|>{m['role']}\n{m['content']}<|im_end|>\n" for m in messages]
    if add_generation_prompt:
        parts.append("<|im_start|>assistant\n")
    return "".join(parts)


def render_qwen(messages: Sequence[Message], add_generation_prompt: bool = False) -> str:
    if not messages or messages[0]["role"] != "system":
        messages = [{"role": "system", "content": "You are a helpful assistant."}, *messages]
    return render_chatml(messages, add_generation_prompt)


def render_llama3(messages: Sequence[Message], add_generation_prompt: bool = False) -> str:
    """Llama 3 / 3.1 / 3.2 instruct format."""
    parts = ["<|begin_of_text|>"]
    for message in messages:
        parts.append(
            f"<|start_header_id|>{message['role']}<|end_header_id|>\n\n{message['content'].strip()}<|eot_id|>"
        )
    if add_generation_prompt:
        parts.append("<|start_header_id|>assistant<|end_header_id|>\n\n")
    return "".join(parts)


def render_deepseek(messages: Sequence[Message], add_generation_prompt: bool = False) -> str:
    """DeepSeek LLM / V2 / V3 chat format."""
    parts: list[str] = ["<｜begin▁of▁sentence｜>"]
    for message in messages:
        role = message["role"]
        content = message["content"].strip()
        if role == "system":
            parts.append(f"{content}\n\n")
        elif role == "user":
            parts.append(f"User: {content}\n\n")
        else:
            parts.append(f"Assistant: {content}<｜end▁of▁sentence｜>")
    if add_generation_prompt:
        parts.append("Assistant:")
    return "".join(parts)


BUILTIN_TEMPLATES: dict[str, Callable[..., str]] = {
    "chatml": render_chatml,
    "qwen": render_qwen,
    "llama3": render_llama3,
    "deepseek": render_deepseek,
}


class HfChatTemplate:
    """Renders with a model's own ``chat_template`` (needs the tokenizer)."""

    def __init__(self, model_id: str) -> None:
        from transformers import AutoTokenizer

        self.model_id = model_id
        self._tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=False)

    def __call__(self, messages: Sequence[Message], add_generation_prompt: bool = False) -> str:
        return self._tokenizer.apply_chat_template(
            list(messages), tokenize=False, add_generation_prompt=add_generation_prompt
        )


def get_renderer(name: str) -> Callable[..., str]:
    """``"qwen"`` -> built-in renderer; ``"hf:<model_id>"`` -> tokenizer template."""
    if name.startswith("hf:"):
        return HfChatTemplate(name[3:])
    try:
        return BUILTIN_TEMPLATES[name]
    except KeyError as exc:
        raise ValueError(
            f"unknown chat template '{name}'; available: {', '.join(BUILTIN_TEMPLATES)} or hf:<model_id>"
        ) from exc
