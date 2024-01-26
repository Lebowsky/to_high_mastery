import time
from collections import Counter
from http import HTTPStatus
from enum import Enum
from typing import Callable

import httpx
import tqdm
from flags import save_flag, DEST_DIR, POP20_CC, BASE_URL

DEFAULT_CONCUR_REQ = 1
MAX_CONCUR_REQ = 1


class DownloadStatus(Enum):
    NOT_FOUND: str = 'NOT FOUND'
    OK: str = 'OK'
    ERROR: str = 'ERROR'


def get_flag(base_url: str, cc: str) -> bytes:
    url = f'{base_url}/{cc}/{cc}.gif'.lower()
    resp = httpx.get(url, timeout=3.1, follow_redirects=True)
    resp.raise_for_status()
    return resp.content


def download_one(cc: str, base_url: str, verbose: bool = False) -> DownloadStatus:
    try:
        image = get_flag(base_url, cc)
    except httpx.HTTPStatusError as exc:
        res = exc.response
        if res.status_code == HTTPStatus.NOT_FOUND:
            status = DownloadStatus.NOT_FOUND
            msg = f'not found: {res.url}'
        else:
            raise

    else:
        save_flag(image, f'{cc}.gif')
        status = DownloadStatus.OK
        msg = 'OK'

    if verbose:
        print(cc, msg)

    return status


def download_many(
        cc_list: list[str],
        base_url: str,
        verbose: bool,
        _unused_concur_req: int
) -> Counter[DownloadStatus]:
    counter: Counter[DownloadStatus] = Counter()
    cc_iter = sorted(cc_list)
    if not verbose:
        cc_iter = tqdm.tqdm(cc_iter)

    for cc in cc_iter:
        try:
            status = download_one(cc, base_url, verbose)
        except httpx.HTTPStatusError as ex:
            error_msg = 'HTTP error {resp.status_code} - {resp.reason_phrase}'
            error_msg = error_msg.format(resp=ex.response)
        except httpx.RequestError as ex:
            error_msg = f'{ex}:{type(ex)}'.strip()
        except KeyboardInterrupt:
            break
        else:
            error_msg = ''

        if error_msg:
            status = DownloadStatus.ERROR

        counter[status] += 1
        if verbose and error_msg:
            print(f'{cc} error: {error_msg}')

    return counter


def main(downloader: Callable[[list[str], str, bool, int], Counter[DownloadStatus]]):
    DEST_DIR.mkdir(exist_ok=True)
    t0 = time.perf_counter()
    downloader(POP20_CC, BASE_URL, True, 0)
    elapsed = time.perf_counter() - t0
    print(f'downloaded by {elapsed:.2f} seconds')


if __name__ == '__main__':
    main(download_many)
