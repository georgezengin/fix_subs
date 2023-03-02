import os
import re

folder_path = os.getcwd() #"path/to/folder" # Replace with the path to the folder containing the folders you want to rename

print(f"[{folder_path}] Current dir")
#year_pattern = re.compile(r"([.\[]?)(19\d{2}|20\d{2})([.\]]?)")
#year_pattern = re.compile(r"([.\[(]?)(19\d{2}|20\d{2})([.\])]?)")
year_pattern = re.compile(r"([._-]|\b)(19\d{2}|20\d{2})([.\])_-]|\b)")

year_only_pattern = re.compile(r"(19\d{2}|20\d{2})")

for folder_name in os.listdir(folder_path):
    if os.path.isdir(os.path.join(folder_path, folder_name)):
        year_match = year_pattern.search(folder_name)
        if year_match is not None:
            year = year_match.group(0)
            year_only_match = year_only_pattern.search(year)
            year_only = year_only_match.group(0)
            
            year_start = year_match.start()
            year_end = year_match.end()
            #print(year_start, year_end)
            if '.' not in folder_name[:year_start+1]:
                continue
            before_year = folder_name[:year_start].replace('.', ' ').strip()
            before_year = before_year.title() if len(before_year.split())>1 else before_year ## capitalize if more than 1 word
            after_year = folder_name[year_end:].strip().replace("[", "").replace("]", "").replace(". ", ".").replace(" ", ".")
            #print(before_year, after_year)

        #else:
        #    before_year = folder_name.replace('.', ' ').strip().title()
        #    after_year = ''

            #new_folder_name = f"{year} - {folder_name}"
            #cap_fname = ' '.join([word.capitalize() for word in folder_name.replace('.', ' ').split()])
            #new_folder_name = f"{year_pattern.sub(' ('+year_only+') [', cap_fname).strip('.[] ').replace('  ', ' ')+']'}"
            new_folder_name = f"{year_pattern.sub('', before_year).strip('.[]() ').replace('  ', ' ')} ({year_only})"
            new_folder_name += " ["+after_year+"]" if after_year else ''
            #new_folder_name = f"{year_pattern.sub(' ({year_only}) [', before_year).strip()} - {after_year}"
            print(f'Rename: <<{folder_name}>> to <<{ new_folder_name}>> ')
            os.rename(os.path.join(folder_path, folder_name), os.path.join(folder_path, new_folder_name))
