"""Simple crontab script for V rising dedicated server.

Author: Mimamsa@Github
Created: 2024.6.30
"""
import os
import time
import psutil
import subprocess as sp
import logging

logger = logging.getLogger('crontab-for-v-rising-server')


chkIntrv = 60  # seconds
runningProc = "VRisingServer.exe"
exeProgPath = "D:/Program Files (x86)/Steam/steamapps/common/VRising/VRising_Server/start_server_example.bat"


def checkAndExecute(runningProc, exeProgPath):
    """Check & execute program if the specific process is running.
    Args
        runningProcName (str): The process to be checked. (e.g. "VRisingServer.exe")
        exeProgPath (str): The program to be executed, can be .bat file. (e.g. "start_server_example_02.bat")
    """
    procList = [p.name() for p in psutil.process_iter()]

    if runningProc not in procList:
        logger.info('\"{}\" is not executing, open process.'.format(runningProc))
        cwd = os.path.dirname(exeProgPath)
        p = sp.Popen(exeProgPath, cwd=cwd)
        stdout, stderr = p.communicate()  # Meaningful logs are in VRisingServer.log, not stdout.
        return p
    else:
        logger.warning('\"{}\" is already executing.'.format(runningProc))
        return None


def main():
    """Main loop """
    proc = None
    while True:
        try:
            p = checkAndExecute(runningProc, exeProgPath)
            if p:
                proc = p
            time.sleep(chkIntrv)

        except KeyboardInterrupt:
            if proc:
                proc.terminate()
            logger.info('Manually interrupted')
            break

        except Exception as e:
            logger.error(e)


if __name__ == '__main__':
    FORMAT = '%(asctime)s [%(levelname)s]: %(message)s'
    logging.basicConfig(filename='simple_cronjob.log', level=logging.DEBUG, format=FORMAT)

    main()