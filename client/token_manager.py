import os
from dotenv import load_dotenv


def load_token():
    try:
        file_path = get_token_file_path()
        load_dotenv(file_path)
        token = os.getenv('TOKEN')

        if not token:
            return None

        return token

    except Exception as e:
        print(f'Error: {e}')


def write_token(token):
    try:
        file_path = get_token_file_path()
        with open(file_path, 'w') as f:
            token = f'TOKEN={token}'
            f.write(token)

    except Exception as e:
        print(f'Encountered unexpected error: {e}')


def get_token_file_path(token_file_name='token.env', root_folder='ai-assistant'):
    try:
        path = os.environ.get('LOCALAPPDATA')
        if not path:
            raise EnvironmentError(
                'LOCALAPPDATA environemt variable not found'
            )

        root_path = os.path.join(path, root_folder)

        if not os.path.exists(root_path):
            create_root_folder(root_folder)

        file_path = os.path.join(root_path, token_file_name)

        if not os.path.exists(file_path):
            create_token_file(root_path, token_file_name)

        return file_path

    except FileNotFoundError as fnf_error:
        print(f'File Not Found Error: {fnf_error}')

    except EnvironmentError as env_error:
        print(f'Environment error: {env_error}')

    except Exception as e:
        print(f'Encountered unexpected error: {e}')


def create_root_folder(root_folder='ai-assistant'):
    localappdata_path = os.environ.get('LOCALAPPDATA')

    root_folder_path = os.path.join(localappdata_path, root_folder)

    os.mkdir(root_folder_path)


def create_token_file(path, token_file_name = 'token.env'):
    file_path = os.path.join(path, token_file_name)
    os.mkdir(file_path)
    print('succesfully created a token file')
