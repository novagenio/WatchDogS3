# import watchdog
import time 
from watchdog.observers import Observer 
from watchdog.events import FileSystemEventHandler

# import S3
from botocore.exceptions import ClientError
import boto
import sys
import boto.s3.connection
from boto.s3.key import Key

# definicion credenciales S3 
access_key = access_key'
secret_key = 'secret_key'

conn = boto.connect_s3(
        aws_access_key_id = access_key,
        aws_secret_access_key = secret_key,
        host = 's3 host',
        calling_format = boto.s3.connection.OrdinaryCallingFormat(),
        )
# nombre bucket S3
bucket = conn.get_bucket('s3 bucket')


# largo caracteres directorio base origen para cortar c:
long_dir_base = 2

# despliega porcentaje transferencia y total
def percent_cb(complete, total):
    print("complete:" + str(complete) + " total: " + str(total))
    sys.stdout.write('.')
    sys.stdout.flush()

# funcion uoload_s3
def upload_s3(file_name):
    k = Key(bucket)
    largo = len(file_name) 
    print ("Fuchero: " + file_name[long_dir_base:largo])
    k.key = "salida/" + file_name[long_dir_base:largo]
    # espera que el fichero termine de crearse. 
    file = None
    while file is None:
        try:
            file = open(file_name)
        except OSError:
            file = None
            print("WAITING FOR FILE TRANSFER....")
            time.sleep(3)
            continue
    # envia fichero
    print("Comienza la subida a S3 de: " + file_name )
    k.set_contents_from_filename(file_name,
          cb=percent_cb, num_cb=10)
  
  
class OnMyWatch: 
    # define el directorio o carpeta que se va a monitorizar
    watchDirectory = 'Y:/Desarrollo/'
  
    def __init__(self): 
        self.observer = Observer() 
  
    def run(self): 
        event_handler = Handler() 
        self.observer.schedule(event_handler, self.watchDirectory, recursive = True) 
        self.observer.start() 
        try: 
            while True: 
                time.sleep(3) 
        except: 
            self.observer.stop() 
            print("Observer Stopped") 
        self.observer.join() 
  
  
class Handler(FileSystemEventHandler): 
    filename_created = ""
    @staticmethod
    def on_any_event(event): 
        if event.is_directory: 
            return None
  
        elif event.event_type == 'created': 
            # Event is created, you can process it now 
            print("Watchdog received created event - % s." % event.src_path)
            filename_created = event.src_path
            time.sleep(1)
            upload_s3(event.src_path)
            print("fin s3")
            
        elif event.event_type == 'modified': 
            # Event is modified, you can process it now 
            print("Watchdog received modified event - % s." % event.src_path)
            print("ruta fichero: " + event.src_path)
            
           
  
if __name__ == '__main__': 
    watch = OnMyWatch() 
    watch.run() 
