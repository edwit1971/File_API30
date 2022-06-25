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
#
#############################################
# The code below was supposed to return the
# name and path of the selected file but it
# never did. It kept returning None.
# no idea why, and I couldn't get it to work
#############################################
# filePathColumn = [MediaStore_Images_Media_DATA]; # String[]
# cursor = currentActivity.getContentResolver().query(selectedUri, filePathColumn, None, None, None)
# cursor.moveToFirst()
# columnIndex = cursor.getColumnIndex(filePathColumn[0])
# fileName = cursor.getString(columnIndex)
# cursor.close()
##############################################################

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
    Env = autoclass('android.os.Environment')
    File = autoclass('java.io.File')
    FileInputStream = autoclass('java.io.FileOutputStream')
    FileOutputStream = autoclass('java.io.FileOutputStream')
#    DocumentsContract = autoclass('android.provider.DocumentsContract')
    
    MediaStore_Images_Media_DATA = "_data"  # Value of MediaStore.Images.Media.DATA
    
    def permissions_callback(permissions, results):
        if all([res for res in results]):
            permissions_granted = True
        else:
            permissions_granted = False
    
    def get_permissions():
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


def Read_File(pFile=None, pLabel=None):
    global Global_Label
    Global_Label = pLabel
    String = 'Read_File()\n\nNot Functional Yet'
    if(platform == 'android'):
        if check_permission("android.permission.WRITE_EXTERNAL_STORAGE") \
        and check_permission("android.permission.READ_EXTERNAL_STORAGE") \
        and check_permission("android.permission.INTERNET"):
        # if permissions_granted:   # variant
            SFP_Read_Doc(pRCallback = Callback_Read_URI, \
                         pFile = pFile)
        else:
            get_permissions()
    return String


def Write_File(pFile=None, pLabel=None):
    if(platform == 'android'):
        if check_permission("android.permission.WRITE_EXTERNAL_STORAGE") \
        and check_permission("android.permission.READ_EXTERNAL_STORAGE") \
        and check_permission("android.permission.INTERNET"):
        # if permissions_granted:   # variant
            SFP_Write_Doc(pWCallback = Callback_Write, \
                          pFile = pFile)
        else:
            get_permissions()
    return


####################################################
# Open the SYSTEM FILE PICKER and call callback with
# absolute filepath of document user selected.
# None if user canceled.
####################################################
def SFP_Read_Doc(pRCallback=None, pFile=None):
    if(platform == 'android'):
        currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
        context = cast('android.content.ContextWrapper', currentActivity.getApplicationContext())
        file_p = cast('java.io.File', context.getExternalFilesDir(Env.DIRECTORY_DOWNLOADS))
        
        ##########################################################
        def on_activity_Load(request_code, result_code, intent):
            if request_code != RESULT_LOAD_DOC:
                Logger.warning('***FILE_API30*** : on_activity_Load: result that was not RESULT_LOAD_DOC')
                return
            
            if result_code == Activity.RESULT_CANCELED:
                Clock.schedule_once(lambda dt: pRCallback(), 0)
                return
            
            if result_code != Activity.RESULT_OK:
                # This may just go into the void...
                raise NotImplementedError('***FILE_API30*** : Unknown result_code "{}"'.format(result_code))

            selectedUri = intent.getData();  # Uri
            
            Clock.schedule_once(lambda dt: pRCallback(pURI=selectedUri), 0)

            return

        activity.bind(on_activity_result = on_activity_Load)
        intent = Intent(Intent.ACTION_GET_CONTENT)  # Open the SYSTEM FILE PICKER
        intent.addCategory(Intent.CATEGORY_OPENABLE)
        intent.setType('text/plain')
        intent.putExtra(Intent.EXTRA_ALLOW_MULTIPLE, False)
        intent.setAction(Intent.ACTION_GET_CONTENT)
        currentActivity.startActivityForResult(intent, RESULT_LOAD_DOC)
    return


####################################################
# This Callback function for reading a Text-File
# reads a text file the user selects with the File
# Systen Picker and displays it's content
####################################################
def Callback_Read_URI(pURI=None):
    global Global_Label
    if(Global_Label != None):
        Global_Label.text = '\nURI = ' + str(pURI.toString) + '\n'
    ################################################
    if( (platform == 'android') and (pURI != None) ):
        currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
        
        try:
            docStream = currentActivity.getContentResolver().openInputStream(pURI)
        except:
            docStream = None
            
        if(docStream != None):
            ints = []
            intVal = docStream.read()
            while intVal != -1:
                ints.append(intVal)
                intVal = docStream.read()
            docStream.close()
            # Convert the array to bytes
            docBytes = bytes(b % 256 for b in ints)
            Global_Label.text += '\n\n' + str(docBytes)
        else:
            Global_Label.text += '\n\n openInputStream Failed'
    return


####################################################
# This Callback function for reading a Text-File
# reads a hard-coded file shit.txt in the download
# folder and displays it's content
####################################################
def Callback_Read_FilePath(pFName=None):
    global Global_Label
    if(Global_Label != None):
        Global_Label.text = '\nfilename = ' + str(pFName) + '\n'
    ################################################
    if( (platform == 'android') and (pFName != None) ):
        currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
        
        try:
            # I got this string from the command
            # Logger.info('***FILE_API30*** : pURI.toString = %s', pURI.toString())
            strContent = 'content://com.android.externalstorage.documents/document/primary%3ADownload%2Fshit.txt'
            fUri = Uri.parse(strContent)
        except:
            Logger.info('***FILE_API30*** : fUri = Uri.parse(strContent) THREW ERROR')
        
        try:
            pfd = currentActivity.getContentResolver().openFileDescriptor(fUri, "r")
        except:
            Logger.info('***FILE_API30*** : pfd = openFileDescriptor(fUri) THREW ERROR')
        
        try:
            docStream = FileInputStream(pfd.getFileDescriptor())
        except:
            Logger.info('***FILE_API30*** : FileInputStream(pfd.getFileDescriptor()) THREW ERROR')
        
        docStream = None
        if(docStream != None):
            ints = []
            intVal = docStream.read()
            while intVal != -1:
                ints.append(intVal)
                intVal = docStream.read()
            docStream.close()
            # Convert the array to bytes
            docBytes = bytes(b % 256 for b in ints)
            Global_Label.text += '\n\n' + str(docBytes)
            Logger.info('***FILE_API30*** : docBytes = %s', str(docBytes))
        else:
            Global_Label.text += '\n\n openInputStream Failed'
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


# fileName = 'None'
# filePaths = selectedUri.getPath()
# Length = len(filePaths)
# if( (Length > 1) and (filePaths.find(':') != -1) ):
#     # Extract the filename they selected
#     n = filePaths.find(':Download/')
#     if(n != -1):
#         # Hard-code the path of the file to be the
#         # internal storage of the Download folder
#         # with the getExternalStoragePublicDirectory(Env.DIRECTORY_DOWNLOADS).toString()
#         dwnldPath = Env.getExternalStoragePublicDirectory(Env.DIRECTORY_DOWNLOADS).toString()
#         fileName = os.path.join(dwnldPath, filePaths[(n+10):Length])

