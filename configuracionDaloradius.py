#!/usr/bin/env python
import os

os.system("clear")

print("En este momento se actulizara su servidor ubuntu-server o Debian")
os.system("apt update -y")
#os.system("apt dist-upgrade -y")

os.system("clear")
#instalacion de mariadb
os.system("apt --no-install-recommends install mariadb-server -y")
print("Debe ajustar su contraseña de root para su base de datos maria db")
os.system("mariadb-secure-installation")
os.system("clear")

#configuracion de base de datos usuario y contraseña
os.system("mysql -u root -e" "CREATE DATABASE raddb;")
os.system("mysql -u root -e" "GRANT ALL ON raddb.* TO 'raduser'@'localhost' IDENTIFIED BY 'radpass';")
os.system("mysql -u root -e" "FLUSH PRIVILEGES;")
os.system("clear")

#os.system("systemctl enable mariadb")

#instalacion de freeradius
#os.system("apt --no-install-recommends install freeradius freeradius-mysql mariadb-client")
#os.system("cd /etc/freeradius/3.0/mods-config/sql/main/mysql")
#os.system("mariadb -u root raddb < schema.sql")


os.system("cd /etc/freeradius/3.0/mods-available/")
os.system("sed -Ei '/^[\t\s#]*tls\s+\{/, /[\t\s#]*\}/ s/^/#/' /etc/freeradius/3.0/mods-available/sql")
os.system("nano /etc/freeradius/3.0/mods-available/sql")

os.system("ln -s /etc/freeradius/3.0/mods-available/sql /etc/freeradius/3.0/mods-enabled/")

os.system("systemctl enable freeradius")
os.system("systemctl restart freeradius")


os.system("apt --no-install-recommends install apache2 php libapache2-mod-php \
                                    php-mysql php-zip php-mbstring php-common php-curl \
                                    php-gd php-db php-mail php-mail-mime \
                                    mariadb-client freeradius-utils")



os.system("apt --no-install-recommends install git")
os.system("cd /var/www")
os.system("git clone https://github.com/lirantal/daloradius.git")


os.system("mkdir -p /var/log/apache2/daloradius/{operators,users}")
print("Ejecuta el siguiente parrafo")

print("cat <<EOF >> /etc/apache2/envvars")
print("# daloRADIUS users interface port")
print("export DALORADIUS_USERS_PORT=80")
print("# daloRADIUS operators interface port")
print("export DALORADIUS_OPERATORS_PORT=8000")
print("# daloRADIUS package root directory")
print("export DALORADIUS_ROOT_DIRECTORY=/var/www/daloradius")  
print("# daloRADIUS administrator's email")
print("export DALORADIUS_SERVER_ADMIN=admin@daloradius.local")
print("EOF")


print("Copia y ejecuta los siguientes comandos")
print("cat <<EOF > /etc/apache2/ports.conf")
print("# daloRADIUS")
print("Listen \${DALORADIUS_USERS_PORT}")
print("Listen \${DALORADIUS_OPERATORS_PORT}")
print("EOF")

virtual=open("/etc/apache2/sites-available/operators", "w")
virtual.write("<VirtualHost *:\${DALORADIUS_OPERATORS_PORT}>\nServerAdmin \${DALORADIUS_SERVER_ADMIN}\nDocumentRoot \${DALORADIUS_ROOT_DIRECTORY}/app/operators\n<Directory \${DALORADIUS_ROOT_DIRECTORY}/app/operators>\nOptions -Indexes +FollowSymLinks\nAllowOverride All\nRequire all granted\n</Directory>\n<Directory \${DALORADIUS_ROOT_DIRECTORY}>\nRequire all denied\n</Directory>\nErrorLog \${APACHE_LOG_DIR}/daloradius/operators/error.log\nCustomLog \${APACHE_LOG_DIR}/daloradius/operators/access.log combined\n</VirtualHost>")
virtual.close()

virtual2=open("/etc/apache2/sites-available/users.conf")
virtual2.write("<VirtualHost *:\${DALORADIUS_USERS_PORT}>\nServerAdmin \${DALORADIUS_SERVER_ADMIN}\nDocumentRoot \${DALORADIUS_ROOT_DIRECTORY}/app/users\n<Directory \${DALORADIUS_ROOT_DIRECTORY}/app/users>\nOptions -Indexes +FollowSymLinks\nAllowOverride None\nRequire all granted\n</Directory>\n<Directory \${DALORADIUS_ROOT_DIRECTORY}>\nRequire all denied\n</Directory>\nErrorLog \${APACHE_LOG_DIR}/daloradius/users/error.log\nCustomLog \${APACHE_LOG_DIR}/daloradius/users/access.log combined\n</VirtualHost>\n")
virtual2.close()    


os.system("cd /var/www/daloradius/app/common/includes")
os.system("cp daloradius.conf.php.sample daloradius.conf.php")
os.system("chown www-data:www-data daloradius.conf.php")
os.system("chmod 664 daloradius.conf.php")



os.system("cd /var/www/daloradius/")
os.system("mkdir -p var/{log,backup}")
os.system("chown -R www-data:www-data var")  
os.system("chmod -R 775 var")


os.system("cd /var/www/daloradius/contrib/db")
os.system("mariadb -u root raddb < fr3-mariadb-freeradius.sql")
os.system("mariadb -u root raddb < mariadb-daloradius.sql")


os.system("a2dissite 000-default.conf")  
os.system("a2ensite operators.conf users.conf")
os.system("systemctl enable apache2")
os.system("systemctl restart apache2")

print("Ahora ve tu direccion ip e inicia a tu servidor daloradius de la siguiente manera")
print("ip-address:8000")
print("usuario: administrator")
print("password: radius")