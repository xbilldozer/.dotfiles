# PROMPT="[%*] %n:%c $(git_prompt_info)%(!.#.$) "
PROMPT='[%{$fg[cyan]%}%*%{$reset_color%}] %{$fg[green]%}%n%{$reset_color%}:%c$(git_prompt_info) %(!.#.$) '

ZSH_THEME_GIT_PROMPT_PREFIX=" %{$fg[yellow]%}("
ZSH_THEME_GIT_PROMPT_SUFFIX=")%{$reset_color%}"
