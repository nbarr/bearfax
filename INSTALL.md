- Install Nano editor:
    ```
    sudo yum install nano screen
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
- Install Uwsgi and Nginx
    ```
    yum -y install uwsgi uwsgi-emperor uwsgi-plugin-python3 uwsgi-logger-file git nginx
    ```
- OPTIONAL: Install lynx browser
    ```
    yum-config-manager --enable rhui-REGION-rhel-server-extras rhui-REGION-rhel-server-optional
    yum install lynx
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
    sudo pip install
    ```
- Add SSH key to deploy data from GitHub:
    ```
    nano ~/.ssh/nano aws-bearfax-github (put your private key for deployment here)
    ```
- Add it to `~/.ssh/config` to avoid specifying each time on pull/push:
    ```
    Host github.com
        HostName github.com
        IdentityFile ~/.ssh/aws-bearfax-github
        User git
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
- Fix owner:
    ```
    sudo chown ec2-user:bearfax /srv/bearfax
    ```
- Link uwsgi conf and fix its owner:
    ```
    sudo ln -sf /srv/bearfax/conf/uwsgi.ini /etc/uwsgi.d/bearfax-dev.ini
    sudo chown -h uwsgi:bearfax /etc/uwsgi.d/bearfax-dev.ini
    ```
- Link nginx conf
    ```
    sudo ln -sf /srv/bearfax/conf/nginx.conf /etc/nginx/conf.d/bearfax-dev.conf
    ```
