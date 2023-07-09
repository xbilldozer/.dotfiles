# dotfiles
Get me up and running bruh.

These are just misc notes for now....

## Pre-requisites

* [Homebrew](https://docs.brew.sh/Installation)
* [iTerm2](https://iterm2.com/downloads.html)
    * [Install monaco nerd-font](https://github.com/Karmenzind/monaco-nerd-fonts)
    ```zsh
    ./scripts/install-font
    ```
    Them follow directions provided by script
    * Install custom kanagawa wave theme
    ```zsh
    ./scripts/install-iterm-theme
    ```
    Then follow directions provided by script
* Neovim
```zsh
brew install neovim
```
* [Install oh-my-zsh](https://ohmyz.sh/#install)
```zsh
brew install stow
```
* tmux + [tmux package manager](https://github.com/tmux-plugins/tpm)
```
brew install tmux
./scripts/install-tmux-tpm
```

## Installation

```zsh
osx
```

Install packer:
```
git clone --depth 1 https://github.com/wbthomason/packer.nvim\
 ~/.local/share/nvim/site/pack/packer/start/packer.nvim
 ```
and then open the packer file
```
nvim ~/.config/nvim/lua/theprimeagen/packer.lua
```
you will get a bunch of errors -- just q through them.
Run `:so %` then `:PackerSync` to download/install all plugins.
Restart nvim and you should see no errors.

## Notes

### neovim

- Uses packer to manage packages
- Treesitter for parsing/syntax highlighting
- Nvimtree replaces netrw, leader+tt to open
- lsp-zero for language severs/autocomplete
    - see `lsp.lua` for default lsps

### Multiple profiles for GitHub

You can set up multiple ssh keys for github by
1. Generating the keys you require
2. Editing ~/.ssh/config to set up profiles for each key
3. Upload the public keys to the github accounts you want to use them with

The config entries look like:
```
Host github.com-username1
  HostName github.com
  User username1
  AddKeysToAgent yes
  IdentityFile ~/.ssh/sshkey1
Host github.com-username2
  HostName github.com
  User username2
  AddKeysToAgent yes
  IdentityFile ~/.ssh/sshkey2
```

#### Troubleshooting

If you forget to check out submodules recursively, you can run this in the top level:
```
git submodule update --init
```
Make sure compiled packer is not present in nvim/plugin/ directory.
`:so %` in lua/packer file and then `:PackerSync`
`:lua ColorMyPencils()` to restore theme and background.
If running into treesitting parsing issues, run `:TSUpdate` to make sure it is up-to-date.
If still having issues, run `:TSInstall! <lang>` and restart neovim.

### tmux

- Prefix remapped to `<C-Space>`
- Uses tpm to manage plugins
Once tmux is opened, run `prefix + I` to install packages
- tmux-resurrect and tmux-continuum for those times IT auto-installs osx updates

