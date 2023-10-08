import argparse
import os
import shutil
import sys
from argparse import ArgumentParser

from pymediainfo import MediaInfo

MOVIE_EXTENSIONS = ['.mkv', '.mp4', '.avi', '.mov']
false: bool = False
true: bool = True
sub_ext: str = '.srt'
arg1: str = ""
arg2: str = ""
current_folder: str = ""
head: str = ""
tail: str = ""
movfile: str = ""
log: list = []

infoMode: bool = False
verbose: bool = False
demomode: bool = False
outfile: str = ''
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


def found_embedded_sub(file_path, sub_lang):
    '''Check for a subtitle in the specified language that is embedded in the movie file. 
    If found, don't look for an external subtitle file with extension .sub'''
    media_info = MediaInfo.parse(file_path)
    langs = {'english': 'en', 'spanish': 'sp'}

    # print(f"{media_info}")
    # for track in media_info.tracks:
    # print(f"track type='{track.track_type}' lang='{track.language}' track='{track}'")
    # if track.track_type == 'Text' and track.language == 'en':
    #    return True
    # return False

    return any(track.track_type == 'Text' and track.language.lower() == langs[sub_lang] for track in media_info.tracks)


# def largest_file(folder_path, masks):
# all_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if any(f.endswith(mask) for mask in masks)]
# largest_file = max(all_files, key=os.path.getsize)
# return largest_file

def find_largest_srt_file(subfolder_path, sub_lang):
    """Find the largest subtitle file in the specified language"""
    all_files = os.listdir(subfolder_path)
    eng_srt_files = filter(lambda x: x.endswith('.srt') and sub_lang in x.lower(), all_files)
    largest_file = max(eng_srt_files, key=lambda x: os.path.getsize(os.path.join(subfolder_path, x)), default=None)
    return largest_file


def copy_srt_in_subs(current_folder, movie_file, sub_lang='english'):
    """Check for srt file in subs folder (if folder exists) in the specified language in parameter sub_lang"""
    head, tail = os.path.split(current_folder)
    subs_folder = os.path.join(current_folder, 'subs')
    if os.path.exists(subs_folder):
        largest_file = find_largest_srt_file(subs_folder, sub_lang)
        if largest_file:
            src_path = os.path.join(subs_folder, largest_file)
            movie_file_name, movie_ext = os.path.splitext(movie_file)
            sub_file = movie_file_name + sub_ext
            dst_path = os.path.join(current_folder, sub_file)
            if not arg2 or arg2 != '--D':
                shutil.copy2(src_path, dst_path)
            print_verb(f"[{tail}]: Found {sub_lang} sub file in Subs folder in [{largest_file}]")
            print_verb(f"[{tail}]: Copied sub file to [{sub_file}].")
            return True
        else:
            print_info(f"[{tail}]: No {sub_lang} sub file in Subs folder")
            return False
    else:
        print_info(f"[{tail}]: No Subs folder")
        return True


def rename_srt_file(current_folder, movie_file):
    head, tail = os.path.split(current_folder)
    movie_file_name, movie_ext = os.path.splitext(movie_file)
    srt_file = movie_file_name + sub_ext
    dst_path = os.path.join(current_folder, srt_file)
    # print_verb(f"[{tail}]: Looking for subtitle [{srt_file}]")

    if os.path.exists(os.path.join(current_folder, srt_file)):
        print_info(f"[{tail}]: File {srt_file} already exists.")
        return 0  # file exists, no need to continue

    for file in os.listdir(current_folder):
        file_name, ext = os.path.splitext(file)
        if ext == sub_ext:
            src_path = os.path.join(current_folder, file)
            print_info(f"[{tail}]: Found sub file [{file}] in same folder as movie file")
            print_info(f"[{tail}]: Copied sub file to [{srt_file}].")
            if (not arg2) or (arg2 != '--D'):
                # os.rename(src_path, dst_path)
                shutil.copy2(src_path, dst_path)  # copy instead of renaming in order to preserve original file
            return 1

    print_verb(f"[{tail}]: No srt file in movie folder, will look in subs folder.")
    return -1  # no .srt found in this language


def check_movie(current_folder, movfile):
    head, tail = os.path.split(current_folder)
    # search for spanish subtitle first if the film name contains the word SPANISH  in the name
    langs2chk = ['spanish', 'english'] if 'spanish' in movfile.lower() else ['english', 'spanish']

    for sub_lang in langs2chk:
        # print_verb(f"[{tail}]: Checking for subtitles in [{sub_lang}] in folder [{current_folder}]")
        if found_embedded_sub(movfile, sub_lang):
            print_info(f"[{tail}]: Embedded {sub_lang} subtitles found.")
            break  # break language file search

        rena_result = rename_srt_file(current_folder, movfile)
        # print_verb(f"[{tail}]: rena_result=[{rena_result}]")

        if rena_result >= 0:
            break
        if copy_srt_in_subs(current_folder, movfile, sub_lang):
            break  # break language file search as found a sub in the language requested
        # else:
        #    print_info(f"[{tail}]: *** No movie files found for language [{sub_lang}] in subs folder***")
    # return


def main():
    current_folder = os.getcwd()
    # print_verb(f"[{current_folder}] Current dir")
    head, tail = os.path.split(current_folder)
    # print_verb(f"Head:[{head}]   Tail:[{tail}] Current folder:[{current_folder}]")

    for movfile in os.listdir(current_folder):
        # check if there is any movie file in the folder
        movie_file_name, movie_ext = os.path.splitext(movfile)
        # if found a file that is a movie
        if movie_ext in MOVIE_EXTENSIONS:
            print_info(f"[{tail}]: Movie file found -> [{movie_file_name + movie_ext}]")
            check_movie(current_folder, movfile)

    # print_info("[*********************************************]")


def parse_args():
    parser: ArgumentParser = argparse.ArgumentParser(prog='fix_subs',
                                     description="Fix subtitles in all subfolders. Run thru subfolders and find English srt file in subs if no other subtitle found in folder.",
                                     epilog='Each movie file in its folder (.mkv or .mp4) will be checked for embedded english subs. \n' +
                                            'If not found a subtitle file in the same folder with any name or an optional [subs] folder that \n' +
                                            'contains one or more *English*.srt files of which the largest will be copied and renamed with the same name as the movie file into its folder.',
                                     add_help=True)
    # group = parser.add_argument_group('Options')
    # group.add_argument('--d', type=str, choices=[x.upper() for x in ['on', 'off']], default='OFF', help='Turn debug mode ON or OFF (no changes done)')
    # group.add_argument('--log', type=str, help='Print to a log file in addition to the console')
    # group.add_argument('--loglevel', type=str, choices=[x.upper() for x in ['info', 'verbose']], default='INFO', help='Specify the level of detail in the log')

    parser.add_argument('filename', nargs='?', default='fix_subs.log')  # positional argument
    parser.add_argument('-c', '--count', nargs='?', default=0)  # option that takes a value
    parser.add_argument('-v', '--verbose', nargs='?', action='store_true', default=True)  # on/off flag

    # parser.add_argument('--debug', type=str, help='Turn debugging function ON or OFF')
    # parser.add_argument('--log',  '--l', type=str, help='The name of the log file')
    # parser.add_argument('--o',     default='fix_subs.log', help='The name of the log file')
    # parser.add_argument('--loglevel',  type=str, help='The type of information to print')
    # parser.add_argument('--demo', action='store_false', help='Turn on demo mode')

    args = vars(parser.parse_args())
    print(args.filename, args.count, args.verbose)

    # updated_args = {k.upper(): v for k, v in args.items()}
    return args  # updated_args


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
        # print(f'Arg:{arg1}')

    if len(sys.argv) > 2 and sys.argv[2]:
        arg2 = sys.argv[2].upper()
        # print(f'Arg:{arg2}')

    if (arg1 and (arg1 == '?' or arg1 == '--?' or arg1 not in ['--I', '--V']) or (arg2 and arg2 != '--D')):
        print(
            "fix_subs Utility: Fix subtitles in all subfolders. Run thru subfolders and find English srt file in subs if no other subtitle found in folder.")
        print("Syntax: fix_subs [--I/V] [--D]")
        print("Parameters: --I for Info")
        print("            --V for Verbose")
        print("            --D for Demo mode (no action taken)")
        sys.exit(1)
    else:
        main()
