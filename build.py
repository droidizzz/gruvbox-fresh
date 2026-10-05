#!/usr/bin/env python3
"""Generate Gruvbox themes for the Fresh terminal editor.

Palette and highlight-group mapping follow morhetz/gruvbox (gruvbox.vim):
  https://github.com/morhetz/gruvbox
Six variants: dark/light x hard/medium/soft, matching g:gruvbox_contrast_*.
Run `python3 build.py` to regenerate themes/*.json.
"""
import json
from pathlib import Path


def hx(h):
    h = h.lstrip("#")
    return [int(h[i:i + 2], 16) for i in (0, 2, 4)]


def blend(fg, bg, a):
    """Mix `a` of fg over bg (used for tinted diff/diagnostic backgrounds)."""
    return [round(f * a + b * (1 - a)) for f, b in zip(fg, bg)]


# ---- morhetz/gruvbox palette -------------------------------------------------
P = {k: hx(v) for k, v in {
    "dark0_hard": "#1d2021", "dark0": "#282828", "dark0_soft": "#32302f",
    "dark1": "#3c3836", "dark2": "#504945", "dark3": "#665c54", "dark4": "#7c6f64",
    "gray": "#928374",
    "light0_hard": "#f9f5d7", "light0": "#fbf1c7", "light0_soft": "#f2e5bc",
    "light1": "#ebdbb2", "light2": "#d5c4a1", "light3": "#bdae93", "light4": "#a89984",
    "bright_red": "#fb4934", "bright_green": "#b8bb26", "bright_yellow": "#fabd2f",
    "bright_blue": "#83a598", "bright_purple": "#d3869b", "bright_aqua": "#8ec07c",
    "bright_orange": "#fe8019",
    "neutral_red": "#cc241d", "neutral_green": "#98971a", "neutral_yellow": "#d79921",
    "neutral_blue": "#458588", "neutral_purple": "#b16286", "neutral_aqua": "#689d6a",
    "neutral_orange": "#d65d0e",
    "faded_red": "#9d0006", "faded_green": "#79740e", "faded_yellow": "#b57614",
    "faded_blue": "#076678", "faded_purple": "#8f3f71", "faded_aqua": "#427b58",
    "faded_orange": "#af3a03",
}.items()}

ACCENTS = ["red", "green", "yellow", "blue", "purple", "aqua", "orange"]


def scheme(mode, contrast):
    """Resolve gruvbox.vim's semantic names (bg0..bg4, fg0..fg4, accents)."""
    dark = mode == "dark"
    sfx = {"hard": "_hard", "medium": "", "soft": "_soft"}[contrast]
    if dark:
        c = dict(bg0=P["dark0" + sfx], bg1=P["dark1"], bg2=P["dark2"], bg3=P["dark3"],
                 bg4=P["dark4"], fg0=P["light0"], fg1=P["light1"], fg2=P["light2"],
                 fg3=P["light3"], fg4=P["light4"])
        acc = "bright"
    else:
        c = dict(bg0=P["light0" + sfx], bg1=P["light1"], bg2=P["light2"], bg3=P["light3"],
                 bg4=P["light4"], fg0=P["dark0"], fg1=P["dark1"], fg2=P["dark2"],
                 fg3=P["dark3"], fg4=P["dark4"])
        acc = "faded"
    c["gray"] = P["gray"]
    for a in ACCENTS:
        c[a] = P[f"{acc}_{a}"]          # foreground accents (vim: s:red, s:green, ...)
        c["n_" + a] = P[f"neutral_{a}"]  # neutral accents (hover states)
    return c


def build(mode, contrast):
    c = scheme(mode, contrast)
    dark = mode == "dark"
    bg0 = c["bg0"]
    tint = lambda col, a: blend(c[col], bg0, a)
    # Beyond-EOF / compose margin: one step outside the page.
    eof = blend([0, 0, 0], bg0, 0.30) if dark else c["bg1"]
    rainbow = [c[k] for k in ("blue", "yellow", "purple", "aqua", "orange", "green")]

    editor = {
        "bg": bg0,
        "fg": c["fg1"],                      # Normal
        "cursor": c["fg1"],                  # Cursor (reverse of Normal)
        "inactive_cursor": c["bg4"],
        "selection_bg": c["bg3"],            # Visual
        "current_line_bg": c["bg1"],         # CursorLine
        "line_number_fg": c["bg4"],          # LineNr
        "line_number_bg": bg0,
        "diff_add_bg": tint("green", 0.15),       # DiffAdd
        "diff_remove_bg": tint("red", 0.15),      # DiffDelete
        "diff_add_highlight_bg": tint("green", 0.30),
        "diff_remove_highlight_bg": tint("red", 0.30),
        "diff_modify_bg": tint("aqua", 0.15),     # DiffChange
        "diff_add_collision_fg": c["fg0"],
        "diff_remove_collision_fg": c["fg0"],
        "diff_modify_collision_fg": c["fg0"],
        "ruler_bg": c["bg1"],                # ColorColumn
        "indentation_guide_fg": c["bg2"],
        "whitespace_indicator_fg": c["bg2"],           # NonText / SpecialKey
        "whitespace_indicator_selected_fg": c["fg4"],  # stays visible on Visual (bg3)
        "bracket_match_fg": c["orange"],
        "bracket_rainbow_match_modifier": ["bold"],    # MatchParen is bold
        "after_eof_bg": eof,
    }
    for i, col in enumerate(rainbow, 1):
        editor[f"indent_rainbow_{i}"] = col
        editor[f"bracket_rainbow_{i}"] = col

    on_accent = bg0  # text drawn on top of an accent-colored fill
    ui = {
        # TabLine / TabLineSel (green on the selected tab)
        "tab_active_fg": c["green"], "tab_active_bg": c["bg2"],
        "tab_inactive_fg": c["fg4"], "tab_inactive_bg": c["bg1"],
        "tab_separator_bg": bg0, "tab_hover_bg": c["bg3"],
        "tab_close_hover_fg": c["red"],
        # Menu bar + dropdowns (Pmenu = fg1 on bg2, PmenuSel = bg2 on blue)
        "menu_bg": c["bg1"], "menu_fg": c["fg1"],
        "menu_active_bg": c["bg2"], "menu_active_fg": c["yellow"],
        "menu_dropdown_bg": c["bg2"], "menu_dropdown_fg": c["fg1"],
        "menu_highlight_bg": c["blue"], "menu_highlight_fg": c["bg2"],
        "menu_hover_bg": c["bg3"], "menu_hover_fg": c["fg0"],
        "menu_border_fg": c["bg4"], "menu_separator_fg": c["bg3"],
        "menu_disabled_fg": c["gray"], "menu_disabled_bg": c["bg2"],
        # StatusLine (fg1 on bg2); palette hint uses the signature yellow
        "status_bar_fg": c["fg1"], "status_bar_bg": c["bg2"],
        "status_palette_fg": on_accent, "status_palette_bg": c["yellow"],
        "status_separator_fg": c["bg4"], "status_separator_bg": c["bg2"],
        "status_lsp_on_fg": on_accent, "status_lsp_on_bg": c["aqua"],
        "status_lsp_actionable_fg": on_accent, "status_lsp_actionable_bg": c["orange"],
        "status_warning_indicator_fg": on_accent, "status_warning_indicator_bg": c["yellow"],
        "status_warning_indicator_hover_fg": on_accent,
        "status_warning_indicator_hover_bg": c["n_yellow"],
        "status_error_indicator_fg": on_accent, "status_error_indicator_bg": c["red"],
        "status_error_indicator_hover_fg": on_accent,
        "status_error_indicator_hover_bg": c["n_red"],
        # Prompt / command line
        "prompt_fg": c["fg1"], "prompt_bg": c["bg1"],
        "prompt_selection_fg": c["fg0"], "prompt_selection_bg": c["bg3"],
        # Popups & completion
        "popup_bg": c["bg2"], "popup_text_fg": c["fg1"], "popup_border_fg": c["bg4"],
        "popup_selection_bg": c["blue"], "popup_selection_fg": c["bg2"],
        "suggestion_bg": c["bg2"], "suggestion_fg": c["fg1"],
        "suggestion_selected_bg": c["bg3"],
        "text_input_selection_bg": c["bg3"],
        "list_drop_target_bg": tint("blue", 0.35),
        # Help
        "help_bg": bg0, "help_fg": c["fg1"], "help_key_fg": c["aqua"],
        "help_separator_fg": c["gray"],
        "help_indicator_fg": c["red"], "help_indicator_bg": bg0,
        "inline_code_bg": c["bg1"],
        # Splits (VertSplit = bg3) & scrollbars
        "split_separator_fg": c["bg3"], "split_separator_hover_fg": c["yellow"],
        "scrollbar_track_fg": c["bg1"], "scrollbar_thumb_fg": c["bg3"],
        "scrollbar_track_hover_fg": c["bg2"], "scrollbar_thumb_hover_fg": c["bg4"],
        "compose_margin_bg": eof,
        # Git blame header band
        "blame_header_fg": c["fg0"] if dark else c["bg0"],
        "blame_header_bg": c["bg3"] if dark else c["fg3"],
        # Occurrence highlight: a warm yellow tint (dark) / muted blue (light).
        # Alphas are tuned so the tint stays >=20 luma away from both the
        # editor bg and the Visual selection, in truecolor and 256-color.
        "semantic_highlight_bg": (
            tint("yellow", {"hard": 0.18, "medium": 0.17, "soft": 0.14}[contrast])
            if dark else c["bg2"]),
        "tour_step_bg": c["bg2"],
        "terminal_bg": bg0, "terminal_fg": c["fg1"],
        "tab_drop_zone_bg": c["bg3"], "tab_drop_zone_border": c["yellow"],
        "settings_selected_bg": c["bg3"], "settings_selected_fg": c["fg0"],
        # File explorer git status
        "file_status_added_fg": c["green"], "file_status_modified_fg": c["yellow"],
        "file_status_deleted_fg": c["red"], "file_status_renamed_fg": c["aqua"],
        "file_status_untracked_fg": c["gray"], "file_status_conflicted_fg": c["purple"],
    }

    search = {
        "match_bg": c["yellow"], "match_fg": on_accent,              # Search
        "current_match_bg": c["orange"],                              # IncSearch
        "current_match_fg": {"color": on_accent, "modifier": ["bold"]},
        "label_bg": c["purple"], "label_fg": on_accent,
    }

    diagnostic = {}
    for kind, col in (("error", "red"), ("warning", "yellow"), ("info", "blue"), ("hint", "aqua")):
        diagnostic[f"{kind}_fg"] = c[col]
        diagnostic[f"{kind}_bg"] = tint(col, 0.12 if dark else 0.10)

    syntax = {
        "keyword": c["red"],                                           # Statement/Keyword
        "string": c["green"],                                          # String
        "comment": {"color": c["gray"], "modifier": ["italic"]},       # Comment
        "function": {"color": c["green"], "modifier": ["bold"]},       # Function
        "type": c["yellow"],                                           # Type
        "variable": c["fg1"],
        "variable_builtin": c["orange"],
        "constant": c["purple"],                                       # Constant/Number/Boolean
        "operator": c["orange"],
        "punctuation_bracket": c["fg2"],
        "punctuation_delimiter": c["fg3"],
    }

    return {
        "name": f"gruvbox-{mode}-{contrast}",
        "editor": editor, "ui": ui, "search": search,
        "diagnostic": diagnostic, "syntax": syntax,
    }


def dump(obj):
    """Pretty JSON with [r, g, b] arrays kept on one line."""
    s = json.dumps(obj, indent=2)
    import re
    return re.sub(r"\[\s+(\d+),\s+(\d+),\s+(\d+)\s+\]", r"[\1, \2, \3]",
                  re.sub(r'\[\s+("[a-z]+")\s+\]', r"[\1]", s)) + "\n"


if __name__ == "__main__":
    root = Path(__file__).parent
    out = root / "themes"
    out.mkdir(exist_ok=True)
    entries = []
    for mode in ("dark", "light"):
        for contrast in ("hard", "medium", "soft"):
            t = build(mode, contrast)
            (out / f"{t['name']}.json").write_text(dump(t))
            entries.append({"file": f"themes/{t['name']}.json",
                            "name": f"Gruvbox {mode.title()} ({contrast})",
                            "variant": mode})
    manifest = {
        "name": "gruvbox-fresh",
        "version": "1.0.0",
        "description": "Retro groove color scheme (morhetz/gruvbox) for Fresh: dark & light, hard/medium/soft contrast",
        "type": "theme-pack",
        "fresh": {"themes": entries},
        "license": "MIT",
        "keywords": ["gruvbox", "retro", "dark", "light", "theme"],
    }
    (root / "package.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print("wrote", len(entries), "themes")
