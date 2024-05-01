import os
import shutil

# Constants
ROOT_BACKUP_PATH = '/mnt/c/Users/ojmlc/Documents/backup/'
SUB_BACKUP_PATH = '/Takeout/Google Fotos/'
EXTENTIONS = ['.jpg', '.JPG', '.jpeg', '.JPEG', '.png', '.PNG', '.mp4', '.MP4', '.gif', '.GIF']
DESTINATION_ABSOLUTE_PATH = '/mnt/c/Users/ojmlc/Documents/google-res/'

# Variables
moved_files = 0
scanned_files = 0
folders_opened = 0
dirs_opened = 0
failed_files = 0

def create_destination_path(destinatio_path) -> None:
    if not os.path.exists(destinatio_path):
        print('Creating destinatio path.. ')
        try:
            os.mkdir(destinatio_path)
            print('Destinatio path created')
        except IOError:
            print('No se puede crear la ruta de destino ', destinatio_path)

    else:
        print('Destination path alrready exists')

def move_backup_files() -> None:
    total_dirs = len(next(os.walk(ROOT_BACKUP_PATH))[1])
    global dirs_opened
    progress_bar(dirs_opened, total_dirs, prefix='Progress:', suffix='Complete', length=50)
    
    for directory in next(os.walk(ROOT_BACKUP_PATH))[1]:
        sub_dir_path = ROOT_BACKUP_PATH + directory + SUB_BACKUP_PATH
        progress_bar(dirs_opened, total_dirs, prefix='Progress:', suffix='Complete', length=50)
        dirs_opened += 1
        
        for subdir in next(os.walk(sub_dir_path))[1]:
            absolute_path = sub_dir_path + subdir
            global folders_opened
            folders_opened += 1
            
            for file in next(os.walk(absolute_path))[2]:
                file_name, file_extention = os.path.splitext(file)
                global scanned_files
                global failed_files
                scanned_files += 1
                
                if file_extention in EXTENTIONS:
                    file_absolute_path = absolute_path + '/' + file
                    destination_path = DESTINATION_ABSOLUTE_PATH
                    
                    try:
                        if (os.path.exists(DESTINATION_ABSOLUTE_PATH + file)):
                            renamed_file = file_name + '-copy' + file_extention
                            renamed_path = absolute_path + '/' + renamed_file
                            destination_path += renamed_file
                            os.rename(file_absolute_path, renamed_path)
                            file_absolute_path = renamed_path
                        
                        destination_path += file

                        shutil.move(file_absolute_path, destination_path)
                        global moved_files
                        moved_files += 1
                    except FileExistsError:
                        print('El archivo {} ya esxiste en la ruta de destino'.format(file))
                        progress_bar(dirs_opened, total_dirs, prefix='Progress:', suffix='Complete', length=50)
                        failed_files += 1
                    except FileNotFoundError:
                        print('No se encontro el archivo {} en la ruta de origen'.format(file))
                        progress_bar(dirs_opened, total_dirs, prefix='Progress:', suffix='Complete', length=50)
                        failed_files += 1
    
    dirs_opened = total_dirs
    progress_bar(dirs_opened, total_dirs, prefix='Progress:', suffix='Complete', length=50)

def progress_bar(iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = '\r'):
    percent = ('{0:.' + str(decimals) + 'f}').format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    
    # Print New Line on Complete
    if iteration == total: 
        print()

def get_report() -> None:
    print()
    print('REPORT:')
    print('Scanned files:', scanned_files)
    print('Moved files:', moved_files)
    print('Failed files:', failed_files)
    print('Folders opened:', folders_opened)

create_destination_path(DESTINATION_ABSOLUTE_PATH)
move_backup_files()
get_report()
