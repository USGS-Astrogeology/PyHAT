"""
This is the progress bar, it will call upon a seperate Thread to do work for us
Once the thread terminates we will receive our result.
*What this means that we should be able to continue on our merry way adding modules

*Yet to be tested
"""

def onStart(self):
    self.progressBar.setRange(0, 0)
    self.myLongTask.start()


def onFinished(self):
    # Stop the pulsation
    self.progressBar.setRange(0, 1)
    self.progressBar.setValue(1)