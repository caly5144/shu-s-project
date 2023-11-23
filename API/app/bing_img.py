from fastapi import APIRouter
from lib.utility import get_bing_img_url, img_to_base64, timeout_decorator

router = APIRouter()

@router.get("/bing_img/")
@timeout_decorator(3)
async def get_bing_img(is_base64: bool = False):
    import time
    time.sleep(2)
    img_url = get_bing_img_url()
    if is_base64:
        return {
            'code' : 200,
            'msg' : 'success',
            'data' : img_to_base64(img_url)
        }
    else:
        return {
            'code' : 200,
            'msg' : 'success',
            'data' : img_url
        }



if __name__ == '__main__':
    pass