   #!/bin/bash

   mysql -uroot -p$MYSQL_ROOT_PASSWORD <<EOF
   GRANT ALL PRIVILEGES ON *.* TO 'django_user'@'%';
   FLUSH PRIVILEGES;
