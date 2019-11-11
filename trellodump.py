#-------------------------------------------------------------------------------
# Name:        trellodump
# Purpose:
#
# Author:      Lorenzo Bolognese
#
# Created:     05/11/2019
# Copyright:   (c) Lorenzo Bolognese 2019
# Licence:     MIT License
#-------------------------------------------------------------------------------

# Included libraries
import datetime
import sys
import time

# User libraries
import trelloauth
import misc

# py-trello (https://pypi.org/project/py-trello)
from trello import TrelloClient

class MainData(object):
    """
    Trello account: grants access to its boards, lists and cards
    """

    def __init__(self, fileName,  debug = True):
        self.fileName = fileName
        self.debug = debug

    def __GetClientBoards(self, client):
        try: return client.list_boards()
        except Exception as e:
            self.__PrintOut("ERROR: unable to get boards. Details: " + str(e))
            return []

    def __GetBoardLists(self, board):
        try: return board.list_lists()
        except Exception as e:
            self.__PrintOut("ERROR: unable to get lists. Details: " + str(e))
            return []

    def __GetListCards(self, tlist):
        try: return tlist.list_cards()
        except Exception as e:
            self.__PrintOut("ERROR: unable to get cards. Details: " + str(e))
            return []

    def __PrintOut(self, text):
        if self.debug == True: print(text)
        f = open(self.fileName, "a")
        f.write(text + "\n")
        f.close()

    def AuthorizeByTrelloRoute(self, apiKey, apiSecret):
        # Less safe since that's method always uses un-variable credentials

        self.client = TrelloClient(
                    api_key = apiKey,
                    api_secret = apiSecret,
                    )
        return 0, None

    def AuthorizeByOAuth(self, apiKey, oAuthSecret):
        # Uses API Key and OAuth key to enquire for a temporary access token (expiration: 1 hour)

        try:
            credentials = trelloauth.CreateOauthToken(expiration="1hour", key=apiKey, secret=oAuthSecret, output=False)
            self.client = TrelloClient(
                        api_key = apiKey,
                        token = credentials['oauth_token'],
                        token_secret = credentials['oauth_token_secret']
                        )
            res = 0
            excptn = None
        except Exception as e:
            res = -1
            excptn = e
        finally:
            return res, excptn

    def Report(self):
        boards = self.__GetClientBoards(self.client)
        for b in boards:
            self.__PrintOut("PROJECT: " + b.name)
            lists = self.__GetBoardLists(b)
            for l in lists:
                self.__PrintOut("    " + l.name.upper())
                cards = self.__GetListCards(l)
                if len(cards) == 0:
                    self.__PrintOut("        --- Void ---")
                else:
                    id = 1
                    for c in cards:
                        if c.due is not None: dueDate = "--> " + c.due[:10]
                        else:                 dueDate = "--> TBD"
                        self.__PrintOut("        " + str(id) + ") " + c.name + " " + dueDate)
                        if len(c.desc) > 0: desc = self.__PrintOut("            " + c.desc.replace("\n", "\n            "))
                        id = id + 1
            self.__PrintOut("")
        self.__PrintOut("Report date and time: " + str(datetime.datetime.now()))

if __name__ == '__main__':
    startTime = datetime.datetime.now()
    print("Trello boards, lists and cards dumper")

    # Get settings from INI file
    res, excptn, dbgEn, reportPath, apiKey, apiSecret, oAuthSecret, oAuthEn = misc.GetSettings('config.ini')
    if res == 0:

        # Check if the destination folder exists and create txt report file
        res, excptn = misc.CreateFile(reportPath)
        if res == 0:
            # Authentication: two methods
            prjBoards = MainData(reportPath, dbgEn)

            if oAuthEn == True:
                print('Authentication by OAuth: please grant the permission on your browser and copy and past the PIN you get')
                res, excptn = prjBoards.AuthorizeByOAuth(apiKey, oAuthSecret)
            else:
                print('Authentication by Trello route')
                res, excptn = prjBoards.AuthorizeByTrelloRoute(apiKey, apiSecret)
            if res == 0:
                # Authorization gone fine: fill report
                print("Please wait while filling " + reportPath + "...")
                prjBoards.Report()
                print("Done!!!\n")
            else:
                print("Unable to proceed. Missing authorization: " + str(excptn) + "\n")
        else:
            print("ERROR: output folder is missing. Details: " + str(e) + "\n")
    else:
        print("Unable to proceed. INI file is wrong: " + str(excptn) + "\n")

    print("Execution time: " + str(datetime.datetime.now() - startTime))
    input("Press Enter to continue...")
