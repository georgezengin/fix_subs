import sys, os, shutil
from pymediainfo import MediaInfo
import argparse


MOVIE_EXTENSIONS = ['.mkv', '.mp4', '.avi', '.mov']
false = False
true = True
sub_ext = '.srt'
arg1 = ""
arg2 = ""
current_folder = ""
head = ""
tail = ""
log = []

infoMode = False
verbose = False
demomode = False
outfile = ''
parser = argparse.ArgumentParser(description='Parse command line arguments.')

def print_info(s):
    if arg1 and (arg1 == '--I' or arg1 == '--V'):
    # if infoMode or verbose: #args['I'] or args['V']:
         print(s)
    #     if args['LOGFILE']:
    #         print(s, file=outfile )

def print_verb(s):
    if arg1 and (arg1 == '--V'):
        print(s)
    # if args['V']:
    #     print(s)
    #     if args['LOGFILE']:
    #         print(s, file=outfile )

        
def has_english_subtitle(file_path):
    media_info = MediaInfo.parse(file_path)
    #print(f"{media_info}")
    
    #for track in media_info.tracks:
        #print(f"track type='{track.track_type}' lang='{track.language}' track='{track}'")
        #if track.track_type == 'Text' and track.language == 'en':
        #    return True
    #return False
    return any(track.track_type == 'Text' and track.language == 'en' for track in media_info.tracks)

def has_spanish_subtitle(file_path):
    media_info = MediaInfo.parse(file_path)
    #print(f"{media_info}")
    
    #for track in media_info.tracks:
        #print(f"track type='{track.track_type}' lang='{track.language}' track='{track}'")
        #if track.track_type == 'Text' and track.language == 'en':
        #    return True
    #return False
    return any(track.track_type == 'Text' and track.language == 'sp' for track in media_info.tracks)

def largest_file(folder_path, masks):
    all_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if any(f.endswith(mask) for mask in masks)]
    largest_file = max(all_files, key=os.path.getsize)
    return largest_file

def rename_srt_file(current_folder, movie_file):
    head, tail = os.path.split(current_folder)
    movie_file_name, movie_ext = os.path.splitext(movie_file)
    srt_file = movie_file_name + sub_ext
    dst_path = os.path.join(current_folder, srt_file)
    #print_verb(f"[{tail}]: Looking for subtitle [{srt_file}]")
    
    if not os.path.exists(os.path.join(current_folder, srt_file)):
        for file in os.listdir(current_folder):
            file_name, ext = os.path.splitext(file)
            if ext == sub_ext:
                src_path = os.path.join(current_folder, file)
                #os.rename(src_path, dst_path)
                if not arg2 or arg2 != '--D':
                    shutil.copy2(src_path, dst_path) # copy instead of renaming in order to preserve original file
                print_info(f"[{tail}]: Found sub file [{file}] in folder")
                print_info(f"[{tail}]: Copied sub file to [{srt_file}].")
                return True
        print_verb(f"[{tail}]: No srt file in current folder, will look in subs.")
        return False #no .srt found, check in subs folder
    else:
        print_info(f"[{tail}]: File {srt_file} already exists.")
        return True #file exists, no need to continue

def find_largest_english_srt_file(subfolder_path):
    all_files = os.listdir(subfolder_path)
    eng_srt_files = filter(lambda x: x.endswith('.srt') and 'english' in x.lower(), all_files)
    largest_file = max(eng_srt_files, key=lambda x: os.path.getsize(os.path.join(subfolder_path, x)), default=None)
    return largest_file

def copy_english_srt(current_folder, movie_file):
    head, tail = os.path.split(current_folder)
    subs_folder = os.path.join(current_folder, 'subs')
    if os.path.exists(subs_folder):
        largest_file = find_largest_english_srt_file(subs_folder)
        if largest_file:
            src_path = os.path.join(subs_folder, largest_file)
            movie_file_name, movie_ext = os.path.splitext(movie_file)
            sub_file = movie_file_name + sub_ext
            dst_path = os.path.join(current_folder, sub_file)
            if not arg2 or arg2 != '--D':
                shutil.copy2(src_path, dst_path)
            print_verb(f"[{tail}]: Found english sub file in subs folder in [{largest_file}]")
            print_verb(f"[{tail}]: Copied sub file to [{sub_file}].")
        else:
            print_info(f"[{tail}]: No english sub file in subs folder")
    else:
        print_info(f"[{tail}]: No Subs folder")

def main():
    current_folder = os.getcwd()
    print_verb(f"[{current_folder}] Current dir")
    head, tail = os.path.split(current_folder)
    #print_verb(f"Head:[{head}]   Tail:[{tail}]")
    
    for movfile in os.listdir(current_folder):
        #check if movie has 
        movie_file_name, movie_ext = os.path.splitext(movfile)
        if movie_ext in MOVIE_EXTENSIONS:
            print_info(f"[{tail}]: Movie file found -> [{movie_file_name + movie_ext}]")

            if has_english_subtitle(movfile):
                print_info(f"[{tail}]: Embedded english subtitles found.")
                break

            if has_spanish_subtitle(movfile):
                print_info(f"[{tail}]: Embedded spanish subtitles found.")
                break

            if not rename_srt_file(current_folder, movfile):
                copy_english_srt(current_folder, movfile)
            break
            
    else:
        print_info(f"[{tail}]: *** No movie files found ***")
    print("[*********************************************]")

def parse_args():
    parser = argparse.ArgumentParser(prog = 'fix_subs',
                    description = f"Fix subtitles in all subfolders. Run thru subfolders and find English srt file in subs if no other subtitle found in folder.",
                    epilog = 'Each movie file in its folder (.mkv or .mp4) will be checked for embedded english subs. \n'+
                             'If not found a subtitle file in the same folder with any name or an optional [subs] folder that \n'+
                             'contains one or more *English*.srt files of which the largest will be copied and renamed with the same name as the movie file into its folder.',
                    add_help=True)
    #group = parser.add_argument_group('Options')
    #group.add_argument('--d', type=str, choices=[x.upper() for x in ['on', 'off']], default='OFF', help='Turn debug mode ON or OFF (no changes done)')
    #group.add_argument('--log', type=str, help='Print to a log file in addition to the console')
    #group.add_argument('--loglevel', type=str, choices=[x.upper() for x in ['info', 'verbose']], default='INFO', help='Specify the level of detail in the log')

    parser.add_argument('filename', nargs='?', default='fix_subs.log')           # positional argument
    parser.add_argument('-c', '--count', nargs='?', default=0)      # option that takes a value
    parser.add_argument('-v', '--verbose', nargs='?', action='store_true', default=True)  # on/off flag
    
    #parser.add_argument('--debug', type=str, help='Turn debugging function ON or OFF')
    #parser.add_argument('--log',  '--l', type=str, help='The name of the log file')
    #parser.add_argument('--o',     default='fix_subs.log', help='The name of the log file')
    #parser.add_argument('--loglevel',  type=str, help='The type of information to print')
    #parser.add_argument('--demo', action='store_false', help='Turn on demo mode')

    args = vars(parser.parse_args())
    print(args.filename, args.count, args.verbose)

    #updated_args = {k.upper(): v for k, v in args.items()}
    return args #updated_args

# if __name__ == '__main__':
#     global args
#     try:
#         args = parse_args()
#         if all(v is not None for v in args.values()):
#             #print(args.demomode) #args['DEBUG'])
#             print(args)
#             #print(args['LOGMODE']) #['I']) #LOG'])
#             #print(args.log)
#             print(args.loglevel) #['V']) #LOGLEVEL'])
#             print(args.demo) #['D']) #DEMO'])
#             main()
#         else:
#             parser.print_help()
#             sys.exit(1)
#     except SystemExit:
#         #print('Unknown argument found!')
#         #parser.print_help()
#         sys.exit(1)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1]:
        arg1 = sys.argv[1].upper()
        #print(f'Arg:{arg1}')
        
    if len(sys.argv) > 2 and sys.argv[2]:
        arg2 = sys.argv[2].upper()
        #print(f'Arg:{arg2}')
        
    if (arg1 and (arg1 == '?' or arg1=='--?' or arg1 not in ['--I','--V']) or (arg2 and arg2 != '--D')):
        print(f"fix_subs Utility: Fix subtitles in all subfolders. Run thru subfolders and find English srt file in subs if no other subtitle found in folder.")
        print(f"Syntax: fix_subs [--I/V] [--D]")
        print(f"Parameters: --I for Info")
        print(f"            --V for Verbose")
        print(f"            --D for Demo mode (no action taken)")
        sys.exit(1)
    else:
       main()

