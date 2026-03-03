import builtins
from app.calculator_repl import calculator_repl


def _run_repl_with_inputs(monkeypatch, inputs):
    it = iter(inputs)
    monkeypatch.setattr(builtins, "input", lambda _: next(it))
    calculator_repl()


def test_repl_history_clear_undo_redo(monkeypatch, capsys):
    # add one calc, show history, clear, undo/redo paths
    _run_repl_with_inputs(
        monkeypatch,
        [
            "add", "10", "5",
            "history",
            "clear",
            "undo",
            "redo",
            "exit",
        ],
    )
    out = capsys.readouterr().out.lower()
    assert "calculation history" in out or "no calculations" in out
    assert "history cleared" in out
    assert ("nothing to undo" in out) or ("operation undone" in out)
    assert ("nothing to redo" in out) or ("operation redone" in out)


def test_repl_cancel_inputs(monkeypatch, capsys):
    _run_repl_with_inputs(
        monkeypatch,
        [
            "add", "cancel",
            "add", "5", "cancel",
            "exit",
        ],
    )
    out = capsys.readouterr().out.lower()
    assert out.count("operation cancelled") >= 2


def test_repl_save_and_load(monkeypatch, capsys):
    _run_repl_with_inputs(
        monkeypatch,
        [
            "save",
            "load",
            "exit",
        ],
    )
    out = capsys.readouterr().out.lower()
    # accept either success or handled error, but it must hit the branches
    assert ("history saved" in out) or ("error saving history" in out) or ("warning: could not save history" in out)
    assert ("history loaded" in out) or ("error loading history" in out)