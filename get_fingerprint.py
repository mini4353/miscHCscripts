import json
import requests
import pandas as pd
import base64

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

cid=input("Enter CID: ")

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

fingerprint=fetch_data(cid)
df=pd.DataFrame(fingerprint,index=[0])
fp64=df.at[0,'Fingerprint2D']

fp64=fp64.encode("ascii")

fp = base64.decodebytes(fp64)
txt="".join(["{:08b}".format(x) for x in fp])
#print(txt)

#separator = "\n"
#res = "" 
#for i in range(0, len(txt), 8): 
#    res += txt[i:i + 8] + separator

#print(res)

filename = cid+".txt"
with open(filename,"w") as f:
	f.write(txt)
	f.write("\n\n" + df.at[0,'Fingerprint2D'])

print(f"Chemical fingerprint has been written to {filename}")
