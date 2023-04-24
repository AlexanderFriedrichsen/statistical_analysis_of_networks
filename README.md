# statistical_analysis_of_networks
Exploratory Assignment Final Deliverable

# Burlington Band Shows Dataset

This dataset was collected through surveying various Burlington bands.

I used the platform Instagram to elicit responses, sending the following message to 26 bands:

"Hey I am compiling a network dataset of burlington bands' past shows, if one of you has like 5 minutes, I would appreciate you going into this spreadsheet and adding your shows [link to spreadsheet]"

I followed up with a second message if I received no response after a week:

"If you have 5 minutes today please fill out your band's part!"

In addition, I replied individually to specific questions or bands who filled out the data or I knew personally.

While the process is seemingly easy, it does require a margin of effort on the part of the band, by going through their own list of shows.

I received data from 6 bands in total, resulting in a set of 164 shows.

The data include show date, bands, venue, and cover fee. There are missing values which are indicated with a hyphen.

I manually cleaned the data to remove duplicate shows, account for misspellings/alternative spellings, reformat data submissions, and capitalize correctly.

The data can be loaded in various ways. In the .ipynb is one implementation to load the data as a bipartite network with bands and venue.
Another implementation could be to use the date to load the network as a temporal network. For instance, one could ask which bands played together more early on.