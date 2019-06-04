### contains Gudhi 2.3.0 dockerfile http://gudhi.gforge.inria.fr/dockerfile/
# Image de base
FROM ubuntu:18.04

# Update and upgrade distribution
RUN apt-get update && \
    apt-get upgrade -y

# Tools necessary for installing and configuring Ubuntu
RUN apt-get install -y \
    apt-utils \
    locales \
    tzdata

# Timezone
RUN echo "Europe/Paris" | tee /etc/timezone && \
    ln -fs /usr/share/zoneinfo/Europe/Paris /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata

# Locale with UTF-8 support
RUN echo en_US.UTF-8 UTF-8 >> /etc/locale.gen && \
    locale-gen && \
    update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# Required for Gudhi compilation
RUN apt-get install -y curl \
    make \
    cmake \
    g++ \
    graphviz \
    doxygen \
    perl \
    libboost-all-dev \
    libeigen3-dev \
    libgmp3-dev \
    libmpfr-dev \
    libtbb-dev \
    locales \
    python3 \
    python3-pip \
    python3-pytest \
    python3-tk \
    libfreetype6-dev \
    pkg-config

RUN apt-get install -y htop \
    silversearcher-ag \
    sudo \
    zip \
    unzip

RUN pip3 install \
    Cython \
    sphinx \
    sphinxcontrib-bibtex \
    matplotlib \
    numpy

RUN pip3 install \
    jupyterlab \
    scipy \
    pandas \
    ipywidgets \
    biopython \
    nglview \
    npm


# apt clean up
RUN apt autoremove && rm -rf /var/lib/apt/lists/*

# # Working directory
# WORKDIR /gudhi

# RUN curl -LO "https://github.com/CGAL/cgal/releases/download/releases%2FCGAL-4.12.1/CGAL-4.12.1.tar.xz" \
# && tar xf CGAL-4.12.1.tar.xz && cd CGAL-4.12.1 \
# && cmake -DCMAKE_BUILD_TYPE=Release -DCGAL_HEADER_ONLY=ON . && make all install && cd .. \
# && curl -LO "https://gforge.inria.fr/frs/download.php/file/37696/2018-09-04-14-25-00_GUDHI_2.3.0.tar.gz" \
# && tar xf 2018-09-04-14-25-00_GUDHI_2.3.0.tar.gz \
# && cd 2018-09-04-14-25-00_GUDHI_2.3.0 \
# && mkdir build && cd build && cmake -DCMAKE_BUILD_TYPE=Release -DWITH_GUDHI_PYTHON=OFF -DPython_ADDITIONAL_VERSIONS=3 ..  \
# && make all doxygen test install \
# && cmake -DWITH_GUDHI_PYTHON=ON . \
# && cd cython \
# && python3 setup.py install

### Gitpod user ###
# '-l': see https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#user
RUN useradd -l -u 33333 -G sudo -md /home/gitpod -s /bin/bash -p gitpod gitpod \
    # passwordless sudo for users in the 'sudo' group
    && sed -i.bkp -e 's/%sudo\s\+ALL=(ALL\(:ALL\)\?)\s\+ALL/%sudo ALL=NOPASSWD:ALL/g' /etc/sudoers
ENV HOME=/home/gitpod
WORKDIR $HOME

### Gitpod user (2) ###
USER gitpod
# use sudo so that user does not get sudo usage info on (the first) login
RUN sudo echo "Running 'sudo' for Gitpod: success"

### Java ###
## Place '.gradle' and 'm2-repository' in /workspace because (1) that's a fast volume, (2) it survives workspace-restarts and (3) it can be warmed-up by pre-builds.
#RUN curl -s "https://get.sdkman.io" | bash \
#  && bash -c ". /home/gitpod/.sdkman/bin/sdkman-init.sh \
#              && sdk install java 8.0.202-zulufx \
#              && sdk install java 11.0.2-zulufx \
#              && sdk default java 8.0.202-zulufx \
#              && sdk install gradle \
#              && sdk install maven \
#              && mkdir /home/gitpod/.m2 \
#              && printf '<settings>\n  <localRepository>/workspace/m2-repository/</localRepository>\n</settings>\n' > /home/gitpod/.m2/settings.xml"
# ENV GRADLE_USER_HOME=/workspace/.gradle/

RUN curl -sL https://deb.nodesource.com/setup_12.x | sudo -E bash -
    && sudo apt-get install -y nodejs



### Node.js ###
# ARG NODE_VERSION=10.15.3
# RUN curl -fsSL https://raw.githubusercontent.com/creationix/nvm/v0.34.0/install.sh | bash \
#     && bash -c ". .nvm/nvm.sh \
#         && nvm install $NODE_VERSION \
#         && npm config set python /usr/bin/python --global \
#         && npm config set python /usr/bin/python \
#         && npm install -g typescript yarn"
# ENV PATH=/home/gitpod/.nvm/versions/node/v${NODE_VERSION}/bin:$PATH

RUN sudo jupyter nbextension enable --py --sys-prefix nglview
RUN sudo jupyter nbextension enable --sys-prefix --py widgetsnbextension
RUN sudo jupyter labextension install @jupyter-widgets/jupyterlab-manager
RUN sudo jupyter-labextension install nglview-js-widgets@1.1.2
RUN sudo jupyter labextension install bqplot