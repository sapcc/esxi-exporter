import paramiko
import logging
import socket

logger = logging.getLogger('esxi')

# trying to remove anyoing exception of banner-timeout that has no effect
logging.getLogger('paramiko.transport').setLevel(logging.CRITICAL)

class SshHelper:

    @staticmethod
    def execute_command(address: str, user: str, password: str, command: str) -> str:
        """
        Runs a ssh command and returns str_out.

        :param address: The address to the remote machine
        :param user:  The ssh user
        :param password:  The ssh password
        :param command: The command to run
        :return: Answer from host or None
        """

        try:
            logger.debug("SSH: connecting to %s" % address)
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname=address, username=user, password=password, banner_timeout=0.5)
            stdin, stdout, stderr = client.exec_command(command, timeout=1)
            answer = stdout.read().decode("utf-8")
            client.close()
            return answer

        except socket.gaierror as ex:
            logger.error("SSH: DNS error. Could not locate %s" % address)
            return None

        except (paramiko.AuthenticationException, paramiko.PasswordRequiredException) as ex:
            logger.error("SSH: authentication error: %s" % address)
            return None
        
        except (paramiko.BadHostKeyException,
                paramiko.SSHException,
                paramiko.ChannelException,
                ) as ex:
            logger.error("S    SH: connection failed to %s " % address)
            return  None




