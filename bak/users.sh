#!/bin/bash
file="input.csv"

while IFS=,  read -r name email; do
 userid="$(echo "$email" | cut -d@ -f1 | tr -d ' ')"
  password="$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 10 | head -n 1)"

  echo "Name: $name"
  echo "Email: $email"
  echo "UserID: $userid"
  echo "Password: $password"
  
  useradd -m "$userid"
  echo "$userid:$password" | chpasswd
  echo "Executing a bash statement"

export userid
export password
export email
export name

python3 pyscript.py $email $name $userid $password
echo "successful"
done < "$file"
