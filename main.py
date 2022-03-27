import shutil
import os
import re
import json

# Use different save dir
mode_different_dir = False

# This hasn't been tested on EGS since late 2020, it's possible it no longer works, use "True" at your own risk.
# Steam or EGS?
mode_egs = True

# Required to find the save data on steam, not used for EGS
# Can be found using https://www.steamidfinder.com/
# Is the part of steamID3 after the last semicolon, 
# e.g. [U:1:123456789] -> 123456789
steam_profile_id = None


# Populates all save slots with the data in the first slot and changes the current selection to the second slot
def clone_slot0_and_set_slot1(user_data_dir_path):
    file_extension = "dat" if mode_egs else "cfg"
    set_profile_num(user_data_dir_path, 1)
    lvl_file_list = [lvldat for lvldat in os.listdir() if "level" in lvldat]
    del_files_list = [x for x in lvl_file_list if re.match(r'\d_.', x)]
    for del_file in del_files_list:
        os.remove(del_file)
    lvl_file_list = [lvldat for lvldat in os.listdir() if "level" in lvldat]
    for i in range(3):
        shutil.copyfile(f'CompleteSave.{file_extension}', f'CompleteSave{i+1}.{file_extension}')
        with open(f'CompleteSave{i+1}.{file_extension}', "r") as f:
            current_save = f.readline()
        with open(f'CompleteSave{i+1}.{file_extension}', "w") as f:
            f.write(current_save.replace('CompleteSave', f'CompleteSave{i+1}'))
        for file in lvl_file_list:
            shutil.copyfile(f'{file}', f'{i + 1}_{file}')
    return


# Sets the profile number
def set_profile_num(user_data_dir_path, profile_num):
    file_extension = "dat" if mode_egs else "cfg"
    os.chdir(user_data_dir_path)
    with open(f"user_profile.{file_extension}", "r") as f:
        current_profile = get_curr_profile(user_data_dir_path)
        if current_profile == profile_num:
            return
        file_data = f.read()
    file_data = re.sub(',"saveSlot":\d', '', file_data)
    if 1 <= profile_num <= 3:
        file_data = re.sub('"lastAgreement":1', f'"lastAgreement":1,"saveSlot":{profile_num}', file_data)
    elif profile_num != 0:
        raise Exception('Profile values must range from 0 to 3')

    with open(f"user_profile.{file_extension}", "w") as f:
        f.write(file_data)
        return


# Get the currently selected profile number
def get_curr_profile(user_data_dir_path):
    file_extension = "dat" if mode_egs else "cfg"
    os.chdir(user_data_dir_path)
    with open(f"user_profile.{file_extension}", "r") as f:
        f.seek(67)
        user_profile_str = f.readline(13)
        if user_profile_str[0:12] != ',"saveSlot":':
            return 0
        else:
            return int(user_profile_str[-1])


if __name__ == '__main__':
    with open('settings.json', 'r') as f:
        settings = json.load(f)
        mode_egs = True if settings.get('mode_egs') == True else False
        steam_profile_id = settings.get('steam_profile_id')
        mode_different_dir = True if settings.get('mode_different_dir') == True else False

        storage_subdir = 0 if not mode_different_dir else 1638
        program_dir = os.getcwd()
        
        if mode_egs:
            save_dir_path = os.path.join(os.environ['USERPROFILE'], 'Documents\\My Games\\SnowRunner')
            backup_dir_path = save_dir_path + '_backup'
            os.chdir(save_dir_path)
            user_data_dir_path = os.path.join(save_dir_path, f'base\\storage\\{storage_subdir}')

        else :
            if steam_profile_id == None:
                exit()
            save_dir_path = os.path.join(f'C:\\Program Files (x86)\\Steam\\userdata\\{steam_profile_id}\\1465360\\remote')
            backup_dir_path = save_dir_path + '_backup'
            os.chdir(save_dir_path)
            user_data_dir_path = save_dir_path

        try:  # Kill snowrunner.exe if running
            if os.system('taskkill /im SnowRunner.exe') != 0:
                raise OSError
        except:
            print('SnowRunner.exe not currently open')

        '''  # Enable to create a backup every time 
        try:
            shutil.rmtree(backup_dir_path)  # Remove existing backup
        except FileNotFoundError:
            print('No old backup to remove')
        '''   
        if not os.path.isdir(backup_dir_path):
            shutil.copytree(save_dir_path, backup_dir_path)  # Create a backup
        else:
            print('Backup already exists')



        clone_slot0_and_set_slot1(user_data_dir_path)

        os.chdir(program_dir)
        try:  
            os.system('SnowRunner.lnk')
        except:
            print('SnowRunner.lnk not found, trying .url...')

        try:
            os.system('SnowRunner.url')
        except:
            print('No launcher found, please run SnowRunner manually.')
