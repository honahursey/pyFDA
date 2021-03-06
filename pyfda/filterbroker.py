# -*- coding: utf-8 -*-
"""
filterbroker.py

Dynamic parameters and settings are exchanged via the dictionaries in this file.
Importing filterbroker.py runs the module once, defining all module variables.
Module variables are global like class variables. 


Author: Christian Muenker
"""

from __future__ import division, unicode_literals

#==============================================================================
# The entries in this file are only used as initial / default entries and
# demonstrate the structure of the global dicts and lists. 

#The actual entries are created resp. overwritten by
#
# ----- FilterTreeBuilder.__init__() ------
#

# Dictionary with translations between short class names and long names for
# design methods
dm_names = {#IIR
            "butter":"Butterworth", "cheby1":"Chebychev 1",
            "bessel":"Bessel",
            # FIR:
            "equiripple":"Equiripple", "firls":"Least-Square",
            "firwin":"Windowed"}

# Dictionary describing the available combinations of response types (rt),
# filter types (ft), design methods (dm) and filter order (fo).
# This dict is built + overwritten by FilterFileReader.buildFilterTree() !
fil_tree = {
    'HP':
        {'FIR':
            {'equiripple':
                {'man': {"par":['N', 'A_PB', 'F_PB']},
                 'min': {"par":['A_PB', 'A_SB', 'F_PB', 'F_SB']}}},
         'IIR':
             {'cheby1':
                 {'man': {"par":['N', 'A_PB', 'F_PB']},
                  'min': {"par":['A_PB', 'A_SB', 'F_PB', 'F_SB']}},
              'cheby2':
                  {'man': {"par":['N', 'A_SB', 'F_SB']},
                   'min': {"par":['A_PB', 'A_SB', 'F_PB', 'F_SB']}}}},
    'BP':
        {'FIR':
            {'equiripple':
                {'man': {"par":['N', 'F_PB', 'F_PB2', 'F_SB', 'F_SB2', 'W_PB', 'W_SB', 'W_SB2']}}},
         'IIR':
             {'cheby1': {'man': {"par":['N', 'A_PB', 'F_PB', 'F_PB2']},
                         'min': {"par":['A_PB', 'A_SB', 'F_PB', 'F_PB2', 'F_SB', 'F_SB2']}},
              'cheby2': {'man': {"par":['N', 'A_SB', 'F_SB', 'F_SB2']},
                         'min': {"par":['A_PB', 'A_SB', 'F_PB', 'F_PB2', 'F_SB', 'F_SB2']}}}},
    'LP':
        {'FIR':
            {'equiripple':
                {'man': {"par":['N', 'A_PB', 'F_PB']},
                 'min': {"par":['A_PB', 'A_SB', 'F_PB', 'F_SB']}}},
         'IIR':
             {'cheby1':
                 {'man': {"par":['N', 'A_PB', 'F_PB']},
                  'min': {"par":['A_PB', 'A_SB', 'F_PB', 'F_SB']}},
             'cheby2': {'man': {"par":['N', 'A_SB', 'F_SB']},
                        'min': {"par":['A_PB', 'A_SB', 'F_PB', 'F_SB']}}}},
    }

#--------------------------------------
# Handle to current filter object
filObj = ""

# -----------------------------------------------------------------------------
# Dictionary containing current filter type, specifications, design and some
# auxiliary information, it is automatically overwritten by input widgets
# and design routines
#--------------------------------------

fil = [None] * 10 # create empty list with length 10 for multiple filter designs
# This functionality is not implemented yet, currently only fil[0] is used

fil[0] = {'rt':'LP', 'ft':'FIR', 'dm':'equiripple', 'fo':'man',
            'N':10, 'f_S':1,
            'A_PB':0.1, 'A_PB2': 1., 'F_PB':0.1, 'F_PB2':0.4, 'F_C': 0.2, 'F_N': 0.2,
            'A_SB':60., 'A_SB2': 60., 'F_SB':0.2, 'F_SB2':0.3, 'F_C2': 0.4, 'F_N2': 0.4,
            'W_PB':1., 'W_PB2':1., 'W_SB':1., 'W_SB2':1.,
            #
            'ba':([1, 1, 1], [3, 0, 2]), # tuple of bb, aa
            'zpk':([-0.5 + 3**0.5/2.j, -0.5 - 3**0.5/2.j],
                   [(2./3)**0.5 * 1j, -(2./3)**0.5 * 1j], 1),
            'sos': None,
            'creator':('ba','filterbroker'), #(format ['ba', 'zpk', 'sos'], routine)
            'freqSpecsRangeType':'Half',
            'freqSpecsRange': [0,0.5],
            'freq_specs_sort' : True,
            'freq_specs_unit' : 'f_S',
            'plt_fLabel':r'$f$ in Hz $\rightarrow$',
            'plt_fUnit':'Hz',
            'plt_tLabel':r'$n \; \rightarrow$',
            'plt_tUnit':'s',
            'plt_phiUnit': 'rad',
            'plt_phiLabel': r'$\angle H(\mathrm{e}^{\mathrm{j} \Omega})$  in rad ' + r'$\rightarrow $',
            'wdg_dyn':{'win':'hann'}
            }


###############################################################################
"""
See also on data persistence and global variables:
http://stackoverflow.com/questions/13034496/using-global-variables-between-files-in-python
http://stackoverflow.com/questions/1977362/how-to-create-module-wide-variables-in-python
http://pymotw.com/2/articles/data_persistence.html

Alternative approaches for data persistence

shelve
------
a persistent dictionary for reading and writing.
This would get rid of the fb global dictionary


import shelve

### write to database:
s = shelve.open('test_shelf.fb')
try:
    s['key1'] = { 'int': 10, 'float':9.5, 'string':'Sample data' }
finally:
    s.close()

### read from database:
s = shelve.open('test_shelf.fb')
# s = shelve.open('test_shelf.fb', flag='r') # read-only
try:
    existing = s['key1']
finally:
    s.close()

print(existing)

### catch changes to objects, store in in-memory cache and write-back upon close
s = shelve.open('test_shelf.fb', writeback=True)
try:
    print s['key1']
    s['key1']['new_value'] = 'this was not here before'
    print s['key1']
finally:
    s.close()


===============================================================================
pickleshare
-----------
https://github.com/pickleshare/pickleshare
PickleShare - a small 'shelve' like datastore with concurrency support
Concurrency is possible because the values are stored in separate files. 
Hence the "database" is a directory where all files are governed by PickleShare.

from pickleshare import *
db = PickleShareDB('~/testpickleshare')
db.clear()
print "Should be empty:",db.items()
db['hello'] = 15
db['aku ankka'] = [1,2,313]
db['paths/are/ok/key'] = [1,(5,46)]
print db.keys()
"""