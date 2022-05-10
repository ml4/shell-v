#!/usr/bin/env python3
#
## hc-vault-probe.sh
## 2022-04-26 ml4
## Automate the outputting of useful information about a Vault Enterprise instance.
## NOTE: this software is provided AS-IS. No warrantee exists with this software.  Read and understand the code
## prior to running, and run in non-production prior to then running in production.
#
#######################################################################################################################

import argparse
import os
import requests
import json

#import subprocess
#import re
#import random
#import signal
#import datetime
#import sys
#import glob

############################################################################
#
#   Globals
#
############################################################################

QUIET = False
VAULT_ADDR = os.getenv('VAULT_ADDR')
VAULT_TOKEN = os.getenv('VAULT_TOKEN')
VAULT_CACERT = os.getenv('VAULT_CACERT')
rows, columns = os.popen('stty size', 'r').read().split()

############################################################################
#
# Class: bcolors
#
############################################################################

## bcolors - used to provide more engaging output
#
class bcolors:
  Red      = '\033[0;31m'
  Green    = '\033[0;32m'
  Blue     = '\033[0;34m'
  Cyan     = '\033[0;36m'
  White    = '\033[0;37m'
  Yellow   = '\033[0;33m'
  Magenta  = '\033[0;35m'
  BRed     = '\033[1;31m'
  BGreen   = '\033[1;32m'
  BBlue    = '\033[1;34m'
  BCyan    = '\033[1;36m'
  BWhite   = '\033[1;37m'
  BYellow  = '\033[1;33m'
  BMagenta = '\033[1;35m'
  Grey     = '\033[90m'
  Default  = '\033[1;32m'
  Endc     = '\033[0m'
#
## End Class bcolors

############################################################################
#
# def getKeysByStringPartValue
#
############################################################################

## https://thispointer.com/python-how-to-find-keys-by-value-in-dictionary/
## Get a list of keys from dictionary which has the given value
#
def getKeysByStringPartValue(dictOfElements, valueToFind):
  listOfKeys = list()
  listOfItems = dictOfElements.items()
  for item in listOfItems:
      type(item)
      # for subStr in item[1].split()
      #     if subStr == valueToFind:
      #         listOfKeys.append(item[0])

  return listOfKeys
#
## End Func getKeysByStringPartValue

############################################################################
#
# def line
#
############################################################################

## output a line the width of the terminal
#
def line():
  line = '#' * int(columns)
  print(line)
#
## End Func line

############################################################################
#
# def callVault
#
############################################################################

## call vault and return json object
#
def callVault(QUIET, path):
  if not path:
    print(f'{bcolors.BRed}No Vault API in calling path{bcolors.Endc}')
    exit(1)

  #if not QUIET:
  #  print(f'{bcolors.BCyan}Calling Vault with {VAULT_ADDR}/v1{path}{bcolors.Endc}')

  headers = {'X-Vault-Token': f'{VAULT_TOKEN}'}
  r = requests.get(f'{VAULT_ADDR}/v1{path}', headers=headers, verify=f'{VAULT_CACERT}')
  json = r.json()
  return(json)
#
## End Func callVault

############################################################################
#
# def outputSystemInfo
#
############################################################################

## output system info
#
def outputSystemInfo(QUIET):
  if not QUIET:
    line()
    print(f'{bcolors.Default}System Information:     {bcolors.BWhite}{VAULT_ADDR}{bcolors.Endc}')
    print()

  ## health
  #
  health = callVault(QUIET, f'/sys/health')
  print(f'{bcolors.Green}health.{bcolors.Default}Initialised:     {bcolors.BWhite}{health["initialized"]}{bcolors.Endc}')
  print(f'{bcolors.Green}health.{bcolors.Default}Sealed:          {bcolors.BWhite}{health["sealed"]}{bcolors.Endc}')
  print(f'{bcolors.Green}health.{bcolors.Default}Standby:         {bcolors.BWhite}{health["standby"]}{bcolors.Endc}')
  print(f'{bcolors.Green}health.{bcolors.Default}PerfStandby:     {bcolors.BWhite}{health["performance_standby"]}{bcolors.Endc}')
  print(f'{bcolors.Green}health.{bcolors.Default}PRMode:          {bcolors.BWhite}{health["replication_performance_mode"]}{bcolors.Endc}')
  print(f'{bcolors.Green}health.{bcolors.Default}DRMode:          {bcolors.BWhite}{health["replication_dr_mode"]}{bcolors.Endc}')
  print(f'{bcolors.Green}health.{bcolors.Default}VaultVersion:    {bcolors.BWhite}{health["version"]}{bcolors.Endc}')
  print(f'{bcolors.Green}health.{bcolors.Default}ClusterName:     {bcolors.BWhite}{health["cluster_name"]}{bcolors.Endc}')
  print(f'{bcolors.Green}health.{bcolors.Default}ClusterID:       {bcolors.BWhite}{health["cluster_id"]}{bcolors.Endc}')
  if not QUIET:
    print()

  sealstatus = callVault(QUIET, f'/sys/seal-status')
  print(f'{bcolors.Green}seal.{bcolors.Default}Type:              {bcolors.BWhite}{sealstatus["type"]}{bcolors.Endc}')
  print(f'{bcolors.Green}seal.{bcolors.Default}NumShares:         {bcolors.BWhite}{sealstatus["n"]}{bcolors.Endc}')
  print(f'{bcolors.Green}seal.{bcolors.Default}ThresholdShares:   {bcolors.BWhite}{sealstatus["t"]}{bcolors.Endc}')
  print(f'{bcolors.Green}seal.{bcolors.Default}StorageType:       {bcolors.BWhite}{sealstatus["storage_type"]}{bcolors.Endc}')
  print(f'{bcolors.Green}seal.{bcolors.Default}RecoverySeal:      {bcolors.BWhite}{sealstatus["recovery_seal"]}{bcolors.Endc}')
  if not QUIET:
    print()

  ## audit
  #
  audit = callVault(QUIET, f'/sys/audit')
  if not audit["data"]:
    print(f'{bcolors.Green}audit.{bcolors.Default}Audit:            {bcolors.BRed}No audit devices yet{bcolors.Endc}')
  else:
    if audit["data"]["file/"]["path"]:
      print(f'{bcolors.Green}audit.{bcolors.Default}Audit.File:       {bcolors.BWhite}On at path {audit["data"]["file/"]["options"]["file_path"]}{bcolors.Endc}')
      print(f'{bcolors.Green}audit.{bcolors.Default}Audit.File:       {bcolors.BWhite}Local: {audit["data"]["file/"]["local"]}{bcolors.Endc}')
    if audit["data"]["syslog/"]["path"]:
      print(f'{bcolors.Green}audit.{bcolors.Default}Audit.Syslog:     {bcolors.BWhite}On with facility {audit["data"]["syslog/"]["options"]["facility"]}{bcolors.Endc}')
      print(f'{bcolors.Green}audit.{bcolors.Default}Audit.Syslog:     {bcolors.BWhite}Local: {audit["data"]["file/"]["local"]}{bcolors.Endc}')
  if not QUIET:
    print()

  ## internal counters - entities
  #
  counters = callVault(QUIET, f'/sys/internal/counters/entities')
  print(f'{bcolors.Green}counters.{bcolors.Default}Entities:      {bcolors.BWhite}{counters["data"]["counters"]["entities"]["total"]}{bcolors.Endc}')

  ## internal counters - service tokens
  #
  counters = callVault(QUIET, f'/sys/internal/counters/tokens')
  print(f'{bcolors.Green}counters.{bcolors.Default}Tokens:        {bcolors.BWhite}{counters["data"]["counters"]["service_tokens"]["total"]}{bcolors.Endc}')

  ## internal counters - client count
  #
  print(f'{bcolors.Green}counters.{bcolors.Default}Clients:       {bcolors.BYellow}Not collected in this version{bcolors.Endc}')
  if not QUIET:
    print()

  ## encryption key-status
  #
  keystatus = callVault(QUIET, f'/sys/key-status')
  print(f'{bcolors.Green}key-status.{bcolors.Default}Encryptions: {bcolors.BWhite}{keystatus["encryptions"]}{bcolors.Endc}')
  if not QUIET:
    print()

  ## ha status
  #
  hastatus = callVault(QUIET, f'/sys/ha-status')
  for node in hastatus["nodes"]:
    active = node["active_node"]
    if active:
      print(f'{bcolors.Green}ha-status.{bcolors.Default}Node:         {bcolors.BWhite}{node["hostname"]} {bcolors.BCyan}ACTIVE{bcolors.Endc}')
    else:
      print(f'{bcolors.Green}ha-status.{bcolors.Default}Node:         {bcolors.BWhite}{node["hostname"]}{bcolors.Endc}')
  if not QUIET:
    print()

  ## leases
  #
  print(f'{bcolors.Green}leases.{bcolors.Default}Leases:          {bcolors.BYellow}Not collected in this version{bcolors.Endc}')
  if not QUIET:
    print()

  ## licence
  #
  licence = callVault(QUIET, f'/sys/license/status')
  print(f'{bcolors.Green}licence.{bcolors.Default}Autoloaded:     {bcolors.BWhite}{licence["data"]["autoloading_used"]}{bcolors.Endc}')
  print(f'{bcolors.Green}licence.{bcolors.Default}Renewable:      {bcolors.BWhite}{licence["renewable"]}{bcolors.Endc}')
  if licence["data"]["autoloading_used"] == True:
    print(f'{bcolors.Green}licence.{bcolors.Default}Expiry:         {bcolors.BWhite}{licence["data"]["autoloaded"]["expiration_time"]}{bcolors.Endc}')
    for feature in licence["data"]["autoloaded"]["features"]:
      print(f'{bcolors.Green}licence.{bcolors.Default}Feature:        {bcolors.BWhite}{feature}{bcolors.Endc}')
  else:
    print(f'{bcolors.Green}licence.{bcolors.Default}Expiry:         {bcolors.BYellow}Autoloading not used{bcolors.Endc}')
  if not QUIET:
    print()

  ## policy
  #
  policy = callVault(QUIET, f'/sys/policy')
  for pol in policy["policies"]:
    print(f'{bcolors.Green}policy.{bcolors.Default}Policy:          {bcolors.BWhite}{pol}{bcolors.Endc}')
  if not QUIET:
    print()

  ## quotas
  #
  quotas = callVault(QUIET, f'/sys/quotas/config')
  print(f'{bcolors.Green}quotas.{bcolors.Default}LogQuotaRejects: {bcolors.BWhite}{quotas["data"]["enable_rate_limit_audit_logging"]}{bcolors.Endc}')
  print(f'{bcolors.Green}quotas.{bcolors.Default}QuotaHeaders:    {bcolors.BWhite}{quotas["data"]["enable_rate_limit_response_headers"]}{bcolors.Endc}')
  for exempt in quotas["data"]["rate_limit_exempt_paths"]:
    print(f'{bcolors.Green}quotas.{bcolors.Default}ExemptPath:      {bcolors.BWhite}{exempt}{bcolors.Endc}')
  #
  ## rate limits
  #
  quotas = callVault(QUIET, f'/sys/quotas/rate-limit?list=true')
  num_rate_limits = 0
  for quo in quotas["data"]["keys"]:
    if quo != "errors":
      num_rate_limits += 1
      #print(f'Adding {quo}')
  print(f'{bcolors.Green}quotas.{bcolors.Default}NumGlobalLimits: {bcolors.BWhite}{num_rate_limits}{bcolors.Endc}')
  if num_rate_limits > 0:
    for rate in quotas["data"]["keys"]:
      print(f'{bcolors.Green}quotas.{bcolors.Default}RateLimit:       {bcolors.BWhite}{rate}{bcolors.Endc}')
  if not QUIET:
    print()

  ## replication
  #
  replication = callVault(QUIET, f'/sys/replication/status')
  print(f'{bcolors.Green}replication.{bcolors.Default}DR:         {bcolors.BWhite}{replication["data"]["dr"]["mode"]}{bcolors.Endc}')
  print(f'{bcolors.Green}replication.{bcolors.Default}PR:         {bcolors.BWhite}{replication["data"]["performance"]["mode"]}{bcolors.Endc}')
  if not QUIET:
    print()

  ## namespaces
  #
  namespaces = callVault(QUIET, f'/sys/namespaces?list=true')
  num_namespaces = len(namespaces["data"]["keys"])
  print(f'{bcolors.Green}namespaces.{bcolors.Default}Number:      {bcolors.BWhite}{num_namespaces}{bcolors.Endc}')
  for ns in namespaces["data"]["keys"]:
    print(f'{bcolors.Green}namespaces.{bcolors.Default}Namespace:   {bcolors.BWhite}{ns}{bcolors.Endc}')
  if not QUIET:
    print()

  ## tally mounts
  #
  total_auth_mounts  = 0
  total_secret_mounts = 0
  for ns in namespaces["data"]["keys"]:
    ns_auth_mounts   = callVault(QUIET, f'/{ns}sys/auth')
    for auth in ns_auth_mounts["data"]:
      #print(f'auth-ns{ns}{auth}')
      total_auth_mounts += 1
    ns_secret_mounts = callVault(QUIET, f'/{ns}sys/mounts')
    for mount in ns_secret_mounts["data"]:
      #print(f'sec-ns{ns}{mount}')
      total_secret_mounts += 1
  #
  ## add the root namespace
  #
  auth_mounts   = callVault(QUIET, f'/sys/auth')
  for auth in auth_mounts["data"]:
    #print(f'auth-root-{auth}')
    total_auth_mounts += 1
  secret_mounts = callVault(QUIET, f'/sys/mounts')
  for mount in secret_mounts["data"]:
    #print(f'sec-root-{mount}')
    total_secret_mounts += 1
  print(f'{bcolors.Green}auth-mounts.{bcolors.Default}Total:      {bcolors.BWhite}{total_auth_mounts}{bcolors.Endc}')
  print(f'{bcolors.Green}secrets-engines.{bcolors.Default}Total:  {bcolors.BWhite}{total_secret_mounts}{bcolors.Endc}')
#
## End Func outputSystemInfo

############################################################################
#
# def outputNamespaceInfo
#
############################################################################

## output namespace info
#
def outputNamespaceInfo(QUIET, namespaceName=all):
  if not QUIET:
    print(f'\n{bcolors.Cyan}Namespace Information.{bcolors.Endc}')
  print(f'\n{bcolors.Cyan}Namespace: {namespaceName}{bcolors.Endc}')
  exit(0)
#
## End Func outputNamespaceInfo

############################################################################
#
# def MAIN
#
############################################################################

#    #   ##   # #    #
##  ##  #  #  # ##   #
# ## # #    # # # #  #
#    # ###### # #  # #
#    # #    # # #   ##
#    # #    # # #    #

## Main
#
def main():
    ## create parser
    #
    parser = argparse.ArgumentParser(
        description=f'HashiCorp Vault Enterprise probe, for convenient iteration of enterprise namespaces for rudimentary reporting',
        formatter_class=lambda prog: argparse.HelpFormatter(prog,max_help_position=80, width=130)
    )
    optional = parser._action_groups.pop()

    system    = parser.add_argument_group('To just output information about the system as a whole')
    namespace = parser.add_argument_group('Focus output to a specific namespace')
    quiet     = parser.add_argument_group('Hide dressing for better pipeline work')

    ## add arguments to the parser
    #
    system.add_argument('-s', '--system',       action='store_true', help='Output information about the system as a whole, not namespaces-level information')

    namespace.add_argument('-n', '--namespace', type=str, help='Specify a namespace to operate on; use the string all for all namespaces on the system')

    quiet.add_argument('-q', '--quiet',         action='store_true', help='Hide extraneous output')

    parser._action_groups.append(optional)

    ## parse
    #
    arg = parser.parse_args()

    if arg.quiet:
      QUIET = True
    else:
      QUIET = False

    if arg.system:
      system = True
    else:
      system = False

    if arg.namespace:
      namespace = True
    else:
      namespace = False

    ## need more time with argparse to work out how to improve this
    #
    if not system and not namespace:
      print(f'{bcolors.BCyan}Start with:\n{bcolors.Endc}')
      print(f'{bcolors.BCyan}hc-vault-probe.py -h{bcolors.Endc}')
      exit(1)

    if system:
      ## output information about the system
      #
      outputSystemInfo(QUIET)

    if namespace:
      if arg.namespace == "all":
        ## generate list of all namespaces
        #
        outputNamespaceInfo(QUIET, "all")
      else:
        ## assign namespace array to just the specified namespace
        #
        outputNamespaceInfo(QUIET, arg.namespace)

        print(f'{bcolors.BCyan}Written agenda {filePath} to disk for {bcolors.BGreen}{author}{bcolors.Endc}')
        print(f'\n{bcolors.Cyan}All done.{bcolors.Endc}')
#
## End Func main

if __name__ == '__main__':
    main()
