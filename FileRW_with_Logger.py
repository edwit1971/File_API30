##############################################################
#
# FileRW.py  created June 2022
#
# All the Functions needed to Read and Write a File
# on an Android device running API30+
#
#
# Using ADB Shell
#
# 1) connect device via USB
# 2) adb start-server : also adb kill-server when needed
# 3) adb devices -l : lists devices connected
#
# 4) install manually or use adb
# 4) adb -s <device> install File_API30.apk : must be inside BIN folder
#
# 5) launch File_API30.apk manually on device
# 6) adb shell pidof com.handgems.file_api30 : all lowercase
# 7) adb logcat --pid=<pid>
# 8) ctrl-c to break
#
#
# adb shell ps : show all processes running
# adb logcat : to get entire logcat
#
##############################################################


#from pathlib import Path
#p = Path(pDest)
#p.as_uri()

import io
import os
import json

from kivy.utils import platform

Global_Label = None

####################################################
####################################################
if platform == 'android':
    from kivy.logger import Logger
    from kivy.clock import Clock
    from jnius import autoclass
    from jnius import cast
    from android import activity
    from android.permissions import Permission, request_permissions, check_permission

    Activity = autoclass('android.app.Activity')
    PythonActivity = autoclass("org.kivy.android.PythonActivity")
    Intent = autoclass('android.content.Intent')
    Uri = autoclass('android.net.Uri')
    File = autoclass('java.io.File')
    Env = autoclass('android.os.Environment')
    FileOutputStream = autoclass('java.io.FileOutputStream')
#    DocumentsContract = autoclass('android.provider.DocumentsContract')
    
    MediaStore_Images_Media_DATA = "_data"  # Value of MediaStore.Images.Media.DATA
    
    def permissions_callback(permissions, results):
        Logger.info('***FILE_API30*** : def permissions_callback()...')
        if all([res for res in results]):
            permissions_granted = True
        else:
            permissions_granted = False
    
    def get_permissions():
        Logger.info('***FILE_API30*** : def get_permissions()...')
        request_permissions([
            Permission.WRITE_EXTERNAL_STORAGE,
            Permission.READ_EXTERNAL_STORAGE,
            Permission.INTERNET],
            permissions_callback)

    # Custom request codes
    RESULT_LOAD_DOC = 1
    CREATE_FILE = 1
####################################################
####################################################


################################################
################################################
# From the received Uri I am getting a data stream

#selectedUri = intent.getData()
#docStream = currentActivity.getContentResolver().openInputStream(selectedUri)

# I get an int array from the stream
#ints = []
#intVal = docStream.read()

#while intVal != -1:
#    ints.append(intVal)
#    intVal = docStream.read()

# And convert the array to bytes and pass it to the callback function
#docBytes = bytes(b % 256 for b in ints)
#Clock.schedule_once(lambda dt: callback(docBytes), 0)
################################################
################################################

def Read_File(pFile=None, pLabel=None):
    global Global_Label
    Global_Label = pLabel
    String = 'Read_File()\n\nNot Functional Yet'
    if(platform == 'android'):
        Logger.info('***FILE_API30*** : def Read_File()...start')
        if check_permission("android.permission.WRITE_EXTERNAL_STORAGE") \
        and check_permission("android.permission.READ_EXTERNAL_STORAGE") \
        and check_permission("android.permission.INTERNET"):
        # if permissions_granted:   # variant
            SFP_Read_Doc(pRCallback = Callback_Read, \
                         pFile = pFile)
        else:
            get_permissions()
        Logger.info('***FILE_API30*** : def Read_File()...end')
    return String


def Write_File(pFile=None, pLabel=None):
    if(platform == 'android'):
        Logger.info('***FILE_API30*** : def Write_File()...start')
        if check_permission("android.permission.WRITE_EXTERNAL_STORAGE") \
        and check_permission("android.permission.READ_EXTERNAL_STORAGE") \
        and check_permission("android.permission.INTERNET"):
        # if permissions_granted:   # variant
            SFP_Write_Doc(pWCallback = Callback_Write, \
                          pFile = pFile)
        else:
            get_permissions()
        Logger.info('***FILE_API30*** : def Write_File()...end')
    return


####################################################
# Open the SYSTEM FILE PICKER and call callback with
# absolute filepath of document user selected.
# None if user canceled.
####################################################
def SFP_Read_Doc(pRCallback=None, pFile=None):
    if(platform == 'android'):
        Logger.info('***FILE_API30*** : def SFP_Read_Doc()...start')
        currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
        context = cast('android.content.ContextWrapper', currentActivity.getApplicationContext())
        file_p = cast('java.io.File', context.getExternalFilesDir(Env.DIRECTORY_DOWNLOADS))
        
        ##########################################################
        def on_activity_Load(request_code, result_code, intent):
            Logger.info('***FILE_API30*** : def on_activity_Load()...start')
            Logger.info('***FILE_API30*** : request_code = %s', str(request_code))
            Logger.info('***FILE_API30*** : result_code = %s', str(result_code))
            if request_code != RESULT_LOAD_DOC:
                Logger.warning('***FILE_API30*** : on_activity_Load: result that was not RESULT_LOAD_DOC')
                return
            
            Logger.info('***FILE_API30*** : Activity.RESULT_CANCELED = %s', str(Activity.RESULT_CANCELED))
            if result_code == Activity.RESULT_CANCELED:
                Clock.schedule_once(lambda dt: pRCallback(None), 0)
                return
            
            Logger.info('***FILE_API30*** : Activity.RESULT_OK = %s', str(Activity.RESULT_OK))
            if result_code != Activity.RESULT_OK:
                # This may just go into the void...
                raise NotImplementedError('***FILE_API30*** : Unknown result_code "{}"'.format(result_code))

            selectedUri = intent.getData();  # Uri
            Logger.info('***FILE_API30*** : selectedUri = %s', str(selectedUri))
            Logger.info('***FILE_API30*** : selectedUri = %s', str(selectedUri.toString()))
            Logger.info('***FILE_API30*** : getScheme() = %s', str(selectedUri.getScheme()))
            Logger.info('***FILE_API30*** :   getPath() = %s', str(selectedUri.getPath()))
            
            # str(selectedUri.getScheme())) == 'content'
                
            filePathColumn = [MediaStore_Images_Media_DATA]; # String[]
            Logger.info('***FILE_API30*** : filePathColumn = %s', str(filePathColumn))
            
            # Cursor
            cursor = currentActivity.getContentResolver().query(selectedUri, filePathColumn, None, None, None)
            # cursor = currentActivity.getContentResolver().query(selectedUri, None, None, None, None)
            cursor.moveToFirst()
            Logger.info('***FILE_API30*** : cursor = %s', str(cursor))

            # int
            columnIndex = cursor.getColumnIndex(filePathColumn[0])
            Logger.info('***FILE_API30*** : columnIndex = %s', str(columnIndex))
            
            # fileName = cursor.getString(columnIndex)
            cursor.close()
            
            filePaths = selectedUri.getPath()
            Length = len(filePaths)
            Logger.info('***FILE_API30*** : Length = %s', str(Length))
            if( (Length > 1) and (filePaths.find(':') != -1) ):
                n = filePaths.find(':')
                Logger.info('***FILE_API30*** : n = %s', str(n))
                n = filePaths.find('/', n)
                Logger.info('***FILE_API30*** : n = %s', str(n))
                dwnldPath = Env.getExternalStoragePublicDirectory(Env.DIRECTORY_DOWNLOADS).toString()
                Logger.info('***FILE_API30*** : dwnldPath = %s', str(dwnldPath))
                fileName = os.path.join(dwnldPath, filePaths[(n+1):Length])
            else:
                fileName = 'None'
            Logger.info('***FILE_API30*** : fileName = %s', str(fileName))
            
            Clock.schedule_once(lambda dt: pRCallback(fileName), 0)
            Logger.info('***FILE_API30*** : def on_activity_Load()...end')
            return

        activity.bind(on_activity_result = on_activity_Load)
        # intent = Intent(Intent.ACTION_OPEN_DOCUMENT)  # Open the SYSTEM FILE PICKER
        intent = Intent(Intent.ACTION_GET_CONTENT)  # Open the SYSTEM FILE PICKER
        intent.addCategory(Intent.CATEGORY_OPENABLE)
        intent.setType('text/plain')
        intent.putExtra(Intent.EXTRA_TITLE, "File_API30.txt")
        intent.putExtra(Intent.EXTRA_ALLOW_MULTIPLE, False)
        # intent.putExtra(DocumentsContract.EXTRA_INITIAL_URI, initialURI)
        intent.setAction(Intent.ACTION_GET_CONTENT)
        currentActivity.startActivityForResult(intent, RESULT_LOAD_DOC)
        Logger.info('***FILE_API30*** : def SFP_Read_Doc()...end')
    return


####################################################
def Callback_Read(filename):
    global Global_Label
    if(Global_Label != None):
        Global_Label.text = '\nfilename = ' + str(filename) + '\n'
    if( (filename != None) and (os.path.isfile(filename)) ):
        if(platform == 'android'):
            Logger.info('***FILE_API30*** : def Callback_Read()...start')
            Logger.info('***FILE_API30*** : filename = %s', str(filename))
            with io.open(filename, encoding='utf-8') as file:
                data = None
                try:
                    Logger.info('***FILE_API30*** : data = json.load(file)')
                    data = json.load(file)
                except:
                    Logger.info('***FILE_API30*** : ERROR data = json.load(file)')
            Logger.info('***FILE_API30*** : def Callback_Read()...end')
    return
    

####################################################
# Open the SYSTEM FILE PICKER and call callback with
# absolute filepath of document to save.
# None if user canceled.
####################################################
def SFP_Write_Doc(pWCallback=None, pFile=None):
    if(platform == 'android'):
        Logger.info('***FILE_API30*** : def SFP_Write_Doc()...start')
        currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
        
        #########################################################
        def on_activity_Save(request_code, result_code, intent):
            Logger.info('***FILE_API30*** : def on_activity_Save()...start')
            Logger.info('***FILE_API30*** : request_code = %s', str(request_code))
            Logger.info('***FILE_API30*** : result_code = %s', str(result_code))
            if(request_code != CREATE_FILE):
                Logger.warning('***FILE_API30*** : on_activity_Save: result that was not RESULT_SAVE_DOC')
                return
            
            Logger.info('***FILE_API30*** : Activity.RESULT_CANCELED = %s', str(Activity.RESULT_CANCELED))
            if(result_code == Activity.RESULT_CANCELED):
                Clock.schedule_once(lambda dt: pWCallback(None), 0)
                return
            
            Logger.info('***FILE_API30*** : Activity.RESULT_OK = %s', str(Activity.RESULT_OK))
            if result_code != Activity.RESULT_OK:
                # This may just go into the void...
                raise NotImplementedError('***FILE_API30*** : Unknown result_code "{}"'.format(result_code))
                
            selectedUri = intent.getData() # Uri
            Logger.info('***FILE_API30*** : selectedUri = %s', str(selectedUri))
            Logger.info('***FILE_API30*** : selectedUri.getPath = %s', str(selectedUri.getPath()))
            
            filePathColumn = [MediaStore_Images_Media_DATA] # String
            Logger.info('***FILE_API30*** : filePathColumn = %s', str(filePathColumn))
            
            # Cursor
            cursor = currentActivity.getContentResolver().query(selectedUri, filePathColumn, None, None, None)
            Logger.info('***FILE_API30*** : cursor = %s', str(cursor))
            cursor.moveToFirst()
            
            columnIndex = cursor.getColumnIndex(filePathColumn[0])  # int
            Logger.info('***FILE_API30*** : columnIndex = %s', str(columnIndex))
            
            fileName = cursor.getString(columnIndex) # String
            Logger.info('***FILE_API30*** : on_activity_Load() : selected = %s', str(fileName))
            
            cursor.close()
            
            Logger.info('***FILE_API30*** : on_activity_Save() selectedUri.getPath() = %s', selectedUri.getPath())
            
###            Clock.schedule_once(lambda dt: pWCallback(selectedUri), 0)

            Logger.info('***FILE_API30*** : def on_activity_Save()...end')
            return
        
        activity.bind(on_activity_result = on_activity_Save)
        # Here's another Intent in contrast to get the file
        intent = Intent(Intent.ACTION_CREATE_DOCUMENT)
        intent.addCategory(Intent.CATEGORY_OPENABLE)
        intent.setType('text/plain')
        intent.putExtra(Intent.EXTRA_TITLE, "File_API30.txt")
        currentActivity.startActivityForResult(intent, CREATE_FILE)
        Logger.info('***FILE_API30*** : def SFP_Write_Doc()...end')
    return
    

####################################################
def Callback_Write(uri):
    if(platform == 'android'):
        Logger.info('***FILE_API30*** : def Callback_Write()...start')
        currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
        # Just some function that returns binary data from somewhere to write to uri
        
        bytedata = []
        Read_BinaryFile(pData = bytedata)
        if(len(bytedata) > 0):
            try:
                # For writing, it is important to get ParcelFileDescriptor from ContentResolver ...
                pfd = currentActivity.getContentResolver().openFileDescriptor(uri, "w")
                
                # ... because from ParcelFileDescriptor you need to use getFileDescriptor() function,
                # which will allow us to create a FileOutputStream (and not a regular OutputStream), ...
                fos = FileOutputStream(pfd.getFileDescriptor())
                
                # ... because FileOutputStream can access the OutputStream channel,
                fos_ch = fos.getChannel()
                
                # ... so that after writing data to a file ...
                fos.write(bytedata)
                
                # ... this channel was able to cut off extra bytes if the number of newly written bytes was less than in the file being rewritten.
                fos_ch.truncate(len(bytedata))
                
                fos.close()
                
                # I save the uri in case of a quick overwrite, so you do not open every time the android file selection window
                openedUri = uri
                
            except:
                print('Saving bytedata failed.')
        Logger.info('***FILE_API30*** : def Callback_Write()...end')


####################################################
def Read_BinaryFile(pData = None):
    if(platform == 'android'):
        Logger.info('***FILE_API30*** : def Read_BinaryFile()...start')
        fo = open("loneliness.txt", "rb")
        if(fo != None):
            byte = fo.read(1)
            while(byte):
                pData.append(byte)
                byte = fo.read(1)
            fo.close()
        Logger.info('***FILE_API30*** : def Read_BinaryFile()...end')
    return 


####################################################
####################################################

String_Data  = 'There is in certain living souls,\n'
String_Data += 'a quality of loneliness unspeakable,\n'
String_Data += 'so great it must be shared,\n'
String_Data += 'as company is shared by lesser beings,\n'
String_Data += 'such a loneliness is mine.\n'
String_Data += 'So know by this,\n'
String_Data += 'that in immensity,\n'
String_Data += 'there is one lonelier than you.\n\n'
String_Data += 'by Theodore Sturgeon'

