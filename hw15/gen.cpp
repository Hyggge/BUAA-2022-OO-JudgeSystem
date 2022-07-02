#include <bits/stdc++.h>

using namespace std;

const int MAX_COL = 3;
const int MAX_ATTRI = 10;
const int MAX_INTER = 5;
const int MAX_LIFE = 20;
const int MAX_MEG = 100;
const int MAX_END = 5;
const int MAX_LEN = 10;
const int PRO = 5;
const int R006_PRO = 3;

static int id = 0;
static vector<string> name_pool;
static bool if_r006;

class Data;
class Message;
class Lifeline;
class EndPoint;
class Interaction;
class Attribute;
class Collaboration;

enum MessageSort {
    SYNCH_CALL,
    ASYNCH_CALL,
    ASYNCH_SIGNAL,
    CREATE_MESSAGE,
    DELETE_MESSAGE,
    REPLY
};

enum Visibility {
    PUBLIC, // public
    PROTECTED,  // protected
    PRIVATE,  // private
    PACKAGE  // package-private
};

vector<string> visibility2string = {
    "public",
    "protected",
    "private",
    "package"
};

vector<string> message_sort2string = {
    "synchCall",
    
    "asynchCall",
    
    "asynchSignal",
    
    "createMessage",
    "createMessage",
    "createMessage",
    
    "deleteMessage",
    
    "reply"
};

string alloc_id() {
    return "AAAAA" + to_string(id++);
}

string& get_visibility() {
    return visibility2string[rand() % 4];
}

string& get_message_sort() {
    return message_sort2string[rand() % message_sort2string.size()];
}

bool str_is_empty(const string& str) {
	for (char c : str) {
		if (c == ' ' || c == '\t') {
			return true;
		}
	}
	return str.empty();
}

class Data {
public:
    string id;
    string parent;
    string name;

    explicit Data(string& id, string& parent, string& name) : id(id), parent(parent), name(name) {}

    static bool if_duplicate() {
        return rand() % PRO == 0;
    }

    static bool if_missing() {
        return rand() % PRO == 0;
    }
    
    static bool if_empty_name() {
    	return rand() % PRO == 0;
	}
	
	static string alloc_empty_name() {
		string result = string("\"");
		int len = rand() % MAX_LEN;
		for (int i = 0;i < len;i++) {
			result += ((rand() % 2) ? string(" ") : string("\t"));
		}
		result += string("\"");
		return result;
	}
};

class Attribute : public Data {
public:
	static int ids;
	
	Attribute(string id, string parent, string name) : Data(id, parent, name) {}
	
    static string alloc_name() {
		if (Data::if_empty_name()) {
			return Data::alloc_empty_name();
		}
	    string s = "\"collaboration_attribute" + to_string(ids++) + "\"";  // not to collide with attribute in UmlModel
	    name_pool.push_back(s);
	    return s;
    }
};

vector<Attribute> attributes;

class Message : public Data {
public:
    static int ids;
    explicit Message(string& id, string& parent, string& name) : Data(id, parent, name) {}

    static string alloc_name() {
        return "\"message" + to_string(ids++) + "\"";
    }
};

class Lifeline : public Data {
public:
    static int ids;
    // bool is_deleted;
    explicit Lifeline(string& id, string& parent, string& name) : Data(id, parent, name) {}

    static string alloc_name() {
    	if (Data::if_empty_name()) {
    		return Data::alloc_empty_name();
		}
        if (if_duplicate()) {
            ids--;
        }
        string s = "\"lifeline" + to_string(ids++) + "\"";
        name_pool.push_back(s);
        return s;
    }
};

class EndPoint : public Data {
public:
    static int ids;
    explicit EndPoint(string& id, string& parent, string& name) : Data(id, parent, name) {}

    static string alloc_name() {
    	if (Data::if_empty_name()) {
    		return Data::alloc_empty_name();
		}
        string s = "\"endpoint" + to_string(ids++) + "\"";
        name_pool.push_back(s);
        return s;
    }
};

class Interaction : public Data {
public:
    static int ids;
    vector<Lifeline> lifelines;
    vector<EndPoint> end_points;
    vector<Message> messages;

    explicit Interaction(string& id, string& parent, string& name) : Data(id, parent, name) {
        create_lifeline();
        create_end_point();
        create_message();
    }

    static string alloc_name() {
    	if (Data::if_empty_name()) {
    		return Data::alloc_empty_name();
		}
        if (if_duplicate()) {
            ids--;
        }
        string s = "\"interaction" + to_string(ids++) + "\"";
        name_pool.push_back(s);
        return s;
    }

    void create_lifeline() {
        for (int i = 0; i < MAX_LIFE; ++i) {
            string lifeline_id = alloc_id();
            string lifeline_name = Lifeline::alloc_name();
            string& parent_id = id;
            Attribute* represent = &attributes[rand() % attributes.size()];
			if (!if_r006) {  // normal case, make sure represent attribute's parent is current interaction's parent
				while (represent->parent != parent) {
					represent = &attributes[rand() % attributes.size()];
				}
			}
			string& represent_id = represent->id;
            string& visibility = get_visibility();
            Lifeline lifeline(lifeline_id, parent_id, lifeline_name);
            lifelines.push_back(lifeline);
            printf(R"({"_parent":"%s","visibility":"%s","name":%s,"_type":"UMLLifeline","isMultiInstance":false,"_id":"%s","represent":"%s"})""\n",
                   parent_id.c_str(), visibility.c_str(), lifeline_name.c_str(), lifeline_id.c_str(), represent_id.c_str());
        }
    }

    void create_end_point() {
        for (int i = 0; i < MAX_END; ++i) {
            string end_point_id = alloc_id();
            string end_point_name = EndPoint::alloc_name();
            string& parent_id = id;
            string& visibility = get_visibility();
            EndPoint end_point(end_point_id, parent_id, end_point_name);
            end_points.push_back(end_point);
            printf(R"({"_parent":"%s","visibility":"%s","name":%s,"_type":"UMLEndpoint","_id":"%s"})""\n",
                   parent_id.c_str(), visibility.c_str(), end_point_name.c_str(), end_point_id.c_str());
        }
    }

    void create_message() {
        for (int i = 0; i < MAX_MEG; ++i) {
            string message_id = alloc_id();
            string message_name = Message::alloc_name();
            string& parent_id = id;
            string& message_sort = get_message_sort();
            string& visibility = get_visibility();
            string *source = nullptr, *target = nullptr;
            bool is_normal = get_source_target(&source, &target);
            if (source == nullptr || target == nullptr || (message_sort == "createMessage" &&
				(!is_normal || *source == *target)) || (message_sort == "deleteMessage" && rand() % (MAX_MEG * MAX_INTER))) {
                continue ;
            }
            printf(R"({"messageSort":"%s","_parent":"%s","visibility":"%s","name":%s,"_type":"UMLMessage","_id":"%s","source":"%s","target":"%s"})""\n",
                  message_sort.c_str(), parent_id.c_str(), visibility.c_str(), message_name.c_str(), message_id.c_str(), source->c_str(), target->c_str());
        }
    }

    bool if_lost() const {
        return !end_points.empty() && rand() % PRO == 0;
    }

    bool if_found() const {
        return !end_points.empty() && rand() % PRO == 0;
    }

    bool get_source_target(string** source_pp, string** target_pp) {
        string* source_p = nullptr;
        string* target_p = nullptr;
        bool is_normal = true;
        if (lifelines.size() >= 2) {
            if (if_lost()) {
                source_p = &lifelines[rand() % lifelines.size()].id;
                target_p = &end_points[rand() % end_points.size()].id;
                while (*source_p == *target_p) {
                	target_p = &end_points[rand() % end_points.size()].id;
				}
                is_normal = false;
            } else if (if_found()) {
                source_p = &end_points[rand() % end_points.size()].id;
                target_p = &lifelines[rand() % lifelines.size()].id;
                while (*source_p == *target_p) {
                	target_p = &end_points[rand() % end_points.size()].id;
				}
                is_normal = false;
            } else {
                source_p = &lifelines[rand() % lifelines.size()].id;
                target_p = &lifelines[rand() % lifelines.size()].id;
                is_normal = true;
            }
        }
        *source_pp = source_p;
        *target_pp = target_p;
        return is_normal;
    }

    void to_instr() {
        string* interaction_name;
        string* lifeline_name;
        if (if_missing()) {
            interaction_name = &name_pool[rand() % name_pool.size()];
        } else {
        	interaction_name = &name;
		}
		if (str_is_empty(interaction_name->substr(1, interaction_name->size() - 2))) {
			return;
		}
        printf("PTCP_OBJ_COUNT %s\n", interaction_name->substr(1, interaction_name->size() - 2).c_str());
        for (int i = 0; i < lifelines.size(); ++i) {
            if (if_missing()) {
                lifeline_name = &name_pool[rand() % name_pool.size()];
            } else {
                lifeline_name = &lifelines[i].name;
            }
            if (if_missing()) {
                interaction_name = &name_pool[rand() % name_pool.size()];
            } else {
                interaction_name = &name;
            }
            if (str_is_empty(interaction_name->substr(1, interaction_name->size() - 2)) ||
				str_is_empty(lifeline_name->substr(1, lifeline_name->size() - 2))) {
            	continue;
			}
            printf("PTCP_CREATOR %s %s\n",
				   interaction_name->substr(1, interaction_name->size() - 2).c_str(),
			       lifeline_name->substr(1, lifeline_name->size() - 2).c_str());
            printf("PTCP_LOST_AND_FOUND %s %s\n",
				   interaction_name->substr(1, interaction_name->size() - 2).c_str(),
			       lifeline_name->substr(1, lifeline_name->size() - 2).c_str());
        }
    }
};

class Collaboration : public Data {
public:
    static int ids;
    vector<Interaction> interactions;

    explicit Collaboration(string& id, string& parent, string& name) : Data(id, parent, name) {
    	create_attribute();
        create_interaction();
    }

    static string alloc_name() {
    	if (Data::if_empty_name()) {
    		return Data::alloc_empty_name();
		}
        string s = "\"collaboration" + to_string(ids++) + "\"";
        name_pool.push_back(s);
        return s;
    }
    
    void create_attribute() {
    	for (int i = 0;i < MAX_ATTRI;i++) {
    		string& parent_id = id;
	    	string attribute_id = alloc_id();
			string attribute_name = Attribute::alloc_name();
			string& visibility = get_visibility();
			attributes.push_back(Attribute(attribute_id, parent_id, attribute_name));
			printf(R"({"_parent":"%s","visibility":"%s","name":%s,"_type":"UMLAttribute","_id":"%s","type":""})""\n",
				   parent_id.c_str(), visibility.c_str(), attribute_name.c_str(), attribute_id.c_str());	
		}
	}

    void create_interaction() {
        for (int i = 0; i < MAX_INTER; ++i) {
            string interaction_id = alloc_id();
            string interaction_name = Interaction::alloc_name();
            string& parent_id = id;
            string& visibility = get_visibility();
            Interaction interaction(interaction_id, parent_id, interaction_name);
            interactions.push_back(interaction);
            printf(R"({"_parent":"%s","visibility":"%s","name":%s,"_type":"UMLInteraction","_id":"%s"})""\n",
                   id.c_str(), visibility.c_str(), interaction_name.c_str(), interaction_id.c_str());
        }
    }

    void to_instr() {
        for (Interaction& interaction : interactions) {
            interaction.to_instr();
        }
    }
};

int Collaboration::ids = 0;
int Interaction::ids = 0;
int Lifeline::ids = 0;
int Message::ids = 0;
int EndPoint::ids = 0;
int Attribute::ids = 0;

int main() {
    srand(time(nullptr));
    if_r006 = rand() % R006_PRO == 0;

    vector<Collaboration> collaborations;

    for (int i = 0; i < MAX_COL; ++i) {
        string collaboration_id = alloc_id();
        string collaboration_name = Collaboration::alloc_name();
        string parent_id = "null";
        printf(R"({"_parent":"%s","name":%s,"_type":"UMLCollaboration","_id":"%s"})""\n",
               parent_id.c_str(), collaboration_name.c_str(), collaboration_id.c_str());
        Collaboration collaboration(collaboration_id, parent_id, collaboration_name);
        collaborations.push_back(collaboration);
    }

    printf("END_OF_MODEL\n");

    for (Collaboration& collaboration : collaborations) {
        collaboration.to_instr();
    }

    return 0;
}

