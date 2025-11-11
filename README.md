# dotfiles
Get me up and running bruh.

These are just misc notes for now....

## Pre-requisites

* Xcode Command Line Tools
Required for git and other tools to work correctly

```zsh
xcode-select --install
```

* [Homebrew](https://docs.brew.sh/Installation)
* [iTerm2](https://iterm2.com/downloads.html)
    * [Install monaco nerd-font](https://github.com/Karmenzind/monaco-nerd-fonts)

    ```zsh
    ./scripts/install-font
    ```
    Then follow directions provided by script

    * Install custom kanagawa wave theme

    ```zsh
    ./scripts/install-iterm-theme
    ```
    Then follow directions provided by script

    * Set up background image rotation script
* [mise tool manager](https://mise.jdx.dev/getting-started.html)
    * Install the tool manager:
        ```zsh
        brew install mise
        ```
    * Install plugin dependencies:
        ```zsh
        brew install libyaml
        ```
    * Install plugins
        ```zsh
        mise install
        ```
    * Make sure all versions are set so that nvim lsp-zero will install lsps as desired!

* Neovim

```zsh
brew install neovim
```

* [Install oh-my-zsh](https://ohmyz.sh/#install)

```zsh
brew install stow
```

* tmux + [fzf](https://github.com/junegunn/fzf) + [tmux package manager](https://github.com/tmux-plugins/tpm)

```zsh
brew install tmux fzf
./scripts/install-tmux-tpm
```

* AWS CLI

```zsh
brew install awscli
```

## Installation

### Install dotfiles

Clone this repo and cd into it, ensure that you have cloned the submodules:

```zsh
git submodule update --init
```

Run the osx script to stow the dotfiles:

```zsh
osx
```

### Setup neovim
Open neovim and allow it to install packer and all plugins.

```zsh
nvim ~/.config/nvim/lua/theprimeagen/packer.lua
```
you will see errors when neovim opens for the first time -- `G` and then `Enter` to continue and install plugins.

Restart neovim and allow it to install lsp-zero and all lsps. If you see errors here, review them with `:MasonLog` and take appropriate action.
Usually, you have forgotten to set default versions of asdf plugins. You can do this by running `asdf global <plugin> <version>`.

### Setup Github Copilot
In neovim, run:

```
:Copilot setup
```

Then follow the instructions to authenticate.

## Notes

### Git

oh-my-zsh uses less pager and the default setting doesn't leave output in the cli -- I like the output because
1. sometimes quit prematurely and then have to run the cmd multiple times
2. sometimes I want to go back and look at the diff later and don't want to craft a special diff with hashes or HEAD~n

```zsh
git config --global core.pager "less -RFX"
```

Other great options to make git work for you (already pre-configured in the .gitconfig):

```zsh
# Sort branches by most recently used
git config --global branch.sort -committerdate

# Sort tags with major.minor.patch more intelligently
git config --global tag.sort version:refname

# iykyk
git config --global init.defaultBranch main

# Makes diff easier to read
git config --global diff.algorithm histogram

# Automatically create the upstream branch on first push
git config --global push.autoSetupRemote true
```

### neovim information

- Uses packer to manage packages
- Treesitter for parsing/syntax highlighting
- lsp-zero for language severs/autocomplete
    - see `after/lsp.lua` for default lsps

### tmux information

- Prefix remapped to `<C-Space>`
- Uses tpm to manage plugins
Once tmux is opened, run `prefix + I` to install packages
- tmux-resurrect and tmux-continuum for those times IT auto-installs osx updates

### Multiple profiles for GitHub

You can set up multiple ssh keys for github by
1. Generate the keys you require. [Github instructions](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)
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

You may need to start the ssh-agent and add the keys:
```zsh
eval "$(ssh-agent -s)"
```

Add your key to the agent:
```zsh
ssh-add --apple-use-keychain ~/.ssh/id_ed25519
```

### Troubleshooting

#### Packer issues

Make sure compiled packer is not present in nvim/plugin/ directory.
`:so %` in lua/packer file and then `:PackerSync`
`:lua ColorMyPencils()` to restore theme and background.

If running into treesitting parsing issues, run `:TSUpdate` to make sure it is up-to-date.

If still having issues, run `:TSInstall! <lang>` and restart neovim.

