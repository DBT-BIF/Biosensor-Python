
library(plotrix)
par(bty="n") # deleting the box
x = sensor$X
y= sensor$seed_mer_length
from <- 155542
to <- max(sensor$seed_mer_length)-100000
gap.plot(x, y, gap=c(from,to), gap.axis="y",type="a", xlab="Nodes in path", ylab="No. of fragments in target node",xlim = c(0,length(sensor$X)),
         ylim = c(10,max(sensor$seed_mer_length)),add = TRUE)
axis.break(2, from, breakcol="snow", style="gap")
axis.break(2, from*(1+0.02), breakcol="black", style="slash")
axis(2, at=from)

