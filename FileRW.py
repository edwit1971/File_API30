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
# selectedUri = intent.getData();  # Uri
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


def Read_File(pLabel=None):
    global Global_Label
    Global_Label = pLabel
    if(platform == 'android'):
        if check_permission("android.permission.WRITE_EXTERNAL_STORAGE") \
        and check_permission("android.permission.READ_EXTERNAL_STORAGE") \
        and check_permission("android.permission.INTERNET"):
            #SFP_Read_Doc(pRCallback = Callback_Read_FilePath)
            SFP_Read_Doc(pRCallback = Callback_Read_URI)
        else:
            get_permissions()
    return


def Write_File(pLabel=None):
    global Global_Label
    Global_Label = pLabel
    if(platform == 'android'):
        if check_permission("android.permission.WRITE_EXTERNAL_STORAGE") \
        and check_permission("android.permission.READ_EXTERNAL_STORAGE") \
        and check_permission("android.permission.INTERNET"):
            SFP_Write_Doc(pWCallback = Callback_Write_URI)
        else:
            get_permissions()
    return


####################################################
# Open the SYSTEM FILE PICKER and call callback with
# absolute filepath of document user selected.
# None if user canceled.
####################################################
def SFP_Read_Doc(pRCallback=None):
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
            Clock.schedule_once(lambda dt: pRCallback(pURI=selectedUri), 0)  # Calls URI Callback
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
    if(pURI == None):
        return
    global Global_Label
    if(Global_Label != None):
        Global_Label.text = '\nURI = ' + str(pURI.toString()) + '\n'
    ################################################
    if(platform == 'android'):
        currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
        
        try:
            docStream = currentActivity.getContentResolver().openInputStream(pURI)
        except:
            docStream = None
            
        if(docStream != None):
            str1 = ''
            intVal = docStream.read()  # Reads Raw Values
            while intVal != -1:
                str1 += str(chr(intVal))
                intVal = docStream.read()
            docStream.close()
            # Convert the array to bytes so we
            # can display the file as text
            Global_Label.text += '\n\n' + str1
        else:
            Global_Label.text += '\n\n openInputStream Failed'
    return


####################################################
# This Callback function for reading a Text-File
# reads a hard-coded file File_API30.txt in the 
# download folder and displays it's content
# (You can change it to whatever you want though)
####################################################
def Callback_Read_FilePath(pURI=None):
    global Global_Label
    if(Global_Label != None):
        Global_Label.text = '\nfilename = File_API30.txt\n'
    ################################################
    if(platform == 'android'):
        currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
        
        try:
            # File_API30.txt Hard-Coded
            # I got strContent from the command
            # pURI.toString() in the Logger ADB view
            # Logger.info('***FILE_API30*** : pURI.toString = %s', pURI.toString())
            strContent = 'content://com.android.externalstorage.documents/document/primary%3ADownload%2FFile_API30.txt'
            fUri = Uri.parse(strContent)
        except:
            Logger.info('***FILE_API30*** : fUri = Uri.parse(strContent) THREW ERROR')
        
        try:
            docStream = currentActivity.getContentResolver().openInputStream(fUri) # Fails
            # docStream = currentActivity.getContentResolver().openInputStream(pURI) # Succeeds
        except:
            Logger.info('***FILE_API30*** : docStream = openInputStream(fUri) THREW ERROR')
            Logger.info('***FILE_API30*** : pURI.toString() = %s', pURI.toString())
            Logger.info('***FILE_API30*** : fUri.toString() = %s', fUri.toString())
            Logger.info('***FILE_API30*** : pURI.getPath() = %s', pURI.getPath())
            Logger.info('***FILE_API30*** : fUri.getPath() = %s', fUri.getPath())
            Logger.info('***FILE_API30*** : pURI.getScheme() = %s', pURI.getScheme())
            Logger.info('***FILE_API30*** : fUri.getScheme() = %s', fUri.getScheme())
            docStream = None
        
        if(docStream != None):
            str1 = ''
            intVal = docStream.read()  # Reads Raw Values
            while intVal != -1:
                str1 += str(chr(intVal))
                intVal = docStream.read()
            docStream.close()
            # Convert the array to bytes so we
            # can display the file as text
            Global_Label.text += '\n\n' + str1
        else:
            Global_Label.text += '\n\n openInputStream Failed'
    return
    

####################################################
# Open the SYSTEM FILE PICKER and call callback with
# absolute filepath of document to save.
# None if user canceled.
####################################################
def SFP_Write_Doc(pWCallback=None):
    if(platform == 'android'):
        currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
        
        #########################################################
        def on_activity_Save(request_code, result_code, intent):
            if(request_code != CREATE_FILE):
                Logger.warning('***FILE_API30*** : on_activity_Save: result that was not RESULT_SAVE_DOC')
                return
            
            if(result_code == Activity.RESULT_CANCELED):
                Clock.schedule_once(lambda dt: pWCallback(), 0)
                return
            
            if result_code != Activity.RESULT_OK:
                # This may just go into the void...
                raise NotImplementedError('***FILE_API30*** : Unknown result_code "{}"'.format(result_code))
                
            selectedUri = intent.getData() # Uri
            Clock.schedule_once(lambda dt: pWCallback(selectedUri), 0)
            return
        
        activity.bind(on_activity_result = on_activity_Save)
        # Here's another Intent in contrast to get the file
        intent = Intent(Intent.ACTION_CREATE_DOCUMENT)
        intent.addCategory(Intent.CATEGORY_OPENABLE)
        intent.setType('text/plain')
        currentActivity.startActivityForResult(intent, CREATE_FILE)
    return
    

####################################################
def Callback_Write_URI(pURI = None):
    if(pURI == None):
        return
    global Global_Label
    if(platform == 'android'):
        currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
        
        try:
            docStream = currentActivity.getContentResolver().openOutputStream(pURI)
        except:
            docStream = None
            
        if(docStream != None):
            try:
                ints = []
                # Convert String Data to BYTE data
                for n in range(0, len(String_Data)):
                    intVal = ord(String_Data[n])
                    ints.append(intVal)
                docStream.write(ints, 0, len(ints))
                docStream.close()
            except:
                Logger.warning('***FILE_API30*** : docStream.write(ints, 0, len(ints)) THREW ERROR!!!')
            Global_Label.text  = 'Path = ' + str(pURI.getPath())
            Global_Label.text += '\n\n File Written'
        else:
            Global_Label.text = '\n\n openOutputStream Failed'
    return


def Get_Internal_Path():
    ret = ''
    if(platform == 'android'):
        try:
            # ret = Env.getExternalStoragePublicDirectory(Env.DIRECTORY_DOWNLOADS).toString() # This works too
            # from android.storage import primary_external_storage_path
            # ret = primary_external_storage_path() # This works too
            ret = Env.getExternalStorageDirectory()
        except:
            ret = ''
    return ret


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

