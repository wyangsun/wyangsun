# wyangsun

目的：
运维批量管理平台

架构：
nginx + tornado + ansible + sqlalchemy

部署环境：
1.python环境（centos）
python-pip install mysql-connector-python
python-pip install tornado
python-pip install sqlalchemy
python-pip install mysql
2.nginx配置
```nginx
        location /js/ {
         root   /root/wyangsun/static/;
        }
        location /css/ {
             root   /root/wyangsun/static/;
        }
        location ~ ^/favicon\.ico$ {
            root   /root/wyangsun/static/;
        }
        location / {
            proxy_pass  http://127.0.0.1:8000;
        }
```
3.ansible配置
/etc/ansible/ansible.cfg:
```ansible
[defaults]
hostfile       = /etc/ansible/hosts
remote_tmp     = $HOME/.ansible/tmp
pattern        = *
forks          = 5
poll_interval  = 15
sudo_user      = sa
transport      = smart
remote_port    = 22
module_lang    = C
gathering = implicit
sudo_exe = sudo
timeout = 10
...
```
