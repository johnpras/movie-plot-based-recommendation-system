•	Content-based recommender: it suggests similar items based on a the plot you want to see.<br>
•	The model will recommend movies based on the plot we want.<br> 
•	It compares the semantic meaning of the descriptions using cosine similarity score.

• api post sends the user input to a temporary txt file and then the python script reads the txt file and generates the results (transformers model)<br> 
• api get sends the results back here<br> 
• using omdbapi we enhance the user generated results and we also display the movie poster and plot <br> 

custom dataset from "movies_metadata"
