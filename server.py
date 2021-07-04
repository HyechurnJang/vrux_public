# -*- coding: utf-8 -*-
'''
  ____  ___   ____________  ___  ___  ____     _________________
 / __ \/ _ | / __/  _/ __/ / _ \/ _ \/ __ \__ / / __/ ___/_  __/
/ /_/ / __ |_\ \_/ /_\ \  / ___/ , _/ /_/ / // / _// /__  / /   
\____/_/ |_/___/___/___/ /_/  /_/|_|\____/\___/___/\___/ /_/    
         Operational Aid Source for Infra-Structure 

Created on 2020. 10. 21..
@author: Hye-Churn Jang, CMBU Specialist in Korea, VMware [jangh@vmware.com]
'''

from pygics import server, setEnv

import config
setEnv(
    vra_fqdn=config.vra_fqdn,
    vidm_fqdn=config.vidm_fqdn,
    vrux_fqdn=config.vrux_fqdn,
    vidm_client_id=config.vidm_client_id,
    vidm_client_token=config.vidm_client_token,
    vra_admin_username=config.vra_admin_username,
    vra_admin_password=config.vra_admin_password
)

if __name__ == '__main__':
    server('0.0.0.0', 8080, 'engine')