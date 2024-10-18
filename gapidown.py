#!/usr/bin/python3
from typing import Union
from pathlib import Path
import argparse
import abc


class BackendInterface(abc.ABC):
    backend_classes = dict()
    URL_TEMPLATE = 'https://www.googleapis.com/drive/v3/files/{file_id}'
    LIST_FOLDER_PARAMETERS_TEMPLATE = 'q=\'{file_id}\'+in+parents'
    DOWNLOADING_PARAMETERS = 'alt=media'

    def __init__(self, token: str) -> None:
        self.headers = {'Authorization': f'Bearer {token}'}

    def __init_subclass__(cls) -> None:
        assert cls.__name__.endswith('Backend')
        cls.backend_classes[cls.__name__[:-7].lower()] = cls
        return super().__init_subclass__()

    @staticmethod
    def __check_file_info_format(data: dict) -> bool:
        if data.keys() != {'mimeType', 'kind', 'id', 'name'}:
            return False
        for x in data.values():
            if not isinstance(x, str):
                return False
        return True

    @staticmethod
    def is_folder_mime_type(mime_type: str) -> bool:
        return mime_type == 'application/vnd.google-apps.folder'

    def get_file_info(self, file_id: str) -> dict:
        url = self.URL_TEMPLATE.format(file_id=file_id)
        data = self._get_file_info(url)
        assert self.__check_file_info_format(data)
        return data

    def list_folder(self, file_id: str) -> list:
        results = list()

        page_token = ''
        while page_token is not None:
            url = [
                self.URL_TEMPLATE.format(file_id=''),
                '?',
                self.LIST_FOLDER_PARAMETERS_TEMPLATE.format(file_id=file_id),
                '&pageToken=',
                page_token,
            ]
            data = self._list_folder(''.join(url))
            assert isinstance(data, dict)
            page_token = data['nextPageToken'] = data.get('nextPageToken', None)
            assert data.keys() == {'files', 'incompleteSearch', 'kind', 'nextPageToken'}
            assert data['kind'] == 'drive#fileList'
            assert data['incompleteSearch'] == False
            assert isinstance(data['files'], list)

            for item in data['files']:
                assert self.__check_file_info_format(item)
            results += data['files']
        return results

    def download_file(self, file_id: str, output_path: Path) -> int:
        url = [
            self.URL_TEMPLATE.format(file_id=file_id),
            '?',
            self.DOWNLOADING_PARAMETERS,
        ]
        return self._download_file(''.join(url), output_path)

    @abc.abstractmethod
    def _get_file_info(self, file_id: str) -> dict:
        pass

    @abc.abstractmethod
    def _list_folder(self, file_id: str) -> Union[list, dict]:
        pass

    @abc.abstractmethod
    def _download_file(self, url: str, output_path: Path) -> int:
        pass


class RequestsBackend(BackendInterface):
    def __init__(self, token: str) -> None:
        super().__init__(token)
        from requests import Session
        from tqdm import tqdm

        self._tqdm = tqdm
        self._session = Session()
        self._session.headers = self.headers.copy()

    def _get_file_info(self, url: str) -> dict:
        resp = self._session.get(url)
        resp.raise_for_status()
        return resp.json()

    def _list_folder(self, url: str) -> dict:
        resp = self._session.get(url)
        resp.raise_for_status()
        return resp.json()

    def _download_file(self, url: str, output_path: Path) -> int:
        total_size = 0
        with self._session.get(url, stream=True) as resp:
            resp.raise_for_status()
            total_size = int(resp.headers.get('Content-Length', 0))
            bar = self._tqdm(
                desc=output_path.as_posix(),
                total=total_size,
                unit='B',
                unit_scale=True,
                unit_divisor=1024,
            )

            with open(output_path, 'wb') as file:
                for chunk in resp.iter_content(chunk_size=1024 * 1024):
                    assert len(chunk) > 0
                    size = file.write(chunk)
                    total_size += size
                    bar.update(size)
            bar.close()
        return total_size


def _recur_download(
    backend: BackendInterface,
    file_info_or_id: Union[dict, str],
    output_root: Path,
) -> int:
    if isinstance(file_info_or_id, str):
        file_info = backend.get_file_info(file_info_or_id)
    else:
        file_info = file_info_or_id
    file_id, filename = file_info['id'], str(file_info['name'])

    if not backend.is_folder_mime_type(file_info['mimeType']):
        output_path = output_root / filename
        if output_path.exists():
            if args.exists == 'skip':
                return 0
            elif args.exists == 'overwrite':
                pass
            elif args.exists == 'error':
                raise FileExistsError(output_path)
            else:
                raise NotImplementedError('option --exists', args.exists)
        return backend.download_file(file_id, output_path)

    output_folder = output_root / filename
    output_folder.mkdir(parents=True, exist_ok=True)

    total_size = 0
    for item in backend.list_folder(file_id):
        total_size += _recur_download(backend, item, output_folder)
    return total_size


def main(args: argparse.Namespace) -> int:
    backend_cls = BackendInterface.backend_classes[args.backend]
    assert issubclass(backend_cls, BackendInterface)
    backend = backend_cls(args.access_token)
    total_size = _recur_download(backend, args.file_id, Path(args.output or '.'))
    print(f'Downloaded {total_size} bytes')
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        usage='''
1. Visit: https://developers.google.com/oauthplayground/
2. Select: Drive API v3 >> https://www.googleapis.com/auth/drive.readonly
3. Authorize API
4. Refresh and copy the access token
'''
    )
    parser.add_argument('access_token', type=str)
    parser.add_argument('file_id', type=str)
    parser.add_argument('--output', '-o', type=str, default=None)
    parser.add_argument(
        '--exists',
        type=str,
        default='error',
        choices=['skip', 'overwrite', 'error'],
    )
    parser.add_argument(
        '--backend',
        type=str,
        default=tuple(BackendInterface.backend_classes.keys())[0],
        choices=BackendInterface.backend_classes.keys(),
    )
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    retc = main(args)
    exit(retc)
