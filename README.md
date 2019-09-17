# Decision-Support-Tool
 A multi objective optimisation tool to aid user in comparing multiple optimal trade-offs between 
 objectives  
- Deployed on https://decision-support-framework.herokuapp.com/

TO RUN THE LOCAL VERSION OF THE APP

- Install all the dependancies from requirements.txt
- Run app.py and go to the listed url in the console ( usually at port-8080)
- upload a csv/xlsx file containing objectives or data
- upload a meta file that specifies the col_names and whether should they be Max/Min during optimisation sort 
  (optional - provide epsilon/precision) 
- use the columns dropdown to select relevant columns for viewing, the highlighted rows will be the data points/observations that             
  are *nondominated* or optimal in the n-dimensional space which corresponds to the number of cols in the metafile ( the app only 
  calculates the non-dominated points using columns ie. objectives that are provided in the metafile).
  
  
- Then the user has a choice to plot the optimal points in a 2D-3D space, to spatially analyze the optimal points
- To do so, while the specific cols are selected navigate to the Plot section of the control panel, and select alteast 2 & upto 3 
  columns for plotting with an additional col to label the points in the plot and click plot.
  (Note: the representation recalculates the optimal points in 2 or 3D space only (wrt given plot columns) so the optimal points   
  visually make sense 
  


Note : both the Decision Matrix (Data Table) and the Pareto Plot are linked, changes in the table ie deletion will update the graph   
       with new optimal points wrt the remaining points in the space 

  
  
  
