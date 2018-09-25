def create_kmer(fileName,k):
        
    ## @title : Create kmer from a gzip fasta file
        
    import re
    import gzip
    from Bio import SeqIO
        
    reverse_records = []
    records = []
        
    with gzip.open(fileName, "rt") as handle:
        for record in SeqIO.parse(handle, "fasta"):
            reverse = re.sub('[^GATC]', "", str(record.seq.reverse_complement()).upper())
            reverse_records.append(reverse)
            sequence = re.sub('[^GATC]', "", str(record.seq).upper())
            records.append(sequence)
    all_records = records + reverse_records
    dna_kmer=[]
    for dna in all_records:
        if len(dna)>=100:
            for i in range(len(dna)-k+1):
                dna_kmer.append(dna[i:i+k])
        else:
            print ('Tiny Genome')
    return dna_kmer


    
