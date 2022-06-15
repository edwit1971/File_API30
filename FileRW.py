##############################################################
#
# FileRW.py  created June 2022
#
# All the Functions needed to Read and Write a File
# on an Android device running API30+
#
##############################################################


#from pathlib import Path
#p = Path(pDest)
#p.as_uri()

import io
import json

from kivy.utils import platform


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


def Read_File():
    if platform == 'android':
        if check_permission("android.permission.WRITE_EXTERNAL_STORAGE") \
        and check_permission("android.permission.READ_EXTERNAL_STORAGE") \
        and check_permission("android.permission.INTERNET"):
        # if permissions_granted:   # variant
            OFC_Read_Doc(Callback_Read)
        else:
            get_permissions()


def Write_File():
    if platform == 'android':
        if check_permission("android.permission.WRITE_EXTERNAL_STORAGE") \
        and check_permission("android.permission.READ_EXTERNAL_STORAGE") \
        and check_permission("android.permission.INTERNET"):
        # if permissions_granted:   # variant
            OFC_Write_Doc(Callback_Write)
        else:
            get_permissions()


####################################################
# Open File chooser and call callback with
# absolute filepath of document user selected.
# None if user canceled.
####################################################
def OFC_Read_Doc(pRCallback):
    if(platform == 'android'):
        currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
        context = cast('android.content.ContextWrapper', currentActivity.getApplicationContext())
        file_p = cast('java.io.File', context.getExternalFilesDir(Env.DIRECTORY_DOCUMENTS))
        
        ##########################################################
        def on_activity_result(request_code, result_code, intent):
            if request_code != RESULT_LOAD_DOC:
                Logger.warning('OFC_Read_Doc: ignoring activity result that was not RESULT_LOAD_DOC')
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
            Logger.info('android_ui: OFC_Read_Doc() selected %s', docPath)

            Clock.schedule_once(lambda dt: pRCallback(docPath), 0)
            return

        activity.bind(on_activity_result = on_activity_result)
        intent = Intent(Intent.ACTION_OPEN_DOCUMENT)
        intent.addCategory(Intent.CATEGORY_OPENABLE)
        intent.setType("*/*")
        intent.putExtra(Intent.EXTRA_ALLOW_MULTIPLE, False)
        intent.setAction(Intent.ACTION_GET_CONTENT)
        currentActivity.startActivityForResult(intent, RESULT_LOAD_DOC)
        return


####################################################
def Callback_Read(filename):
    with io.open(filename, encoding='utf-8') as file:
        data = None
        try:
            data = json.load(file)
        except:
            # print('JSON not loaded')
            return False
    

####################################################
def OFC_Write_Doc(pWCallback):
    if(platform == 'android'):
        currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
        
        #########################################################
        def on_activity_save(request_code, result_code, intent):
            if request_code != RESULT_SAVE_DOC:
                Logger.warning('OFC_Write_Doc: ignoring activity result that was not RESULT_SAVE_DOC')
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
            Logger.info('android_ui: OFC_Write_Doc() selected %s', selectedUri.getPath())
            
            Clock.schedule_once(lambda dt: pWCallback(selectedUri), 0)
            return

        activity.bind(on_activity_result = on_activity_save)
        
        # Here's another Intent in contrast to get the file
        intent = Intent(Intent.ACTION_CREATE_DOCUMENT)
        intent.addCategory(Intent.CATEGORY_OPENABLE)
        intent.setType('*/*')
        currentActivity.startActivityForResult(intent, RESULT_SAVE_DOC)
        return
    

####################################################
def Callback_Write(uri):
    if(platform == 'android'):
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


####################################################
def Read_BinaryFile(pData = None):
    fo = open("loneliness.txt", "rb")
    if(fo != None):
        byte = fo.read(1)
        while(byte):
            pData.append(byte)
            byte = fo.read(1)
        fo.close()
    return 


####################################################
####################################################

