import asyncio
from collections import Counter
from http import HTTPStatus
from pathlib import Path

import httpx
import tqdm

from flags2_common import DownloadStatus, save_flag, POP20_CC, BASE_URL

DEFAULT_CONCUR_REQ = 5
MAX_CONCUR_REQ = 1000


async def get_flag(client: httpx.AsyncClient,
                   base_url: str,
                   cc: str) -> bytes:
    url = f'{base_url}/{cc}/{cc}.gif'.lower()
    resp = await client.get(url, timeout=3.1, follow_redirects=True)
    resp.raise_for_status()
    return resp.content


async def download_one(client: httpx.AsyncClient,
                       cc: str,
                       base_url: str,
                       semaphore: asyncio.Semaphore,
                       verbose: bool) -> DownloadStatus:
    try:
        async with semaphore:
            image = await get_flag(client, base_url, cc)
    except httpx.HTTPStatusError as exc:
        res = exc.response
        if res.status_code == HTTPStatus.NOT_FOUND:
            status = DownloadStatus.NOT_FOUND
            msg = f'not found: {res.url}'
        else:
            raise

    else:
        await asyncio.to_thread(save_flag, image, f'{cc}.gif')
        status = DownloadStatus.OK
        msg = 'OK'
    if verbose and msg:
        print(cc, msg)
    return status


async def supervisor(base_url, cc_list, concur_req, verbose=False):
    # вернуть должны Counter статусов
    counter = Counter()
    # семафор инициализируется количеством потоков
    semaphore = asyncio.Semaphore(concur_req)
    # в контексте http-клиента
    async with httpx.AsyncClient() as client:
        # Сделать список корутин для загрузки
        coro_list = [download_one(client, cc, base_url, semaphore, verbose) for cc in sorted(cc_list)]
        # метод as_complete формирует итератор объектов сопрограм,
        # который будет возвращать каждый раз результат завершившейся сопрограммы
        coro_iter = asyncio.as_completed(coro_list)
        if not verbose:
            # его мы можем оберунть в прогресс бар, если не нужно выводить детальную информацию
            coro_iter = tqdm.tqdm(coro_iter)

        error = None
        # в цикле получаем результаты выполнения сопрограмм
        for coro in coro_iter:
            try:
                status = await coro
            except httpx.HTTPStatusError as exc:
                error_msg = 'HTTP error {resp.status_code} - {resp.reason_phrase}'
                error_msg = error_msg.format(resp=exc.response)
                error = exc
            except httpx.RequestError as exc:
                error_msg = f'{exc} - {type(exc)}'.strip()
                error = exc
            except KeyboardInterrupt:
                break

            if error:
                status = DownloadStatus.ERROR
                if verbose:
                    url = str(error.request.url)
                    cc = Path(url).stem.upper()
                    print(f'{cc} error: {error_msg}')
                counter[status] += 1

        return counter


# download many по сути запускает наш supervisor в асинхронном режиме
def download_many():
    return asyncio.run(
        supervisor(
            base_url=BASE_URL,
            cc_list=POP20_CC,
            concur_req=DEFAULT_CONCUR_REQ
        )
    )


def main():
    print(download_many())


if __name__ == '__main__':
    main()
