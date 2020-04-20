import glob
import os


class Path_config:
    def __init__(self, android_base_path, mac_base_path, android_folder, mac_folder):
        self.android_base=android_base_path
        self.mac_base=mac_base_path
        self.android_folder=android_folder
        self.mac_folder = mac_folder

class Config:
    def __init__(self, source):
        self.source=source

def main():
    try:
        path_config=Path_config(
                                '/storage/emulated/0/Music/Collection/','~/Music/Collection/',
                                '~/pyLearn/pyCharm_projects/playlists-sync/android/',
                                '~/pyLearn/pyCharm_projects/playlists-sync/mac/'
                                )
        config=Config('android')

        for filepath in glob.iglob(path_config.android_folder+'*.*'):
            file_set=get_file_set(filepath, path_config, config)
            playlist_name=get_playlist_name(filepath)
            create_m3u8_file(playlist_name, file_set, path_config, config)
            # print(file_set)

    except Exception as e:
        print("Error: " + str(e))


def get_file_set(filepath, path_config, config):
    file_set = set()
    with open(filepath, 'r') as file:
        for line in file:
            line = remove_extra_new_lines(line)
            relative_path = remove_base_path(line, path_config.android_base)
            file_set.add(relative_path)
    return file_set


def remove_extra_new_lines(line):
    if (line.endswith('\n')):
        stripped_line = line.replace('\n','')
    else:
        stripped_line = line
    return stripped_line



def remove_base_path(line, base_path):
    try:
        if(base_path in line):
            return line.replace(base_path,'')
        else:
            raise Exception
    except Exception as e:
        print("Error: " + str(e))

def get_playlist_name(filepath):
    filename=os.path.basename(filepath)
    playlist_name=filename.replace('.m3u8','')
    return playlist_name

def create_m3u8_file(filepath,file_set, path_config, config):
    with open(path_config.mac_folder+filepath+'.m3u8','w+') as file_to_write:
        for file_name in file_set:
            # print(path_config.mac_base+file_name)
            file_to_write.write(path_config.mac_base+file_name)
            file_to_write.write('\n')




if __name__ == '__main__':
    main()