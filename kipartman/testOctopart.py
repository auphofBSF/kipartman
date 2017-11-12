#import rest
#import BSFE-kipartman
#from kipartman.octopart.extractor  import OctopartExtractor
#from kipartman.octopart.queries import PartsQuery
#import octopart as octopart
#from ..octopart.models import Models
from octopart.queries import PartsQuery
#import kipartman.octopart.queries.PartsQuery
#from kipartman.octopart import queries
#import octopart.models




searchpart='2N2222'
if searchpart!='':
    q = PartsQuery()
    q.get(searchpart)
    data = q.results()
else:
    data = []
print data