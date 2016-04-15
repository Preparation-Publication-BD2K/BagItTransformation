############################################################
# Dockerfile to build bagit_extract
############################################################

# Set the base image to python v3
FROM python:2.7-slim

# File Author / Maintainer
MAINTAINER Charles Blatti

# Update the repository sources list
RUN apt-get update && apt-get install -y rsync wget python-pip

RUN pip install bagit

# Set default contain command on run
CMD /bin/bash

# Set container execution behavior
# ENTRYPOINT