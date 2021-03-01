#------------------------------------------#
# Title: CDInventory.py
# Desc: Working with classes and functions.
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# BReinhart, 2021-Feb-20, Moved add CD, delete CD, write to file functionality to functions
# BReinhart, 2021-Feb-21, Added Doc Strings to functions
# BReinhart, 2021-Feb-28, Added error handling
# BReinhart, 2021-Feb-28, Converted to binary data
#------------------------------------------#

import pickle

# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # dictionary of data row
strFileName = 'CDInventory.dat'  # binary data storage file
objFile = None  # file object


# -- PROCESSING -- #
class DataProcessor:
    """Processing the data to add or delete a CD"""

    @staticmethod
    def add_CD(cdData, table):
        """Function to add a new row of data to the inventory
        
        Takes in the data from the cdData list and puts it in a new row (dictionary) to add to the 
        2D table (list of dicts) specified by table
        
        Args:
            cdData (list of strings): list of user inputted data (strings) for the new cd
            table (list of dicts): 2D data structure (list of dicts) that holds the data during runtime
        
        Returns:
            None.
            
        """
        dicRow = {'ID': cdData[0], 'Title': cdData[1], 'Artist': cdData[2]}
        table.append(dicRow)

    @staticmethod
    def del_CD(delRow, table):
        """Function to delete a row of data from the inventory
        
        Takes a user inputted row ID, delRow, to remove from 2D table (list of dicts), table. 
        
        Args:
            delRow (integer): user inputted integer of CD ID to delete
            table (list of dicts): 2D data structure (list of dicts) that hold the data during runtime
        
        Returns:
            None.
            
        """
        intRowNr = -1
        blnCDRemoved = False
        for row in table:
            intRowNr += 1
            if row['ID'] == delRow:
                del table[intRowNr]
                blnCDRemoved = True
                break
        return blnCDRemoved

class FileProcessor:
    """Processing the data to and from binary file"""

    @staticmethod
    def read_file(file_name, table):
        """Function to manage data ingestion from binary file to a list of dictionaries

        Reads the data from file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.

        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
            
        """
        table.clear()  # this clears existing data and allows to load data from file
        try:
            with open(file_name, 'rb') as objFile:
                data = pickle.load(objFile)
                for row in data:
                    table.append(row)
        except pickle.UnpicklingError as e:
            print('Data could not be unpickled! Data not loaded!')
            print('Built in error info:')
            print(type(e), e, e.__doc__, sep='\n')
        except FileNotFoundError as e:
            print('File does not exist! Data not loaded!')
            print('Built in error info:')
            print(type(e), e, e.__doc__, sep='\n')

    @staticmethod
    def write_file(file_name, table):
        """Function to manage data saving from a list of dictionaries to a file

        Saves the data from a 2D table (list of dicts) identified by table.
        Each dictionary row in table is saved as a line to the file identified by file_name.
        
        Args:
            file_name (string): name of file used to save the data to
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
            
        """
        try:
            with open(file_name, 'wb') as objFile:
                pickle.dump(table, objFile)
        except pickle.PicklingError as e:
            print('Data cannot be pickled! does not exist!')
            print('Built in error info:')
            print(type(e), e, e.__doc__, sep='\n')
        except FileNotFoundError as e:
            print('File does not exist!')
            print('Built in error info:')
            print(type(e), e, e.__doc__, sep='\n')

# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
            
        """

        print('Menu\n\n[l] Load Inventory from File\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] Delete CD from Inventory\n[s] Save Inventory to File\n[x] Exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x

        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            try:
                choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
            except Exception as e:
                print('There is a general error!')
                print('Built in error info:')
                print(type(e), e, e.__doc__, sep='\n')
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table

        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.

        """
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by: {})'.format(*row.values()))
        print('======================================')

    @staticmethod
    def cd_input():
        """Gets user input for adding a CD to inventory
        
        Args:
            None.
        
        Returns:
            [strID (string), strTitle (string), strArtist (string)]: 
                a list of strings of the users input for the new CD ID, Title and Artist
                
        """
        try:
            strID = input('Enter ID: ').strip()
            strTitle = input('What is the CD\'s title? ').strip()
            strArtist = input('What is the Artist\'s name? ').strip()
        except Exception as e:
            print('There is a general error!')
            print('Built in error info:')
            print(type(e), e, e.__doc__, sep='\n')
        return [strID, strTitle, strArtist]

# 1. When program starts, read in the currently saved Inventory
FileProcessor.read_file(strFileName, lstTbl)

# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()

    # 3. Process menu selection
    # 3.1 process exit first
    if strChoice == 'x':
        break
    # 3.2 process load inventory
    if strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        try:
            strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled')
        except Exception as e:
            print('There is a general error!')
            print('Built in error info:')
            print(type(e), e, e.__doc__, sep='\n')
        if strYesNo.lower() == 'yes':
            print('reloading...')
            FileProcessor.read_file(strFileName, lstTbl)
            IO.show_inventory(lstTbl)
        else:
            try:
                input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            except Exception as e:
                print('There is a general error!')
                print('Built in error info:')
                print(type(e), e, e.__doc__, sep='\n')
            IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.3 process add a CD
    elif strChoice == 'a':
        # 3.3.1 Ask user for new ID, CD Title and Artist
        addedCD = IO.cd_input()
        
        while True:
            try:
                addedCD[0] = int(addedCD[0])
                break
            except ValueError as e:
                print('ID entered is not an integer!')
                print('Built in error info:')
                print(type(e), e, e.__doc__, sep='\n')
                addedCD[0] = input('Please re-enter the ID as an integer: ')

        # 3.3.2 Add item to the table
        DataProcessor.add_CD(addedCD, lstTbl)
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.5 process delete a CD
    elif strChoice == 'd':
        # 3.5.1 get Userinput for which CD to delete
        # 3.5.1.1 display Inventory to user
        IO.show_inventory(lstTbl)
        # 3.5.1.2 ask user which ID to remove
        while True:
            try:
                intIDDel = int(input('Which ID would you like to delete? ').strip())
                break
            except ValueError as e:
                print('That is not an integer! ')
                print('Built in error info:')
                print(type(e), e, e.__doc__, sep='\n')
            except Exception as e:
                print('There is a general error')
                print('Built in error info:')
                print(type(e), e, e.__doc__, sep='\n')
        # 3.5.2 search thru table and delete CD
        blnCDRemoved = DataProcessor.del_CD(intIDDel, lstTbl)
        if blnCDRemoved:
            print('The CD was removed')
        else: 
            print('Could not find this CD!')
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.6 process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        try:
            strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
            # 3.6.2 Process choice
            if strYesNo == 'y':
                # 3.6.2.1 save data
                FileProcessor.write_file(strFileName, lstTbl)
            else:
                input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        except Exception as e:
            print('There is a general error!')
            print('Built in error info:')
            print(type(e), e, e.__doc__, sep='\n')
        continue  # start loop back at top.
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be save:
    else:
        print('General Error')




