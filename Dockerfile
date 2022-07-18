FROM docker.io/continuumio/miniconda3:4.12.0
RUN git clone https://github.com/thomleysens/pbf2graph
RUN mkdir data
RUN conda env create -f pbf2graph/environment.yml
RUN echo "source activate pbf2graph" > ~/.bashrc
ENV PATH /opt/conda/envs/env/bin:$PATH