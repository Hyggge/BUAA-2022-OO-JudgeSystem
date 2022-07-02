from colorfulPrint import ColorfulPrint
import json
import sys
import time
import os
import random
import string

MODEL_NUM = 1

CLASS_NUM_MAX = 20     # must greater than or equal to "2"
INTERFACE_NUM_MAX = 20  # must greater than or equal to "2"
ATTRIBUTE_NUM_MAX = 20
OPERATION_NUM_MAX = 20
PARAMETER_NUM_MAX = 20

EXTEND_NUM_MAX = 3
IMPLEMENT_NUM_MAX = 3

model_id_set = set()
class_id_set = set()
interface_id_set = set()
operation_id_set = set()
lut = {}  # lookup table

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


class Project :
    _type = "Project"

    def __init__(self, name) :
        self._id = get_id()
        lut[self._id] = self
        self.name = name
        self.ownedElements = []
    
    def get_model(self) :
        for i in range(MODEL_NUM) :
            new_model = UMLModel("Model" + str(i), self._id)
            self.ownedElements.append(new_model)
    
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
    named_type_list = ["byte", "short", "int", "long", "float", "double", "char", "boolean", "String"]
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
    named_type_list = ["byte", "short", "int", "long", "float", "double", "char", "boolean", "String"]

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

    uml = json.dumps(project.to_dict(), indent=4)
    with open ("input_UML.mdj", "w") as f :
        f.write(uml)
    
def get_json() :
    cmd = "java -jar U4T1.jar dump -s \"input_UML.mdj\" -n Model0 > input_json.txt"
    os.system(cmd)

def get_instr() :
    instr_list = []
    # instr_1
    instr_list.append("CLASS_COUNT")
    # instr_2
    for i in range(0, CLASS_NUM_MAX + 3) :
        instr_list.append("CLASS_SUBCLASS_COUNT Class" + str(i))
    # instr_3
    for i in range(0, CLASS_NUM_MAX + 3) :
        instr_list.append("CLASS_OPERATION_COUNT Class" + str(i))
    # instr_4
    for i in range(0, CLASS_NUM_MAX + 3) :
        for j in range(0, OPERATION_NUM_MAX + 3) :
            instr_list.append("CLASS_OPERATION_VISIBILITY Class" + str(i) + " Operation" + str(j))
    # instr_5
    for i in range(0, CLASS_NUM_MAX + 3) :
        for j in range(0, OPERATION_NUM_MAX + 3) :
            instr_list.append("CLASS_OPERATION_COUPLING_DEGREE Class" + str(i) + " Operation" + str(j))
    # instr_6
    for i in range(0, CLASS_NUM_MAX + 3) :
        instr_list.append("CLASS_ATTR_COUPLING_DEGREE Class" + str(i))
    # instr_7
    for i in range(0, CLASS_NUM_MAX + 3) :
        instr_list.append("CLASS_IMPLEMENT_INTERFACE_LIST Class" + str(i))
    # instr_8
    for i in range(0, CLASS_NUM_MAX + 3) :
        instr_list.append("CLASS_DEPTH_OF_INHERITANCE Class" + str(i))

    with open ("input_instr.txt", "w") as f :  
        for line in instr_list :
            f.write(line + "\n")      
    
player = ['czh', 'xjh', 'xyy']
playerNum = 3
maxErrorNum = 5

def showError(lineNum, inStr, exceptStr, readStr, name):
    ColorfulPrint.colorfulPrint('***** ' + name + ' ERROR IN LINE: ' + str(lineNum) + ' *****', ColorfulPrint.MODE_BOLD, ColorfulPrint.COLOR_RED)
    ColorfulPrint.colorfulPrint('Input: ' + inStr, ColorfulPrint.MODE_BOLD, ColorfulPrint.COLOR_RED)
    ColorfulPrint.colorfulPrint('We excepted: ' + exceptStr, ColorfulPrint.MODE_BOLD, ColorfulPrint.COLOR_RED)
    ColorfulPrint.colorfulPrint('Your output: ' + readStr, ColorfulPrint.MODE_BOLD, ColorfulPrint.COLOR_RED)

def makeLog(num, size, tle = False):
    if tle == False:
        with open('input.txt', 'r') as f:
            con = f.read()
        with open('./logWA/input' + str(num) + '.txt', 'w') as f:
            f.write(con)
        for i in range(size):
            name1 = 'output' + str(i + 1) + '.txt'
            name2 = './logWA/output' + str(i + 1) + '_' + str(num) + '.txt'
            with open(name1, 'r') as f:
                con = f.read()
            with open(name2, 'w') as f:
                f.write(con)
    else:
        with open('input.txt', 'r') as f:
            con = f.read()
        with open('./logTLE/input' + str(num) + '.txt', 'w') as f:
            f.write(con)
        for i in range(size):
            name1 = 'output' + str(i + 1) + '.txt'
            name2 = './logTLE/output' + str(i + 1) + '_' + str(num) + '.txt'
            with open(name1, 'r') as f:
                con = f.read()
            with open(name2, 'w') as f:
                f.write(con)

def runAndCmp():
    countError = 0
    if playerNum <= 1:
        ColorfulPrint.colorfulPrint('***** TOO LESS! *****', ColorfulPrint.MODE_BOLD, ColorfulPrint.COLOR_RED)
        return
    for i in range(playerNum):
        begTime = time.time()
        cmd = 'java -jar ' + player[i] + '.jar < input.txt > output' + str(i + 1) + '.txt'
        os.system(cmd)
        ColorfulPrint.colorfulPrint('>>>>> ' + player[i] + ' use time: ' + str(time.time() - begTime) + 's <<<<<', ColorfulPrint.MODE_BOLD, ColorfulPrint.COLOR_BLUE)
    with open('input.txt', 'r') as f:
        stdin = f.readlines()
        count  = 0
        while stdin[count] != 'END_OF_MODEL\n':
            count += 1
        stdin = stdin[count + 1:]
    stdout = []
    for i in range(playerNum):
        with open('output' + str(i + 1) + '.txt', 'r') as f:
            stdout.append(f.readlines())
    for j in range(len(stdout[0])):
        for i in range(playerNum):
            if i == 0:
                continue
            if stdout[0][j] != stdout[i][j]:
                if countError >= maxErrorNum:
                    return False
                countError += 1
                showError(j + 1, stdin[j][:-1], stdout[0][j][:-1], stdout[i][j][:-1], player[i])
    if countError == 0:
        return True
    else:
        return False
    

if __name__ == '__main__' : 
    get_UML()
    get_json()
    get_instr()
    
    with open("input.txt", "w") as data :
        f = open("input_json.txt", "r")
        temp = f.readlines()
        data.writelines(temp)
        f.close()

        data.write("END_OF_MODEL\n")

        f = open("input_instr.txt", "r")
        temp = f.readlines()
        data.writelines(temp)
        f.close()
        
    if runAndCmp() == True:
        ColorfulPrint.colorfulPrint('===== ACCEPTED =====', ColorfulPrint.MODE_BOLD, ColorfulPrint.COLOR_GREEN)
    else:
        ColorfulPrint.colorfulPrint('***** WRONG ANSWER *****', ColorfulPrint.MODE_BOLD, ColorfulPrint.COLOR_RED)
        makeLog(int(sys.argv[1]), playerNum)
    


    
