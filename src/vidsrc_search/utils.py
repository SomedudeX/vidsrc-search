import os
import shutil


HELP_TEXT = ("\
Usage: vidsrc-search <command> [options]            \n\
                                                    \n\
Available commands:                                 \n\
    help        shows this menu                     \n\
    search      search a movie by name              \n\
    library     actions regarding the movie lib     \n\
                                                    \n\
Use 'vidsrc-search help <command>' for info         \n\
on a specific command.                              \n\
")

HELP_HELP = ("\
Usage: vidsrc-search help <option>                  \n\
                                                    \n\
Available options:                                  \n\
    help        shows detailed help for 'help'      \n\
    search      shows detailed help for 'search'    \n\
    library     shows detailed help for 'library'   \n\
                                                    \n\
Example:                                            \n\
     vidsrc-search help library                     \n\
     vidsrc-search help help                        \n\
")

HELP_SEARCH = ("\
Usage: vidsrc-search search <option>                \n\
                                                    \n\
Required option:                                    \n\
    <str>       a movie title that you would like   \n\
                vidsrc-search to search for         \n\
                                                    \n\
Example:                                            \n\
    vidsrc-search search 'oppenheimer'              \n\
    vidsrc-search search 'avatar'                   \n\
")

HELP_LIB = ("\
Usage: vidsrc-search library <option>               \n\
                                                    \n\
Required options:                                   \n\
    remove      removes the movies library          \n\
    download    downloads the latest movies library \n\
                from https://vidsrc.to              \n\
                                                    \n\
Example:                                            \n\
    vidsrc-search library download                  \n\
")


def show_help():
    print(HELP_TEXT)
    return


def show_help_help():
    print(HELP_HELP)
    return
    
    
def show_help_search():
    print(HELP_SEARCH)
    return
    
    
def show_help_lib():
    print(HELP_LIB)
    return


def make_directory(path: str) -> None:
    if os.path.exists(path):
        return
    os.makedirs(path)
    

def delete_directory_recursive(path: str) -> None:
    shutil.rmtree(path)


def cleanup() -> None:
    path_one = os.path.expanduser("~/.config/pymovie/movie_buffer")
    path_two = os.path.expanduser("~/.config/pymovie/tv_buffer")
    delete_directory_recursive(path_one)
    delete_directory_recursive(path_two)
    return


def bootstrap() -> None:
    required_path_one = os.path.expanduser("~/.config/pymovie")
    required_path_two = os.path.expanduser("~/.config/pymovie/movie_buffer")
    required_path_three = os.path.expanduser("~/.config/pymovie/tv_buffer")
    
    make_directory(required_path_one)
    make_directory(required_path_two)
    make_directory(required_path_three)
    return
