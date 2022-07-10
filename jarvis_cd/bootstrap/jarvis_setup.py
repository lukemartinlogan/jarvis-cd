from jarvis_cd.installer.git_node import GitNode, GitOps
from jarvis_cd.installer.modify_env_node import ModifyEnvNode, ModifyEnvNodeOps
from jarvis_cd.installer.pip_node import LocalPipNode
from jarvis_cd.basic.exec_node import ExecNode
from jarvis_cd.bootstrap.package import Package
from jarvis_cd.comm.ssh_node import SSHNode
from jarvis_cd.comm.scp_node import SCPNode
import sys,os
import shutil

class JarvisSetup(Package):
    def Install(self):
        jarvis_root = self.config['jarvis_cd']['path']
        SCPNode('copy jarvis', self.config['jarvis_cd']['path'], self.config['jarvis_cd']['path'], hosts=self.all_hosts, ssh_info=self.ssh_info).Run()
        cmds = [
            f"./{jarvis_root}/dependencies.sh",
            f"export PYTHONPATH={jarvis_root}",
            f"cd {self.config['jarvs']['path']}",
            f"./bin/jarvis-bootstrap deps local_install jarvis"
        ]
        SSHNode('install jarvis', cmds, hosts=self.all_hosts, ssh_info=self.ssh_info).Run()

    def _LocalInstall(self):
        jarvis_root = self.config['jarvis_cd']['path']

        #Ensure that the variables aren't already being set
        ModifyEnvNode('jarvis_root', self.bashni, f"export JARVIS_ROOT", ModifyEnvNodeOps.REMOVE).Run()
        ModifyEnvNode('pypath', self.bashni, f"export PYTHONPATH", ModifyEnvNodeOps.REMOVE).Run()

        #Set the variables to their proper values
        ModifyEnvNode('jarvis_root', self.bashni, f"export JARVIS_ROOT={jarvis_root}", ModifyEnvNodeOps.APPEND).Run()
        ModifyEnvNode('pypath', self.bashni, f"export PYTHONPATH=\`sudo -u {self.username} \$JARVIS_ROOT/bin/jarvis-py-paths\`:\$PYTHONPATH", ModifyEnvNodeOps.APPEND).Run()

    def _LocalUpdate(self):
        jarvis_root = os.environ['JARVIS_ROOT']
        GitNode('clone', self.config['jarvis_cd']['repo'], jarvis_root, GitOps.UPDATE,
                branch=self.config['jarvis_cd']['branch'], commit=self.config['jarvis_cd']['commit']).Run()
        ExecNode('deps', f"./{jarvis_root}/dependencies.sh").Run()
        LocalPipNode('install', jarvis_root).Run()

    def _LocalUninstall(self):
        jarvis_root = os.environ['JARVIS_ROOT']
        shutil.rmtree(jarvis_root)
        ModifyEnvNode('jarvis_root', self.bashni, f"export JARVIS_ROOT", ModifyEnvNodeOps.REMOVE).Run()
        ModifyEnvNode('pypath', self.bashni, f"export PYTHONPATH", ModifyEnvNodeOps.REMOVE).Run()