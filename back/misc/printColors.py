# Utility class for printing messages in different colors to the terminal

from datetime import datetime

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Stamp:
    """
    Set up a a schema for messages as needed
    Choosing stamp color and message to be displayed
    """
    def __init__(self, stampColor, stamp):
        self.color = stampColor
        self.stamp = stamp
        self.ENDC = '\033[0m'
        self.timeColor = '\033[92m'
        self.ErrorColor = '\033[91m'
        self.WarningColor = '\033[93m'

    def print_msg(self, msg, error=0):
        """
        :param msg:
        :param error: 0 - No Error 1 - Error 2 - Warning
        :return:
        """
        if error == 1:
            print(f"{self.color}{self.stamp}{self.ENDC} | {self.timeColor}{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')}{self.ENDC} | {self.ErrorColor}{msg}{self.ENDC}")
        elif error == 2:
            print(f"{self.color}{self.stamp}{self.ENDC} | {self.timeColor}{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')}{self.ENDC} | {self.WarningColor}{msg}{self.ENDC}")
        else:
            print(f"{self.color}{self.stamp}{self.ENDC} | {self.timeColor}{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')}{self.ENDC} | {msg}")

    def setStamp(self, newStamp):
        self.stamp = newStamp

    def setColor(self, newColor):
        self.color = newColor


if __name__ == "__main__":
    example = Stamp(stampColor=bcolors.OKGREEN, stamp='DB Message')
    example.print_msg(msg='This is a message from the DB')