#!/usr/bin/env zsh

stow_install() {
  package_dir=$1
  target_dir=$2
  packages=$3

  if [[ -z $package_dir ]]; then
    echo "Must set package_dir as the base directory for the packages you want to install"  
    return 1
  fi
  if [[ -z $target_dir ]]; then
    echo "Must set target_dir as the directory into which you wish to install your pacakges (usually your home directory)"  
    return 1
  fi
  if [[ -z $packages ]]; then
    echo "Must provide packages as comma-delimited list of packages to install"  
    return 1
  fi

  all_succeeded=true
  pushd $package_dir
  for folder in $(echo $packages | sed "s/,/ /g")
  do
      if ! stow -t $target_dir -R $folder; then
        echo "FAILED: stowing package $package_dir/$folder" >&2
        all_succeeded=false
      fi
  done
  popd

  if $all_succeeded; then
    return 0
  else
    return 1
  fi
}
