Welcome to the GooglyEyeService.

The code runs on FastAPI and Python with a single HTTP EndPoint to fetch the uploaded image, process and return it.

To ease the packaging, testing and production process,the code is wrapped with tox and also docker option is provided.

Pytest is used to run the testing of endpoints.
There are 2 tests written.
    1. Upload a sample image and testing the response from the TestClient.
    2. Calling the server using TestClient 50 times and checking the performance under load.


To run the application using tox,
    
    1. Install tox (tox==4.21.2) 
    2. cd googly_eye_generator/
    3. And run the command - tox 
        This command installs the required packages mentioned in requirements.txt 
        and create a virtaul environment under '.tox' folder.
        It runs the pytest to test the endpoints and finally starts the uvicorn server.

To create a docker using the Dockerfile

    1. Install docker
    2. Run - docker build -t googly_image .
    3. To execute - docker run -e PORT=3000 -p 3000:3000 googly_image
        Here -e in the env variable of the container port at which it runs the app
        -p is the host_port:container_port 
        (-e PORT and container port in -p should be same)
    4. Open http://0.0.0.0:host_port to view the app on the browser.

