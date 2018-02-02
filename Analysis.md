---
title: "Analysis of SF311 data for city events "
output: html_document
---

We have considered the [SF311 data](https://data.sfgov.org/City-Infrastructure/Case-Data-from-San-Francisco-311-SF311-/vw6y-z8j6) for the city infrastructural events in San Francisco,which contains a tabular list of reports. The duration of the data collected is from May 2014 to August 2015.

Loading a 247K row file with 16 columns into R can take awhile. We have used *readr*, another R package by *ggplot2*, which grants access to a *read_csv()* function that has nearly 10x the speed of the base *read.csv()* R function.



```r
library(readr)
path <- "C:\\Users\\Archana\\OneDrive\\Coursera\\City event extraction\\311 data\\Case_Data_from_SF311.csv"
data <- read.csv(path,stringsAsFactors = FALSE)
```

## Number of Open requests

We first look into the requests that are not yet resolved(from Aug 2015 till Dec 2015).


```r
library(plyr)
library(dplyr) 
data_open <- data %>% filter(grepl("Open",Status))
```

So there are still **6211 Open requests**!!

Now lets see the agencies which are resposible for those Open requests.

First, we *group_by()* the Responsible.Agency, and then use *summarize()* to perform an aggregate on each group; in this case, count how many entries for each agency.  We can also ensure that the counts are in descending order to get the most number of open requests with respect to the responsible agencies.(We get the top 10 resposible agencies with open requests)


```r
#Since both dplyr and plyr are loaded there will be a conflict with the summarize command
detach("package:plyr", unload=TRUE)
data_open_agencies <- data_open %>% 
                      group_by(Responsible.Agency) %>% 
                      summarize(count = n()) %>% 
                      arrange(desc(count))
top_data_open_agencies <- head(data_open_agencies,10)
```

We now plot the ouput using *ggplot2*.


```r
library(ggplot2)
g <- ggplot(top_data_open_agencies, aes(top_data_open_agencies$Responsible.Agency, top_data_open_agencies$count))
g + 
geom_bar(stat = 'identity', fill = 'cyan') + 
labs(x = "Resposible agencies")+ labs(y = "No. of open requests") + 
labs(title = "Top 10 agencies with more number of open requests") + 
theme_bw() + theme(axis.text.x = element_text(angle=90,vjust=1),
      plot.title = element_text(size=15),
      axis.title.x = element_text(size=15),
      axis.title.y = element_text(size=15))
```

![plot of chunk unnamed-chunk-4](figure/unnamed-chunk-4-1.png) 

By visualizing the output we can say that **DPW BSSR Queue** has more number of open requests**(1532 )** that are not yet resolved from Aug '15 till Dec '15.


## Common request types and their location


We first look at the most common request or the most common infrastructural issue in the city of San Francisco.


```r
library(ascii)
#library(pander)
data_event <- data %>%
              group_by(Category) %>% 
              summarize(count = n()) %>% 
              arrange(desc(count))

print(ascii(data_event), type = 'rest')
```


+---+------------------------------+-----------+
|   | Category                     | count     |
+===+==============================+===========+
| 1 | Street and Sidewalk Cleaning | 139750.00 |
+---+------------------------------+-----------+
| 2 | Graffiti Public Property     | 44872.00  |
+---+------------------------------+-----------+
| 3 | Damaged Property             | 19581.00  |
+---+------------------------------+-----------+
| 4 | Sewer Issues                 | 13397.00  |
+---+------------------------------+-----------+
| 5 | Streetlights                 | 11266.00  |
+---+------------------------------+-----------+
| 6 | Street Defects               | 7927.00   |
+---+------------------------------+-----------+
| 7 | Litter Receptacles           | 7886.00   |
+---+------------------------------+-----------+

```r
#panderOptions('table.split.table', Inf)
#pandoc.table(data_event)
```

**Street and Sidewalk Cleaning** has the maximum number of requests.

Lets make things interesting by plotting the locations with most number of requests.

First, we split the 'Point' column in the data into latitude(Lat) and longitude(Long).Once the column is split, remove all the punctuations like '(' and ')' from Lat and Long columns.
Next we get the rows for Street and Sidewalk Cleaning requests.

We then plot the Lat and Long using *ggmap* from *ggplot2* package to visualize the locations for Street and Sidewalk Cleaning requests in SF.*ggmap* is used to visualize data on static maps from various online sources like Google maps and Stamen maps.



```r
library(ggmap)
data_split <- data.frame(do.call('rbind', strsplit(as.character(data$Point),',',fixed=TRUE)))
data_split$X1 <- gsub("^[[:punct:]]", "", data_split$X1)
data_split$X2 <- gsub("[[:punct:]]$", "", data_split$X2)
names(data_split)<- c('Lat', 'Long')
data <- cbind(data,data_split)
data$Lat <- as.numeric(data$Lat)
data$Long <- as.numeric(data$Long)

data_max_req <- subset(data, Category == as.character(data_event[1,1]$Category))

#Get the count of most common locations
data_max_loc <- data_max_req %>%
                group_by(Lat,Long) %>%
                summarize(count = n())
data_max_loc <- data_max_loc[order(-data_max_loc$count),]
plot_map <- head(data_max_loc,500)

map_max_req <- get_map(location = c(lon = mean(plot_map$Long), lat = mean(plot_map$Lat)), zoom = 13, maptype = "roadmap", scale = 2)

ggmap(map_max_req, extent = 'device') + geom_point(data = plot_map, aes(x = Long, y = Lat, fill = "red", alpha = 0.8), size = 2, shape = 21) + guides(fill=FALSE, alpha=FALSE, size=FALSE) + ggtitle("Locations in SF with most number of requests")+
theme(plot.title = element_text(size = rel(1.5), color = 'red'))
```

![plot of chunk unnamed-chunk-6](figure/unnamed-chunk-6-1.png) 

We can see that the concentration of requests are around the **Mission district** and **Financial district** localities. The responsible authorities can make use of this data and take required action for the requests.

But when do requests occur the most? To be more clear about this lets look at the next section.

## Distribution of events


We have collected the data for more than a year(i.e, from May 2014 - Aug 2015). So we look at events grouped for each month and distributed for all the weekdays for that month. This could be done by using *facet* a tool in *ggplot2*.

We need to mould the data before we plot it.This requires us to get the month and the day of week for each requests.

**Day of week**

We get the day of week for each entry of the request using the column 'Opened' using the function *weekdays()* which gives us the day of week for a given date. 

**Month**

We use *strsplit()* to split a single date value to Month, Day and Year components, take the first value (Month), and convert that value to a numeric value (instead of text) For example, "08/12/2014" input returns 8. Since this has to be done for every row in the data we use *sapply()* function.

Finally we count the number of requests for a given day of week and month.We group by 'Category', 'Month' and 'Dayofweek'.



```r
Dayofweek <- weekdays(as.Date(data$Opened,"%m/%d/%Y"))
data <- cbind(data,Dayofweek)

get_month <- function(x) {
  return (as.numeric(strsplit(x,"/")[[1]][1]))
}

data_event_time <- data %>%
                    mutate(Month = sapply(Opened, get_month)) %>%
                    group_by(Category, Month, Dayofweek) %>%
                    summarize(count = n())

#Convert numeric month to type string(abbreviation)
data_event_time$Month <- month.abb[data_event_time$Month]

#Arrange the month in ascending order for plotting
data_event_time$Month <- factor(data_event_time$Month, levels=c
('Jan','Feb','Mar','Apr','May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'))
```

We plot heatmap for each 'Category' for a given day of week and month.



```r
plot <- ggplot(data_event_time, aes(x = factor(Dayofweek, levels = c('Monday','Tuesday', 'Wednesday', 'Thursday', 'Friday','Saturday', 'Sunday')), y = Category, fill = count)) 

plot + 
geom_tile() + 
labs(x = "Day of week", y = "Category", title = "No. of requests per month") +
theme(plot.title = element_text(size = rel(2)), axis.text.x = element_text(angle=90, vjust = 0.6, size = 8), axis.title.x = element_text(size = rel(1.5)), axis.title.y = element_text(size = rel(1.5))) +
scale_fill_gradient(low = "white", high = "blue") + 
facet_wrap(~ Month, nrow = 4)
```

![plot of chunk unnamed-chunk-8](figure/unnamed-chunk-8-1.png) 


The plot looks interesting!

We can see that there are lot more requests during summer(May-Aug) and the requests are low during other months.
Also the number of requests reduce a lot over the weekends!!

