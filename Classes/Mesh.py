# -*- coding: utf-8 -*-
"""Warning : this file has been generated, you shouldn't edit it"""

from os import linesep
from pyleecan.Classes.check import check_init_dict, check_var, raise_
from pyleecan.Functions.save import save
from pyleecan.Classes.frozen import FrozenClass

# Import all class method
# Try/catch to remove unnecessary dependencies in unused method
try:
    from pyleecan.Methods.Mesh.Mesh.set_submesh import set_submesh
except ImportError as error:
    set_submesh = error


from pyleecan.Classes.check import InitUnKnowClassError
from pyleecan.Classes.Element import Element
from pyleecan.Classes.Node import Node


class Mesh(FrozenClass):
    """Gather the mesh storage format"""

    VERSION = 1

    # cf Methods.Mesh.Mesh.set_submesh
    if isinstance(set_submesh, ImportError):
        set_submesh = property(
            fget=lambda x: raise_(
                ImportError("Can't use Mesh method set_submesh: " + str(set_submesh))
            )
        )
    else:
        set_submesh = set_submesh
    # save method is available in all object
    save = save

    def __init__(self, element=None, node=None, submesh=list(), init_dict=None):
        """Constructor of the class. Can be use in two ways :
        - __init__ (arg1 = 1, arg3 = 5) every parameters have name and default values
            for Matrix, None will initialise the property with an empty Matrix
            for pyleecan type, None will call the default constructor
        - __init__ (init_dict = d) d must be a dictionnary wiht every properties as keys

        ndarray or list can be given for Vector and Matrix
        object or dict can be given for pyleecan Object"""

        if element == -1:
            element = Element()
        if node == -1:
            node = Node()
        if init_dict is not None:  # Initialisation by dict
            check_init_dict(init_dict, ["element", "node", "submesh"])
            # Overwrite default value with init_dict content
            if "element" in list(init_dict.keys()):
                element = init_dict["element"]
            if "node" in list(init_dict.keys()):
                node = init_dict["node"]
            if "submesh" in list(init_dict.keys()):
                submesh = init_dict["submesh"]
        # Initialisation by argument
        self.parent = None
        # element can be None, a Element object or a dict
        if isinstance(element, dict):
            self.element = Element(init_dict=element)
        else:
            self.element = element
        # node can be None, a Node object or a dict
        if isinstance(node, dict):
            self.node = Node(init_dict=node)
        else:
            self.node = node
        # submesh can be None or a list of Mesh object
        self.submesh = list()
        if type(submesh) is list:
            for obj in submesh:
                if obj is None:  # Default value
                    self.submesh.append(Mesh())
                elif isinstance(obj, dict):
                    self.submesh.append(Mesh(init_dict=obj))
                else:
                    self.submesh.append(obj)
        elif submesh is None:
            self.submesh = list()
        else:
            self.submesh = submesh

        # The class is frozen, for now it's impossible to add new properties
        self._freeze()

    def __str__(self):
        """Convert this objet in a readeable string (for print)"""

        Mesh_str = ""
        if self.parent is None:
            Mesh_str += "parent = None " + linesep
        else:
            Mesh_str += "parent = " + str(type(self.parent)) + " object" + linesep
        Mesh_str += "element = " + str(self.element.as_dict()) + linesep + linesep
        Mesh_str += "node = " + str(self.node.as_dict()) + linesep + linesep
        if len(self.submesh) == 0:
            Mesh_str += "submesh = []"
        for ii in range(len(self.submesh)):
            Mesh_str += (
                "submesh[" + str(ii) + "] = " + str(self.submesh[ii].as_dict()) + "\n"
            )
        return Mesh_str

    def __eq__(self, other):
        """Compare two objects (skip parent)"""

        if type(other) != type(self):
            return False
        if other.element != self.element:
            return False
        if other.node != self.node:
            return False
        if other.submesh != self.submesh:
            return False
        return True

    def as_dict(self):
        """Convert this objet in a json seriable dict (can be use in __init__)
        """

        Mesh_dict = dict()
        if self.element is None:
            Mesh_dict["element"] = None
        else:
            Mesh_dict["element"] = self.element.as_dict()
        if self.node is None:
            Mesh_dict["node"] = None
        else:
            Mesh_dict["node"] = self.node.as_dict()
        Mesh_dict["submesh"] = list()
        for obj in self.submesh:
            Mesh_dict["submesh"].append(obj.as_dict())
        # The class name is added to the dict fordeserialisation purpose
        Mesh_dict["__class__"] = "Mesh"
        return Mesh_dict

    def _set_None(self):
        """Set all the properties to None (except pyleecan object)"""

        if self.element is not None:
            self.element._set_None()
        if self.node is not None:
            self.node._set_None()
        for obj in self.submesh:
            obj._set_None()

    def _get_element(self):
        """getter of element"""
        return self._element

    def _set_element(self, value):
        """setter of element"""
        check_var("element", value, "Element")
        self._element = value

        if self._element is not None:
            self._element.parent = self

    # Storing connectivity
    # Type : Element
    element = property(
        fget=_get_element, fset=_set_element, doc=u"""Storing connectivity"""
    )

    def _get_node(self):
        """getter of node"""
        return self._node

    def _set_node(self, value):
        """setter of node"""
        check_var("node", value, "Node")
        self._node = value

        if self._node is not None:
            self._node.parent = self

    # Storing nodes
    # Type : Node
    node = property(fget=_get_node, fset=_set_node, doc=u"""Storing nodes""")

    def _get_submesh(self):
        """getter of submesh"""
        for obj in self._submesh:
            if obj is not None:
                obj.parent = self
        return self._submesh

    def _set_submesh(self, value):
        """setter of submesh"""
        check_var("submesh", value, "[Mesh]")
        self._submesh = value

        for obj in self._submesh:
            if obj is not None:
                obj.parent = self

    # Storing submeshes. Node and element numbers/tags or group must be the same.
    # Type : [Mesh]
    submesh = property(
        fget=_get_submesh,
        fset=_set_submesh,
        doc=u"""Storing submeshes. Node and element numbers/tags or group must be the same.""",
    )