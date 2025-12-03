from astroquery.sdss import SDSS
from astropy.io import fits

sdss_path = "/mnt/364E6D864E6D3FAB/Files/data/bar_ellipse_tofit/images/sdss/"
def sdss_download(catalog_df):
    # catalog df is the df containing the catalog(fun things are fun and people die when they are killed lol)
    # https://skyserver.sdss.org/dr19/SearchTools/sql
    print("downloading sdss data\n")
    for _, galaxy in catalog_df.iterrows():
        ra = galaxy["ra"]
        dec = galaxy["dec"]
        obj = galaxy["object"]
        
        radius = 0.1
        #ra, dec, radius = 186.860045, 6.262747, 0.083 #deeg, deg, arcmin
        print("\n---------------------\n",obj,"\n")
        query = ("SELECT TOP 1 p.objid, p.obj, p.type, p.run,p.rerun,p.camcol,p.field,p.ra, p.dec "+
                 f"FROM fGetNearbyObjEq({ra},{dec},{radius}) n,   PhotoPrimary p "+
                 "WHERE n.objID=p.objID AND p.type = 3 "
                 )
        res = SDSS.query_sql(query)
        band = ["u","g","r"]
        images = SDSS.get_images(matches = res,
                                 band = band
                                 )
        
        for i,hdulist in enumerate(images):
            hdul = fits.HDUList(hdulist)
            iband = band[i]
            hdul.writeto(sdss_path+obj+f"/{obj}_{iband}_sdss.fits",overwrite=True)
