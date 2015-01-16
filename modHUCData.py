import gdal, ogr, osr, numpy, sys,glob,os.path,shutil
from modOSGeo import zonal_stats, loop_zonal_stats, loop_count_stats,zonal_count, AreaOfPoly
'''   Version 0.5 of the objHUC approach for basin hydrology.
      Daryl_Van_Dyke@fws.gov
	  public domain code
'''


class HUCData:
    def __init__(self,inputName,inSHP):
        inputName = "HUC_10"
        self.name = inputName
        self.SHPpath = inSHP
        self.shp = ogr.Open(inSHP)
        self.lyr = self.shp.GetLayer()
        self.HUCLevel = 10
        self.featList = range( self.lyr.GetFeatureCount() )    
        #  Which Params bookkeeping? =fix= 
        self.listParams = []

        self.dictPPT = {}
        self.listActiveParams = ['ppt']            
    #  Hydrologic Data       
        self.dictYearlyAll = {}
        self.dictCellCounts = {}
    #   {Parameter:                                                          }
    #           {Year:                                                     }
    #                           {Month:                                 }
    #                                         {  Day:                 }
    #                                                   { FID:      }
#  outer Dict      <FID>: <value_tuple>
#                  {  key  : |->              value                                       <-|       }
#  dictHUCValues = { <FID> : ( (<HUC10Code>    ),{'<param>.<stat>' : (<value>,<unit>),... ]  ), ... }
#          dictHUCs[FID] =   |  \    -0-        |       -1-                                  |
#                            |                  |                                            |
#  <value_tuple>[0]          |    <HUC10Code>   |                                            |
#  <value_tuple>[1]          |                  |         <dictParamVals>                    |
#                            |                  |                                            |
#           Huc10 for unit    \   (val_tuple)[0]|                                           /  
#           dict of Values     \                |  (val_tuple)[1]                          /  ==> dictVal
# show me what param.stats are here    dictHUCValues['13'][1].keys
#            e.g 'ppt.sum' or 'tmax.max'
#       Packing instructions:
#                  1)                                     (         dictParamVals  )
#                  2) 
        self.dictHUCtoFID = {}
        #construct dictHUCtoFID
        for units in self.featList:
            feat = self.lyr.GetFeature(units)
            HUCVal = feat.GetFieldAsString("HUC_10")
            self.dictHUCtoFID[HUCVal] = units

        self.dictFIDAreas = {}
        #  Construct Dictionary of Areas
        self.dictFIDAreas = AreaOfPoly(self.lyr)

    def calculateStats(self, inPrismOBJ, listStats =['sum'], inMonth="all"):
        ''' args: (1)  inPrismYearOBJ, 
                  (2)  listStats default=['sum'], 
                          inputListStat { 'min', 'max', 'sum', 'mean', 'median', 'stddev'  }

                   (3)  Months? : "all" or 2-digt string listStrYears => ['01','12']
        '''
        # for a year, a HUCScale
        thisParam = inPrismOBJ.parameter
        self.listParams.append(thisParam)
        if not inPrismOBJ.inventoryDone:
            return 0
        else:
            LdictMonths = inPrismOBJ.dictMonths
            if inMonth == "all":
                listMonths = ['01','02','03','04','05','06','07','08','09','10','11','12']
            else:
                listMonths = inMonth
                returnedDictVals = inPrismOBJ.calcStat(listStats,listMonths,self)

    def cellCountAreas(self,inputDictCellCounts):
        '''   input is dictCellCounts -
                  Check that the values are there, 
                  if they are, they are the same, right?
        '''
        if len(self.dictCellCounts) < 1:
            self.dictCellCounts = inputDictCellCounts
        else:
            for fids in inputDictCellCounts:
                if inputDictCellCounts[fids] == self.dictCellCounts[fids]:
                    pass
                else:
                    print "\n \n Bad Areas \n \n  "
                    self.dictCellCounts = inputDictCellCounts


    def writeOutTable(self,inputListOfListRows, outputPathAndName = r"B:\\Test.csv"):
        '''   Write out a CSV of the prepared list.
        '''
        import csv
        listRows = inputListOfListRows
        with open(outputPathAndName, 'w') as f:
            for rows in listRows:
                f.write(rows + "\n")
        f.close()

    def writeOutTimeSeries(self,inputFID , outputPathAndName , parameter = 'ppt' ):
        '''  Write out Time Series

        '''
        listRow = []
        listOfRows = []
        yearlydict = {}
        monthlydict = {}
        dailydict = {}
        fiddict = {}
        paramdict = {}

        csep = ","
        datesep = "-"

        #yearlydict = self.dictYearlyAll[parameter] 
        yearlydict = self.dictYearlyAll

        for years in yearlydict:       # for each year
            monthlydict = yearlydict[years]   # pull out the dict of Months
            for months in monthlydict:    #  for each month
                dailydict = monthlydict[months]
                for days in dailydict:
                    fiddict = dailydict[days]
                    for fids in fiddict:
                        paramdict = fiddict[fids]
                        for params in paramdict:
                            for keys in paramdict:
                                if parameter in keys:  
                                    thisVal = paramdict[keys]
                                    strRow = str(years)+datesep+str(months)+datesep+str(days)+csep+str(fids)+csep+str(thisVal)
                                    #listStrRow = [strRow]
                                    listRow.append(strRow)
        self.writeOutTable(listRow)

