# Amazon EC2 instance creation

Below described how to create EC2 instace through web interface

- Goto Amazon Console -> EC2.
- Pick "Instances" from the sidebar and click button "Launch Instance".
- From the OSes list choose "Red Hat". On the moment of this document creation 
latest version is 7.3 64-bit and click "Select".
- It makes sense to pick initially configuration eligible for free tier (later 
it can be scaled) so choose `t2.micro` type. Click "Next: Configure Instance 
Details".
- On this page check checkbox "Protect against accidental termination" and 
ensure that in field "Tenancy" selected "Shared" to avoid shocking bills later. 
Click "Next: Add Storage".
- For free-tier types you can choose up to 30Gb hard disk so increase size to 
30 Gb. Click "Next: Add Tags".
- Click "Next: Configure Security Group"
- If you have static IP address then for SSH row fill "Source" cell with 
"My IP". Otherwise (you don't know or your provider gives to you dynamic IP) 
choose "Anywhere"
- Add rule "HTTP" with "Anywhere" access
- Add rule "HTTPS" with "Anywhere" access
- If your instance will provide other services add all required ports that 
should be visible from outer internet.
- Or you can create security group (i.e. set of rules) before and just chose 
"Select an existing security group" an pick desired one.
- Click "Review and Launch"
- Check that everything is correct and click "Launch". You will be asked to 
pick keys pair to inject to created system. **IMPORTANT**: ensure that you have 
corresponding private key (.pem) downloaded before. Your PUBLIC key will be 
added to the file `/home/ec2-user/.ssh/authorized_keys`. This file contains 
list of public keys that allowed to connect to this instance.
- Choose one and click "Launch"
- After short time your new instance will be up and running. Click "Instances" 
on sidebar and check it.
- Now your instance has DYNAMIC IP. It means that after each start/stop it 
COULD BE changed (never while instance running).
- You can connect to it using IP address from section "IPv4 Public IP" in 
properties list, see [Amazon EC2 instance access](amazon-ec2-instance-acces).


# Amazon RDS database creation
- Goto Amazon Console -> RDS.
- Pick "Instances" from the sidebar and click button "Launch DB Instance".
- Pick "MariaDB". Amazon Aurora is a good choice but a bit more expensive.
- Chose required environment. It is ok to work using "Dev/Test" in production.
- Choose latest engin in "DB Engine Version"
- Choose "b.t2.micro" in "DB Instance Class" for free tier
- Fill "DB Instance Identifier" with any database identifier that will be 
visible on instances list
- Fill "Master Username" and "Master Password"
- Click "Next"
- Fill "Database Name" with name of future database (single RDS instance can 
has any number of databases)
- In "VPC Security Group(s)" choose group that allows you to access from 
"0.0.0.0/0" to your instance. Or, if no such group, update any of existing 
later. Otherwise you will be unable to connect to this instance.
- Click "Launch DB Instance"


# EC2 instance IP address management

If you want that your instance has constantly only one IP address you can add 
it in "Elastic IPs" section.

- Create new Elastic IP
- Associate it with your instance (each instance could be associated with only 
one Elastic IP and must be released before reassigning)

From this moment even after restart your instance will be accessible by single 
IP address.


# Amazon EC2 instance access

EC2 instance can be accessed only through SSH (command line). Please refer to 
section [Amazon EC2 instance creation](#amazon-ec2-instance-creation) to ensure 
that you added chosen correct key pair to inject into created image.

To connect to instance you shoul use next command:
```
ssh ec2-user@XXX.XXX.XXX.XXX -i /path/to/your/private_key_for_instance
```
where `XXX.XXX.XXX.XXX` is IP address of your instance. If you already have 
domain name attached you canuse it instead of IP.

If you haven't multiple keys then your one usually called `id_rsa` and used by 
default (you do not need to specify key file explicitly with `-i` option). If 
you have many keys you have to provide it.

For the first time SSH warn you then identity cannot be established, i.e. you 
have no local record that this host is it. Just answer "yes" and continue. 
After that you'll have access to remote EC2 machive's command line. User 
`ec2-user` has `sudo` privileges to manage entire system


# Amazon RDS database access

By default site server by MariaDB, it is fork on MySQL database hosted on 
Amazon Cloud.
It can be accessed using any SQL client (MySQL Workbench, HeidiSQL, DBeaver, 
etc.)

- Open "RDS" section in Amazon console
- Click "Instances"
- Click on your db instance and check "Endpoint" section
- To initial login use credentioans defined on database instance creation time. 
- Create database.
- Create user with "SELECT,INSERT,UPDATE,DELETE" permissions to this database.
- Try to login using this user credentials.
- It is good idea to disallow login for "root" once you create all requied 
databases and users. Just remove line for 'root' from `mysql.user` table where 
`hostname` contains `%`. Or, if want to use superuser account later put IP 
address if your EC2 instance with Elastic IP. Thus you can connect under "root" 
only from EC2 instance's command line.



# Application and requirements installation

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

