import gdal, ogr, osr, numpy,inspect
from gdalconst import *

""" unzip.py
    Version: 1.1

    Extract a zipfile to the directory provided
    It first creates the directory structure to house the files
    then it extracts the files to it.

    Sample usage:
    command line
    unzip.py -p 10 -z c:\testfile.zip -o c:\testoutput

    python class
    import unzip
    un = unzip.unzip()
    un.extract(r'c:\testfile.zip', 'c:\testoutput')


    By Doug Tolton
"""

import sys
import zipfile
import os
import os.path
import getopt

class unzip:
    def __init__(self, verbose = False, percent = 10):
        self.verbose = verbose
        self.percent = percent

    def extract(self, file, dir):
        if not dir.endswith(':') and not os.path.exists(dir):
            os.mkdir(dir)

        zf = zipfile.ZipFile(file)

        # create directory structure to house files
        self._createstructure(file, dir)

        num_files = len(zf.namelist())
        percent = self.percent
        divisions = 100 / percent
        perc = int(num_files / divisions)

        # extract files to directory structure
        for i, name in enumerate(zf.namelist()):

            if self.verbose == True:
                print "Extracting %s" % name
            elif perc > 0 and (i % perc) == 0 and i > 0:
                complete = int (i / perc) * percent
                print "%s%% complete" % complete

            if not name.endswith('/'):
                outfile = open(os.path.join(dir, name), 'wb')
                outfile.write(zf.read(name))
                outfile.flush()
                outfile.close()


    def _createstructure(self, file, dir):
        self._makedirs(self._listdirs(file), dir)


    def _makedirs(self, directories, basedir):
        """ Create any directories that don't currently exist """
        for dir in directories:
            curdir = os.path.join(basedir, dir)
            if not os.path.exists(curdir):
                os.mkdir(curdir)

    def _listdirs(self, file):
        """ Grabs all the directories in the zip structure
        This is necessary to create the structure before trying
        to extract the file to it. """
        zf = zipfile.ZipFile(file)

        dirs = []

        for name in zf.namelist():
            if name.endswith('/'):
                dirs.append(name)

        dirs.sort()
        return dirs

def usage():
    print """usage: unzip.py -z <zipfile> -o <targetdir>
    <zipfile> is the source zipfile to extract
    <targetdir> is the target destination

    -z zipfile to extract
    -o target location
    -p sets the percentage notification
    -v sets the extraction to verbose (overrides -p)

    long options also work:
    --verbose
    --percent=10
    --zipfile=<zipfile>
    --outdir=<targetdir>"""


def main():
    shortargs = 'vhp:z:o:'
    longargs = ['verbose', 'help', 'percent=', 'zipfile=', 'outdir=']

    unzipper = unzip()

    try:
        opts, args = getopt.getopt(sys.argv[1:], shortargs, longargs)
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    zipsource = ""
    zipdest = ""

    for o, a in opts:
        if o in ("-v", "--verbose"):
            unzipper.verbose = True
        if o in ("-p", "--percent"):
            if not unzipper.verbose == True:
                unzipper.percent = int(a)
        if o in ("-z", "--zipfile"):
            zipsource = a
        if o in ("-o", "--outdir"):
            zipdest = a
        if o in ("-h", "--help"):
            usage()
            sys.exit()

    if zipsource == "" or zipdest == "":
        usage()
        sys.exit()

    unzipper.extract(zipsource, zipdest)

if __name__ == '__main__': main()

class Constants():  
    def __init__(self):
        self.M2InAcre = 4046.86
        self.AcresInM2 = 0.000247105
        self.M2InCell = 159882.893167291
        dictFID_PercErrorAreas = {'77':0.00749901098320551, '37':-0.00269958659357035, '59':0.00194949790999129, 
                                  '75':0.0138222691782118, '33':-0.0013983823407459, '45':0.00343328655110873, 
                                  '57':0.00433360261779069, '38':-0.00275443057429014, '2':-0.0135109785532004, 
                                  '8':-0.0102922130748825, '6':-0.0112334051817948, '56':0.000309424807316793, 
                                  '65':0.00791314538790073, '40':-0.00130483318311444, '69':0.00987502549650723, 
                                  '61':0.0053618608440597, '41':-0.000650829560863626, '58':0.0014463251775104, 
                                  '82':0.0281121807144725, '49':0.0101077704445578, '14':-0.0121544898561589,
                                  '72':0.0101468966070456, '70':0.0088102200477106, '53':0.00636056763503004,
                                  '27':-0.00310505163045037, '52':0.00521718218820521, '51':0.00308144408796752,
                                  '48':0.000411720283923223, '63':0.00879996229744317, '44':0.0103856396507562,
                                  '46':0.0029363440918779, '43':0.00198443789326981, '23':-0.00848060440767853,
                                  '28':-0.00315981500159674, '55':0.000404614198646176, '35':-0.0033909558823831,
                                  '60':0.00155718031049419, '73':0.0153718248548305, '17':0.0044997684253529,
                                  '19':-0.00286441667386301, '68':0.00521697203704951, '78':0.0143918429377471,
                                  '54':0.00218488750176559, '21':-0.00179642732918872, '42':-0.000807522567676187, 
                                  '34':0.000335102825334579, '71':0.00991473351218472, '31':0.0048776710250254,
                                  '4':-0.0157279410664557, '83':0.0204000454397619, '39':0.00175854448789423, 
                                  '50':0.00936651020181367, '25':-0.00122503948181629, '13':-0.0133489267021653,
                                  '74':0.015899852371635, '9':-0.00628744077874436, '30':0.0031328490982053,
                                  '86':0.0177320437204622, '67':0.00892519867521738, '10':-0.00817249858860592, 
                                  '36':-0.00150242158687318, '76':0.0181333224718068, '84':0.0176516525398981,
                                  '18':0.00205155760347567, '5':-0.0108932800490226, '7':-0.0167842122846489, 
                                  '22':-0.0057089561251082, '85':0.0215921987145269, '11':-0.0124906276311875, 
                                  '79':0.0128364452637759, '32':-0.000489528170793775, '64':0.0113615564652624,
                                  '24':-0.00270328716356547, '0':-0.0137332993637779, '80':0.0165405425764739,
                                  '62':0.0110832864681149, '20':-0.00468849502517225, '66':0.0109639199771549,
                                  '81':0.0133949864091464, '29':-0.00187048893231144, '1':-0.0200721919712223,
                                  '47':0.00623856576105997, '16':0.00135189129380769, '3':-0.0185386150990908, 
                                  '26':0.00241731064875858, '15':-0.00717276498561102, '12':-0.0091629162635420}

def array_to_raster(array, TemplateRaster,dst_filename = r'B://testing.tif', randomizeName = True):
    """Array > Raster
    Save a raster from a C order array.

    :param array: ndarray
    """
    #dst_filename = r'B://testing.tif'

    tdataset = gdal.Open( TemplateRaster, GA_ReadOnly )
    geotransform = tdataset.GetGeoTransform()
    print geotransform



    x_pixels,y_pixels = array.shape

    # You need to get those values like you did.
    x_pixels = 16  # number of pixels in x
    y_pixels = 16  # number of pixels in y
    PIXEL_SIZE = geotransform[1]
    x_min = geotransform[0]  
    y_max = geotransform[3]  # x_min & y_max are like the "top left" corner.
    wkt_projection = tdataset.GetProjection()

    driver = gdal.GetDriverByName('GTiff')

    dataset = driver.Create(
        dst_filename,
        x_pixels,
        y_pixels,
        1,
        gdal.GDT_Float32, )

    #dataset.SetGeoTransform((
    #    x_min,    # 0
    #    PIXEL_SIZE,  # 1
    #    0,                      # 2
    #    y_max,    # 3
    #    0,                      # 4
    #    -PIXEL_SIZE))  

    dataset.SetGeoTransform( geotransform )

    dataset.SetProjection(wkt_projection)
    dataset.GetRasterBand(1).WriteArray(array)
    dataset.FlushCache()  # Write to disk.
    return dataset, dataset.GetRasterBand(1)  #If you need to return, remenber to return  also the dataset because the band don`t live without dataset.

def zonal_export(feat, input_zone_polygon, input_value_raster):
    '''   Zonal Stats for a FID:  zonal_stats(31,inputZonePolyPath,inputValueRaster, inputListStat)
                 inputListStat { 'min', 'max', 'sum', 'mean', 'median', 'stddev'  }
    '''

    # Open data
    lyr = Lyr_or_SHP(input_zone_polygon)

    raster = gdal.Open(input_value_raster)

    # Get raster georeference info
    transform = raster.GetGeoTransform()
    xOrigin = transform[0]
    yOrigin = transform[3]
    pixelWidth = transform[1]
    pixelHeight = transform[5]

    # Get extent of feat
    geom = feat.GetGeometryRef()
    if (geom.GetGeometryName() == 'MULTIPOLYGON'):
        count = 0
        pointsX = []; pointsY = []
        for polygon in geom:
            geomInner = geom.GetGeometryRef(count)    
            ring = geomInner.GetGeometryRef(0)
            numpoints = ring.GetPointCount()
            for p in range(numpoints):
                lon, lat, z = ring.GetPoint(p)
                pointsX.append(lon)
                pointsY.append(lat)    
            count += 1
    elif (geom.GetGeometryName() == 'POLYGON'):
        ring = geom.GetGeometryRef(0)
        numpoints = ring.GetPointCount()
        pointsX = []; pointsY = []
        for p in range(numpoints):
            lon, lat, z = ring.GetPoint(p)
            pointsX.append(lon)
            pointsY.append(lat)

    else:
        sys.exit()

    xmin = min(pointsX)
    xmax = max(pointsX)
    ymin = min(pointsY)
    ymax = max(pointsY)

    # Specify offset and rows and columns to read
    xoff = int((xmin - xOrigin)/pixelWidth)
    yoff = int((yOrigin - ymax)/pixelWidth)
    xcount = int((xmax - xmin)/pixelWidth)+1
    ycount = int((ymax - ymin)/pixelWidth)+1

    # Create memory target raster
    target_ds = gdal.GetDriverByName('MEM').Create('', xcount, ycount, gdal.GDT_Byte)
    target_ds.SetGeoTransform((
        xmin, pixelWidth, 0,
        ymax, 0, pixelHeight,
    ))

    # Create for target raster the same projection as for the value raster
    raster_srs = osr.SpatialReference()
    raster_srs.ImportFromWkt(raster.GetProjectionRef())
    target_ds.SetProjection(raster_srs.ExportToWkt())

    # Rasterize zone polygon to raster
    gdal.RasterizeLayer(target_ds, [1], lyr, burn_values=[1])

    # Read raster as arrays
    banddataraster = raster.GetRasterBand(1)
    dataraster = banddataraster.ReadAsArray(xoff, yoff, xcount, ycount).astype(numpy.float)

    bandmask = target_ds.GetRasterBand(1)
    datamask = bandmask.ReadAsArray(0, 0, xcount, ycount).astype(numpy.float)

    # Mask zone of raster
    zoneraster = numpy.ma.masked_array(dataraster,  numpy.logical_not(datamask))

    # Calculate statistics of zonal raster
    #inputListStat { 'min', 'max', 'sum', 'mean', 'median', 'stddev'  }
    #                  0       1     2      3       4           5
    listMatchStat = ['min', 'max', 'sum', 'mean', 'median', 'stddev']
    for items in listStat:
        listIncludeStat = []
        if items in listMatchStat:
            listIncludeStat.append(items)
        else:
            pass
    if len(listIncludeStat) == 0:
        return 1

    dictReturn = {}
    dictNaming = {}
    dictParamVals = {}

    if "max" in listIncludeStat:
        val_max = numpy.max(zoneraster)
        dictParamVals["max"] = val_max

    if "min" in listIncludeStat:
        val_min = numpy.min(zoneraster)
        dictParamVals["min"] = val_min

    if "mean" in listIncludeStat:
        val_mean = numpy.mean(zoneraster)
        dictParamVals["mean"] = val_mean

    if "median" in listIncludeStat:
        val_med  = numpy.median(zoneraster)
        dictParamVals["med"] = val_med

    if "stddev" in listIncludeStat:
        val_stddev = numpy.std(zoneraster)
        dictParamVals["stddev"] = val_stddev

    if "sum" in listIncludeStat:
        zone = numpy.array(zoneraster)
        val_sum = zone.sum()
        dictParamVals["sum"] = val_sum

    returnString = ""

    #print value  

    return dictParamVals

def Lyr_or_SHP(input_zone_polygon):
    try:
        shp = ogr.Open(input_zone_polygon)
        lyr = shp.GetLayer()        
    except:
        lyr = input_zone_polygon   
    return lyr



def AreaOfPoly(input_zone_polygon):
    constants = Constants()
    '''Returns a dictionary of areas from a polygon
             dictArea[fid] = ( m2, geom.GetArea <GCS>, field Acres  )
    '''
    lyr = Lyr_or_SHP(input_zone_polygon)

    featList = range(lyr.GetFeatureCount())
    dictArea = {}

    for FID in featList:
        feat = lyr.GetFeature(FID)    
        geom = feat.GetGeometryRef()
        acres = feat.GetField("acres")
        m2 = constants.M2InAcre * acres
        dictArea[FID]=  (m2,acres, geom.GetArea())
    return dictArea

def zonal_count(feat, input_zone_polygon, input_value_raster):
    '''   Zonal Stats for a FID:  zonal_stats(31,inputZonePolyPath,inputValueRaster, inputListStat)

    '''
    # Open data
    lyr = Lyr_or_SHP(input_zone_polygon)

    raster = gdal.Open(input_value_raster)

    # Get raster georeference info
    transform = raster.GetGeoTransform()
    xOrigin = transform[0]
    yOrigin = transform[3]
    pixelWidth = transform[1]
    pixelHeight = transform[5]

    # Get extent of feat
    geom = feat.GetGeometryRef()
    if (geom.GetGeometryName() == 'MULTIPOLYGON'):
        count = 0
        pointsX = []; pointsY = []
        for polygon in geom:
            geomInner = geom.GetGeometryRef(count)    
            ring = geomInner.GetGeometryRef(0)
            numpoints = ring.GetPointCount()
            for p in range(numpoints):
                lon, lat, z = ring.GetPoint(p)
                pointsX.append(lon)
                pointsY.append(lat)    
            count += 1
    elif (geom.GetGeometryName() == 'POLYGON'):
        ring = geom.GetGeometryRef(0)
        numpoints = ring.GetPointCount()
        pointsX = []; pointsY = []
        for p in range(numpoints):
            lon, lat, z = ring.GetPoint(p)
            pointsX.append(lon)
            pointsY.append(lat)

    else:
        sys.exit()

    xmin = min(pointsX)
    xmax = max(pointsX)
    ymin = min(pointsY)
    ymax = max(pointsY)

    # Specify offset and rows and columns to read
    xoff = int((xmin - xOrigin)/pixelWidth)
    yoff = int((yOrigin - ymax)/pixelWidth)
    xcount = int((xmax - xmin)/pixelWidth)+1
    ycount = int((ymax - ymin)/pixelWidth)+1

    # Create memory target raster
    target_ds = gdal.GetDriverByName('MEM').Create('', xcount, ycount, gdal.GDT_Byte)
    target_ds.SetGeoTransform((
        xmin, pixelWidth, 0,
        ymax, 0, pixelHeight,
    ))

    # Create for target raster the same projection as for the value raster
    raster_srs = osr.SpatialReference()
    raster_srs.ImportFromWkt(raster.GetProjectionRef())
    target_ds.SetProjection(raster_srs.ExportToWkt())

    # Rasterize zone polygon to raster
    gdal.RasterizeLayer(target_ds, [1], lyr, burn_values=[1])
    # Read raster as arrays
    banddataraster = raster.GetRasterBand(1)
    dataraster = banddataraster.ReadAsArray(xoff, yoff, xcount, ycount).astype(numpy.float)

    bandmask = target_ds.GetRasterBand(1)
    datamask = bandmask.ReadAsArray(0, 0, xcount, ycount).astype(numpy.float)

    # Mask zone of raster
    zoneraster = numpy.ma.masked_array(dataraster,  numpy.logical_not(datamask))

    return zoneraster.count()


def loop_count_stats(input_zone_polygon, input_value_raster):
    '''     Pass a input_zone_polygon Path-To-SHP
                   or
            an OGR layer object ( shp = ogr.Open(path); lyr = shp.GetLayer() )
    '''
    lyr = Lyr_or_SHP(input_zone_polygon)    

    featList = range(lyr.GetFeatureCount())
    statDict = {}

    for FID in featList:
        feat = lyr.GetFeature(FID)
        value = zonal_count(feat, input_zone_polygon, input_value_raster)
        statDict[FID] = value
    return statDict   # return { 'FID' :  {stat:val, stat2:val2.... }   }

def zonal_stats_exp_v0(FID, input_zone_polygon, input_value_raster,listStat = ['sum'],zoneXYScaling = 10,OutDS = True):
    '''   Zonal Stats for a FID:  zonal_stats(31,inputZonePolyPath,inputValueRaster, inputListStat,ZoneXYScaling = 1.0)
                 inputListStat { 'min', 'max', 'sum', 'mean', 'median', 'stddev'  }
    '''
    from modOGR import writeSHP
    # Open data
    lyr = Lyr_or_SHP(input_zone_polygon)
    feat = lyr.GetFeature(FID)
    strFilter = "FID ='"+str(FID)+"'"
    lyr.SetAttributeFilter(strFilter)

    raster = gdal.Open(input_value_raster)

    # Get raster georeference info
    transform = raster.GetGeoTransform()
    xOrigin = transform[0]
    yOrigin = transform[3]
    pixelWidth = transform[1]
    pixelHeight = transform[5]

    # Get extent of feat
    geom = feat.GetGeometryRef()
    if (geom.GetGeometryName() == 'MULTIPOLYGON'):
        count = 0
        pointsX = []; pointsY = []
        for polygon in geom:
            geomInner = geom.GetGeometryRef(count)    
            ring = geomInner.GetGeometryRef(0)
            numpoints = ring.GetPointCount()
            for p in range(numpoints):
                lon, lat, z = ring.GetPoint(p)
                pointsX.append(lon)
                pointsY.append(lat)    
            count += 1
    elif (geom.GetGeometryName() == 'POLYGON'):
        ring = geom.GetGeometryRef(0)
        numpoints = ring.GetPointCount()
        pointsX = []; pointsY = []
        for p in range(numpoints):
            lon, lat, z = ring.GetPoint(p)
            pointsX.append(lon)
            pointsY.append(lat)

    else:
        sys.exit()

    xmin = min(pointsX)
    xmax = max(pointsX)
    ymin = min(pointsY)
    ymax = max(pointsY)

    # Specify offset and rows and columns to read
    xoff = int((xmin - xOrigin)/pixelWidth)
    yoff = int((yOrigin - ymax)/pixelWidth)
    xcount = int((xmax - xmin)/pixelWidth) +1
    ycount = int((ymax - ymin)/pixelWidth) +1

    xCountScaled = ( (int((xmax - xmin)/pixelWidth) + 1) * zoneXYScaling )  
    yCountScaled = ( (int((ymax - ymin)/pixelWidth) + 1) * zoneXYScaling ) 

    # Create memory target raster
    #target_ds = gdal.GetDriverByName('MEM').Create('', xcount, ycount, gdal.GDT_Byte)
    #target_ds.SetGeoTransform((
    #    xmin, pixelWidth, 0,
    #    ymax, 0, pixelHeight,
    #))
        #Create memory target zone raster
    target_ds = gdal.GetDriverByName('MEM').Create('', xCountScaled, yCountScaled,1, gdal.GDT_Byte)
    target_ds.SetGeoTransform((
        xmin, pixelWidth/zoneXYScaling, 0,
        ymax, 0, pixelHeight/zoneXYScaling,
    ))    

        #Create memory target resampled value raster
    target_val_ds = gdal.GetDriverByName('MEM').Create('', xCountScaled, yCountScaled,1, gdal.GDT_Float32)
    target_val_ds.SetGeoTransform((
        xmin, pixelWidth/zoneXYScaling, 0,
        ymax, 0, pixelHeight/zoneXYScaling,
    ))  

        # memory target raster to write
    zoneraster = gdal.GetDriverByName('MEM').Create('', xCountScaled, yCountScaled,1, gdal.GDT_Float32)     
    zoneraster.SetGeoTransform((
        xmin, pixelWidth/zoneXYScaling, 0,
        ymax, 0, pixelHeight/zoneXYScaling,
    ))

        # Create for target raster the same projection as for the value raster
    raster_srs = osr.SpatialReference()
    raster_srs.ImportFromWkt( raster.GetProjectionRef() )

        #set all SRS on targets
    target_ds.SetProjection( raster_srs.ExportToWkt() )
    target_val_ds.SetProjection( raster_srs.ExportToWkt() )
    zoneraster.SetProjection( raster_srs.ExportToWkt() )

    out_ZR_band = zoneraster.GetRasterBand(1)

        # Rasterize zone polygon to raster
    gdal.RasterizeLayer(target_ds, [1], lyr, burn_values=[1])

        # Read raster as arrays
    banddataraster = raster.GetRasterBand(1)
    dataraster = banddataraster.ReadAsArray(xoff, yoff, xcount, ycount).astype(numpy.float)

    bandmask = target_ds.GetRasterBand(1)
    datamask = bandmask.ReadAsArray(0, 0, xcount, ycount).astype(numpy.float)

        #Polygonify    
    dst_layername = "POLYGONIZED_STUFF"
    drv = ogr.GetDriverByName( "Memory" )
    dst_ds = drv.CreateDataSource( 'out' ) 
    #make layer    
    dst_layer = dst_ds.CreateLayer(dst_layername, srs = None )
    #new field defn
    newfield = ogr.FieldDefn("value", ogr.OFTReal)   
    newfield.SetPrecision(10)

    dst_layer.CreateField(newfield)   

    #and the raster polys in dst_layer
    gdal.Polygonize( banddataraster, None, dst_layer, 0, [], callback=None )
    #gdal.Polygonize( banddataraster, None, dst_layer, 0, [], callback=None )
        #now back in to the target_val_ds
    writeSHP(dst_layer)
    gdal.RasterizeLayer(target_val_ds, [1], dst_layer,options = ["ATTRIBUTE=value"])


    #zoneraster = driver.Create()
    # Mask zone of raster
    #zoneraster = numpy.ma.masked_array(dataraster,  numpy.logical_not(datamask))
    #zoneraster = target_ds.ReadAsArray()*dataraster
    #outZRband.WriteArray(target_ds.ReadAsArray()*target_val_ds.ReadAsArray())
    out_ZR_band.WriteArray(target_val_ds.ReadAsArray().astype(numpy.float))#*target_val_ds.ReadAsArray())
    zoneraster.FlushCache()

    if OutDS:
        ds_format = "GTiff"
        driver = gdal.GetDriverByName( ds_format )        
        out_ds = driver.Create( r"B:\\testOut"+str(feat.GetFID())+".tif",xCountScaled,yCountScaled,1,gdal.GDT_Float32)
        out_ds.SetGeoTransform( target_ds.GetGeoTransform() )        
        out_ds.SetProjection(raster_srs.ExportToWkt())
        #out_ras = BUP
        out_ds.GetRasterBand(1).WriteArray( zoneraster.ReadAsArray().astype(numpy.float) )
        out_ds = None

    # Calculate statistics of zonal raster
    #inputListStat { 'min', 'max', 'sum', 'mean', 'median', 'stddev'  }
    #                  0       1     2      3       4           5
    listMatchStat = ['min', 'max', 'sum', 'mean', 'median', 'stddev']
    for items in listStat:
        listIncludeStat = []
        if items in listMatchStat:
            listIncludeStat.append(items)
        else:
            pass
    if len(listIncludeStat) == 0:
        return 1

    dictReturn = {}
    dictNaming = {}
    dictParamVals = {}

    zone = zoneraster.ReadAsArray()    

    if "max" in listIncludeStat:
        val_max = zone.max()
        dictParamVals["max"] = val_max

    if "min" in listIncludeStat:
        val_min = zone.min()
        dictParamVals["min"] = val_min

    if "mean" in listIncludeStat:
        val_mean = zone.mean()
        dictParamVals["mean"] = val_mean

    if "median" in listIncludeStat:
        val_med  = numpy.median(zone)
        dictParamVals["med"] = val_med

    if "stddev" in listIncludeStat:
        val_stddev = numpy.std(zone)
        dictParamVals["stddev"] = val_stddev

    if "sum" in listIncludeStat:
        val_sum = zone.sum()
        dictParamVals["sum"] = val_sum

    returnString = ""
    if val_sum > 0.0:
        print "squawk!"
    #print value  

    return dictParamVals

def zonal_stats(feat, input_zone_polygon, input_value_raster,listStat = ['sum'],zoneXYScaling = 10):
    '''   Zonal Stats for a FID:  zonal_stats(31,inputZonePolyPath,inputValueRaster, inputListStat,ZoneXYScaling = 1.0)
                 inputListStat { 'min', 'max', 'sum', 'mean', 'median', 'stddev'  }
    '''

    # Open data
    lyr = Lyr_or_SHP(input_zone_polygon)

    raster = gdal.Open(input_value_raster)

    # Get raster georeference info
    transform = raster.GetGeoTransform()
    xOrigin = transform[0]
    yOrigin = transform[3]
    pixelWidth = transform[1]
    pixelHeight = transform[5]

    # Get extent of feat
    geom = feat.GetGeometryRef()
    if (geom.GetGeometryName() == 'MULTIPOLYGON'):
        count = 0
        pointsX = []; pointsY = []
        for polygon in geom:
            geomInner = geom.GetGeometryRef(count)    
            ring = geomInner.GetGeometryRef(0)
            numpoints = ring.GetPointCount()
            for p in range(numpoints):
                lon, lat, z = ring.GetPoint(p)
                pointsX.append(lon)
                pointsY.append(lat)    
            count += 1
    elif (geom.GetGeometryName() == 'POLYGON'):
        ring = geom.GetGeometryRef(0)
        numpoints = ring.GetPointCount()
        pointsX = []; pointsY = []
        for p in range(numpoints):
            lon, lat, z = ring.GetPoint(p)
            pointsX.append(lon)
            pointsY.append(lat)

    else:
        sys.exit()

    xmin = min(pointsX)
    xmax = max(pointsX)
    ymin = min(pointsY)
    ymax = max(pointsY)

    # Specify offset and rows and columns to read
    xoff = int((xmin - xOrigin)/pixelWidth)
    yoff = int((yOrigin - ymax)/pixelWidth)
    xcount = int((xmax - xmin)/pixelWidth)+1
    ycount = int((ymax - ymin)/pixelWidth)+1

    xCountScaled = ( int((xmax - xmin)/pixelWidth) * zoneXYScaling ) + 1 
    yCountScaled = ( int((ymax - ymin)/pixelWidth) * zoneXYScaling ) + 1

    # Create memory target raster
    #target_ds = gdal.GetDriverByName('MEM').Create('', xcount, ycount, gdal.GDT_Byte)
    #target_ds.SetGeoTransform((
    #    xmin, pixelWidth, 0,
    #    ymax, 0, pixelHeight,
    #))
    # Create memory target raster
    target_ds = gdal.GetDriverByName('MEM').Create('', xCountScaled, yCountScaled, gdal.GDT_Byte)
    target_ds.SetGeoTransform((
        xmin, pixelWidth/zoneXYScaling, 0,
        ymax, 0, pixelHeight/zoneXYScaling,
    ))    

    # Create for target raster the same projection as for the value raster
    raster_srs = osr.SpatialReference()
    raster_srs.ImportFromWkt(raster.GetProjectionRef())
    target_ds.SetProjection(raster_srs.ExportToWkt())

    # Rasterize zone polygon to raster
    gdal.RasterizeLayer(target_ds, [1], lyr, burn_values=[1])

    # Read raster as arrays
    banddataraster = raster.GetRasterBand(1)
    dataraster = banddataraster.ReadAsArray(xoff, yoff, xcount, ycount).astype(numpy.float)

    bandmask = target_ds.GetRasterBand(1)
    datamask = bandmask.ReadAsArray(0, 0, xcount, ycount).astype(numpy.float)

    # Mask zone of raster
    zoneraster = numpy.ma.masked_array(dataraster,  numpy.logical_not(datamask))

    # Calculate statistics of zonal raster
    #inputListStat { 'min', 'max', 'sum', 'mean', 'median', 'stddev'  }
    #                  0       1     2      3       4           5
    listMatchStat = ['min', 'max', 'sum', 'mean', 'median', 'stddev']
    for items in listStat:
        listIncludeStat = []
        if items in listMatchStat:
            listIncludeStat.append(items)
        else:
            pass
    if len(listIncludeStat) == 0:
        return 1

    dictReturn = {}
    dictNaming = {}
    dictParamVals = {}

    if "max" in listIncludeStat:
        val_max = numpy.max(zoneraster)
        dictParamVals["max"] = val_max

    if "min" in listIncludeStat:
        val_min = numpy.min(zoneraster)
        dictParamVals["min"] = val_min

    if "mean" in listIncludeStat:
        val_mean = numpy.mean(zoneraster)
        dictParamVals["mean"] = val_mean

    if "median" in listIncludeStat:
        val_med  = numpy.median(zoneraster)
        dictParamVals["med"] = val_med

    if "stddev" in listIncludeStat:
        val_stddev = numpy.std(zoneraster)
        dictParamVals["stddev"] = val_stddev

    if "sum" in listIncludeStat:
        zone = numpy.array(zoneraster)
        val_sum = zone.sum()
        dictParamVals["sum"] = val_sum

    returnString = ""

    #print value  

    return dictParamVals


def loop_zonal_stats(input_zone_polygon, input_value_raster,inListStats):
    '''     Pass a input_zone_polygon Path-To-SHP
                   or
            an OGR layer object ( shp = ogr.Open(path); lyr = shp.GetLayer() )
    '''
    lyr = Lyr_or_SHP(input_zone_polygon)    

    featList = range(lyr.GetFeatureCount())
    statDict = {}
    dictFIDAreaCount = {}

    for FID in featList:
        #feat = lyr.GetFeature(FID)
        #meanValue = zonal_stats(feat, input_zone_polygon, input_value_raster, inListStats)   ORI
        meanValue = zonal_stats_exp(FID, lyr, input_value_raster, inListStats)

        statDict[FID]         = meanValue[0]
        dictFIDAreaCount[FID] = meanValue[1]

    return (statDict, dictFIDAreaCount)   # return { 'FID' :  {stat:val, stat2:val2.... }   }


#if __name__ == '__main__':
    ## Raster dataset
    #input_value_raster = 'popc_0ADProj.tif'
    ## Vector dataset(zones)
    #input_zone_polygon = 'borders_tribes.shp'

    #print loop_zonal_stats(input_zone_polygon, input_value_raster)

def zonal_stats_exp(FID, input_zone_polygon, input_value_raster,listStat = ['sum'],zoneXYScaling = 10,OutDS = False):
    '''   Zonal Stats for a FID:  zonal_stats(31,inputZonePolyPath,inputValueRaster,
                              inputListStat,
                 inputListStat { 'min', 'max', 'sum', 'mean', 'median', 'stddev'  }
                             ZoneXYScaling = 1.0,  OutDS = False <export clipped raster> )
    '''
    from modOGR import writeSHP
    # Open data
    lyr = Lyr_or_SHP(input_zone_polygon)
    feat = lyr.GetFeature(FID)
    strFilter = "FID ='"+str(FID)+"'"
    lyr.SetAttributeFilter(strFilter)

    raster = gdal.Open(input_value_raster)

    # Get raster georeference info
    transform = raster.GetGeoTransform()
    xOrigin = transform[0]
    yOrigin = transform[3]
    pixelWidth = transform[1]
    pixelHeight = transform[5]

    # Get extent of feat
    geom = feat.GetGeometryRef()
    if (geom.GetGeometryName() == 'MULTIPOLYGON'):
        count = 0
        pointsX = []; pointsY = []
        for polygon in geom:
            geomInner = geom.GetGeometryRef(count)    
            ring = geomInner.GetGeometryRef(0)
            numpoints = ring.GetPointCount()
            for p in range(numpoints):
                lon, lat, z = ring.GetPoint(p)
                pointsX.append(lon)
                pointsY.append(lat)    
            count += 1
    elif (geom.GetGeometryName() == 'POLYGON'):
        ring = geom.GetGeometryRef(0)
        numpoints = ring.GetPointCount()
        pointsX = []; pointsY = []
        for p in range(numpoints):
            lon, lat, z = ring.GetPoint(p)
            pointsX.append(lon)
            pointsY.append(lat)

    else:
        sys.exit()

    xmin = min(pointsX)
    xmax = max(pointsX)
    ymin = min(pointsY)
    ymax = max(pointsY)

    # Specify offset and rows and columns to read
    xoff = int((xmin - xOrigin)/pixelWidth)
    yoff = int((yOrigin - ymax)/pixelWidth)
    xcount = int((xmax - xmin)/pixelWidth) +1
    ycount = int((ymax - ymin)/pixelWidth) +1

    xCountScaled = ( (int((xmax - xmin)/pixelWidth) + 1) * zoneXYScaling )  
    yCountScaled = ( (int((ymax - ymin)/pixelWidth) + 1) * zoneXYScaling ) 


        #Create memory target zone raster
    target_ds = gdal.GetDriverByName('MEM').Create('', xCountScaled, yCountScaled,1, gdal.GDT_Byte)
    target_ds.SetGeoTransform((
        xmin, pixelWidth/zoneXYScaling, 0,
        ymax, 0, pixelHeight/zoneXYScaling,
    ))    

        #Create memory target resampled value raster
    target_val_ds = gdal.GetDriverByName('MEM').Create('', xCountScaled, yCountScaled,1, gdal.GDT_Float32)
    target_val_ds.SetGeoTransform((
        xmin, pixelWidth/zoneXYScaling, 0,
        ymax, 0, pixelHeight/zoneXYScaling,
    ))  

        # memory target raster to write
    zoneraster = gdal.GetDriverByName('MEM').Create('', xCountScaled, yCountScaled,1, gdal.GDT_Float32)     
    zoneraster.SetGeoTransform((
        xmin, pixelWidth/zoneXYScaling, 0,
        ymax, 0, pixelHeight/zoneXYScaling,
    ))

        # Create for target raster the same projection as for the value raster
    raster_srs = osr.SpatialReference()
    raster_srs.ImportFromWkt( raster.GetProjectionRef() )

        #set all SRS on targets
    target_ds.SetProjection( raster_srs.ExportToWkt() )
    target_val_ds.SetProjection( raster_srs.ExportToWkt() )
    zoneraster.SetProjection( raster_srs.ExportToWkt() )

    out_ZR_band = zoneraster.GetRasterBand(1)

        # Rasterize zone polygon to raster
    gdal.RasterizeLayer(target_ds, [1], lyr, burn_values=[1])
                #  target_ds <-------  has the 0/1 watershed definition
    #values for the watershed
    countFIDArea = target_ds.ReadAsArray().sum()

        # Read raster as arrays
    banddataraster = raster.GetRasterBand(1)
    dataraster = banddataraster.ReadAsArray(xoff, yoff, xcount, ycount).astype(numpy.float)

    gdal.ReprojectImage(raster,target_val_ds,None,None,gdal.GRA_CubicSpline )    
                #  target_val_ds <-------- has the resampled values

    out_ZR_band.WriteArray(target_ds.ReadAsArray()*target_val_ds.ReadAsArray())
    #out_ZR_band.WriteArray(target_val_ds.ReadAsArray().astype(numpy.float))#*target_val_ds.ReadAsArray())
    zoneraster.FlushCache()


    # Calculate statistics of zonal raster
    #inputListStat { 'min', 'max', 'sum', 'mean', 'median', 'stddev'  }
    #                  0       1     2      3       4           5
    listMatchStat = ['min', 'max', 'sum', 'mean', 'median', 'stddev']
    for items in listStat:
        listIncludeStat = []
        if items in listMatchStat:
            listIncludeStat.append(items)
        else:
            pass
    if len(listIncludeStat) == 0:
        return 1

    dictReturn = {}
    dictNaming = {}
    dictParamVals = {}

    zone = zoneraster.ReadAsArray()    

    if "max" in listIncludeStat:
        val_max = zone.max()
        dictParamVals["max"] = val_max

    if "min" in listIncludeStat:
        val_min = zone.min()
        dictParamVals["min"] = val_min

    if "mean" in listIncludeStat:
        val_mean = zone.mean()
        dictParamVals["mean"] = val_mean

    if "median" in listIncludeStat:
        val_med  = numpy.median(zone)
        dictParamVals["med"] = val_med

    if "stddev" in listIncludeStat:
        val_stddev = numpy.std(zone)
        dictParamVals["stddev"] = val_stddev

    if "sum" in listIncludeStat:
        val_sum = zone.sum()
        dictParamVals["sum"] = val_sum

    returnString = ""
    if val_sum > 0.0:
        #print "squawk!"
        if OutDS:
            ds_format = "GTiff"
            driver = gdal.GetDriverByName( ds_format )        
            out_ds = driver.Create( r"B:\\testOut"+str(feat.GetFID())+".tif",xCountScaled,yCountScaled,1,gdal.GDT_Float32)
            out_ds.SetGeoTransform( target_ds.GetGeoTransform() )        
            out_ds.SetProjection(raster_srs.ExportToWkt())
            out_ds.GetRasterBand(1).WriteArray( zoneraster.ReadAsArray().astype(numpy.float) )
            out_ds = None        
    #print value  

    return (dictParamVals, countFIDArea)