UAV test generator code the phd position at Unibe

To build the docker image:

docker build -t image_name/tag .

To run the code inside docker container's bash:

docker run -it image_name/tag bash

To run the test generator code

python3 cli.py generate case_studies/mission1.yaml budget num

Budget - allowed simulations
num - number of obstacles (1 for now)
