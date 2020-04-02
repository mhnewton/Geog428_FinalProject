install.packages("ggplot2")
library("ggplot2")

#Set working directory
dir <- "/Users/mikenewton/Desktop/Geog428/FinalProject/Data/FirePrediction/Fires/Methods"
setwd(dir)

#Reading in dataset
firePoly <- read.csv("firePolyWeather2017_for_scatterplot.csv")
#colnames(firePoly)
#head(firePoly)

#subset columns
firePoly <- firePoly[,c(7,14,23:25,29,36,37)]
colnames(firePoly)
head(firePoly)

#convert hospital distance and population values to log
firePoly$SIZE_HA <- log(firePoly$SIZE_HA + 1) #add 1 so values less than 1 are not negative
firePoly$Near.totalPrecip <- log(firePoly$Near.totalPrecip + 1)
firePoly$Interpolate.AvePrecip <- log(firePoly$Interpolate.AvePrecip + 1)
firePoly$Near.AveTemp <- (firePoly$Near.AveTemp)
#head(firePoly)

#linear models
lm.model.NearTemp <- lm(firePoly$SIZE_HA~firePoly$Near.AveTemp)
lm.model.NearPrecip <- lm(firePoly$SIZE_HA~firePoly$Near.totalPrecip)
lm.model.IntTemp <- lm(firePoly$SIZE_HA~firePoly$Interpolate.AveTemp)
lm.model.IntPrecip <- lm(firePoly$SIZE_HA~firePoly$Interpolate.AvePrecip)

#summary of Linear models
summary(lm.model.NearTemp)
par(mfrow = c(2,2)) #sets up result plots in 2 by 2 pane
plot(lm.model.NearTemp) 

summary(lm.model.NearPrecip)
par(mfrow = c(2,2)) #sets up result plots in 2 by 2 pane
plot(lm.model.NearPrecip) 

summary(lm.model.IntTemp)
par(mfrow = c(2,2)) #sets up result plots in 2 by 2 pane
plot(lm.model.IntTemp) 

summary(lm.model.IntPrecip)
par(mfrow = c(2,2)) #sets up result plots in 2 by 2 pane
plot(lm.model.IntPrecip) 

#scatterplot Near tool Temp
png("./NearTempScatterplot.png", width = 8, height = 6, units = "in", res = 300) #create a png file
ggplot(firePoly, aes(x=Near.AveTemp, y=SIZE_HA)) + #classify x and y, qualitative classes
  geom_point(size = 0.5) + #set point size
  stat_smooth(data = firePoly, aes(x=Near.AveTemp, y=SIZE_HA), method = lm, se = FALSE, formula = y ~ x) +
  labs(title = "Average Monthly Temperature vs. fire size in British Columbia 2017\nUsing Find Nearest tool", x = "Monthly Temperature (°C)", y = "Fire Size (log(hectares)",
       caption = "Figure 1: Scatterplot of average monthly temperature and fire size of fire incidents during 2017 in British Columbia.") + #label plot, x axis, y axis
  theme_classic() + #set the theme to classic (removes background and borders etc.)
  theme(plot.title = element_text(face = "bold", hjust = 0.5), plot.caption = element_text(hjust = 0)) #set title to center and bold
dev.off()

#scatterplot near tool Precip
png("./NearPrecipScatterplot.png", width = 8, height = 6, units = "in", res = 300) #create a png file
ggplot(firePoly, aes(x=Near.totalPrecip, y=SIZE_HA)) + #classify x and y, qualitative classes
  geom_point(size = 0.5) + #set point size
  stat_smooth(data = firePoly, aes(x=Near.totalPrecip, y=SIZE_HA), method = lm, se = FALSE, formula = y ~ x) +
  abline(lm.model.NearPrecip, lwd = 2, col = "blue")+
  labs(title = "Monthly Precipitation vs. fire size in British Columbia 2017\nUsing Find Nearest tool", x = "Monthly Total Precipitation (log(mm))", y = "Fire Size (log(hectares)",
       caption = "Figure 2: Scatterplot of monthly total precipitation and fire size of fire incidents during 2017 in British Columbia.") + #label plot, x axis, y axis
  theme_classic() + #set the theme to classic (removes background and borders etc.)
  theme(plot.title = element_text(face = "bold", hjust = 0.5), plot.caption = element_text(hjust = 0)) #set title to center and bold
dev.off()

#scatterplot Interpolation Temp
png("./InterpolateTempScatterplot.png", width = 8, height = 6, units = "in", res = 300) #create a png file
ggplot(firePoly, aes(x=Interpolate.AveTemp, y=SIZE_HA)) + #classify x and y, qualitative classes
  geom_point(size = 0.5) + #set point size
  stat_smooth(data = firePoly, aes(x=Near.AveTemp, y=SIZE_HA), method = lm, se = FALSE, formula = y ~ x) +
  abline(lm.model.IntTemp, lwd = 2, col = "red")+
  labs(title = "Average Monthly Temperature vs. fire size in British Columbia 2017\nUsing Interpolation and Zonal Statistics", x = "Monthly Temperature (°C)", y = "Fire Size (log(hectares)",
       caption = "Figure 3: Scatterplot of average monthly temperature and fire size of fire incidents during 2017 in British Columbia.") + #label plot, x axis, y axis
  theme_classic() + #set the theme to classic (removes background and borders etc.)
  theme(plot.title = element_text(face = "bold", hjust = 0.5), plot.caption = element_text(hjust = 0)) #set title to center and bold
dev.off()

#scatterplot Interpolation Precip
png("./InterpolatePrecipScatterplot.png", width = 8, height = 6, units = "in", res = 300) #create a png file
ggplot(firePoly, aes(x=Interpolate.AvePrecip, y=SIZE_HA)) + #classify x and y, qualitative classes
  geom_point(size = 0.5) + #set point size
  stat_smooth(data = firePoly, aes(x=Near.totalPrecip, y=SIZE_HA), method = lm, se = FALSE, formula = y ~ x) +
  abline(lm.model.IntPrecip, lwd = 2, col = "blue")+
  labs(title = "Average Monthly Precipitation vs. fire size in British Columbia 2017\nUsing Interpolation and Zonal Statistics", x = "Monthly Total Precipitation (log(mm))", y = "Fire Size (log(hectares))",
       caption = "Figure 4: Scatterplot of average monthly temperature and fire size of fire incidents during 2017 in British Columbia.") + #label plot, x axis, y axis
  theme_classic() + #set the theme to classic (removes background and borders etc.)
  theme(plot.title = element_text(face = "bold", hjust = 0.5), plot.caption = element_text(hjust = 0)) #set title to center and bold
dev.off()
