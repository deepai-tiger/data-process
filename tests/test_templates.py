"""Chat-template rendering for the target model families."""

from __future__ import annotations

import pytest

from kdp.dataset.templates import (
    BUILTIN_TEMPLATES,
    get_renderer,
    render_chatml,
    render_deepseek,
    render_llama3,
    render_qwen,
)

MESSAGES = [
    {"role": "system", "content": "당신은 유용한 조수입니다."},
    {"role": "user", "content": "제곱근을 LaTeX로 쓰시오."},
    {"role": "assistant", "content": r"\sqrt{x}"},
]


def test_chatml_wraps_every_turn():
    rendered = render_chatml(MESSAGES)
    assert rendered.count("<|im_start|>") == 3
    assert rendered.count("<|im_end|>") == 3
    assert "<|im_start|>user\n제곱근을 LaTeX로 쓰시오.<|im_end|>" in rendered


def test_chatml_generation_prompt_opens_an_unclosed_assistant_turn():
    rendered = render_chatml(MESSAGES[:2], add_generation_prompt=True)
    assert rendered.endswith("<|im_start|>assistant\n")
    assert rendered.count("<|im_start|>") == rendered.count("<|im_end|>") + 1


def test_qwen_inserts_a_default_system_turn_when_none_is_given():
    rendered = render_qwen(MESSAGES[1:])
    assert rendered.startswith("<|im_start|>system\nYou are a helpful assistant.<|im_end|>")


def test_qwen_keeps_an_explicit_system_turn():
    assert render_qwen(MESSAGES).startswith("<|im_start|>system\n당신은 유용한 조수입니다.<|im_end|>")


def test_llama3_uses_header_and_eot_tokens():
    rendered = render_llama3(MESSAGES)
    assert rendered.startswith("<|begin_of_text|>")
    assert "<|start_header_id|>user<|end_header_id|>\n\n제곱근을 LaTeX로 쓰시오.<|eot_id|>" in rendered
    assert rendered.count("<|eot_id|>") == 3


def test_llama3_generation_prompt_ends_with_an_open_assistant_header():
    rendered = render_llama3(MESSAGES[:2], add_generation_prompt=True)
    assert rendered.endswith("<|start_header_id|>assistant<|end_header_id|>\n\n")


def test_deepseek_uses_its_sentence_markers_and_role_prefixes():
    rendered = render_deepseek(MESSAGES)
    assert rendered.startswith("<｜begin▁of▁sentence｜>당신은 유용한 조수입니다.\n\n")
    assert "User: 제곱근을 LaTeX로 쓰시오.\n\n" in rendered
    assert rendered.endswith(r"Assistant: \sqrt{x}<｜end▁of▁sentence｜>")


def test_deepseek_generation_prompt_ends_with_the_assistant_cue():
    assert render_deepseek(MESSAGES[:2], add_generation_prompt=True).endswith("Assistant:")


@pytest.mark.parametrize("name", sorted(BUILTIN_TEMPLATES))
def test_every_builtin_template_preserves_the_content(name):
    rendered = get_renderer(name)(MESSAGES)
    assert "제곱근을 LaTeX로 쓰시오." in rendered
    assert r"\sqrt{x}" in rendered


def test_an_unknown_template_name_is_rejected_with_the_available_ones():
    with pytest.raises(ValueError, match="qwen"):
        get_renderer("gpt9")


def test_multiline_latex_survives_rendering():
    messages = [{"role": "assistant", "content": "$$\n\\begin{aligned}\na &= b\n\\end{aligned}\n$$"}]
    assert "\\begin{aligned}" in render_chatml(messages)
