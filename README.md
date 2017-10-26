# WeblogicWLSTScripts
WLST scripts to interact with Weblogic MBeans
## Abstract
Weblogic WLST scripts written in python connect to WLST interface and works with MBeans directly, which provides a more control in managing a weblogic domain.

## Pre-requisites
- Most enterprise servers do not allow plain text password to connect to WLST or store plain text credentials.
- Recommended approach is to use encrypted credentials, follow below sections to encrypt credentials.

## Encrypting credentials
1. set WLST environment and connect to WLST
    - _java weblogic.WLST_
2. connect to admin server
    - connect('<admin-user-name>','admn-password','t3://admin-listen-address:admin-listen-port')
3. generate credential files
    - storeUserConfig('home-folder-WebLogicConfig.properties','home-folder-WebLogicKey.properties')
- Now these files can be used to connect to the domain instead of plain text credentials.
