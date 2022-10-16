# WaterLevels_Measurement_Elbe
Measures the level of river elbe every 5 mins.<br />
The REST api retrieve request is filtered so the payload contains only data from stations of the river Elbe. <br />
This measurement data is obtained as list of dictionaries with subdictionaries. The 7, 8, 9 measurements are used for further processing. <br />

Measurements are written into csv file every 5 mins.<br />
An email is sent if the waterlevel of any of the measurements is below/above 100. The email is sent with smtp.
<br />
<br />
Remark:<br />
The email sent appears to be comming from the same measurement. This is not the case. This is because, very specific names contain characters which could not be encoded by ascii for smtp transmission. A much generic name was used, and these names in the email are the same. This names constitute 3 sequential stations on the Elbe.<br />
References:<br />
-https://www.nylas.com/blog/use-python-requests-module-rest-apis/
Datasource:<br />
-https://pegelonline.wsv.de/<br />
