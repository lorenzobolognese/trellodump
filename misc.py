#-------------------------------------------------------------------------------
# Name:        misc
# Purpose:
#
# Author:      Lorenzo Bolognese
#
# Created:     08/11/2019
# Copyright:   (c) Lorenzo Bolognese 2019
# Licence:     MIT License
#-------------------------------------------------------------------------------

import configparser

def GetSettings(configurationFile):
    """
    Returns configuration parameters of "config.ini" file
    """

    config = configparser.ConfigParser()
    try:
        config.read(configurationFile)
        debugPrintoutEnable = config.getboolean('SETTINGS', 'debug_printout_enable')
        reportFileNameAndPath = config.get('SETTINGS', 'report_file_name_and_path')
        oAuthEnable = config.getboolean('SETTINGS', 'oauth_authentication_enable')
        trelloApiKey = config.get('TRELLO_API', 'api_key')
        trelloApiSecret = config.get('TRELLO_API', 'api_secret')
        trelloOAuthSecret = config.get('TRELLO_API', 'oauth_secret')
        return 0, None, debugPrintoutEnable, reportFileNameAndPath, trelloApiKey, trelloApiSecret, trelloOAuthSecret, oAuthEnable
    except Exception as e:
        return -1, e, False, "", "", "", "", False

def CreateFile(fileName):
    """
    Create an empty file as per passed path and name
    """

    try:
        f = open(fileName, "w+")
        f.close()
        return 0, None
    except Exception as e:
        return -1, e

if __name__ == '__main__':
    pass