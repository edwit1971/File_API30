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
    RESULT_SAVE_DOC = 1
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
    String = 'Read_File()\n\nNot Functional Yet'
    if(platform == 'android'):
        Logger.info('***FILE_API30*** : def Read_File()...start')
        if check_permission("android.permission.WRITE_EXTERNAL_STORAGE") \
        and check_permission("android.permission.READ_EXTERNAL_STORAGE") \
        and check_permission("android.permission.INTERNET"):
        # if permissions_granted:   # variant
            OFC_Read_Doc(pRCallback = Callback_Read, \
                         pFile = pFile, \
                         pLabel = pLabel)
            if(pLabel != None):
                pLabel.text = ''
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
            OFC_Write_Doc(pWCallback = Callback_Write, \
                          pFile = pFile, \
                          pLabel = pLabel)
        else:
            get_permissions()
        Logger.info('***FILE_API30*** : def Write_File()...end')
    return


####################################################
# Open File chooser and call callback with
# absolute filepath of document user selected.
# None if user canceled.
####################################################
def OFC_Read_Doc(pRCallback=None, pFile=None, pLabel=None):
    if(platform == 'android'):
        Logger.info('***FILE_API30*** : def OFC_Read_Doc()...start')
        currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
        context = cast('android.content.ContextWrapper', currentActivity.getApplicationContext())
        file_p = cast('java.io.File', context.getExternalFilesDir(Env.DIRECTORY_DOCUMENTS))
        
        ##########################################################
        def on_activity_result(request_code, result_code, intent):
            Logger.info('***FILE_API30*** : def on_activity_result()...start')
            if request_code != RESULT_LOAD_DOC:
                Logger.warning('on_activity_result: ignoring activity result that was not RESULT_LOAD_DOC')
                return

            if result_code == Activity.RESULT_CANCELED:
                Clock.schedule_once(lambda dt: pRCallback(None), 0)
                return

            if result_code != Activity.RESULT_OK:
                # This may just go into the void...
                raise NotImplementedError('Unknown result_code "{}"'.format(result_code))

            selectedFile = intent.getData();  # Uri
            filePathColumn = [MediaStore_Images_Media_DATA]; # String[]
            # Cursor
            cursor = currentActivity.getContentResolver().query(selectedFile, filePathColumn, None, None, None)
            cursor.moveToFirst()

            # int
            columnIndex = cursor.getColumnIndex(filePathColumn[0]);
            # String
            docPath = cursor.getString(columnIndex);
            cursor.close();
            Logger.info('***FILE_API30*** : on_activity_result() : selected %s', docPath)
            Logger.info('***FILE_API30*** : on_activity_result() : selected %s', str(docPath))
            
            Clock.schedule_once(lambda dt: pRCallback(docPath), 0)
            Logger.info('***FILE_API30*** : def on_activity_result()...end')
            return

        activity.bind(on_activity_result = on_activity_result)
        intent = Intent(Intent.ACTION_OPEN_DOCUMENT)
        intent.addCategory(Intent.CATEGORY_OPENABLE)
        intent.setType("*/*")
        intent.putExtra(Intent.EXTRA_ALLOW_MULTIPLE, False)
        intent.setAction(Intent.ACTION_GET_CONTENT)
        currentActivity.startActivityForResult(intent, RESULT_LOAD_DOC)
        Logger.info('***FILE_API30*** : def OFC_Read_Doc()...end')
    return


####################################################
def Callback_Read(filename):
    if(filename != None):
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
    else:
        Logger.info('***FILE_API30*** : filename = NONE')
    return
    

####################################################
def OFC_Write_Doc(pWCallback=None, pFile=None, pLabel=None):
    if(platform == 'android'):
        Logger.info('***FILE_API30*** : def OFC_Write_Doc()...start')
        currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
        
        #########################################################
        def on_activity_save(request_code, result_code, intent):
            Logger.info('***FILE_API30*** : def on_activity_save()...start')
            if request_code != RESULT_SAVE_DOC:
                Logger.warning('on_activity_save: ignoring activity result that was not RESULT_SAVE_DOC')
                return
            
            if result_code == Activity.RESULT_CANCELED:
                Clock.schedule_once(lambda dt: pWCallback(None), 0)
                return
            
            if result_code != Activity.RESULT_OK:
                # This may just go into the void...
                raise NotImplementedError('Unknown result_code "{}"'.format(result_code))
            
            selectedUri = intent.getData()                  # Uri
            filePathColumn = [MediaStore_Images_Media_DATA] # String
            
            # Cursor
            cursor = currentActivity.getContentResolver().query(selectedUri, filePathColumn, None, None, None)
            cursor.moveToFirst()
            
            # If you need to get the document path, but I used selectedUri.getPath()
            # columnIndex = cursor.getColumnIndex(filePathColumn[0])  # int
            # docPath = cursor.getString(columnIndex)                 # String
            cursor.close()
            Logger.info('***FILE_API30*** : android_ui: on_activity_save() selected %s', selectedUri.getPath())
            
            Clock.schedule_once(lambda dt: pWCallback(selectedUri), 0)
            Logger.info('***FILE_API30*** : def on_activity_save()...end')
            return

        activity.bind(on_activity_result = on_activity_save)
        
        # Here's another Intent in contrast to get the file
        intent = Intent(Intent.ACTION_CREATE_DOCUMENT)
        intent.addCategory(Intent.CATEGORY_OPENABLE)
        intent.setType('*/*')
        currentActivity.startActivityForResult(intent, RESULT_SAVE_DOC)
        Logger.info('***FILE_API30*** : def OFC_Write_Doc()...end')
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

