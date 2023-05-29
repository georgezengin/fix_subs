import sys, os, shutil
from pymediainfo import MediaInfo


MOVIE_EXTENSIONS = ['.mkv', '.mp4', '.avi', '.mov']
false = False
true = True
sub_ext = '.srt'
arg1 = ""
arg2 = ""
current_folder = ""
head = ""
tail = ''

def print_info(s):
    if arg1 and (arg1 == '--I' or arg1 == '--V'):
        print(s)

def print_verb(s):
    if arg1 and (arg1 == '--V'):
        print(s)
        
def has_english_subtitle(file_path):
    media_info = MediaInfo.parse(file_path)
    return any(track.track_type == 'Text' and track.language == 'English' for track in media_info.tracks)
    
    #for track in media_info.tracks:
    #    if track.track_type == 'Text' and track.language == 'English':
    #        return True
    #return False

def largest_file(folder_path, masks):
    all_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if any(f.endswith(mask) for mask in masks)]
    largest_file = max(all_files, key=os.path.getsize)
    return largest_file

def rename_srt_file(current_folder, movie_file):
    head, tail = os.path.split(current_folder)
    movie_file_name, movie_ext = os.path.splitext(movie_file)
    srt_file = movie_file_name + sub_ext
    dst_path = os.path.join(current_folder, srt_file)
    print_verb(f"[{tail}]: Looking for subtitle [{srt_file}]")
    
    if not os.path.exists(os.path.join(current_folder, srt_file)):
        for file in os.listdir(current_folder):
            file_name, ext = os.path.splitext(file)
            if ext == sub_ext:
                src_path = os.path.join(current_folder, file)
                #os.rename(src_path, dst_path)
                if not arg2 or arg2 != '--D':
                    shutil.copy2(src_path, dst_path) # copy instead of renaming in order to preserve original file
                print_info(f"[{tail}]: Found sub file [{file}] in folder, copied to [{srt_file}].")
                return True
        print_verb(f"[{tail}]: No srt file in current folder, will look in subs.")
        return False #no .srt found, check in subs folder
    else:
        print_info(f"[{tail}]: File {srt_file} already exists.")
        return True #file exists, no need to continue

def copy_english_srt(current_folder, movie_file):
    head, tail = os.path.split(current_folder)
    subs_folder = os.path.join(current_folder, 'subs')
    if os.path.exists(subs_folder):
        largest_file = None
        largest_file_size = 0
        for file in os.listdir(subs_folder):
            if 'english' in file.lower():
                file_path = os.path.join(subs_folder, file)
                file_size = os.path.getsize(file_path)
                if file_size > largest_file_size:
                    largest_file_size = file_size
                    largest_file = file
        if largest_file:
            src_path = os.path.join(subs_folder, largest_file)
            movie_file_name, movie_ext = os.path.splitext(movie_file)
            sub_file = movie_file_name + sub_ext
            dst_path = os.path.join(current_folder, sub_file)
            if not arg2 or arg2 != '--D':
                shutil.copy2(src_path, dst_path)
            print_verb(f"[{tail}]: Found english sub file in subs folder, copied as [{sub_file}]")
        else:
            print_info(f"[{tail}]: No english sub file in subs folder")
    else:
        print_info(f"[{tail}]: No Subs folder")

def main():
    current_folder = os.getcwd()
    print_verb(f"[{current_folder}] Current dir")
    head, tail = os.path.split(current_folder)
    print_verb(f"Head:[{head}]   Tail:[{tail}]")
    
    for movfile in os.listdir(current_folder):
        #check if movie has 
        movie_file_name, movie_ext = os.path.splitext(movfile)
        if movie_ext in MOVIE_EXTENSIONS:
            if has_english_subtitle(movfile):
                print_info(f"[{tail}]: Embedded english subtitles found.")
                break
            
            print_info(f"[{tail}]: Movie file found -> [{movie_file_name + movie_ext}]")
            if not rename_srt_file(current_folder, movfile):
                copy_english_srt(current_folder, movfile)
            break
            
    else:
        print_info(f"[{tail}]: *** No movie files found ***")
    print("[*********************************************]")
    
if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1]:
        arg1 = sys.argv[1].upper()
        print(f'Arg:{arg1}')
    if len(sys.argv) > 2 and sys.argv[2]:
        arg2 = sys.argv[2].upper()
        print(f'Arg:{arg2}')
        
    if (arg1 and (arg1 == '?' or arg1=='--?' or arg1 not in ['--I','--V'])) or (arg2 and arg2 != '--D'):
        print(f"fix_subs Utility: Fix subtitles in all subfolders. Run thru subfolders and find English srt file in subs if no other subtitle found in folder.")
        print(f"Syntax: fix_subs [--I/V] [--D]")
        print(f"Parameters: --I for Info")
        print(f"            --V for Verbose")
        print(f"            --D for Demo mode (no action taken)")
    else:
        main()

