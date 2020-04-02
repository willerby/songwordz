********************************************************
* songwordz - test application for analysing song lyrics
********************************************************


I developed and tested this code mostly using Pycharm, but I have also tested it
in Powershell. I don't have a Linux environment available at the moment.

I have to confess I'm not skilled at distributing Python apps, so apologies if
the installation is somewhat awkward. Believe it or not, we actually developed our
own deployment tools at my last site, thus I'm not too familiar with standard Python deployment tools.

Anyway, the following worked for me, allowing me to deploy from git hub, onto my laptop (I'm making the assumption
you have pip and Python (>=3.6) already installed on your machine):

1) Download zip from github, and extract to a directory of your choosing
2) Open a Powershell / cmd window, and navigate to the root folder of the application
3) Run the following command to install dependencies:

	pip install -r requirements.txt
	
4) invoke your Python executable in the current directory, and the app should start.

	python .
	

***************************************************************
* Usage notes
***************************************************************

1) The app runs via a CLI
2) Some results may run into issues with text-wrapping, so it is inadvisable to run with a small CMD /Powershell window.
3) The demo chart I included looks much better when its window is maximised.

