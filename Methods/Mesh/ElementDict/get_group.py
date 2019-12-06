# -*- coding: utf-8 -*-

import numpy as np


def get_group(self, group_number):
    """Define an Element object as submesh of parent mesh object

     Parameters
     ----------
     self : ElementDict
         an ElementDict object
     group_number : int
         a group number which define the elements which constitute the submesh

     Returns
     -------
     subelem: ElementDict
         an ElementDict which is a submesh of parent mesh self related to group_number

     """
    module = __import__("pyleecan.Classes." + "ElementDict", fromlist=["ElementDict"])
    subelem = getattr(module, "ElementDict")()
    subelem.connectivity = dict()
    subelem.group = dict()
    subelem.tag = dict()
    subelem.nb_elem = dict()
    subelem.nb_node_per_element = dict()

    connect_parent = self.connectivity
    groups = self.group
    tags = self.tag

    for key in groups:
        Ielem = np.where(groups[key] == group_number)[0]
        subelem.connectivity[key] = connect_parent[key][Ielem, :]
        subelem.group[key] = groups[key][Ielem]  # Should be only one type
        subelem.tag[key] = tags[key][Ielem]
        subelem.nb_elem[key] = len(Ielem)
        subelem.nb_node_per_element[key] = self.nb_node_per_element[key] # Must be the same


    return subelem
