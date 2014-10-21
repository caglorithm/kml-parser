GOOGLE LOCATION SERVICE KML PARSER (0.1)
This was tested only with the kml's that are produced by Google from your
Android phones location data.
If you have enabled the location reporting on your phone you can view
the location data on an interactive map at
https://maps.google.com/locationhistory/
You can download the kml file of your location data using this link
https://maps.google.com/locationhistory/b/0/kml?startTime=0&endTime=2383260400000
It will request the location saved from the beginning of time until a very
far timestamp in the future, so everything you ever submitted should be included.
Name or path to the kml file to parse
docname = 'big.kml'

docname = 'medium.kml'
Save your custom locations here
Format is [(x-coord), (y-cood), (radius), name]
Coordinates have to be put in decimals! For exmaple 49.006033 instead of something
like 49 0'21.72".
A radius of 0.004 has proven to be reasonable for a place like a home or workplace.
(Python beginners: don't forget to add a colon (,) at the end of the old last line
and don't forget to shift the new line that you add properly to match the other lines)