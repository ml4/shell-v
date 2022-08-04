#!/usr/bin/env bash
#
## hc-vault-recursive-namespace-list.sh - Recursive list of Vault Enterprise namespaces
#
## usage: hc-vault-recursive-namespace-list.sh [starting_location]
#
## HashiCorp best practice is to use namespaces sparingly. See and follow:
##   https://learn.hashicorp.com/tutorials/vault/namespace-structure?in=vault/enterpris
#
#########################################################################################

function list_namespace {
  entry_point=$(echo ${1} | sed 's/\/$//')
  echo "${entry_point}"

  ## first, check if root ns, and if so collect children slightly differently due to path specification
  #
  if [[ "${entry_point}" == "root" ]]
  then
    child_namespaces=$(vault namespace list -format=json | jq -r .[] | tr '\012' ' ' | tr -d '/')
    entry_point=
  else
    child_namespaces=$(vault namespace list -namespace ${entry_point} -format=json | jq -r .[] | tr '\012' ' ')
    child_namespaces=$(echo ${child_namespaces} | sed 's/ $//')
    if [[ -n ${child_namespaces} ]]
    then
      child_namespaces=$(echo ${child_namespaces} | sed -e "s~^~${entry_point}/~" -e "s~ ~ ${entry_point}/~")
    fi
  fi

  ## iterate found child namespaces
  #
  if [[ -n ${child_namespaces} ]]
  then
    for namespace in $(echo ${child_namespaces})
    do
      list_namespace "${namespace}"
    done
  fi
}

if [[ -z "${1}" ]]
then
  list_namespace root
else
  list_namespace ${1}
fi

