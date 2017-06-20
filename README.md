# Slave commander
A python utility for executing arbitrary commands on jenkins slaves

## Usage
```
python slave_commander.py [TARGET LABEL] [COMMAND]
```
Where `TARGET LABEL` is the label of nodes you want to target and `COMMAND` is the command to execute. For now, the options of what Jenkins instance to access, as well as credentials for access are assumed to be accessible as environment variables. The environment variables are:

- JENKINS_URL - Always available when running from a jenkins job
- jenkins_api_user - Added as a global variable in Jenkins configuration
- jenkins_api_token - Also added as a global password and injected into builds

When these values are not found in environment variables, defaults are used (embedded in the code for prod jenkins)

## Further notes

In order to target all nodes that are online, use the 'all' label.

For windows file paths, use '/' instead of '\\' 

When the connection is made, not all PATH locations are loaded. For example, 
```
npm list
``` 

will not work when executed as a command, but 
```
C:/Users/Monish/AppData/Roaming/local/npm/npm.cmd list
``` 
will work. Remember to quote the whole command!
```
python slave_commander.py windows "C:/Users/Monish/AppData/Roaming/local/npm/npm.cmd install typescript -g"
```


Hapy hacking!