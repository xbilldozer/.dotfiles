# dotfiles
Get me up and running bruh.

These are just misc notes for now....


## Pre-requisites

* [Homebrew](https://docs.brew.sh/Installation)
* Neovim
```zsh
brew install neovim
```
* [Install oh-my-zsh](https://ohmyz.sh/#install)

```zsh
brew install stow
```


## neovim

Troubleshooting

Make sure compiled packer is not present in nvim/plugin/ directory.
`:so %` in lua/packer file and then `:PackerSync`
`:lua ColorMyPencils()` to restore theme and background.
If running into treesitting parsing issues, run `:TSUpdate` to make sure it is up-to-date.
If still having issues, run `:TSInstall! <lang>` and restart neovim.
