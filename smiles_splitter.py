mol_frags=["C1=CC=C(CCN2CCCCC2)C=C1", "C1=CC=C(NC2CCNCC2)C=C1", "CC1(CCCC(C1)C)CCCCCC", "CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC", 'c1ccccc1c1cnc(CCCCCC)cc1']

def smile_splitter(smiles_list):
	smile_frag_list = []
	for i in smiles_list:
		if len(i) > 16:																#arbitrarily chose this as teh cutoff for what we consider a long substruture
			n=0
			while n<10:
				dig_ind=[]
				lbrac_ind=[]
				rbrac_ind=[]
				for j, char in enumerate(i):										#finds indecies of digits and brackets
					if char == str(n):
						dig_ind.append(j)
					elif char == '(':
						lbrac_ind.append(j)
					elif char == ')':
						rbrac_ind.append(j)
				smile_frag=''
				lbrac_count=0
				rbrac_count=0
				if len(dig_ind) != 0:												#checks for brackets in ring fragment and counts amount of each
					for j, char in enumerate(i):
						if j >= dig_ind[0]-1 and j <= dig_ind[1]:
							smile_frag = smile_frag + char
							if char == '(':
								lbrac_count += 1
							elif char == ')':
								rbrac_count += 1
				while lbrac_count != rbrac_count:									#if counts of each type of bracket do not match, remove the last occurrence of the left bracket until they do
					rm = smile_frag.rfind('(')
					smile_frag = smile_frag[:rm] + smile_frag[rm  + 1:]
					lbrac_count -= 1
				if lbrac_count != 0:												#if there are still brackets, isolate whatever is inside those brackets as its own fragment
					lb_ind = smile_frag.find('(')
					rb_ind = smile_frag.rfind(')')
					brac = smile_frag[lb_ind+1:rb_ind]
					smile_frag_list.append(brac)
					smile_frag = smile_frag[:lb_ind] + smile_frag[rb_ind+1:]
				n += 1
				if len(smile_frag) != 0:
					smile_frag_list.append(smile_frag)
	if len(smile_frag_list) != 0:													#removes any duplicates and returns the fragment list if it contains anything
		smile_frag_list = list(dict.fromkeys(smile_frag_list))
		return(smile_frag_list)

defragged = smile_splitter(mol_frags)
print(defragged)