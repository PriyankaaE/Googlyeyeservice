import pytest
import cv2
import base64

@pytest.mark.asyncio
async def test_upload_image(test_data, client):
    """
        Uploads the test image in binary format as form Input and checks the response
    """
    form_image = f"data:image/png;base64,{test_data}"

    # Send POST request to the API
    response = client.post("upload-canvas-image/", data={"image": form_image})

    # Assert the response
    assert response.status_code == 200
    response_data = response.json()
    assert "image_url" in response_data
    assert response_data["image_url"].startswith("data:image/png;base64,")