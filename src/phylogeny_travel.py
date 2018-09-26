#!/usr/bin/env python
# coding=utf-8


import os
import re
from .kmer import *

class TravelPhylogeny(object):
    
    """
        Python Class for Making DNA-Sensors by Creating Phylogeny of life includes Searching, Traversing,
        Making Graphs, Downloading Genomic Data using ftp and Creating K-mers manually to accelerate
        development project of Biosensors in BioInformatics.
        Extremely easy to learn and use, friendly construction.
    """
    

    
    
    def Graph_from_sqldb(sqlite_db):
        
        ## @title : creating a graph from sqlitedb
        
        import networkx as nx
        import pandas as pd
        import sqlite3
        
        conn = sqlite3.connect(sqlite_db)
        print("sqlite database connected")
        df = pd.read_sql_query("select * from species;", conn)
        print(df.head())
        G = nx.DiGraph(directed = True)
        i = 0
        for taxaid in df['taxid']:
            G.add_node(taxaid, name=str(df.iloc[i][2]), rank=str(df.iloc[i][4]), genome = [])
            i = i+1
        df = df[df['taxid'] != 1]
        print(df.head(n = 20))

        ## adding edges for Graph
        edge_list = []
        i = 0
        for taxaid in df['taxid']:
            edge = (df.iloc[i][1],taxaid)
            edge_list.append(edge)
            i = i+1

        ## making Edges from list
        G.add_edges_from(edge_list)
        
        return G
    
    
    
    def assembly_file_process(assembly_file_name):
        
        ## @title : Process assembly files to add full ftp path
        
        import os
        import pandas as pd
        import subprocess
        
        grep_assembly = "grep -E '.*' " + assembly_file_name +" | cut -f 20 > ftp_folder.txt2"
        print (grep_assembly)
        os.system(grep_assembly)
        os.system(str("sed '1d' ftp_folder.txt2 > ftp_folder3.txt"))
        
        cmd = """awk 'BEGIN{FS=OFS="/";filesuffix="genomic.fna.gz"}{ftpdir=$0;asm=$10;file=asm"_"filesuffix;print "wget -nc "ftpdir,file}' ftp_folder3.txt > all_wget_link.sh"""

        subprocess.getstatusoutput(cmd)

        with open('all_wget_link.sh') as f:
            all_links = f.read().splitlines()
        assembly = pd.read_table(assembly_file_name)
        assembly['FTP_download'] = all_links
        
        return assembly





    
    def pust_list_and_node(node,dnamer):
        
        from pymongo import MongoClient
        import pymongo
        
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["mydatabase1"]
        posts = db.posts
        print (posts)
        
        post_data = {'_id':node,
                     'dnamer': dnamer,
                    }
        
        posts.insert_one(post_data)
        client.close()
        
        return True
    
    
    
    def search_db(node):
        import pymongo
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["mydatabase1"]
        posts = db.posts
        result = posts.find_one({'_id': node})
        client.close()
        
        return result
    
    
    
    def put_list_node_in_gzip(node,dnamer):
        import gzip
        filename = str(node)+".gzip"
        with gzip.open("kmer_folder/" + filename, 'w') as fw:
            fw.write('\n'.join(dnamer))
            #fw.write('\n')
        fw.close()
        
        
        
    def write_path(filename,path):
        
        ## @title : write the fpath to be traveled in text gzip file
        
        import gzip
        
        filename = str(filename)+".gzip"
        with gzip.open("path_travelled/" + filename, 'wb') as fw:
            for line in path:
                fw.write(str(line))
                fw.write('\n')
            fw.close()
            
            
            
    def find_file_and_node_in_directory(directory_path):
        
        ## @title : return filename with extension and file name without extension
        
        from os import listdir
        from os.path import isfile, join
        
        files = [f for f in listdir(directory_path) if isfile(join(directory_path, f))]
        files_names = []
        for filename in files:
            files_names.append(os.path.splitext(filename)[0])
        
        return files,files_names
    
    
    
    def read_gzip_file_in_list(filename):
        
        ## @title : Read gzip line by line
        
        import gzip
        
        content = []
        with gzip.open(filename,'r') as fin:
            for line in fin:
                content.append(line.rstrip('\n'))
        
        return content  
    
    
    
    def create_seed_mer(seed,G,k=100):
        
        """ Download and create kmer from seed ftp link files
            Take a seed node and create kmer """








        all_dna_mer = []
        seed_ftp = G.node[seed]['genome']
        for link in seed_ftp:
            try:
                os.system(link)
            except:
                print ('No links found in seedmer')
            fileName = str(re.findall('(?:.+\/)(.+)',link)[0])
            dna_mer = create_kmer(fileName,k)
            all_dna_mer.append(list(dna_mer))
            
        return set(sum(all_dna_mer, []))
    
    
    
    def create_and_save_kmer_from_path_of_search_space(G,k,seed_mer,path_of_search_space):

        
        """ 
            Read nodes ftp links, download it and create kmer of it, 
            at last substract seedmer to dnamer and write files for nodes in search space 
        """


        import os
        import re
        import pandas as pd
        
        completed_node=[]
        folderfiles, name = find_file_and_node_in_directory('kmer_folder/')
        df = pd.DataFrame(columns=['filename', 'seed_mer_length'])
        df = df.append({'fileName':path_of_search_space[0], 'seed_mer_length':len(seed_mer)},
                          ignore_index=True )
        
        #k = 0
        for i in name:
            completed_node.append(int(i))
        for node in path_of_search_space[1:]:
            print (node)
            
            if node in completed_node:
                continue
            else:
                all_dna_mer = []
                list_of_ftp_links = []
                list_of_ftp_links=G.node[node]['genome']
                
                for link in list_of_ftp_links:
                    try:
                        os.system(link)
                    except:
                        True
                    
                    fileName = str(re.findall('(?:.+\/)(.+)',link)[0])
                    dna_mer = set(create_kmer(fileName,k))
                    seed_mer = seed_mer - dna_mer
                    #all_dna_mer.append(list(dna_mer))
                    print (fileName,len(seed_mer))
                    df = df.append({'fileName':fileName,'seed_mer_length':len(seed_mer)},ignore_index=True )
                    df.to_csv('plot_data.csv', sep='\t')
            #put_list_node_in_gzip(node=node,dnamer=sum(all_dna_mer, []))




            
