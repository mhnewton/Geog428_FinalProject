import arcpy as ap

#allow to overwrite data
ap.env.overwriteOutput = True
print("\n\nStarting Program...")

#Create variable for filepath
dataPath = r"E:\School\Geog428\FinalProject"

#Create new geodatabase
ap.management.CreateFileGDB(dataPath, "WorkingFinalProject.gdb")
print("Created new file geodatabase...")

#set workspace
gdb = dataPath + r"\WorkingFinalProject.gdb"
ap.env.workspace = gdb
print("Workspace GDB set...")

#variables for importing fire data
inFeaturesFireCentre = dataPath + r"\Data\FirePrediction\Fires\FireCentres.shp"
fireCentres = 'fireCentre'

inFeaturesFires = dataPath + r"\Data\FirePrediction\Fires\FireIncidentPoly.shp"
firePoly = 'fireIncidentsPoly'

#creating fire feature classes in gdb
ap.FeatureClassToFeatureClass_conversion(inFeaturesFireCentre, gdb, fireCentres)
print("Copied Fire Centre Feature Class...")
ap.FeatureClassToFeatureClass_conversion(inFeaturesFires, gdb, firePoly)
print("Copied Fire Polygon Feature Class...")

#variables for importing weather stations
in_tableTemp = dataPath + r"\Data\FirePrediction\Weather\WeatherStationTemp.csv"
tableTemp = 'tableTemp'
stationTemp = 'weatherStationTemp'
x_coordsTemp = "long"
y_coordsTemp = "lat"

in_tablePrecip = dataPath + r"\Data\FirePrediction\Weather\WeatherStationPrecip.csv"
tablePrecip = 'tablePrecip'
stationPrecip = 'weatherStationPrecip'
x_coordsPrecip = "long"
y_coordsPrecip = "lat"

#import temp and precip .csv files to gdb
ap.conversion.TableToTable(in_tableTemp, gdb, tableTemp)
ap.conversion.TableToTable(in_tablePrecip, gdb, tablePrecip)
print("Imported temperature and precipitation weather station data...")

#convert XY to point 
ap.management.XYTableToPoint(tableTemp, stationTemp, x_coordsTemp, y_coordsTemp)
ap.management.XYTableToPoint(tablePrecip, stationPrecip, x_coordsPrecip, y_coordsPrecip)
print("Converted Weather Station XY into Points...")

#intersect Fires to Fire Centre
firePoly_Centres = 'firePoly_Centre_intersect'
ap.analysis.Intersect([firePoly, fireCentres], firePoly_Centres)
print("Intersect complete")

#create new fields for Year and Month
ap.management.AddField(firePoly_Centres, "YEAR", "SHORT")
ap.management.AddField(firePoly_Centres, "MONTH", "TEXT")
fireYear = "YEAR"
fireMonth = "MONTH"
print("\n" + fireYear + " and " + fireMonth + " Fields created...")

#change field name of FireCentre
ap.management.AlterField(firePoly_Centres, 'MFFRCNTRNM', 'FireCentre', 'FireCentre')
fireCentre = "FireCentre"
print("Changed " + fireCentre + " Field name...")

'''
#list fields
fieldList = ap.ListFields(firePoly_Centres)
for field in fieldList:
    print(field.name)
'''
#Due to unforeseen circumstances and not having access to ArcPro the remainder of the project was completed on ArcOnline and R
#outline for code if I was able to continue with arcPy

#summary statistics variables
fireCentreName = ["Southeast Fire Centre", "Kamloops Fire Centre", "Cariboo Fire Centre", "Coastal Fire Centre", "Prince George Fire Centre", "Northwest Fire Centre"]
fireCentreCount = [0] * len(fireCentreName)
fireCentreSumFire = [0] * len(fireCentreName)
fireYearArray = ['2017', '2018']
fireYearUpdate = [2017, 2018]
fireMonthArray = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
fireMonthUpdate = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"] 
fireCentre = "FireCentre"
fireSize = "SIZE_HA"
fireRecorded = "FIRE_DATE"
originalYears = "FIRE_YEAR"
fireYear = "YEAR"
fireMonth = "MONTH"
minYear = 2017
maxYear = 2018
print("Assigned variables for summary statistics...")

#SQL Query for summary statistics
whereExpr = "((" + fireRecorded + " LIKE '%%%s%%'" %minYear + ") OR (" + fireRecorded + " LIKE '%%%s%%'" %maxYear + "))"
print("SQL expression = " + whereExpr)
count = 0
#Search cursor summary statistics (all years)
with ap.da.SearchCursor(firePoly_Centres, (fireSize, fireCentre), whereExpr) as cursor:
    for i in cursor:
        count += 1
        if i[1] == fireCentreName[0]:
            fireCentreCount[0] += 1
            fireCentreSumFire[0] += i[0]
        #print("starting" + str(fireCentreName[0]) + "...")
        elif i[1] == fireCentreName[1]:
            fireCentreCount[1] += 1
            fireCentreSumFire[1] += i[0]
        #print("starting" + str(fireCentreName[1]) + "...")
        elif i[1] == fireCentreName[2]:
            fireCentreCount[2] += 1
            fireCentreSumFire[2] += i[0]
        #print("starting" + str(fireCentreName[2]) + "...")
        elif i[1] == fireCentreName[3]:
            fireCentreCount[3] += 1
            fireCentreSumFire[3] += i[0]
        #print("starting" + str(fireCentreName[3]) + "...")
        elif i[1] == fireCentreName[4]:
            fireCentreCount[4] += 1
            fireCentreSumFire[4] += i[0]
        #print("starting" + str(fireCentreName[4]) + "...")
        else:
            fireCentreCount[5] += 1
            fireCentreSumFire[5] += i[0]
        #print("starting" + str(fireCentreName[5]) + "...")
    print("Completed Summary Statistics...\n")

print("There were " + str(count) + " fires during " + str(minYear) + " and " + str(maxYear) + ":")
print(str(fireCentreName[0]) + ": " + str(round(fireCentreCount[0])) + ", with " + str(round(fireCentreSumFire[0])) + " hectares burned...\n" +
      str(fireCentreName[1]) + ": " + str(round(fireCentreCount[1])) + ", with " + str(round(fireCentreSumFire[1])) + " hectares burned...\n" +
      str(fireCentreName[2]) + ": " + str(round(fireCentreCount[2])) + ", with " + str(round(fireCentreSumFire[2])) + " hectares burned...\n" +
      str(fireCentreName[3]) + ": " + str(round(fireCentreCount[3])) + ", with " + str(round(fireCentreSumFire[3])) + " hectares burned...\n" +
      str(fireCentreName[4]) + ": " + str(round(fireCentreCount[4])) + ", with " + str(round(fireCentreSumFire[4])) + " hectares burned...\n" +
      str(fireCentreName[5]) + ": " + str(round(fireCentreCount[5])) + ", with " + str(round(fireCentreSumFire[5])) + " hectares burned.\n")

print("Transfering fire date into " + fireYear + " and " + fireMonth + " Fields...")
print("SQL expression = " + whereExpr)
with ap.da.UpdateCursor(firePoly_Centres, (fireRecorded, fireYear, fireMonth), whereExpr) as cursor:
    for i in cursor:
        #update fireYear Field
        if (i[0].startswith(fireYearArray[0])):
            i[1] = fireYearUpdate[0]
        if (i[0].startswith(fireYearArray[1])):
            i[1] = fireYearUpdate[1]

        #update fireMonth Field
        if (i[0][4:6] == fireMonthArray[0]): #take the values in FIRE_DATE in the 4th and 5th position according to fireMonthNewArray and assign it as corresponding month
            i[2] = fireMonthUpdate[0]
        if (i[0][4:6] == fireMonthArray[1]):
            i[2] = fireMonthUpdate[1]
        if (i[0][4:6] == fireMonthArray[2]):
            i[2] = fireMonthUpdate[2]
        if (i[0][4:6] == fireMonthArray[3]):
            i[2] = fireMonthUpdate[3]
        if (i[0][4:6] == fireMonthArray[4]):
            i[2] = fireMonthUpdate[4]
        if (i[0][4:6] == fireMonthArray[5]):
            i[2] = fireMonthUpdate[5]
        if (i[0][4:6] == fireMonthArray[6]):
            i[2] = fireMonthUpdate[6]
        if (i[0][4:6] == fireMonthArray[7]):
            i[2] = fireMonthUpdate[7]
        if (i[0][4:6] == fireMonthArray[8]):
            i[2] = fireMonthUpdate[8]
        if (i[0][4:6] == fireMonthArray[9]):
            i[2] = fireMonthUpdate[9]
        if (i[0][4:6] == fireMonthArray[10]):
            i[2] = fireMonthUpdate[10]
        if (i[0][4:6] == fireMonthArray[11]):
            i[2] = fireMonthUpdate[11]
        cursor.updateRow(i)

print("\nUpdated " + fireYear + " and " + fireMonth + " Fields...")
        
print("Done!")

'''
for list of years{
    for list of months{
        copy selection (select tool) of all fires that have these years and months
        do near function #using select shapefiles
        do interpolation #using select shapefiles
        do zonal statistics
    }
}
'''

            
