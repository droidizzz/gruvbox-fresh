# Gruvbox for Fresh

The [gruvbox](https://github.com/morhetz/gruvbox) retro-groove color scheme for the
[Fresh](https://getfresh.dev) terminal editor, in all six of gruvbox's variants:

| Theme | Background |
| --- | --- |
| `gruvbox-dark-hard` | `#1d2021` |
| `gruvbox-dark-medium` | `#282828` |
| `gruvbox-dark-soft` | `#32302f` |
| `gruvbox-light-hard` | `#f9f5d7` |
| `gruvbox-light-medium` | `#fbf1c7` |
| `gruvbox-light-soft` | `#f2e5bc` |

Dark variants use gruvbox's *bright* accents, light variants its *faded* accents,
exactly as `gruvbox.vim` does.

## Install

```sh
mkdir -p ~/.config/fresh/themes
cp themes/*.json ~/.config/fresh/themes/
```

Then pick one with `Ctrl+P` → **Select Theme**, or set it in `~/.config/fresh/config.json`:

```json
{ "theme": "gruvbox-dark-medium.json" }
```

`package.json` is a Fresh `theme-pack` manifest, so the folder can also be published
as a git repo and referenced by URL (`"theme": "https://github.com/<you>/gruvbox-fresh#gruvbox-dark-hard"`).

## How colors map

Mapped from gruvbox.vim's highlight groups rather than eyeballed:

| Fresh | gruvbox.vim | Color |
| --- | --- | --- |
| `syntax.keyword` | Keyword / Statement | red |
| `syntax.string` | String | green |
| `syntax.function` | Function | green, **bold** |
| `syntax.type` | Type | yellow |
| `syntax.constant` | Constant / Number / Boolean | purple |
| `syntax.comment` | Comment | gray, *italic* |
| `syntax.operator`, `variable_builtin` | (gruvbox.nvim) | orange |
| `editor.selection_bg` | Visual | bg3 |
| `editor.current_line_bg`, `ruler_bg` | CursorLine, ColorColumn | bg1 |
| `editor.line_number_fg` | LineNr | bg4 |
| `ui.status_bar_*` | StatusLine | fg1 on bg2 |
| `ui.popup_*`, `menu_highlight_*` | Pmenu / PmenuSel | fg1 on bg2 / bg2 on blue |
| `ui.tab_active_fg` | TabLineSel | green |
| `ui.split_separator_fg` | VertSplit | bg3 |
| `search.match_*` | Search | yellow, reversed |
| `search.current_match_*` | IncSearch | orange, reversed |
| diagnostics | error / warning / info / hint | red / yellow / blue / aqua |

## Customizing

Edit `build.py` and run `python3 build.py` to regenerate every variant at once,
or tweak a single JSON with Fresh's built-in **Edit Theme** command.

## Tested

All six files validate against Fresh's `theme.schema.json` and were run through
Fresh's own built-in-theme test suite (required keys, blame-header contrast,
visible selection indicators, occurrence-highlight visibility and syntax legibility).
The dark variants pass everything. The light variants pass everything in truecolor;
on 256-color-only terminals the occurrence highlight sits close to the selection,
because gruvbox's cream background and its `bg3` selection quantize to neighbouring
palette entries.
