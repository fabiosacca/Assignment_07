#------------------------------------------#
# Title: CDInventory.py
# Desc: Working with classes and functions.
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# fabiosacca, 2022-Nov-20, Updated File from starter code. Resolved TODOs
# fabiosacca, 2022-Nov-27, Updated File to handle errors and use binary data for permanent storage
#------------------------------------------#

import pickle

# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
strFileNameB = 'CDInventory.dat'  # data storage file (binary)
objFile = None  # file object


# -- PROCESSING -- #
class DataProcessor:
    """Processing the data held in memory during runtime"""
        
    @staticmethod
    def del_cd(ID, table):
        """Function to manage data removal from list of dictionaries based on user input

        Remove a row from a 2D table (list of dicts) in memory during runtime.

        Args:
            ID: ID to be deleted
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            Confirmation message the CD was removed or not found.
        """
        #TODone: Add structured error handling for user interaction
        ID = IO.del_cd_input()
        intRowNr = -1
        blnCDRemoved = False
        for row in table:
            intRowNr += 1
            if row['ID'] == ID:
                del table[intRowNr]
                blnCDRemoved = True
                break
        if blnCDRemoved:
            print('The CD was removed')
        else:
            print('Could not find this CD in inventory. Try again!')
        
    def add_cd(ID, album, artist, table, row):

        """Function to manage data ingestion from user input to a list of dictionaries

        Adds data from user entry into a 2D table (list of dicts) in memory during runtime.

        Args:
            data (list): values entered by user for ID, CD Title, Artist Name
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            Confirmation message the CD was added to inventory.
        """
        row = {'ID': ID, 'Title': album, 'Artist': artist}
        table.append(row)
        print('The CD was added to Inventory')
        
    def load_inventory(file_name, table):
        
        """Function to process user request to load inventory from file

        Confirms user choice before loading inventory data from runtime and deletes all entries in memory

        Args:
            file_name (string): name of file used to write the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None
        """
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('Type \'yes\' to continue and reload from file. Otherwise reload will be canceled: ')
        if strYesNo.lower() == 'yes':
            print('reloading...')
            FileProcessor.read_file(file_name, table)
            IO.show_inventory(table)
        else:
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.show_inventory(table)
        
     
    def save_inventory(file_name, table):
        
        """Function to process user request to save inventory from file

        Confirms user choice to daves Inventory data from runtime to permanent memory

        Args:
            file_name (string): name of file used to write the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None
        """
        # 3.6.2 Process choice

        while True:
            strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
            if strYesNo == 'y':
        # 3.6.2.1 save data
                FileProcessor.write_file(file_name, table)
                break
            elif strYesNo == 'n':
                input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
                break
            else:
                print('Incorrect choice!! Please try again.\n')
                continue
        
class FileProcessor:
    """Processing the data to and from text file"""
    
    @staticmethod
    # TODone: Modify the permanent data store to use binary data.
    # TODone: Add structured error handling for file access operations.
    def read_file(file_name, table):
        """Function to manage data ingestion from file to a list of dictionaries

        Reads the data from file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.

        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Args:
            fileName (string): name of file used to read the data from
        
        Returns:
            table (list): results from file fileName
        """
        try:
            with open(file_name, 'rb') as fileObj:
                table.clear()
                data = pickle.load(fileObj)
                for i in range(len(data)):
                    table.append(data[i])      
            return table
        except FileNotFoundError as e:
            print('There is no file to open')
            print('\nBuild in error info:', type(e), e, e.__doc__, sep='\n\t')
        except Exception as e:
            print('\nThere was a general error!')
            print('\nBuild in error info:', type(e), e, e.__doc__, sep='\n\t')
            
    @staticmethod
    def write_file(fileName, table):
    # TODone: Modify the permanent data store to use binary data.
    # ToDone: Add structured error handling for file access operations.
        """Function to manage data storage from a list of dictionaries to a binary file

        Saves the data to file identified by file_name from a 2D table
        (list of lists).

        Args:
            file_name (string): name of file used to write the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        try:
            with open(fileName, 'wb') as fileObj:
                pickle.dump(table, fileObj)
        except Exception as e:
            print('\nThere was a general error!')
            print('\nBuild in error info:', type(e), e, e.__doc__, sep='\n\t')
        # Structured error handling for FileNotFound not needed in this case as saving creates a new file. 

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
        print('\nMenu\n\n[l] Load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] Delete CD from Inventory\n[s] Save Inventory to file\n[x] Exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x

        """
        choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            print('Invalid choice. Please select one of the options listed.\n')
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def get_user_input():
        """ Function to get the user input for adding a CD entry

        The entry will be returned to be used by a DataProcessor function that will Add it to inventory.

        Args:
            None
            
        Returns:
            intID (int): User supplied ID for entry
            strTitle (string): Title of CD
            stArtist (string): Name of artist
        """
        #TODone: Add structured error handling for type casting (string to int)
        while True:
            strID = input('\nEnter ID: ').strip()
            try:
                intID = int(strID)
                break
            except ValueError as e:
                print('\nThat is not a valid ID number. Please try again.')
                print('\nBuild in error info:', type(e), e, e.__doc__, sep='\n\t')
            except Exception as e:
                print('\nThere was a general error!')
                print('\nBuild in error info:', type(e), e, e.__doc__, sep='\n\t')
        strTitle = input('What is the CD\'s title? ').strip()
        strArtist = input('What is the Artist\'s name? ').strip()
        return intID, strTitle, strArtist
        
    @staticmethod
    def show_inventory(table):
        """Displays current inventory table

        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.

        """
        print('\n======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================')

    def del_cd_input():
        """Function to get the user input for deleting a CD

        The entry will be returned to be used by a DataProcessor function that will Remove the chosen entry.

        Args:
            None   
         
        Returns:
            ID (int): ID to be deleted
        """
        #TODone: Add structured error handling for user interaction
        while True:
            try:
                intIDDel = int(input('\nWhich ID would you like to delete? ').strip())
                return intIDDel
                break
            except ValueError as e:
                print('\nThat is not a valid ID number. Please try again.')
                print('\nBuild in error info:', type(e), e, e.__doc__, sep='\n\t')
            except Exception as e:
                print('\nThere was a general error!')
                print('\nBuild in error info:', type(e), e, e.__doc__, sep='\n\t')


# 1. When program starts, read in the currently saved Inventory
FileProcessor.read_file(strFileNameB, lstTbl)

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
        DataProcessor.load_inventory(strFileNameB, lstTbl)
        continue  # start loop back at top.

    # 3.3 process add a CD
    elif strChoice == 'a':
        # 3.3.1 Ask user for new ID, CD Title and Artist
        strID, strTitle, stArtist = IO.get_user_input()              
        # 3.3.2 Add item to the table
        DataProcessor.add_cd(strID, strTitle, stArtist, lstTbl, dicRow)    
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
        # 3.5.2 search thru table and delete CD
        DataProcessor.del_cd(dicRow, lstTbl)
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
        
    # 3.6 process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        DataProcessor.save_inventory(strFileNameB, lstTbl)
        continue  # start loop back at top
        
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be save:
    else: 
        print('Invalid choice. Please select one of the options listed.')
        continue  # start loop back at top.
