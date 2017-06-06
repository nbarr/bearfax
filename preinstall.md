# Create new conf.d with correct seling permissions
sudo mv /etc/nginx/conf.d.orig
sudo rm -rf /etc/nginx/conf.d
sudo mkdir --context=system_u:object_r:httpd_config_t /etc/nginx/conf.d
sudo mv /etc/nginx/conf.d.orig/* /etc/nginx/conf.d/

# Set selinux permission on config file
chcon --reference /etc/nginx/nginx.conf /etc/nginx/conf.d/bearfax-dev.conf

# Create selinux permissions file for uwsgi socket and apply it
# show the new rules to be generated
grep nginx /var/log/audit/audit.log | audit2allow

# show the full rules to be applied
grep nginx /var/log/audit/audit.log | audit2allow -m nginx

# generate the rules to be applied
grep nginx /var/log/audit/audit.log | audit2allow -M nginx

# apply the rules
semodule -i nginx.pp

rm nginx.pp nginx.te
