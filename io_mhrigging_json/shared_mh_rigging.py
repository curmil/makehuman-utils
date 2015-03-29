"""
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    https://bitbucket.org/MakeHuman/makehuman/

**Author:**            Manuel Bastioni

**Copyright(c):**      Manuel Bastioni 2014

**Licensing:**         AGPL3

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.


Abstract
--------

Export a json file with a rigging designed upon the makehuman base mesh.

"""

import math
import bpy
from bpy.types import Operator
import mathutils

VERSION = 102
DELTAMIN = 0.01
MIN_NUM_OF_VERS = 15128 #Number of vertices of base mesh without helpers
FULL_NUM_OF_VERS = 19158 #Number of vertices of base mesh with helpers

    
JOINTS_VERT_INDICES =[
    (13998,13999,14000,14001,14002,14003,14004,14005,),
    (14318,14319,14320,14321,14322,14323,14324,14325,),
    (14390,14391,14392,14393,14394,14395,14396,14397,),
    (14094,14095,14096,14097,14098,14099,14100,14101,),
    (13974,13975,13976,13977,13978,13979,13980,13981,),
    (13958,13959,13960,13961,13962,13963,13964,13965,),
    (14358,14359,14360,14361,14362,14363,14364,14365,),
    (14374,14375,14376,14377,14378,14379,14380,14381,),
    (14470,14471,14472,14473,14474,14475,14476,14477,),
    (14278,14279,14280,14281,14282,14283,14284,14285,),
    (14198,14199,14200,14201,14202,14203,14204,14205,),
    (13990,13991,13992,13993,13994,13995,13996,13997,),
    (14166,14167,14168,14169,14170,14171,14172,14173,),
    (14054,14055,14056,14057,14058,14059,14060,14061,),
    (14550,14551,14552,14553,14554,14555,14556,14557,),
    (14150,14151,14152,14153,14154,14155,14156,14157,),
    (13846,13847,13848,13849,13850,13851,13852,13853,),
    (14326,14327,14328,14329,14330,14331,14332,14333,),
    (13654,13655,13656,13657,13658,13659,13660,13661,),
    (14486,14487,14488,14489,14490,14491,14492,14493,),
    (13830,13831,13832,13833,13834,13835,13836,13837,),
    (13806,13807,13808,13809,13810,13811,13812,13813,),
    (14590,14591,14592,14593,14594,14595,14596,14597,),
    (14174,14175,14176,14177,14178,14179,14180,14181,),
    (14038,14039,14040,14041,14042,14043,14044,14045,),
    (13870,13871,13872,13873,13874,13875,13876,13877,),
    (14366,14367,14368,14369,14370,14371,14372,14373,),
    (14062,14063,14064,14065,14066,14067,14068,14069,),
    (14430,14431,14432,14433,14434,14435,14436,14437,),
    (13862,13863,13864,13865,13866,13867,13868,13869,),
    (14230,14231,14232,14233,14234,14235,14236,14237,),
    (14518,14519,14520,14521,14522,14523,14524,14525,),
    (14574,14575,14576,14577,14578,14579,14580,14581,),
    (14422,14423,14424,14425,14426,14427,14428,14429,),
    (13798,13799,13800,13801,13802,13803,13804,13805,),
    (14286,14287,14288,14289,14290,14291,14292,14293,),
    (13822,13823,13824,13825,13826,13827,13828,13829,),
    (14182,14183,14184,14185,14186,14187,14188,14189,),
    (14350,14351,14352,14353,14354,14355,14356,14357,),
    (13742,13743,13744,13745,13746,13747,13748,13749,),
    (13814,13815,13816,13817,13818,13819,13820,13821,),
    (14342,14343,14344,14345,14346,14347,14348,14349,),
    (13630,13631,13632,13633,13634,13635,13636,13637,),
    (13702,13703,13704,13705,13706,13707,13708,13709,),
    (13686,13687,13688,13689,13690,13691,13692,13693,),
    (14030,14031,14032,14033,14034,14035,14036,14037,),
    (14334,14335,14336,14337,14338,14339,14340,14341,),
    (14582,14583,14584,14585,14586,14587,14588,14589,),
    (19150,19151,19152,19153,19154,19155,19156,19157,),
    (13662,13663,13664,13665,13666,13667,13668,13669,),
    (14206,14207,14208,14209,14210,14211,14212,14213,),
    (14110,14111,14112,14113,14114,14115,14116,14117,),
    (14566,14567,14568,14569,14570,14571,14572,14573,),
    (14438,14439,14440,14441,14442,14443,14444,14445,),
    (14270,14271,14272,14273,14274,14275,14276,14277,),
    (14382,14383,14384,14385,14386,14387,14388,14389,),
    (14014,14015,14016,14017,14018,14019,14020,14021,),
    (14406,14407,14408,14409,14410,14411,14412,14413,),
    (14046,14047,14048,14049,14050,14051,14052,14053,),
    (14262,14263,14264,14265,14266,14267,14268,14269,),
    (14190,14191,14192,14193,14194,14195,14196,14197,),
    (14478,14479,14480,14481,14482,14483,14484,14485,),
    (14510,14511,14512,14513,14514,14515,14516,14517,),
    (14134,14135,14136,14137,14138,14139,14140,14141,),
    (13942,13943,13944,13945,13946,13947,13948,13949,),
    (13758,13759,13760,13761,13762,13763,13764,13765,),
    (14006,14007,14008,14009,14010,14011,14012,14013,),
    (14158,14159,14160,14161,14162,14163,14164,14165,),
    (14462,14463,14464,14465,14466,14467,14468,14469,),
    (13854,13855,13856,13857,13858,13859,13860,13861,),
    (13774,13775,13776,13777,13778,13779,13780,13781,),
    (13622,13623,13624,13625,13626,13627,13628,13629,),
    (13614,13615,13616,13617,13618,13619,13620,13621,),
    (13694,13695,13696,13697,13698,13699,13700,13701,),
    (13750,13751,13752,13753,13754,13755,13756,13757,),
    (13838,13839,13840,13841,13842,13843,13844,13845,),
    (13950,13951,13952,13953,13954,13955,13956,13957,),
    (14118,14119,14120,14121,14122,14123,14124,14125,),
    (13718,13719,13720,13721,13722,13723,13724,13725,),
    (14078,14079,14080,14081,14082,14083,14084,14085,),
    (13710,13711,13712,13713,13714,13715,13716,13717,),
    (14246,14247,14248,14249,14250,14251,14252,14253,),
    (14126,14127,14128,14129,14130,14131,14132,14133,),
    (14454,14455,14456,14457,14458,14459,14460,14461,),
    (14526,14527,14528,14529,14530,14531,14532,14533,),
    (14310,14311,14312,14313,14314,14315,14316,14317,),
    (14494,14495,14496,14497,14498,14499,14500,14501,),
    (13646,13647,13648,13649,13650,13651,13652,13653,),
    (13982,13983,13984,13985,13986,13987,13988,13989,),
    (14446,14447,14448,14449,14450,14451,14452,14453,),
    (13918,13919,13920,13921,13922,13923,13924,13925,),
    (13910,13911,13912,13913,13914,13915,13916,13917,),
    (14222,14223,14224,14225,14226,14227,14228,14229,),
    (13782,13783,13784,13785,13786,13787,13788,13789,),
    (14102,14103,14104,14105,14106,14107,14108,14109,),
    (13606,13607,13608,13609,13610,13611,13612,13613,),
    (14302,14303,14304,14305,14306,14307,14308,14309,),
    (13790,13791,13792,13793,13794,13795,13796,13797,),
    (13966,13967,13968,13969,13970,13971,13972,13973,),
    (13886,13887,13888,13889,13890,13891,13892,13893,),
    (13934,13935,13936,13937,13938,13939,13940,13941,),
    (14294,14295,14296,14297,14298,14299,14300,14301,),
    (14502,14503,14504,14505,14506,14507,14508,14509,),
    (13670,13671,13672,13673,13674,13675,13676,13677,),
    (13902,13903,13904,13905,13906,13907,13908,13909,),
    (14022,14023,14024,14025,14026,14027,14028,14029,),
    (14238,14239,14240,14241,14242,14243,14244,14245,),
    (13878,13879,13880,13881,13882,13883,13884,13885,),
    (14542,14543,14544,14545,14546,14547,14548,14549,),
    (13926,13927,13928,13929,13930,13931,13932,13933,),
    (14414,14415,14416,14417,14418,14419,14420,14421,),
    (13726,13727,13728,13729,13730,13731,13732,13733,),
    (13678,13679,13680,13681,13682,13683,13684,13685,),
    (13638,13639,13640,13641,13642,13643,13644,13645,),
    (13766,13767,13768,13769,13770,13771,13772,13773,),
    (14558,14559,14560,14561,14562,14563,14564,14565,),
    (14086,14087,14088,14089,14090,14091,14092,14093,),
    (14254,14255,14256,14257,14258,14259,14260,14261,),
    (13734,13735,13736,13737,13738,13739,13740,13741,),
    (13894,13895,13896,13897,13898,13899,13900,13901,),
    (14070,14071,14072,14073,14074,14075,14076,14077,),
    (14214,14215,14216,14217,14218,14219,14220,14221,),
    (14142,14143,14144,14145,14146,14147,14148,14149,),
    (14398,14399,14400,14401,14402,14403,14404,14405,),
    (14534,14535,14536,14537,14538,14539,14540,14541,),
]

MISSEDJOINTS = {
    "foot.L____tail": [13670, 13671, 13672, 13673, 13674, 13675, 13676, 13677, 13830, 13831, 13832, 13833, 13834, 13835, 13836, 13837],
    "foot.R____tail": [14110, 14111, 14112, 14113, 14114, 14115, 14116, 14117, 14270, 14271, 14272, 14273, 14274, 14275, 14276, 14277],
    "upperleg01.L____tail": [10891, 10938, 11025, 12991],
    "upperleg02.L____head": [10891, 10938, 11025, 12991],
    "upperleg02.R____head": [4260 ,4308, 4407, 6394],
    "upperleg01.R____tail": [4260, 4308, 4407, 6394],
    "upperarm02.R____head": [1404, 1406, 1419, 1429, 1440, 1442, 1628, 1638, 1639, 1640, 1648, 1649, 1652, 1662, 3759, 3760],
    "shoulder02.R____tail": [1404, 1406, 1419, 1429, 1440, 1442, 1628, 1638, 1639, 1640, 1648, 1649, 1652, 1662, 3759, 3760],
    "upperarm02.L____head": [8092, 8094, 8107, 8117, 8128, 8130, 8300, 8310, 8311, 8312, 8320, 8321, 8324, 8334, 10426, 10427],
    "shoulder02.L____tail": [8092, 8094, 8107, 8117, 8128, 8130, 8300, 8310, 8311, 8312, 8320, 8321, 8324, 8334, 10426, 10427],
    "tongue07.L____head": [14558, 14559, 14560, 14561, 14562, 14563, 14564, 14565, 14550, 14551, 14552, 14553, 14554, 14555, 14556, 14557],
    "tongue07.R____head": [14558, 14559, 14560, 14561, 14562, 14563, 14564, 14565, 14550, 14551, 14552, 14553, 14554, 14555, 14556, 14557],
    "neck03____head": [823, 829, 835, 886, 887, 888, 5278, 5279, 5285, 7534, 7540, 7546, 7588, 7589, 7590, 11885, 11886, 11891],
    "neck02____head": [818, 819, 820, 821, 824, 825, 826, 827, 830, 831, 832, 833, 836, 837, 838, 839, 7529, 7530, 7531, 7532, 7535, 7536, 7537, 7538, 7541, 7542, 7543, 7544, 7547, 7548, 7549, 7550],
    "neck02____tail": [823, 829, 835, 886, 887, 888, 5278, 5279, 5285, 7534, 7540, 7546, 7588, 7589, 7590, 11885, 11886, 11891],
    "neck01____tail": [818, 819, 820, 821, 824, 825, 826, 827, 830, 831, 832, 833, 836, 837, 838, 839, 7529, 7530, 7531, 7532, 7535, 7536, 7537, 7538, 7541, 7542, 7543, 7544, 7547, 7548, 7549, 7550]
}


def vdist(vect1,vect2):
    """
    This function returns the euclidean distance (the straight-line distance)
    between two vector coordinates.
    The distance between two points is the length of the vector joining them.

    Parameters
    ----------

    vect1:
        *float list*. The first vector - in the format[x,y,z]
        (or [x,y,z,0] for affine transformations in an homogeneous space).

    vect2:
        *float list*. The second vector - in the format [x,y,z]
        (or [x,y,z,0] for affine transformations in an homogeneous space).
    """
    joiningVect = [vect1[0] - vect2[0], vect1[1] - vect2[1], vect1[2] - vect2[2]]
    return math.sqrt(joiningVect[0] * joiningVect[0] + joiningVect[1] * joiningVect[1] + joiningVect[2] * joiningVect[2])

def centroid(vertsList):
    """
    This function returns the baricenter of a set of Blender vertices,
    returning a coordinate vector formatted as a float list
    [float X,float Y, float Z].
    This is the sum of all of the vectors divided by the number of vectors.

    Parameters
    ----------

    vertsList:
        List of Blender meshvertex objects.
    """
    nVerts = len(vertsList)
    xTot = 0.0; yTot = 0.0; zTot = 0.0
    for v in vertsList:
        xTot += v.co[0]
        yTot += v.co[1]
        zTot += v.co[2]
    if nVerts != 0:
        centrX = xTot/nVerts
        centrY = yTot/nVerts
        centrZ = zTot/nVerts
    else:
        print("Warning: no verts to calc centroid")
        return [0,0,0]
    return [centrX,centrY,centrZ]
    
def vertsindexToCentroid(vertIndexList):
    """
    This function return the centroid of a groups of vertices,
    retrieved using their index.
    """ 
    vertices = []
    if vertIndexList != None:
        for i in vertIndexList:
            try:
                vertices.append(getObject().data.vertices[i])
            except IndexError:
                print("Index {0} out of range".format(i))
        
    return centroid(vertices)

    
def getObject():
    """
    Return the active object
    """
    if len(bpy.context.selected_objects) > 0:
        
        #Get latest selected obj and make it the active one
        bpy.context.scene.objects.active = bpy.context.selected_objects[0]
    
        activeObject = bpy.context.object       
        return activeObject  
    else:
        print("No object selected")
        return None


class UI_messagebox(Operator):
    bl_idname = "box1.message"
    bl_label = "Wrong MH mesh: see console for details"

    def execute(self, context):
        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

def get_plane_coords(plane_joints, jointCoordinates):
    v1 = jointCoordinates[plane_joints[0]]
    v2 = jointCoordinates[plane_joints[1]]
    v3 = jointCoordinates[plane_joints[2]]
    return [v1, v2, v3]

def get_normal(plane_verts):
    v1 = mathutils.Vector(plane_verts[0])
    v2 = mathutils.Vector(plane_verts[1])
    v3 = mathutils.Vector(plane_verts[2])

    pvec = (v2-v1).normalized()
    yvec = (v3-v2).normalized()
    return yvec.cross(pvec).normalized()

