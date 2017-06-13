- Install Nano editor:
    ```
    sudo yum -y install nano screen
    ```
- Aliases in ~/.bashrc:
    ```
    alias yum='sudo yum'
    alias service='sudo service'
    alias chkconfig='sudo chkconfig'
    alias ed='sudo nano'
    ```
- Turn off unnecessary services:
    ```
    chkconfig postfix off
    service postfix stop
    chkconfig chronyd off
    service chronyd stop
    ```
- Install EPEL:
    ```
    yum install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
    ```
- Install Python 3
    ```
    yum -y install python34 python34-pip
    ```
- Install Uwsgi and Nginx
    ```
    yum -y install uwsgi uwsgi-emperor uwsgi-plugin-python3 uwsgi-logger-file git nginx
    ```
- Turn off uwsgi's tyrant mode
    ```
    sudo nano /etc/uwsgi.ini
    emperor-tyrant = true -> emperor-tyrant = false
    ```
- OPTIONAL: Install lynx browser
    ```
    yum-config-manager --enable rhui-REGION-rhel-server-extras rhui-REGION-rhel-server-optional
    yum -y install lynx
    ```
- Upgrade pip:
    ```
    sudo pip install --upgrade pip
    ```
- Fix pip binary:
    ```
    sudo ln -sf /bin/pip3 /bin/pip
    ```
- Install virtualenv:
    ```
    sudo pip install virtualenv
    ```
- Add SSH key to deploy data from GitHub:
    ```
    nano ~/.ssh/aws-bearfax-github (put your private key for deployment here)
    ```
- Add it to `~/.ssh/config` to avoid specifying each time on pull/push:
    ```
    Host github.com
        HostName github.com
        IdentityFile ~/.ssh/aws-bearfax-github
        User git
    ```
- Fix SSH permissions
    ```
    sudo chmod 0600 ~/.ssh/config
    sudo chmod 0600 ~/.ssh/aws-bearfax-github
    ```
- Make group common for uwsgi and nginx to allow then to write to application directory
    ```
    sudo groupadd --force bearfax
    ```
- Add uwsgi and nginx user to group `bearfax`
    ```
    sudo usermod --append --groups bearfax uwsgi
    sudo usermod --append --groups bearfax nginx
    ```
- Prepare app dir
    ```
    sudo mkdir /srv/bearfax
    sudo chown ec2-user:bearfax /srv/bearfax/
    sudo chmod 0775 /srv/bearfax/
    ```
- Uwsgi logging to file:
    ```
    sudo touch /var/log/uwsgi.log
    sudo chown uwsgi:root /var/log/uwsgi.log
    ```
- Append to /etc/uwsgi.ini
    ```
    logto = /var/log/uwsgi.log
    ```
- Create virtual environment
    ```
    cd /srv/bearfax/
    virtualenv .venv
    ```
- Clone repo
    ```
    git clone git@github.com:nbarr/bearfax.git
    ```
- Fix owner (after each deploy):
    ```
    sudo chown -R ec2-user:bearfax /srv/bearfax
    ```
- Setup uwsgi and nginx configs
    ```
    sudo ln -sf /srv/bearfax/conf/uwsgi.ini /etc/uwsgi.d/bearfax-dev.ini
    sudo ln -sf /srv/bearfax/conf/nginx.conf /etc/nginx/conf.d/bearfax-dev.conf
    ```


source ./venv/bin/activate
pip install -r requirements.txt

grep nginx /var/log/audit/audit.log | audit2allow -m nginx > nginx.te
checkmodule -M -m -o nginx.mod nginx.te
semodule_package -o nginx.pp -m nginx.mod
semodule -i nginx.pp
service nginx restart