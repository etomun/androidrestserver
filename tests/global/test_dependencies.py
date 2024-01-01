import pytest
from fastapi import HTTPException
from starlette import status

from src.dependencies import verify_admin_token


@pytest.mark.asyncio
async def test_verify_admin_token_valid():
    valid_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ5WDRvR21vSkFqQzZrb1dicG5pSU9jVTFRSWVFUXlVM2tHS2M5RlZ5ZW9xbGRleWxzaER4cFFQM1VoRUd3SVlPbTVxSDlJRWl5eTJUYTFkT1ZjMEhsS3Z5MUN3V0tVaW5JVzZXekdlY1NaUzhmQ2Y2eHdZcUJOVURRRldtUEVCbCI6ImJ2R0s3TGVpNmh6WGJpSjZ5UU9LZUNKNTFUSXMyYkh1UWUzZU43dHpRV3l1TnVvYll5V2hhYzllQXN6eWRhblJ6TktSUG5wRkU1UVdGcmVjOVVrSzBOM2Zjekh1SjVOZ1BOZ3ZVNDBydk5GbWRMTHZTTXA4UjlZYUFjS3d6VXdjIn0._xVIBq5PBOndRxuKCXgceWbl5-5JipLIhc8sOEWdhZ4"
    result = await verify_admin_token(token=valid_token)
    assert result == True


@pytest.mark.asyncio
async def test_verify_admin_token_insufficient_key():
    insufficient_token = "1bvGK7Lei6hzXbiJ6yQOKeCJ51TIs2bHuQe3eN7tzQWyuNuobYyWhac9eAszydanRzNKRPnpFE5QWFrec9UkK0N3fczHuJ5NgPNgvU40rvNFmdLLvSMp8R9YaAcKwzUwc"
    with pytest.raises(HTTPException) as exc_info:
        await verify_admin_token(token=insufficient_token)
    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc_info.value.detail == "Could not validate admin credentials"


def test_verify_admin_token_invalid_key():
    assert False
