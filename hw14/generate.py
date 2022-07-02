import json
import os
import random
import string


CLASS_NUM_MAX = 20     # must greater than or equal to "2"
INTERFACE_NUM_MAX = 20  # must greater than or equal to "2"
ATTRIBUTE_NUM_MAX = 20
OPERATION_NUM_MAX = 20
PARAMETER_NUM_MAX = 20
STATE_MACHINE_NUM_MAX = 10
STATE_NUM_MAX = 20
TRIGGER_NUM_MAX = 3
EFFECT_NUM_MAX = 3

EXTEND_NUM_MAX = 3
IMPLEMENT_NUM_MAX = 3

model_id_set = set()
class_id_set = set()
interface_id_set = set()
operation_id_set = set()

state_machine_id_set = set()
region_id_set = set()
transition_id_set = set()

lut = {}  # lookup tableF

class Tree :
    def __init__(self) :
        self.tree = {}
    
    def add_relation(self, son_id, father_id) :
        if (son_id not in self.tree) :
            self.tree[son_id] = []
        self.tree[son_id].append(father_id)


    def judge_valid(self, son_id, father_id) :
        self.ret = False
        self.dfs_check(father_id, son_id)
        # 0 means success while -1 means failure
        if (self.ret == True) : return -1
        else : return 0
    

    def dfs_check(self, src, dst) :    
        if (src == dst) :
            self.ret = True
            return
        if (src not in self.tree.keys()) :
            return
        for it in self.tree[src] :
            self.dfs_check(it, dst)

extend_tree = Tree()

class DisjointSet :
    def __init__(self) :
        self.pre = {}
        self.rank = {}
    
    def add (self, id) :
        if (id not in self.pre.keys()) :
            self.pre[id] = id
            self.rank[id] = 0

    def find(self, id) :
        rep = id
        while (rep != self.pre[rep]) :
            rep = self.pre[rep]
        
        now = id
        while (now != rep) :
            fa = self.pre[now]
            self.pre[now] = rep
            now = fa
        return rep
    
    def union(self, id1, id2) :
        fa1 = self.find(id1)
        fa2 = self.find(id2)
        rank1 = self.rank[id1]
        rank2 = self.rank[id2]

        if (rank1 < rank2) :
            self.pre[fa1] = fa2
        elif (rank1 > rank2) :
            self.pre[fa2] = fa1
        else :
            self.pre[fa1] = fa2
            self.rank[fa2] += 1
    
    def is_linked(self, id1, id2) :
        return self.find(id1) == self.find(id2)


disjoint_set = DisjointSet()


class Project :
    _type = "Project"
    state_machine_no_set = set()

    def __init__(self, name) :
        self._id = get_id()
        lut[self._id] = self
        self.name = name
        self.ownedElements = []


    def __get_state_machine_name(self) :
        if (random.uniform(0, 1) < 0.2 and self.state_machine_no_set) :
            return "StateMachine" + str(random.choice(list(self.state_machine_no_set)))
        name_no = random.randint(0, STATE_MACHINE_NUM_MAX)
        while (name_no in self.state_machine_no_set) :
            name_no = random.randint(0, STATE_MACHINE_NUM_MAX)
        self.state_machine_no_set.add(name_no)    
        return "StateMachine" + str(name_no)
    
    def get_model(self) :
        new_model = UMLModel("Model", self._id)
        self.ownedElements.append(new_model)
    
    def get_state_machines(self) :
        num = random.randint(2, STATE_MACHINE_NUM_MAX)
        for _ in range(num) :
            state_machine_name = self.__get_state_machine_name()
            new_state_machine = UMLStateMachine(state_machine_name, self._id)
            self.ownedElements.append(new_state_machine)
    
    
    def to_dict(self) :
        ret =   { "_type" : self._type, 
                    "_id" : self._id, 
                    "name" : self.name, 
                    "ownedElements" : to_dict_list(self.ownedElements) 
                }
        return ret    


class UMLModel :
    _type = "UMLModel"
    
    def __init__(self, name, parent_id):
        self._id = get_id()
        lut[self._id] = self
        model_id_set.add(self._id)
        self._parent = {"$ref" : parent_id}
        self.name = name
        self.ownedElements = []

        self.class_name_no_set = set()
        self.interface_name_no_set = set()

    def __get_class_name(self) :
        # Guarantee a certain probability of the same name
        if (random.uniform(0, 1) < 0.2 and self.class_name_no_set) :
            return "Class" + str(random.choice(list(self.class_name_no_set)))
        name_no = random.randint(0, CLASS_NUM_MAX)
        while (name_no in self.class_name_no_set) :
            name_no = random.randint(0, CLASS_NUM_MAX)
        self.class_name_no_set.add(name_no)    
        return "Class" + str(name_no)
    
    def __get_interface_name(self) :
        name_no = random.randint(0, INTERFACE_NUM_MAX)
        while (name_no in self.interface_name_no_set) :
            name_no = random.randint(0, INTERFACE_NUM_MAX)
        self.interface_name_no_set.add(name_no)    
        return "Interface" + str(name_no)

    def get_classes(self) :
        num = random.randint(2, CLASS_NUM_MAX)
        for _ in range(num) :
            class_name = self.__get_class_name()
            new_class = UMLClass(class_name, self._id)
            self.ownedElements.append(new_class)

    def get_interfaces(self) :
        num = random.randint(2, INTERFACE_NUM_MAX)
        for _ in range(num) :
            interface_name = self.__get_interface_name()
            new_interface = UMLInterface(interface_name, self._id)
            self.ownedElements.append(new_interface)

    
    def to_dict(self) :
        ret =   { "_type" : self._type, 
                    "_id" : self._id, 
                    "_parent" : self._parent,
                    "name" : self.name, 
                    "ownedElements" : to_dict_list(self.ownedElements) 
                }
        return ret        
        
        
        
class UMLClass :
    _type = "UMLClass"
    

    def __init__(self, name, parent_id):
        self._id = get_id()
        lut[self._id] = self
        class_id_set.add(self._id)
        self._parent = {"$ref" : parent_id}
        self.name = name
        self.ownedElements = []
        self.attributes = []
        self.operations = []

        self.operation_name_no_set = set()
        self.operation_paras_list = []
        self.attribute_name_no_set = set()
        self.generalization_id_set = set()
        self.realization_id_set = set()
        
    def __get_attribute_name(self) :
        name_no = random.randint(0, ATTRIBUTE_NUM_MAX)
        while (name_no in self.attribute_name_no_set) :
            name_no = random.randint(0, ATTRIBUTE_NUM_MAX)
        self.attribute_name_no_set.add(name_no)    
        return "Attribute" + str(name_no)

    def __get_operation_name(self) :
        # Guarantee a certain probability of the same name
        if (random.uniform(0, 1) < 0.3 and self.operation_paras_list) :
            return "Operation" + str(random.choice(list(self.operation_name_no_set)))
        name_no = random.randint(0, OPERATION_NUM_MAX)
        while (name_no in self.operation_name_no_set) :
            name_no = random.randint(0, OPERATION_NUM_MAX)
        self.operation_name_no_set.add(name_no)    
        return "Operation" + str(name_no)
   
    def get_generalization(self) :
        if (random.uniform(0, 1) > 0.7) :
            if (len(self.generalization_id_set) >= len(class_id_set) - 1) : 
                return
            new_generalization = UMLGeneralization(self._id, "class")
            source_id = new_generalization.source["$ref"]
            target_id = new_generalization.target["$ref"]
            if (extend_tree.judge_valid(source_id, target_id) == 0) :
                self.ownedElements.append(new_generalization)
                extend_tree.add_relation(source_id, target_id)
            
    
    def get_realization(self) :
        num = random.randint(0, IMPLEMENT_NUM_MAX)
        for _ in range(num) :
            if (len(self.realization_id_set) >= len(interface_id_set)) : 
                break
            self.ownedElements.append(UMLInterfaceRealization(self._id))
    
    def get_attributes(self) :
        num = random.randint(0, ATTRIBUTE_NUM_MAX)
        for _ in range(num) :
            attribute_name = self.__get_attribute_name()
            if (random.uniform(0, 1) < 0.5) :
                new_attribute = UMLAttribute(attribute_name, self._id, "named")
                self.attributes.append(new_attribute)
            else :
                new_attribute = UMLAttribute(attribute_name, self._id, "referenced")
                self.attributes.append(new_attribute)

    def get_operations(self) :
        num = random.randint(0, OPERATION_NUM_MAX)
        for _ in range(num) :
            operation_name = self.__get_operation_name()
            if (random.uniform(0, 1) < 0.5 and self.operation_paras_list) :
                # Guarantee a certain probability of the same parameters
                new_operation = UMLOperation(operation_name, self._id, random.choice(self.operation_paras_list))
            else :
                new_operation = UMLOperation(operation_name, self._id)
            self.operations.append(new_operation)
            self.operation_paras_list.append(new_operation.parameters)
         

    def to_dict(self) :
        ret =   { "_type" : self._type, 
                    "_id" : self._id, 
                    "_parent" : self._parent,
                    "name" : self.name
                }
        if (self.ownedElements) :
            ret["ownedElements"] = to_dict_list(self.ownedElements)
        if (self.attributes) :
            ret["attributes"] = to_dict_list(self.attributes)
        if (self.operations) :
            ret["operations"] = to_dict_list(self.operations)
        return ret   


class UMLInterface :
    _type = "UMLInterface"
    
    def __init__(self, name, parent_id):
        self._id = get_id()
        lut[self._id] = self
        interface_id_set.add(self._id)
        self._parent = {"$ref" : parent_id}
        self.name = name
        self.ownedElements = []
        self.attributes = []
        self.operations = []

        self.operation_paras_list = []
        self.operation_name_no_set = set()
        self.attribute_name_no_set = set()

        self.generalization_id_set = set()
        

    def __get_attribute_name(self) :
        name_no = random.randint(0, ATTRIBUTE_NUM_MAX)
        while (name_no in self.attribute_name_no_set) :
            name_no = random.randint(0, ATTRIBUTE_NUM_MAX)
        self.attribute_name_no_set.add(name_no)    
        return "Attribute" + str(name_no)

    def __get_operation_name(self) :
        if (random.uniform(0, 1) < 0.2 and list(self.operation_name_no_set)) :
            return "Operation" + str(random.choice(list(self.operation_name_no_set)))
        name_no = random.randint(0, OPERATION_NUM_MAX)
        while (name_no in self.operation_name_no_set) :
            name_no = random.randint(0, OPERATION_NUM_MAX)
        self.operation_name_no_set.add(name_no)    
        return "Operation" + str(name_no)


    def get_generalization(self) :
        num = random.randint(0, EXTEND_NUM_MAX)
        for _ in range(num) :
            if (len(self.generalization_id_set) >= len(interface_id_set) - 1) :
                break
            new_generalization = UMLGeneralization(self._id, "interface")
            source_id = new_generalization.source["$ref"]
            target_id = new_generalization.target["$ref"]
            if (extend_tree.judge_valid(source_id, target_id) == 0) :
                self.ownedElements.append(new_generalization)
                extend_tree.add_relation(source_id, target_id)
            else :
                continue

    def get_attributes(self) :
        num = random.randint(0, ATTRIBUTE_NUM_MAX)
        for _ in range(num) :
            attribute_name = self.__get_attribute_name()
            if (random.uniform(0, 1) < 0.5) :
                new_attribute = UMLAttribute(attribute_name, self._id, "named")
                self.attributes.append(new_attribute)
            else :
                new_attribute = UMLAttribute(attribute_name, self._id, "referenced")
                self.attributes.append(new_attribute)

    def get_operations(self) :
        num = random.randint(0, OPERATION_NUM_MAX)
        for _ in range(num) :
            operation_name = self.__get_operation_name()
            if (random.uniform(0, 1) < 0.5 and self.operation_paras_list) :
                new_operation = UMLOperation(operation_name, self._id, random.choice(self.operation_paras_list))
            else :
                new_operation = UMLOperation(operation_name, self._id)
            self.operations.append(new_operation)
            self.operation_paras_list.append(new_operation.parameters)

    def to_dict(self) :
        ret =   { "_type" : self._type, 
                    "_id" : self._id, 
                    "_parent" : self._parent,
                    "name" : self.name
                }
        if (self.ownedElements) :
            ret["ownedElements"] = to_dict_list(self.ownedElements)
        if (self.attributes) :
            ret["attributes"] = to_dict_list(self.attributes)
        if (self.operations) :
            ret["operations"] = to_dict_list(self.operations)
        return ret  
    


class UMLAttribute :
    _type = "UMLAttribute"
    named_type_list = ["byte", "short", "int", "long", "float", "double", "char", "boolean", "String", "ErrorType1", "ErrorType2",  "ErrorType3"]
    visibility_list = ["public", "protected", "private", "package"]

    def __init__(self, name, parent_id, type):
        self._id = get_id()
        lut[self._id] = self
        self._parent = {"$ref" : parent_id}
        self.name = name
        self.visibility = random.choice(self.visibility_list)
        if (type == "named") :
            self.type = random.choice(self.named_type_list)
        else :
            self.type = {"$ref" : random.choice(list(class_id_set) + list(interface_id_set))}

            
    def to_dict(self) :
        ret =   { "_type" : self._type, 
                    "_id" : self._id, 
                    "_parent" : self._parent,
                    "name" : self.name, 
                    "visibility" : self.visibility,
                    "type" : self.type
                }
        return ret   
    

class UMLOperation :
    _type = "UMLOperation"
    visibility_list = ["public", "protected", "private", "package"]

    def __init__(self, name, parent_id, certain_paras = None):
        self._id = get_id()
        lut[self._id] = self
        operation_id_set.add(self._id)
        self._parent = {"$ref" : parent_id}
        self.name = name
        self.visibility = random.choice(self.visibility_list)
        self.parameters = []
        self.parameter_name_no_set = set()
        self.certain_paras = certain_paras
        
    def __get_parameter_name(self) :
        name_no = random.randint(0, PARAMETER_NUM_MAX)
        while (name_no in self.parameter_name_no_set) :
            name_no = random.randint(0, PARAMETER_NUM_MAX)
        self.parameter_name_no_set.add(name_no)    
        return "Parameter" + str(name_no)

    def get_parameters(self) :    
        if (self.certain_paras != None) :
            for para in self.certain_paras :
                parameter_name = self.__get_parameter_name()
                new_parameter = UMLParameter(parameter_name, self._id, para.type, para.direction, True)
                self.parameters.append(new_parameter)
            return

        num = random.randint(0, PARAMETER_NUM_MAX)
        for _ in range(num) :
            parameter_name = self.__get_parameter_name()
            new_parameter = UMLParameter(parameter_name, self._id, random.choice(["named", "reference"]), "in")
            self.parameters.append(new_parameter)
            
        
        if (random.uniform(0, 1) < 0.5) :
            new_parameter = UMLParameter(None, self._id, random.choice(["named", "reference"]), "return")
            self.parameters.append(new_parameter)
        

    def to_dict(self) :
        ret =   { "_type" : self._type, 
                    "_id" : self._id, 
                    "_parent" : self._parent,
                    "name" : self.name,
                    "visibility" : self.visibility
                }
        if (self.parameters) :
            ret["parameters"] = to_dict_list(self.parameters)

        return ret   



class UMLParameter :
    _type = "UMLParameter"
    named_type_list = ["byte", "short", "int", "long", "float", "double", "char", "boolean", "String", "ErrorType1", "ErrorType2",  "ErrorType3"]

    def __init__(self, name, parent_id, type, direction, certain = False):
        self._id = get_id()
        lut[self._id] = self
        self._parent = {"$ref" : parent_id}
        self.name = name
        self.direction = direction
        if (certain == True) :
            self.type = type
            return
        else :
            if (type == "named") :
                if (direction == "in") :
                    self.type = random.choice(self.named_type_list)
                else :    
                    self.type = random.choice(self.named_type_list + ["void"])
            else :
                self.type = {"$ref" : random.choice(list(class_id_set) + list(interface_id_set))}
        

    def to_dict(self) :
        if (self.direction == "in") :
            ret =   { "_type" : self._type, 
                        "_id" : self._id,  
                        "_parent" : self._parent,
                        "name" : self.name, 
                        "type" : self.type
                    }
        else :
            ret =   { "_type" : self._type, 
                        "_id" : self._id,  
                        "_parent" : self._parent,
                        "type" : self.type, 
                        "direction" : self.direction
                    }
        return ret   


class UMLInterfaceRealization : 
    _type = "UMLInterfaceRealization"

    def __init__(self, parent_id):
        self._id = get_id()
        lut[self._id] = self
        self._parent = {"$ref" : parent_id}
        self.source = {"$ref" : parent_id}
        target_id = random.choice(list(interface_id_set))
        while (target_id in lut[parent_id].realization_id_set) :
            target_id = random.choice(list(interface_id_set))
        self.target = {"$ref" : target_id}
        lut[parent_id].realization_id_set.add(target_id)
        

    def to_dict(self) :
        ret =   { "_type" : self._type, 
                    "_id" : self._id, 
                    "_parent" : self._parent,
                    "source" : self.source, 
                    "target" : self.target 
                }    
        return ret   



class UMLGeneralization :
    _type = "UMLGeneralization"

    def __init__(self, parent_id, type):
        self._id = get_id()
        lut[self._id] = self
        self._parent = {"$ref" : parent_id}
        self.source = {"$ref" : parent_id}
        if (type == "class") :
            target_id = random.choice(list(class_id_set))
            while (target_id == parent_id or target_id in lut[parent_id].generalization_id_set) :
                target_id = random.choice(list(class_id_set))
        else : 
            target_id = random.choice(list(interface_id_set))
            while (target_id == parent_id or target_id in lut[parent_id].generalization_id_set) :
                target_id = random.choice(list(interface_id_set))
        self.target = {"$ref" : target_id}
        lut[parent_id].generalization_id_set.add(target_id)

    def to_dict(self) :
        ret =   { "_type" : self._type, 
                    "_id" : self._id, 
                    "_parent" : self._parent,
                    "source" : self.source,
                    "target" : self.target
                }
        return ret   


class UMLStateMachine :
    _type = "UMLStateMachine"

    def __init__(self, name, parent_id) :
        self._id = get_id()
        lut[self._id] = self
        state_machine_id_set.add(self._id)
        self._parent = {"$ref" : parent_id }
        self.name = name
        self.regions = []
    
    def get_region(self) :
        new_region = UMLRegion(self._id)
        self.regions.append(new_region)
        
    def to_dict(self) :
        ret =   { "_type" : self._type, 
                    "_id" : self._id, 
                    "_parent" : self._parent,
                    "name" : self.name,
                    "regions" : to_dict_list(self.regions)
                }
        return ret   
        
class UMLRegion :
    _type = "UMLRegion"

    def __init__(self, parent_id) :
        self._id = get_id()
        lut[self._id] = self
        region_id_set.add(self._id)
        self._parent = {"$ref" : parent_id}
        self.vertices = []
        self.transitions = []

        self.state_name_no_set = set()
        self.pseudo_state_id = ""
        self.final_state_id_set = set()
        self.state_id_set = set()
    
    def __get_state_name(self) :
        if (random.uniform(0, 1) < 0.2 and self.state_name_no_set) :
            return "State" + str(random.choice(list(self.state_name_no_set)))
        name_no = random.randint(0, STATE_NUM_MAX)
        while (name_no in self.state_name_no_set) :
            name_no = random.randint(0, STATE_NUM_MAX)
        self.state_name_no_set.add(name_no)    
        return "State" + str(name_no)

    def __create_new_transition(self, source, target) :
        new_transition = UMLTransition(self._id, source, target)
        self.transitions.append(new_transition)

    def get_states(self) :
        # get pseudo state
        new_pseudo_state = UMLPseudostate("initial", self._id)
        self.pseudo_state_id = new_pseudo_state._id
        self.vertices.append(new_pseudo_state)
        disjoint_set.add(new_pseudo_state._id)
        
        # get state
        num = random.randint(0, STATE_NUM_MAX)
        for _ in range(num) :
            state_name = self.__get_state_name()
            new_state = UMLState(state_name, self._id)
            self.state_id_set.add(new_state._id)
            self.vertices.append(new_state)
            disjoint_set.add(new_state._id)

        # get final state
        final_state_num = random.randint(0, 3)
        for i in range(final_state_num) :
            new_final_state = UMLFinalState("final" + str(i), self._id)
            self.final_state_id_set.add(new_final_state._id)
            self.vertices.append(new_final_state)
            disjoint_set.add(new_final_state._id)


    def get_transitions(self) :
    
        init_dst_id = set()

        if (random.uniform(0, 1) < 0.2 and self.final_state_id_set) :
            source = self.pseudo_state_id
            target = random.choice(list(self.final_state_id_set))
            self.__create_new_transition(source, target)
            disjoint_set.union(source, target)
        
        
        num = random.randint(0, len(self.state_id_set)) 
        for _ in range(num) :
            target = random.choice(list(self.state_id_set))
            while (target in init_dst_id) :
                target = random.choice(list(self.state_id_set))
            self.__create_new_transition(self.pseudo_state_id, target)
            disjoint_set.union(self.pseudo_state_id, target)
            init_dst_id.add(target)

        num = random.randint(0, 2 * len(self.state_id_set))
        for _ in range(num) :
            source = random.choice(list(self.state_id_set))
            target = random.choice(list(self.state_id_set))
            self.__create_new_transition(source, target)
            disjoint_set.union(source, target)
        
        if (random.uniform(0, 1) > 0.2 and self.final_state_id_set) :
            num = random.randint(0, len(self.state_id_set) >> 1)
            for _ in range(num) :
                flag = random.randint(0, 1)
                target = random.choice(list(self.final_state_id_set))
                for state_id in self.state_id_set :
                    if (flag == 0 and disjoint_set.is_linked(self.pseudo_state_id, state_id)) :
                        self.__create_new_transition(state_id, target)
                        break
                    if (flag == 1 and not disjoint_set.is_linked(self.pseudo_state_id, state_id)) :
                        self.__create_new_transition(state_id, target)
                        break

    def to_dict(self) :
        ret =   { "_type" : self._type, 
                    "_id" : self._id, 
                    "_parent" : self._parent,
                    "vertices" : to_dict_list(self.vertices),
                    "transitions" : to_dict_list(self.transitions)
                }
        return ret   


class UMLState :
    _type = "UMLState"

    def __init__(self, name, parent_id) :
        self._id = get_id()
        lut[self._id] = self
        self._parent = {"$ref" : parent_id}
        self.name = name

    def to_dict(self) :
        ret =   { "_type" : self._type, 
                    "_id" : self._id, 
                    "_parent" : self._parent,
                    "name" : self.name
                }
        return ret  


class UMLPseudostate :
    _type = "UMLPseudostate"

    def __init__(self, name, parent_id):
        self._id = get_id()
        lut[self._id] = self
        self._parent = {"$ref" : parent_id}
        self.name = name
    
    def to_dict(self) :
        ret =   { "_type" : self._type, 
                    "_id" : self._id, 
                    "_parent" : self._parent,
                    "name" : self.name,
                    "kind" : "initial"
                }
        return ret   


class UMLFinalState :
    _type = "UMLFinalState"

    def __init__(self, name, parent_id):
        self._id = get_id()
        lut[self._id] = self
        self._parent = {"$ref" : parent_id}
        self.name = name
    
    def to_dict(self) :
        ret =   { "_type" : self._type, 
                    "_id" : self._id, 
                    "_parent" : self._parent,
                    "name" : self.name
                }
        return ret  


class UMLTransition :
    _type = "UMLTransition"

    def __init__(self, parent_id, source, target) :
        self._id = get_id()
        lut[self._id] = self
        transition_id_set.add(self._id)
        self._parent = {"$ref" : parent_id}
        self.source = {"$ref" : source}
        self.target = {"$ref" : target}
        self.triggers = []
        self.effects = []

        self.trigger_name_no_set = set()
        self.effect_name_no_set = set()

    def __get_trigger_name(self) :
        name_no = random.randint(0, TRIGGER_NUM_MAX)
        while (name_no in self.trigger_name_no_set) :
            name_no = random.randint(0, TRIGGER_NUM_MAX)
        self.trigger_name_no_set.add(name_no)    
        return "Trigger" + str(name_no)

    def __get_effect_name(self) :
        name_no = random.randint(0, EFFECT_NUM_MAX)
        while (name_no in self.effect_name_no_set) :
            name_no = random.randint(0, EFFECT_NUM_MAX)
        self.effect_name_no_set.add(name_no)    
        return "Effect" + str(name_no)

    def get_triggers(self) :
        num = random.randint(1, TRIGGER_NUM_MAX)
        for _ in range(num) :
            trigger_name = self.__get_trigger_name()
            new_trigger = UMLEvent(trigger_name, self._id)
            self.triggers.append(new_trigger)

    def get_effects(self) :
        num = random.randint(1, EFFECT_NUM_MAX)
        for _ in range(num) :
            effect_name = self.__get_effect_name()
            new_effect = UMLOpaqueBehavior(effect_name, self._id)
            self.effects.append(new_effect)
    
    def to_dict(self) :
        ret =   { "_type" : self._type, 
                    "_id" : self._id, 
                    "_parent" : self._parent,
                    "source" : self.source,
                    "target" : self.target,
                    "triggers" : to_dict_list(self.triggers),
                    "effects" : to_dict_list(self.effects)
                }
        return ret  



class UMLEvent :
    _type = "UMLEvent"

    def __init__(self, name, parent_id) :
        self._id = get_id()
        lut[self._id] = self
        self._parent = {"$ref" : parent_id}
        self.name = name

    def to_dict(self) :
        ret =   { "_type" : self._type, 
                    "_id" : self._id, 
                    "_parent" : self._parent,
                    "name" : self.name
                }
        return ret  


class UMLOpaqueBehavior :
    _type = "UMLOpaqueBehavior"

    def __init__(self, name, parent_id) :
        self._id = get_id()
        lut[self._id] = self
        self._parent = {"$ref" : parent_id}
        self.name = name
    
    def to_dict(self) :
        ret =   { "_type" : self._type, 
                    "_id" : self._id, 
                    "_parent" : self._parent,
                    "name" : self.name
                }
        return ret  


def get_id() :
    id = ""
    for _ in range(15) :
        id += str(random.choice(string.ascii_letters + string.digits))
    return "AAAAA" + id + "="

def to_dict_list(ele_list) :
    dict_list = []
    for ele in ele_list :
        dict_list.append(ele.to_dict())
    return dict_list

def get_UML() :
    project = Project("my_project")
    project.get_model()
    project.get_state_machines()

    # Class diagram

    for model_id in model_id_set :
        model = lut[model_id]
        model.get_classes()
        model.get_interfaces()

    for class_id in class_id_set :
        classs = lut[class_id]
        classs.get_generalization()
        classs.get_realization()
        classs.get_attributes()
        classs.get_operations()

    for interface_id in interface_id_set :
        interface = lut[interface_id]
        interface.get_generalization()
        interface.get_attributes()
        interface.get_operations()
    
    for operation_id in operation_id_set :
        operation = lut[operation_id]
        operation.get_parameters()

    # state diagram

    for state_machine_id in state_machine_id_set :
        state_machine = lut[state_machine_id]
        state_machine.get_region()
    
    for region_id in region_id_set :
        region = lut[region_id]
        region.get_states()
        region.get_transitions()
    
    for transition_id in transition_id_set :
        transition = lut[transition_id]
        transition.get_triggers()
        transition.get_effects()
    

    uml = json.dumps(project.to_dict(), indent=4)
    with open ("input_UML.mdj", "w") as f :
        f.write(uml)
    
def get_json() :
    f = open("input_json.txt", "w")
    f.close()

    # cmd = "java -jar U4T2.jar dump -s \"input_UML.mdj\" -n Model -t UMLModel > input_json.txt"
    # os.system(cmd)

    for no in Project.state_machine_no_set :
        cmd = "java -jar U4T2.jar dump -s \"input_UML.mdj\" -n StateMachine" + str(no) + " -t UMLStateMachine >> input_json.txt"
        os.system(cmd)
 

def get_instr() :
    instr_list = []
    # # class diagram
    # # instr_1
    # instr_list.append("CLASS_COUNT")
    # # instr_2
    # for _ in range(0, CLASS_NUM_MAX + 3) :
    #     instr_list.append("CLASS_SUBCLASS_COUNT Class" + str(i))
    # # instr_3
    # for _ in range(0, CLASS_NUM_MAX + 3) :
    #     instr_list.append("CLASS_OPERATION_COUNT Class" + str(i))
    # # instr_4
    # for _ in range(0, CLASS_NUM_MAX + 3) :
    #     for j in range(0, OPERATION_NUM_MAX + 3) :
    #         instr_list.append("CLASS_OPERATION_VISIBILITY Class" + str(i) + " Operation" + str(j))
    # # instr_5
    # for _ in range(0, CLASS_NUM_MAX + 3) :
    #     for j in range(0, OPERATION_NUM_MAX + 3) :
    #         instr_list.append("CLASS_OPERATION_COUPLING_DEGREE Class" + str(i) + " Operation" + str(j))
    # # instr_6
    # for _ in range(0, CLASS_NUM_MAX + 3) :
    #     instr_list.append("CLASS_ATTR_COUPLING_DEGREE Class" + str(i))
    # # instr_7
    # for _ in range(0, CLASS_NUM_MAX + 3) :
    #     instr_list.append("CLASS_IMPLEMENT_INTERFACE_LIST Class" + str(i))
    # # instr_8
    # for _ in range(0, CLASS_NUM_MAX + 3) :
    #     instr_list.append("CLASS_DEPTH_OF_INHERITANCE Class" + str(i))

    # state diagram
    for i in range(0, STATE_MACHINE_NUM_MAX + 3) :
        instr_list.append("STATE_COUNT StateMachine" + str(i))

    for i in range(0, STATE_MACHINE_NUM_MAX + 3) :
        for j in range(0, STATE_NUM_MAX + 3) :
            instr_list.append("STATE_IS_CRITICAL_POINT StateMachine" + str(i) + " State" + str(j))
    

    for i in range(0, STATE_MACHINE_NUM_MAX + 3) :
        for j in range(0, STATE_NUM_MAX + 3) :
            for k in range(0, STATE_NUM_MAX + 3) :
                instr_list.append("TRANSITION_TRIGGER StateMachine" + str(i) + " State" + str(j) + " State" + str(k))
      

    with open ("input_instr.txt", "w") as f :  
        for line in instr_list :
            f.write(line + "\n")      


if __name__ == '__main__' : 
    get_UML()
    get_json()
    get_instr()
    
    with open("input1.txt", "w") as data :
        f = open("input_json.txt", "r")
        temp = f.readlines()
        data.writelines(temp)
        f.close()

        data.write("END_OF_MODEL\n")

        f = open("input_instr.txt", "r")
        temp = f.readlines()
        data.writelines(temp)
        f.close()
    
    # cmd = "java -jar czh.jar < input.txt > output.txt"
    # os.system(cmd)
