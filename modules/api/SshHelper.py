import paramiko
import logging

class SshHelper:

    @staticmethod
    def execute_command(address: str, user: str, password: str, command: str) -> str:
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname=address, username=user, password=password, banner_timeout=0.5)
            stdin, stdout, stderr = client.exec_command(command, timeout=1)
            answer = stdout.read().decode("utf-8")
            client.close()
            return answer
        except Exception as ex:
            return None
