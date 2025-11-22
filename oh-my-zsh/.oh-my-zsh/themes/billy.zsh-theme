# PROMPT="[%*] %n:%c $(git_prompt_info)%(!.#.$) "
PROMPT='[%{$fg[cyan]%}%*%{$reset_color%}] %{$fg[green]%}%n@%m%{$reset_color%}:%{$fg[yellow]%}%c%{$reset_color%}$(git_prompt_info) %(!.#.$) '

ZSH_THEME_GIT_PROMPT_PREFIX=" ("
ZSH_THEME_GIT_PROMPT_SUFFIX=")"
