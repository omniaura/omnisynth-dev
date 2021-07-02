Installation Guide
==================

Welcome to the OmniSynth installation guide! Please follow the instructions below that correspond to your environment.


RaspberryPi 
^^^^^^^^^^^

#. Install Raspbian OS

    * We recommend the `latest 2019 version`_ of Raspbian OS to avoid installing Pulseaudio, a sound driver that messes with Supercollider's Jack interface.

#. Install SuperCollider

    * Follow the `official build instructions`_ from SuperCollider. Do not run "sudo apt-get dist-upgrade" or you will accidentally install Pulseaudio.

#. Install OmniSynth

    * Clone OmniSynth:

    .. code-block:: console 

        git clone git@github.com:omniaura/omnisynth.git

    * Install required Python packages:

    .. code-block:: console

        pip3 install Kivy==2.0.0
        pip3 install py-midi
        pip3 install python-osc
        pip install kivy-garden
        garden install graph
        garden install matplotlib

#. Running the OmniSynth GUI

    * Set the DISPLAY port:

    .. code-block:: console

        export DISPLAY=:0.0

    * Start the OmniSynth SuperCollider server:

    .. code-block:: console

        cd omnisynth/
        sclang dsp/main.scd

    * Start the GUI:

    .. code-block:: console

        cd omnisynth/
        python3 gui/gui.py

    

Mac / Linux / Windows
^^^^^^^^^^^^^^^^^^^^^

#. Install Supercollider 

    * Visit the official `SuperCollider downloads page`_ to install the correct build for your OS. 

#. Install OmniSynth

    * Clone OmniSynth:

    .. code-block:: console 

        git clone git@github.com:omniaura/omnisynth.git

    * Install required Python packages:

    .. code-block:: console

        pip install Kivy==2.0.0
        pip install py-midi
        pip install python-osc
        pip install kivy-garden
        garden install graph
        garden install matplotlib

#. Running the OmniSynth GUI

    * Start the OmniSynth SuperCollider server:

    .. code-block:: console

        cd omnisynth/
        sclang dsp/main.scd

    * Start the GUI:

    .. code-block:: console

        cd omnisynth/
        python gui/gui.py

.. _official build instructions: https://github.com/supercollider/supercollider/blob/develop/README_RASPBERRY_PI.md
.. _latest 2019 version: https://downloads.raspberrypi.org/raspbian/images/raspbian-2019-09-30/
.. _SuperCollider downloads page: https://supercollider.github.io/download

