# wyangsun

目的：
运维批量管理平台

架构：
nginx + tornado + ansible + sqlalchemy

欢迎各界小白大神拍砖。

部署环境：
1.nginx配置
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
2.ansible配置
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
