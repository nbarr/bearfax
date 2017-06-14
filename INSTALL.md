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
- Install Python 3, git, Nginx and Supervisor
    ```
    yum -y install python34 python34-pip git nginx supervisor
    ```
- Fix supervisor's config, open `/etc/supervisord.conf` and uncomment:
    ```
    chmod=0700
    chown=nobody:nobody
    ```
- Fix supervisor's log permissions
    ```
    chown nobody  /var/log/supervisor/supervisord.log
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
- Create user to down privileges from root
    ```
    sudo useradd -b /srv -g bearfax -M -s /sbin/nologin bearfax
    ```
- Make group common for deploy user and nginx to allow then to write to application directory
    ```
    sudo groupadd --force bearfax
    ```
- Make group common for run user and nginx to allow then to write to application directory
    ```
    sudo groupadd --force bearfax
    ```
- Add user `bearfax` and `nginx` to group `bearfax`
    ```
    sudo usermod --append --groups bearfax bearfax
    sudo usermod --append --groups bearfax nginx
    ```
- Prepare app dir
    ```
    sudo mkdir /srv/bearfax
    sudo chown ec2-user:bearfax /srv/bearfax/
    sudo chmod 0775 /srv/bearfax/
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
- Setup supervisor and nginx configs
    ```
    sudo ln -sf /srv/bearfax/conf/supervisor.ini /etc/supervisord.d/bearfax-dev.ini
    sudo ln -sf /srv/bearfax/conf/nginx.conf /etc/nginx/conf.d/bearfax-dev.conf
    ```
- Install project requirements
    ```
    source /srv/bearfax/venv/bin/activate
    pip install -r requirements.txt
    ```
- Fix nginx SELinux permissions (if required)
    ````
    grep nginx /var/log/audit/audit.log | audit2allow -m nginx > nginx.te
    checkmodule -M -m -o nginx.mod nginx.te
    semodule_package -o nginx.pp -m nginx.mod
    semodule -i nginx.pp
    service nginx restart
    ````
