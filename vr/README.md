# Learning body pose using neural networks
In this exercise we try to predict the position of elbows, knees, front and back based on input from a virtual reality headset and controllers.
Take a look at [these slides](https://uob-my.sharepoint.com/personal/lb17101_bristol_ac_uk/_layouts/15/guestaccess.aspx?docid=0cb898751d07a41a4b909cbda5235801f&authkey=AZ8tTilg0tIpO80VyfcwZDA&expiration=2017-12-20T17%3a06%3a45.000Z) for a short overview of the problem as well as [this video](https://github.com/davidglo/ML-CHAMPS-Sept2017/blob/master/vr/documentation/body-tracking-screen-grab.mp4?raw=true)

## Required packages:

1. pandas
2. seaborn
3. scikit-learn

## Visualisation:
In the notebook we visualise the predictions with a 3D-renderer.
Pre-compiled versions for windows, mac and linux are available in the [bin directory](https://github.com/davidglo/ML-CHAMPS-Sept2017/tree/master/vr/bin).
To visualise the predictions, execute the binary for your operating system, select 800x600 and pres OK.
When running the notebook a server will be started that sends data to the renderer.
At this point, pres the connect button in the renderer.
