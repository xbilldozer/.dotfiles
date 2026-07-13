1. From iTerm, Scripts > Manage > Import...
2. Select each script below
3. Scripts > (script name) -- if not installed, iTerm will prompt you to install the python runtime. Select Yes
4. You will be prompted to enable the Python API -- select Allow.
5. Ensure that you have wallpapers in the wallpaper directory. Default is ~/src/wallpapers/**/*

To configure blending scripts, you must set keybindings for all three functions. Suggest:

cmd + option + - for blend_less
cmd + option + = for blend_more
cmd + option + 0 for blend_reset.

Provide `id` as the session id -- it's a magic variable.

## Location

Scripts location is something like:

```
cd $HOME/Library/Application\ Support/iTerm2/Scripts/
```

## Troubleshooting

If the background flickers or half-renders, turn off Settings > Magic > Enable GPU rendering
