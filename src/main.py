import argparse
import pandas as pd
import graphviz

max_opacity = 30
max_width = 10
max_length_in_inches = 7

def parse_args(): # pragma: no cover
    parser = argparse.ArgumentParser(description="This script will plot the given two graphs. Assumed that both graphs have the same edges, only differing in their lengths of these branches.  Assumed files are in tsv format, three columns, first two are node names, the third is the branch length",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-f1', '--file1', type=str, help="Name of the first file.")
    parser.add_argument('-f2', '--file2', type=str, help="Name of the second file.")
    args = parser.parse_args()
    return args

last = 0
dic = {}
def get_encoding(vertex_name):
    global last
    global dic
    if vertex_name in dic.keys():
        return dic[vertex_name]
    else:
        dic[vertex_name] = str(last)
        last = last + 1
        return dic[vertex_name]

def get_hex_from_intensity(intensity):
    in_numbers = int(max_opacity * intensity) + 10
    ret_str = "{x:X}".format(x=in_numbers)
    if len(ret_str) == 1:
        return '0' + ret_str
    else:
        return ret_str

def main(): # pragma: no cover
    args = parse_args()
    file1 = args.file1
    file2 = args.file2

    df1 = pd.read_csv(file1, delimiter='\t')
    df2 = pd.read_csv(file2, delimiter='\t')

    vertex_1_list = df1['parent'].tolist()
    vertex_2_list = df1['child'].tolist()

    lengths_in_graph1 = df1['edge_length'].tolist()
    lengths_in_graph2 = df2['edge_length'].tolist()
    sum_of_lengths = [ x+y for (x,y) in list(zip(lengths_in_graph1, lengths_in_graph2)) ]
    difference_of_lengths = [ abs(x-y) for (x,y) in list(zip(lengths_in_graph1, lengths_in_graph2)) ]

    intensity_list = [ 1.0*x/y for (x,y) in list( zip(difference_of_lengths, sum_of_lengths) ) ]

    # graphs
    g = graphviz.Graph('G', filename='hello.gv', engine='sfdp', format='svg', node_attr={'width' : '0.02', 'height':'0.02', 'fixedsize':'true', 'label':''})
    for (v1, v2, intensity, length) in list( zip(vertex_1_list, vertex_2_list, intensity_list, lengths_in_graph1) ):
        pen_width = str( max_width * intensity )
        opacity = get_hex_from_intensity(intensity)
        g.edge( get_encoding(v1.strip()) , get_encoding(v2.strip()), **{'color':'#0000ff' + opacity, 'penwidth':pen_width, 'len':str(max_length_in_inches*length)} )
    g.view()

if __name__ == '__main__':
    main()
