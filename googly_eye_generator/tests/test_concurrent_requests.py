import pytest
import cv2
import base64
import time
import asyncio


@pytest.mark.asyncio
async def test_concurrent_image_uploads(test_data, client):
    """
    This test checks how the FastAPI app handles multiple concurrent image uploads.
    """
    form_image = f"data:image/png;base64,{test_data}"
    
    # Number of concurrent requests to simulate
    num_requests = 50

    async def send_request():
        response = client.post("/upload-canvas-image/", data={"image": form_image})
        assert response.status_code == 200
        assert "image_url" in response.json()

    # Start timing the test
    start_time = time.time()

    # Run multiple concurrent requests
    await asyncio.gather(*[send_request() for _ in range(num_requests)])

    # End timing the test
    total_time = time.time() - start_time

    # Output the time taken for the test
    print(f"Processed {num_requests} requests in {total_time:.2f} seconds")

    # Check if the requests were handled within a reasonable time (threshold)
    assert total_time < 20  # Adjust threshold as needed based on your app's performance
