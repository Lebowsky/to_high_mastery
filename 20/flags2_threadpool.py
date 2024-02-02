from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from http import HTTPStatus

import httpx
import tqdm

from flags2_common import DownloadStatus, save_flag, main

DEFAULT_CONCUR_REQ = 30
MAX_CONCUR_REQ = 1000


def get_flag(base_url: str, cc: str):
    url = f'{base_url}/{cc}/{cc}.gif'.lower()
    resp = httpx.get(url, timeout=3.1, follow_redirects=True)
    resp.raise_for_status()
    return resp.content


def download_one(cc: str, base_url: str, verbode: bool = False) -> DownloadStatus:
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
        msg = f'OK'

    if verbode:
        print(cc, msg)

    return status


def download_many(
        cc_list: list,
        base_url: str,
        verbose: bool,
        concur_req: int
) -> Counter[DownloadStatus]:
    counter: Counter[DownloadStatus] = Counter()
    with ThreadPoolExecutor(max_workers=concur_req) as executor:
        to_do_map = {}
        for cc in sorted(cc_list):
            future = executor.submit(download_one, cc, base_url, verbose)
            to_do_map[future] = cc

        done_iter = as_completed(to_do_map)

        if not verbose:
            done_iter = tqdm.tqdm(done_iter)

        for future in done_iter:
            try:
                status = future.result()
            except httpx.HTTPStatusError as exc:
                error_msg = 'HTTP error {resp.status_code} - {resp.reason_phrase}'
                error_msg = error_msg.format(resp=exc.response)
            except httpx.RequestError as exc:
                error_msg = f'{exc} {type(exc)}'.strip()
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


if __name__ == '__main__':
    main(download_many, DEFAULT_CONCUR_REQ, MAX_CONCUR_REQ)