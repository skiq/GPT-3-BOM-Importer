from six.moves import urllib
import json
import os

# adapted from https://octopart.com/api/v4/getting-started
class GraphQLClient:
    def __init__(self, endpoint):
        self.endpoint = endpoint
        self.token = None
        self.headername = None

    def execute(self, query, variables=None):
        return self._send(query, variables)

    def inject_token(self, token, headername='token'):
        self.token = token
        self.headername = headername

    def _send(self, query, variables):
        data = {'query': query,
                'variables': variables}
        headers = {'Accept': 'application/json',
                   'Content-Type': 'application/json'}

        if self.token is not None:
            headers[self.headername] = '{}'.format(self.token)

        req = urllib.request.Request(self.endpoint, json.dumps(data).encode('utf-8'), headers)

        try:
            response = urllib.request.urlopen(req)
            return response.read().decode('utf-8')
        except urllib.error.HTTPError as e:
            print((e.read()))
            print('')
            raise e

def match_mpns(client, mpns):
    dsl = '''
    query match_mpns($queries: [PartMatchQuery!]!) {
        multi_match(queries: $queries) {
            hits
            reference
            parts {
                manufacturer {
                    name
                }
                mpn
                octopart_url
            }
        }
    }
    '''

    queries = []
    for mpn in mpns:
        queries.append({
            'mpn_or_sku': mpn,
            'start': 0,
            'limit': 10,
            'reference': mpn,
        })
    resp = client.execute(dsl, {'queries': queries})
    return json.loads(resp)['data']['multi_match']


"""
Input: MPN string.

Return:
Null if no match. List of parts with a dictionary each, if it matched.

How to use:

match = match_single_mpn('LMC6482IMX/NOPB')
if match is not None:
    for part in match['parts']:
        print(match['reference'], '\t',match['hits'], '\t', part['manufacturer_name'], '\t', part['mpn'], '\t', part['octopart_url'])
else:
    print("Not found")

reference: provided number
hits: number of parts found
manufacturer_name: part manufacturer name
mpn: Octopart MPN
octopart_url: part URL
"""
def match_single_mpn(mpn):
    client = GraphQLClient('https://octopart.com/api/v4/endpoint')
    # client.inject_token(os.getenv('OCTOPART_TOKEN'))
    client.inject_token("1b4cc2d2-4221-4fc5-852d-ff9d211c1c4c")
    mpns = [mpn]
    matches = match_mpns(client, mpns)
    match = matches[0]

    # print(match)
    if match["hits"] == 0:
        return
    else:
        for part in match['parts']:
            part['manufacturer_name'] = part['manufacturer']['name']
        return match



"""
Input:
Takes a list of mpns as an input (must be strings).

Return:
For each MPN, if there is a match, it returns a list of parts.
If there is no match, it returns an empty list.
For cases where there is no match, it returns a list of parts.
Each part is a dictioary with multiple values.

How to use:

matches = match_multiple_mpn(['LMC6482IMX/NOPB','XYZ6482IMX/NOPB','PCF8583T/F5,112'])

for match in matches:

    # check if there is a part matched
    if len(match) is not 0:
        # if so, get the info from the parts
        for part in match['parts']:
            print(match['reference'], '\t',match['hits'], '\t', part['manufacturer_name'], '\t', part['mpn'], '\t', part['octopart_url'])
    # if len = 0, it means this MPN had no match
    else:
        print("Not found")

reference: provided input MPN
hits: number of parts found
manufacturer_name: part manufacturer name
mpn: true MPN from Octopart
octopart_url: part URL
"""

def match_multiple_mpn(mpns):
    client = GraphQLClient('https://octopart.com/api/v4/endpoint')
    # client.inject_token(os.getenv('OCTOPART_TOKEN'))
    client.inject_token("1b4cc2d2-4221-4fc5-852d-ff9d211c1c4c")
    matches = match_mpns(client, mpns)
    match = matches[0]

    matches_list = []
    for match in matches:
        if match["hits"] == 0:
            matches_list.append([])
        else:
            # standardize naming
            for part in match['parts']:
                part['manufacturer_name'] = part['manufacturer']['name']
            matches_list.append(match)
    return matches_list


if __name__ == '__main__':
    match = match_single_mpn('2N7002PW')
    if match is not None:
        for part in match['parts']:
            print(match['reference'], '\t',match['hits'], '\t', part['manufacturer_name'], '\t', part['mpn'], '\t', part['octopart_url'])
    else:
        print("Not found")
