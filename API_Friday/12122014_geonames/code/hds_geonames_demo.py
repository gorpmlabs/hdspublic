# -*- coding: utf-8 -*-
'''
    Code developed as part of HDS article :
        http://hds.gorpmdev.com/site/?p=102
        
    to do quick and fun things with GeoNames API (http://www.geonames.org/export/web-services.html).
    
    @author: rpmlabs / keith maull    
    @license: MIT, no warranty, guarantees 
    @date: circa Dec-6-2014
'''
import operator
import requests
import json
import pprint
import time
import sys
import conf

'''
    Given a bounding box, return the cities in that bounding 
    box using <geonames_api>/citiesJSON.
    
    @author: rpmlabs / keith maull
'''
def geonames_get_ppl_metadata(bbox):
    payload = {'west': bbox['west'], 'north': bbox['north'], \
               'east': bbox['east'], 'south': bbox['south'], \
               'username': conf.username, \
               'maxRows': conf.maxpplrows}
    try: 
        r = requests.get("http://api.geonames.org/citiesJSON", params=payload)
        resp_obj = json.loads(r.text)
        
        if resp_obj.has_key('geonames'):
            ppl_metadata = []
 
            for o in resp_obj['geonames']:
                if o['population'] > conf.population_min :
                    # the elevation data is not part of the payload with this API call, so get it and add to o
                    o['astergdem'] = geonames_get_astergdem(o['lat'],o['lng']) 
                    ppl_metadata.append(o)
            return ppl_metadata
        else:
            return {} # oops
    except: # TODO : handle 503 errors
        print sys.exc_info()
        return {}
    
'''
    Given an arbitrary lat and lon, return the astergdem altitude.
    @author: rpmlabs / keith maull
'''
def geonames_get_astergdem(lat,lng):
    payload = {'lat': lat, 'lng': lng,\
               'username': conf.username }
    try: 
        r = requests.get("http://api.geonames.org/astergdemJSON", params=payload)
        resp_obj = json.loads(r.text)
        return resp_obj['astergdem']
    except: #handle 503 errors
        print sys.exc_info()
        return -19010101 # arbitrary, but we jnow w

'''
    Given a north, south, east, west coord set, create
    partitions with given ns and we step.
    
    Example :
        * create a bounding box from 
            w: -180
            e: -150
            n: 85
            s: 65
            
        * slice the east west with a step of 5 degrees (-180, -175, -170, -165, -160, -155, -150)
        * slice the north west with a step of 10 degrees (65,75,85)
        
        * resulting in 4 x 2 = 8 partitions each
        
            e.g. -180,75,-175, 65 (w,n,e,s)
            
    This method is not only useful for making computation easier, but it can be used to make algorithms
    run better / smarter.
    
    @author: rpmlabs / keith maull
'''
def get_bounding_box_partitions(west, east, we_step, north, south, ns_step):
    partitions = []
    
    # start from left -180 go to right +180 by step
    if we_step > 0 : 
        if west > east :
            we_slices = range(east,west+we_step,we_step)
        else : 
            we_slices = range(west,east+we_step,we_step)
    else : we_slices = [west,east]
    
    if ns_step > 0 : 
        if north > south :
            ns_slices = range(south,north+ns_step,ns_step)
        else :
            ns_slices = range(north,south+ns_step,ns_step)
    else: ns_slices = [north, south]
                    
    for i,n in enumerate(we_slices):
        for j,m in enumerate(ns_slices):
            if j < len(ns_slices)-1 and i < len(we_slices)-1:
                partitions.append({'west': we_slices[i],'north': ns_slices[j], 'east': we_slices[i+1], 'south': ns_slices[j+1]})

    return partitions

'''
'''
def print_city_data_report_simple(title=None, data=None):
    if title and data :
        print title
        for c in data:
            print "%s, %s \n\tAltitude: %d feet\n\tPopulation: %s" % (c['name'],c['countrycode'],int(c['astergdem'])*conf.ft_to_meters,c['population'])
                    
'''
    Basic testing of code.
'''
def main(): 
        
    # original example data
    # X  = get_bounding_box_partitions(-180,-160,0,85,65,0)
    
    # south american andes geek add-on
    X  = get_bounding_box_partitions(-90,-60,0,-30,-10,0)
    
    '''
    if you want to play, uncommment these segments, which should cover the whole earth (or most of it anyway)
    
        A  = get_bounding_box_partitions(-180,180,90,85,65,5)
        A_ = get_bounding_box_partitions(-180,180,90,-85,-65,5)
        B  = get_bounding_box_partitions(-180,180,45,65,45,5)
        B_ = get_bounding_box_partitions(-180,180,45,-65,-45,5)
        C  = get_bounding_box_partitions(-180,180,30,45,0,5)
        C_ = get_bounding_box_partitions(-180,180,30,-45,0,5)

    '''    
    the_world = [ X ] 

    # TODO: consider an  OO approach and make blocks and parts objects for clearner design    
    for parts in the_world :
        # careful, now ... these blocks will take time to crunch, so BE NICE!
        for block in parts:    
            block['geonames'] = geonames_get_ppl_metadata(block)  

            citycount = len(block['geonames'])           # population
            sorted_cities_by_population = sorted(block['geonames'],key=operator.itemgetter('population'),reverse=True)

            print_city_data_report_simple(title='5 most populous cities (of top %s in [%d,%d,%d,%d])' % \
                                          (citycount, block['west'],block['north'],\
                                           block['east'],block['south']),\
                                           data=sorted_cities_by_population[:5])
            print "\n\n"
            print_city_data_report_simple(title='5 least populous cities (of top %s in [%d,%d,%d,%d])' % \
                                          (citycount, block['west'],block['north'],\
                                           block['east'],block['south']),\
                                           data=sorted_cities_by_population[-5:])
            print "\n\n"
            # altitude 
            sorted_cities_by_altitude = sorted(block['geonames'],key=operator.itemgetter('astergdem'),reverse=True)
        
            print_city_data_report_simple(title='5 highest altitude cities (of top %s in [%d,%d,%d,%d])' % \
                                          (citycount, block['west'],block['north'],\
                                           block['east'],block['south']),\
                                           data=sorted_cities_by_altitude[:5])                                       
            print "\n\n"
            print_city_data_report_simple(title='5 lowest altitude cities (of top %s in [%d,%d,%d,%d])' % \
                                          (citycount, block['west'],block['north'],\
                                           block['east'],block['south']),\
                                           data=sorted_cities_by_altitude[-5:])                                       

if __name__ == "__main__": main()
