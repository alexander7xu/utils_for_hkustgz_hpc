#! bash oh-my-bash.module

# This theme is based on cupcake theme
# https://github.com/ohmybash/oh-my-bash/blob/master/themes/cupcake/cupcake.theme.sh

# virtualenv prompts
VIRTUALENV_CHAR="ⓔ "
OMB_PROMPT_CONDAENV_FORMAT='%s'
OMB_PROMPT_SHOW_PYTHON_VENV=${OMB_PROMPT_SHOW_PYTHON_VENV:=true}

# SCM prompts
SCM_NONE_CHAR=""
SCM_GIT_CHAR="[±] "
SCM_GIT_BEHIND_CHAR="${_omb_prompt_brown}↓${_omb_prompt_normal}"
SCM_GIT_AHEAD_CHAR="${_omb_prompt_bold_green}↑${_omb_prompt_normal}"
SCM_GIT_UNTRACKED_CHAR="⌀"
SCM_GIT_UNSTAGED_CHAR="${_omb_prompt_bold_olive}•${_omb_prompt_normal}"
SCM_GIT_STAGED_CHAR="${_omb_prompt_bold_green}+${_omb_prompt_normal}"

SCM_THEME_PROMPT_DIRTY=""
SCM_THEME_PROMPT_CLEAN=""
SCM_THEME_PROMPT_PREFIX=""
SCM_THEME_PROMPT_SUFFIX=""

# Git status prompts
GIT_THEME_PROMPT_DIRTY=" ${_omb_prompt_brown}✗${_omb_prompt_normal}"
GIT_THEME_PROMPT_CLEAN=" ${_omb_prompt_bold_green}✓${_omb_prompt_normal}"
GIT_THEME_PROMPT_PREFIX=""
GIT_THEME_PROMPT_SUFFIX=""

# ICONS =======================================================================

icon_start="┌─ "
icon_user=" 🤖 "
icon_directory=" 📁 "
icon_end="\n└❯ "

match_hostname=$(grep -r $(hostname) /hpc2ssd/JH_DATA/spooler/hlin199/*)
if [ "$match_hostname" == "" ]; then
  host="$(hostname)"
else
  filename=${match_hostname%%:*}
  lastline=$(tail -n 1 ${filename})
  jobid=${lastline%%[*}
  create_date=${lastline#*INFO }
  create_date=${create_date%% *}
  create_date=${create_date:5}
  name=$(ls ${match_hostname%%output*})
  name=${name%%.hcl*}
  host="$name($create_date-$jobid)"
fi

# extra spaces ensure legiblity in prompt

# FUNCTIONS ===================================================================

# Rename tab
function tabname {
  printf "\e]1;$1\a"
}

# Rename window
function winname {
  printf "\e]2;$1\a"
}

# PROMPT OUTPUT ===============================================================

# Displays the current prompt
function _omb_theme_PROMPT_COMMAND() {
  if [ "$(condaenv_prompt)" == "" ]; then
    conda_env=''
  else
    conda_env=" 🐍 ${_omb_prompt_bold_purple}$(condaenv_prompt)${_omb_prompt_normal}"
  fi

  PS1="\n${icon_start}${_omb_prompt_bold_red}\u${icon_user}${_omb_prompt_normal}${_omb_prompt_bold_blue}${host}${_omb_prompt_normal}${conda_env}${icon_directory}${_omb_prompt_bold_yellow}\w${_omb_prompt_normal} $(scm_prompt_info)${_omb_prompt_normal}${icon_end}"
  PS2="${icon_end}"
}

# Runs prompt (this bypasses oh-my-bash $PROMPT setting)
_omb_util_add_prompt_command _omb_theme_PROMPT_COMMAND