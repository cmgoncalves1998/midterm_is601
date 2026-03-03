import builtins
import pytest

import app.calculator_repl as repl


def test_repl_keyboard_interrupt(monkeypatch, capsys):
    # first input raises Ctrl+C, second exits
    calls = iter([KeyboardInterrupt(), "exit"])

    def fake_input(_prompt):
        v = next(calls)
        if isinstance(v, BaseException):
            raise v
        return v

    monkeypatch.setattr(builtins, "input", fake_input)

    repl.calculator_repl()

    out = capsys.readouterr().out.lower()
    assert "operation cancelled" in out
    assert "goodbye" in out


def test_repl_eof_exits(monkeypatch, capsys):
    def fake_input(_prompt):
        raise EOFError()

    monkeypatch.setattr(builtins, "input", fake_input)

    repl.calculator_repl()

    out = capsys.readouterr().out.lower()
    assert "exiting" in out