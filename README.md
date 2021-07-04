# vrux_public

## Pre-Requisition
  - Ubuntu20
  - NginX
  - Python3

## Install

** Install Environment **

	$ apt install -y python3 python3-pip nginx
	$ pip3 install pygics
	$ mv /etc/nginx/nginx.conf /etc/nginx/nginx.conf.bak
	$ VRUX_HOME=/opt/vrux

** Clone Repository **

	$ cd /opt
	/opt $ git clone https://github.com/HyechurnJang/vrux_public.git

** Post Cloning **

	$ cd /opt
	/opt $ mv vrux_public /vrux
	/opt $ ln -s /opt/vrux/etc/nginx/nginx.conf /etc/nginx/nginx.conf

## Configurations
 
  - Config vRealize environments ==> $VRUX_HOME/config.py

	vra_fqdn = '' # VRA_FQDN
	vidm_fqdn = '' # VIDM_FQDN
	vrux_fqdn = '' # PORTAL_FQDN
	vidm_client_id = '' # OAuth Client ID
	vidm_client_token = '' # OAuth Client Share Secret
	 
	vra_admin_username = '' # vRA Admin Username
	vra_admin_password = '' # vRA Admin Password

  - Config Service FQDNs from DNS Reserved & SSL Certiciation Path ==> $VRUX_HOME/etc/nginx/nginx.conf

	ssl_certificate             {{SSL_CERTIFICATE}};
    ssl_certificate_key         {{SSL_CERT_KEY}};
	 
	server {
        listen          443 ssl;
        server_name     www.{{DOMAIN_FQDN}};
        return          302 https://{{PORTAL_FQDN}};
    }
	 
    server {
        listen          443 ssl;
        server_name     {{PORTAL_FQDN}};
        location /auth  { proxy_pass http://localhost:8080/auth; }
        location /vra   { proxy_pass http://localhost:8080/vra; }
        location /      { alias /opt/vrux/www/; }
    }

## Running

	$ cd /opt/vrux
	/opt/vrux $ systemctl restart nginx
	/opt/vrux $ python3 server.py 
