from cProfile import label
from turtle import color
from graphviz import Digraph


g = Digraph('G', filename='cluster.gv')

total_stacks = 0
cluster = 0
finished = 0
last_pushed = ""
first_thing = 0

teste = [
    "a * ( b - c / d * e ) / f - g * h",

    "- ( a * b )",
    
    "not A or B and ( not C or D )",
    
    "¬ A ^ ( B \/ C ) \/ D ^ ¬ E",
    
    "a - - - - b",
    
    "( a - ( - ( - ( - b ) ) ) )",
    
    "a * b + - c",
    
    "( - b ) * ( - c + b )",
    
    "not A and ( B or C ) or D and not E",
    
    "b * ( - - - c )",
    
    "¬ A ^ ( B \/ C ) \/ D ^ ¬ E",
    
    "( 1 + 2 ) * 3 + 4",

    "1 + 2 + 3 + 4 + 5",

    "a ^ c * ( b + n ^ p )"
]
prop = teste[-1]


termen = [{'name': 'term_0', 'equals' : ['a', '+', 'b']}]




# this is for Values

left_queue = []
# this is for operators

# right queue[i] {'operator': '-', 'precendence': 1, 'action': } if action = push, it is pushed, if action = wait, i need to pop out previous operators
right_queue = []


paranthesis = "()"
operators = ["*", "-", "+", "/", "not", "or", "and", "¬", "\/", "^"]

paranthesis = "()"
precendence = {
    "*" : 2,
    "-" : 1,
    "+" : 1,
    "/" : 2,
    "not" : 3,
    "or" : 1,
    "and" : 2,
    "¬" : 4,
    "\/" : 2,
    "^": 3,
}

# pastrez fiecare termen intr-o lista
def generare_lista():
    rez = []
    # for i in range(len(prop)):
    #     if prop[i] == ' ':
    #         continue
    #     if prop[i] not in operators and prop[i] not in paranthesis:
    #         termen += prop[i]
        
    #     if prop[i] in operators:

    #         if termen != '':
    #             rez.append(termen)
    #             termen = ''
    #         rez.append(prop[i])

    #     if prop[i] in paranthesis:
    #         if termen != '':
    #             rez.append(termen)
    #             termen = ''
    #         rez.append(prop[i])
    
    # rez.append(termen)
    rez = prop.split(" ")

    if len(rez) == 1:
        termen.append({'name': "term_1", 'equals': rez[0]})
    return rez

last_end = ''
def create_cluster(values: list, instructions: list, contor: int):
    # NOTE shape Msquare is used when an operator wants to join but his precendece doesn't allow it yet, so we proceed with popping operators
    global first_thing
    global total_stacks
    total_stacks += 1
    global cluster
    cluster += 1

    if first_thing == 0:
        g.node("start_prop", f"Starting point is: {prop}", shape="box")
        g.edge("start_prop", f'{contor}_start_{total_stacks}', label="", color="transparent")

    first_thing += 1




    with g.subgraph(name=f'cluster_{cluster}') as c:
        edges = []

        for i in range(len(values)):
            c.node(f'{contor}_{cluster}_value_{i}', values[i])

        for i in range(len(values) - 1):
            edges.append((f'{contor}_{cluster}_value_{i}', f'{contor}_{cluster}_value_{i + 1}'))
        
        c.edges(edges)
        c.attr(label='Values')

    cluster += 1
    with g.subgraph(name=f'cluster_{cluster}') as c:
        edges = []

        for i in range(len(instructions)):
            if instructions[i]['action'] == 'wait':
                c.node(f'{contor}_{cluster}_instruction_{i}', instructions[i]['operator'] + r'\l' + str(instructions[i]['precendence']) + r'\r', shape='Msquare')
            else:
                c.node(f'{contor}_{cluster}_instruction_{i}', instructions[i]['operator'] + r'\l' + str(instructions[i]['precendence']) + r'\r')



        for i in range(len(instructions) - 1):
            edges.append((f'{contor}_{cluster}_instruction_{i}', f'{contor}_{cluster}_instruction_{i + 1}'))
        
        c.edges(edges)
        c.attr(label='Instructions')
    
    cluster += 1


    if len(values) > 0 and "term_" in values[0]:
        k = int(values[0][5:])
        if finished == 0:
            g.node(f'{contor}_start_{total_stacks}', f"< <FONT COLOR='BLUE' > We can't push the last operator, so we pop, and create a term </FONT> >", shape="box")
        else:
            g.node(f'{contor}_start_{total_stacks}', f"< <FONT COLOR='BLUE' > No more operators to push, so we pop, and create a term </FONT> >", shape="box")
    else:
        if last_pushed == "right":
            g.node(f'{contor}_start_{total_stacks}', f"< <FONT COLOR='BLUE' > We push the operator: </FONT> <FONT COLOR='RED'> {instructions[0]['operator']} </FONT> >", shape="box")
        elif last_pushed == "left":        
            g.node(f'{contor}_start_{total_stacks}', f"< <FONT COLOR='BLUE' > We push variable: </FONT> <FONT COLOR='RED' > {values[0]} </FONT> >" , shape="box")
        else:
            g.node(f'{contor}_start_{total_stacks}')

    if len(values) > 0:
        g.edge(f'{contor}_start_{total_stacks}', f'{contor}_{cluster - 2}_value_0', label='', color="transparent")

        if "term_" in values[0]:
            k = int(values[0][5:])

            g.node(f'term_{total_stacks}', values[0] + ' = ' + ' '.join(termen[k]['equals']), shape="box")
            g.edge(f'{contor}_start_{total_stacks}', f'term_{total_stacks}')

    if len(instructions) > 0:
        g.edge(f'{contor}_start_{total_stacks}', f'{contor}_{cluster - 1}_instruction_0', label='', color="transparent")
    

    global last_end
    last_end = f'{contor}_end_{total_stacks}'
    g.node(f'{contor}_end_{total_stacks}', label='', color='transparent')

    if len(values) > 0:
        g.edge(f'{contor}_{cluster-2}_value_{len(values) - 1}', f'{contor}_end_{total_stacks}', label='', color="transparent")


    if len(instructions) > 0:
        g.edge(f'{contor}_{cluster-1}_instruction_{len(instructions) - 1}', f'{contor}_end_{total_stacks}', label='', color="transparent")




    
    

    if(total_stacks != 1):
        g.edge(f'{contor - 1}_end_{total_stacks - 1}', f'{contor}_start_{total_stacks}', label='', color="transparent")



def apply_pop(last_pop = 0, unary = False):
    global contor
    global pop_displayed
    print("Apply_pop::::::")
    print(right_queue)

    while(( len(right_queue) > 1 and right_queue[0]['precendence'] <= right_queue[1]['precendence'] ) or last_pop == 1 ) :
        
        get_equals = []            
        
        give_operator = right_queue[1 - last_pop]['operator']
        if len(left_queue) >= 1:
            get_equals.append( left_queue.pop(0) )

            give_operator = right_queue[1 - last_pop]['operator']

        # NOTE not operator is always unary

        get_equals.insert(0, f'{give_operator}')

        if len(left_queue) >= 1:

            
            if (give_operator not in ["not", "¬", '-']):
                get_equals.insert(0,left_queue.pop(0))

            if give_operator == '-' and unary == False:
                get_equals.insert(0,left_queue.pop(0))

        right_queue.pop(1 - last_pop)

        # when poping, we create terms
        termen.append({'name': f'term_{len(termen)}', 'equals': get_equals})

        # push the term
        left_queue.insert(0, termen[-1]['name'])


        # after a pop show the state
        contor += 1

        if len(right_queue) == 1:
            right_queue[0]['action'] = 'push'
        
        create_cluster(left_queue, right_queue, contor)
        pop_displayed = 1

        if last_pop == 1:
            break


contor = 0
pop_displayed = 0
def create_stacks(rez :list):

    # NOTE
    # for a symbol to become unary
    # it is the start of the proposition or it has an opening paranthesis in front



    global contor
    global pop_displayed
    adaug = 0
    consecutive_operators = 0

    unary = False
    global last_pushed
    last_pushed = ""
    for x in rez:
        pop_displayed = 0
        if x == '':
            continue
        if x in paranthesis:
            if x == '(':
                adaug += 100
                unary = True
            else:
                adaug -= 100
            continue
        if x in operators:
            # check if I can push the new operator
            importance = precendence[x] + adaug
            if len(right_queue) == 0 or (importance > right_queue[0]['precendence']):

               
                right_queue.insert(0, {'operator' : x, 'precendence': precendence[x] + adaug, 'action': 'push'})

                if last_pushed == "right":
                    unary = True
                
                last_pushed = "right"

            else:
                action = 'wait'
                if importance == right_queue[0]['precendence'] and right_queue[0]['operator'] == '-' and x == '-':
                    pop_displayed = 1
                    action = 'push'


                right_queue.insert(0, {'operator' : x, 'precendence': precendence[x] + adaug, 'action': action})


                if last_pushed == "right":
                    unary = True
                
                last_pushed = "right"

                contor += 1
                create_cluster(left_queue, right_queue, contor)
                
                if action == 'wait':
                    apply_pop(unary=unary)
                    unary = False

        else:
            left_queue.insert(0, x)
            last_pushed = "left"

        if pop_displayed == 0:
            contor += 1
            create_cluster(left_queue, right_queue, contor)

    print(right_queue)

    # apply pop for the last time
    global finished
    finished = 1
    while len(right_queue) >= 1:

        apply_pop(last_pop=1, unary=unary)
        unary = False
        



actual_graph = {

}


def go_deeper():
    # advance one more level with the graph, meaning, if I still have a node with the value term_{}
    # then transform that term in his coresponding graph
    # if a node has the key i, his left son is at i * 2, and the right son is at i * 2 + 1
    i = 0
    ok = 1
    for key in actual_graph.copy():

        if "term_" in actual_graph[key]:

            try: 
                # i need to unpack, create the subgraph
                index_term = int(actual_graph[key][5:])
                equals = termen[index_term]['equals']

                if len(equals) == 1:
                     actual_graph[key] = equals[0]
                     continue

                # make the right son
                right_key = str(int(key) * 2 + 1)
                actual_graph[right_key] = equals[-1]

                # change the curent key to the operator
                actual_graph[key] = equals[-2]

                if len(equals) == 3:
                    # make the left son
                    left_key = str(int(key) * 2)
                    actual_graph[left_key] = equals[0]
                
                break
            except:
                pass

def show_graph():
    print(actual_graph)





def give_dfs_indexes(rez: list, key: str):
    rez.append(key)

    # check for the left son
    left_son = str(int(key) * 2)

    if left_son in actual_graph.keys():
        give_dfs_indexes(rez, left_son)
    
    right_son = str(int(key) * 2 + 1)

    if right_son in actual_graph.keys():
        give_dfs_indexes(rez, right_son)


def create_one_graph(graphs: int):
    # make use of the actual_graph list

    node_index = 0

    polish_notation = ''

    
    g.node(f'Graph_{graphs}')

    g.node(last_end, color="black", label="< <FONT COLOR='BLUE' > Creating the graphs </FONT> >")
    
    g.edge(last_end, f'Graph_{graphs}')

    rez = []
    give_dfs_indexes(rez, '1')
    

    print('THIS IS REZ')
    print(rez)



    # f'< <FONT COLOR="RED"> {new_nod.nod}) </FONT> {new_nod.symbol}  >'
    for key in rez:
        
        node_index += 1
        
        if graphs == len(termen):
            g.node(f'Graph_{graphs}_node_{key}', f'< <FONT COLOR="RED"> {node_index}) </FONT> {actual_graph[key]} >')
        else:
            g.node(f'Graph_{graphs}_node_{key}', f'{actual_graph[key]}')

        polish_notation += actual_graph[key]

        
        if node_index == 1:
            g.edge(f'Graph_{graphs}', f'Graph_{graphs}_node_{key}')

        else:
            father = str(int(key) // 2)

            g.edge(f'Graph_{graphs}_node_{father}', f'Graph_{graphs}_node_{key}')

    print('THIS IS POLISH')
    print(polish_notation)

    if graphs == len(termen):
        g.node(f'polish', f'The polish notation in preorder is: {polish_notation}', shape='plaintext')
        g.edge(f'Graph_{graphs}', 'polish')




def create_graphs():
    graphs = 0

    actual_graph['1'] = termen[-1]['name']


    for i in range(len(termen)):
        graphs += 1
        create_one_graph(graphs)

        print('THIS IS THE GRAPH')
        show_graph()
        go_deeper()



    # all nodes will be Graph_{graphs}_node_{nodes}







values = ['a', 'b', 'c']
instructions = [{'operator': '-', 'precendence': 1, 'action': 'push'}, {'operator': '*', 'precendence': 2, 'action': 'push'}]


rez = generare_lista()
create_stacks(rez)



print(generare_lista())

print()
print(termen)

create_graphs()
g.view()
