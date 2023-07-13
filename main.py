from unittest import skip
import numpy as np
import astroquery
from astroquery import simbad
from astroquery.simbad import Simbad
import astropy.units as u
import astropy.coordinates as coord
import numpy.ma as ma
import matplotlib.pyplot as plt

def make_star_box(star_name, radius, depth_start, depth_end):
    
    """Star Mapper in 3D

    Create a 3 dimensional box autopopulated with objects near the object of interest.

    Args:
        star_name (string): Name of object. Queried from Simbad.
        radius (float): Radius in arcseconds. Radius that creates a 2d circle around the object of interest (in the plane of the sky).
        depth_start (float): Distance in parsecs. The distance to the closest object wanted within the sample.
        depth_end (float): Distance in parsecs. The distance to the farthest object wanted within the sample.

    Returns:
        plot: 3 dimensional box filled with objects in the area of interest
    """
    
    Simbad.add_votable_fields('plx', 'distance')
    star_result=Simbad.query_object(star_name)
    star_id=star_result["MAIN_ID"]
    RA=star_result["RA"].value
    DEC=star_result["DEC"].value
    c=coord.SkyCoord(RA, DEC, unit=(u.hourangle, u.deg), frame='icrs')
    RA=c.ra.value
    DEC=c.dec.value

    parallax=star_result["PLX_VALUE"].value
    distance=1/(parallax/1000)*u.pc
    print("The distance to ", star_name, " is ", distance)
    
    #query the region around the object of interest
    region= Simbad.query_region(c, radius=radius*u.deg)
    
    #only keep objects within the specified range of depth
    defined_region=[]
    for test_obj in region:
        
        parallax_test_obj=test_obj["PLX_VALUE"]
        
        if ma.is_masked(parallax_test_obj):
            skip
        else:
            distance_test_obj=1/(parallax_test_obj/1000) #unit pc
            if distance_test_obj>depth_start and distance_test_obj<depth_end:
                defined_region.append(test_obj)

    #begin plotting objects in 3d
    fig = plt.figure(figsize=(12, 12))
    ax = fig.add_subplot(projection='3d')
    
    #plot every object 
    final_RA=[]
    final_DEC=[]
    final_distance=[]

    for final_obj in defined_region:
        RA_obj=final_obj["RA"]
        DEC_obj=final_obj["DEC"]
        c=coord.SkyCoord(RA_obj, DEC_obj, unit=(u.hourangle, u.deg))
        RA_obj=c.ra.value
        DEC_obj=c.dec.value

        parallax_obj=final_obj["PLX_VALUE"]
        distance_obj=1/(parallax_obj/1000) #parsecs
        
        final_RA.append(RA_obj)
        final_DEC.append(DEC_obj)
        final_distance.append(distance_obj)
    
    orig_map=plt.cm.get_cmap('magma')
    reversed_map = orig_map.reversed()

    objects=ax.scatter(final_RA, final_DEC, final_distance, c=final_distance, cmap=reversed_map)
    ax.scatter(RA, DEC, distance, label=star_name, s=200, marker="*", c='gold')
    fig.colorbar(objects, ax=ax, label='Distance from Earth (pc)')

    ax.set_xlabel('Right Ascension (degrees)')
    ax.set_ylabel('Declination (degrees)')
    ax.w_zaxis.line.set_lw(0.)
    ax.set_zticks([])

    plt.legend()
    plt.show()