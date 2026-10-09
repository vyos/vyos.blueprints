# Security policy

## Reporting a vulnerability

Please do **not** open a public issue or pull request for a security problem.
Report it privately through GitHub instead: on this repository's **Security** tab,
choose **Report a vulnerability**. Only the maintainers can see the report, and we
will work with you on a fix and on disclosure.

Please include what is affected (role, playbook or workflow), how to reproduce it,
and what an attacker could do with it.

## Scope

In scope:

- the roles and playbooks in this collection - for example a role that leaves a
  router more exposed than its documentation says, or writes secrets to logs or
  files without protection
- this repository's CI workflows

Out of scope - please report these where they belong:

- vulnerabilities in VyOS itself - through the VyOS project's security process
- vulnerabilities in vyos.vyos, ansible-core or other dependencies - to those projects

## Supported versions

Fixes are made on `main` and released in the next version of the collection.
