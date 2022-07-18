#from jarvis_cd.node import Node
from jarvis_cd.shell.jarvis_exec_node import JarvisExecNode
from jarvis_cd.ssh.ssh_config import GetPrivateKey
import os
import re

class ToOpenSSHConfig(JarvisExecNode):
    def __init__(self, register_hosts, register_ssh, **kwargs):
        super().__init__(**kwargs)
        self.register_hosts = register_hosts
        self.register_ssh = register_ssh

    def _LocalRun(self):
        #OpenSSH config
        ossh_config_path = os.path.join(os.environ['HOME'], '.ssh', 'config')
        text = ''
        if os.path.exists(ossh_config_path):
            with open(ossh_config_path, 'r') as fp:
                text = fp.read()
        ossh_config = {}

        #Convert SSH config to dictionary indexed by host IP
        host = None
        lines = text.splitlines()
        for line in lines:
            if re.match('Host', line):
                host = line.strip().split()[1]
                ossh_config[host] = {}
                continue
            if host is None:
                continue
            #Ignore # comments
            line = line.split('#',1)[0]
            #Key, Value
            words = line.strip().split(None,1)
            if len(words) != 2:
                continue
            key = words[0]
            value = words[1]
            ossh_config[host][key] = value

        #Modify/create entry for hosts
        for host in self.register_hosts:
            if host not in ossh_config:
                ossh_config[host] = {}
            if 'port' in self.register_ssh:
                ossh_config[host]['Port'] = self.register_ssh['port']
            if 'username' in self.register_ssh:
                ossh_config[host]['User'] = self.register_ssh['username']
            if 'key' in self.register_ssh:
                ossh_config[host]['IdentityFile'] = GetPrivateKey(self.register_ssh['key_dir'], self.register_ssh['key'])

        #Create updated text
        text = ""
        for host,host_info in ossh_config.items():
            text += f"Host {host}\n"
            for key, value in host_info.items():
                text += f"  {key} {value}\n"

        #Write the updated ssh_config
        with open(ossh_config_path, 'w') as fp:
            fp.write(text)