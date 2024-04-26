install.packages('igraph')
library(igraph)
df <- read.csv(file = 'github/ica-authors/data/plots/cntry_chord_from_firstauthor.csv')
head(df)

df.g <- graph.data.frame(d = df, directed = TRUE)
plot(df.g, vertex.label = V(df.g)$name)

plot(df.g, 
     rescale = TRUE,
     edge.width=E(df.g)$Weight*0.5,
     edge.arrow.size = 0.4,
     vertex.size= degree(df.g)*0.5,
     main="Degree Centrality",
     layout=layout_with_sugiyama,
     )

degree(df.g)
rescale = function(x,a,b,c,d){c + (x-a)/(b-a)*(d-c)}
rescale(degree(df.g), 0, 60, 1, 5)
