def merge(names,nodes,delnodes,merged):
    
    #import librarys.
    import csv  
    import pandas as pd
    
    #create empty DataFrame df_names and df_nodes.
    df_names = pd.DataFrame()
    df_nodes = pd.DataFrame()
    
    #read .dmp files with use of parameters.
    df_names = pd.read_csv(names,delimiter='\t',header=None)
    df_nodes = pd.read_csv(nodes,delimiter='\t',header=None)
    
    #collect usefull columns from DataFrames.
    df_nodes = df_nodes[[0,2,4]] 
    df_names = df_names[[0, 2, 6]]
    
    #apply key on column 6 in df_named and extract column 0 and 2.
    df_names = df_names[df_names[6]=='scientific name'][[0,2]]
    
    #lenth of dataframe in range(.....).
    df_names.index = range(len(df_names))
    
    #merge both DataFrames df_nodes and df_names in new DataFrame df_merge.
    df_merge = pd.DataFrame()
    df_merge = df_nodes.merge(df_names[[0,2]],how = "left",left_on = [0],right_on= [0])
    
    #rename columns of DataFrame df_merge.
    df_merge = df_merge.rename(columns={0:'taxa_ids','2_x':'parent_id',4:'rank','2_y':'scientfic_name'})
    
    #create empty DataFrame df_delnodes and df_merged.
    df_delnodes = pd.DataFrame()
    df_merged = pd.DataFrame()
    #read .dmp files with use of parameters.
    df_delnodes = pd.read_csv(delnodes,delimiter='\t',header=None)
    df_merged = pd.read_csv(merged,delimiter='\t',header=None)
    
    #creat two empty lists taxaid and taxaids assign them with set of df_merge['taxa_ids'] and df_merged[0].
    taxaid = list(set(df_merge['taxa_ids']))
    taxaids = list(set(df_merged[0]))
    
    #print common values in lists.
    print("modified values are",list(set(taxaid) & set(taxaids)))
    

    #convert DataFrame in .csv formate and assign to file_csv .
    file_csv = df_merge.to_csv("final_merge.csv")
    print ("csv file created as final_merge.csv")
    
    #return file_csv
    return file_csv, len(df_merge)




#pass path of .dmp files in parameters.
merge(names = 'taxadmp/names.dmp',nodes = 'taxadmp/nodes.dmp',merged = 'taxadmp/merged.dmp',delnodes = 'taxadmp/delnodes.dmp')
