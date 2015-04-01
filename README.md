# Watchseries

Unofficial Linux client for watchseriestv.to which allows you to stream or download videos from the site (currently videos from gorillavid.in are only supported). It is encouraged that the following policy listed in the "Watch Series Link Removal Policy (DMCA)" - http://watchseriestv.to/dmca - be kept in mind and adhered to while using this application

```
[...]WatchSeries is a simple search engine of videos available at a wide variety of third party 
websites.

Any videos shown on third party websites are the responsibility of those sites and not WatchSeries.
We have no knowledge of whether content shown on third party websites is or is not authorized by 
the content owner as that is a matter between the host site and the content owner. WatchSeries does
not host any content on its servers or network.
```

#Usage

use the following command to run the application

*python watchseries.py -[e|s] -[d]*  
  
  -e : Directly lists all episodes of the series selected  
  -s : Lists the seasons of the series first and then the episodes  
  -d : Download mode  
            Downloads video to current directory

#ToDo

- Add checks for non-numeric input
- Add checks to ensure user input is within bounds
- Add try-except to handle "too many requests error"
- Add option to change download directory
- Change Structure(add classes) of code ; separate out watchseries and plugins (gorilavid etc.)
- Use local storage to limit repeated accesses to the site
- Add option to add favourites which will be listed on the first page in addition to search
 

