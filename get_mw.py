import sys
import subprocess
import pkg_resources
import json
import requests

required = {'pandas', 'openpyxl'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed

if missing:
    python = sys.executable
    subprocess.check_call([python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)

import pandas as pd

plist = [
    'Title', 'IUPACName', 'MolecularFormula', 'Charge', 'MolecularWeight', 
    'AtomStereoCount', 'BondStereoCount', 'CanonicalSMILES', 'IsomericSMILES', 
    'InChI', 'InChIKey', 'XLogP', 'ExactMass', 'MonoisotopicMass', 'TPSA', 
    'Complexity', 'HBondDonorCount', 'HBondAcceptorCount', 'RotatableBondCount', 
    'HeavyAtomCount', 'IsotopeAtomCount', 'DefinedAtomStereoCount', 
    'UndefinedAtomStereoCount', 'BondStereoCount', 'DefinedBondStereoCount', 
    'UndefinedBondStereoCount', 'CovalentUnitCount', 'PatentCount', 
    'PatentFamilyCount', 'LiteratureCount', 'Volume3D', 'XStericQuadrupole3D', 
    'YStericQuadrupole3D', 'ZStericQuadrupole3D', 'FeatureCount3D', 
    'FeatureAcceptorCount3D', 'FeatureDonorCount3D', 'FeatureAnionCount3D', 
    'FeatureCationCount3D', 'FeatureRingCount3D', 'FeatureHydrophobeCount3D', 
    'ConformerModelRMSD3D', 'EffectiveRotorCount3D', 'ConformerCount3D', 
    'Fingerprint2D'
]
properties = ",".join(plist)

file=input("Enter filename (include file extension): ")
ex_df=pd.read_excel(file)
df=pd.DataFrame()
df['CID']=ex_df.iloc[1:,0]
df['Input_Molecule_Name']=ex_df.iloc[1:,1]
#cid=['1234','3345','8079']
#cid='3345'

def fetch_data(cid):
    """Fetches data for a single CID and returns it as a dictionary."""
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/property/{properties}/json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data["PropertyTable"]["Properties"][0]
    except requests.exceptions.HTTPError as err:
        if response.status_code == 429:  # Too Many Requests
            print("Rate limit hit. Pausing...")
            sleep(60)  # Wait 1 minute before retrying
        else:
            print(f"HTTP error for CID {cid}: {err}")
    except KeyError:
        print(f"Key missing in JSON response for CID {cid}")
    except Exception as e:
        print(f"An error occurred for CID {cid}: {e}")
    return None

def get_mw(input_cid):
    fingerprint=fetch_data(input_cid)
    df=pd.DataFrame(fingerprint,index=[0])
    mw=df.at[0,'MolecularWeight']
    return mw

molw_l=[]
n=0
for i in df['CID']:
    n += 1
    print(f'{n}: ' + f'Pulling the molecular weight for compound CID "{i}".')
    molw=get_mw(i)
    molw_l.append(molw)

df['MolWeight']=molw_l
df.to_excel('output.xlsx')
print('Data has been written to "output.xlsx"')
