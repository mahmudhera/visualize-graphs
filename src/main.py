import argparse
import pandas as pd
import graphviz

def parse_args(): # pragma: no cover
    parser = argparse.ArgumentParser(description="This script will plot the given two graphs. Assumed that both graphs have the same edges, only differing in their lengths of these branches.  Assumed files are in tsv format, three columns, first two are node names, the third is the branch length",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-f1', '--file1', type=str, help="Name of the first file.")
    parser.add_argument('-f2', '--file2', type=str, help="Name of the second file.")
    args = parser.parse_args()
    return args

last = -500
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

    color_intensity = [ 1.0*x/y for (x,y) in list( zip(difference_of_lengths, sum_of_lengths) ) ]

    # graphs
    g = graphviz.Graph('G', filename='hello.gv', engine='sfdp', format='svg', node_attr={'width' : '0.02', 'height':'0.02', 'fixedsize':'true', 'label':''})
    for (v1, v2, color, length) in list( zip(vertex_1_list, vertex_2_list, color_intensity, lengths_in_graph1) ):
        pen_width = str( 7.0 * color )
        g.edge( get_encoding(v1.strip()) , get_encoding(v2.strip()), **{'color':'red', 'penwidth':pen_width, 'len':str(5*length)} )
    g.view()

if __name__ == '__main__':
    main()
