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
* [asdf version manager](https://asdf-vm.com/guide/getting-started.html)
    * Install plugins
        * [Install ruby](https://github.com/asdf-vm/asdf-ruby) please read migration guide!!
        * [Install python](https://github.com/asdf-community/asdf-python)
        * [Install java](https://github.com/halcyon/asdf-java)
        * [Install nodejs](https://github.com/asdf-vm/asdf-nodejs)
        * [Complete list of plugins](https://github.com/asdf-vm/asdf-plugins?tab=readme-ov-file)
    * [Install versions](https://asdf-vm.com/manage/versions.html)
* Neovim
```zsh
brew install neovim
```
* [Install oh-my-zsh](https://ohmyz.sh/#install)
```zsh
brew install stow
```
* tmux + [fzf](https://github.com/junegunn/fzf) + [tmux package manager](https://github.com/tmux-plugins/tpm)
```
brew install tmux fzf
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

### Git

oh-my-zsh uses less pager and the default setting doesn't leave output in the cli -- I like the output because
1. sometimes quit prematurely and then have to run the cmd multiple times
2. sometimes I want to go back and look at the diff later and don't want to craft a special diff with hashes or HEAD~n

```
git config --global core.pager "less -RFX"
```

### neovim

- Uses packer to manage packages
- Treesitter for parsing/syntax highlighting
- Nvimtree replaces netrw, leader+tt to open
- lsp-zero for language severs/autocomplete
    - see `lsp.lua` for default lsps

### Multiple profiles for GitHub

You can set up multiple ssh keys for github by
1. Generate the keys you require
2. Edit ~/.ssh/config to set up profiles for each key
3. Upload the public keys to the github accounts you want to use them with
4. Enable ssh-agent and add the keys
5. When you clone, ensure you are using the ssh aliases you set up

The config entries will look something like:
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
