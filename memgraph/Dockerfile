FROM memgraph/memgraph-mage:1.01

USER root

# Install pip packages
COPY requirements.txt ./
RUN pip3 install -r requirements.txt

# Copy the local query modules
COPY procedures/ /proceduress
COPY transformations/ /transformations

USER memgraph
