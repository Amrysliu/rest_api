import requests

class MediumType:
    def __init__(self, host, flavor, arch):
        self.host = host
        self.flavor = flavor
        self.arch = arch
        
    def getAllMediumType(self):
        url = self.host + "/api/v1/products"
        resp = requests.get(url, verify=False)
        if resp.status_code != 200:
            result = resp.json()
            return result["error"]
        product_data = resp.json()
        self.product = product_data["Products"]

    def findMediumTypeIDs(self):
        self.getAllMediumType()
        arch_array = self.arch.split(",")
        dic_flavor = {}
        for one in arch_array:
            key = self.flavor + "-" + one
            dic_flavor[key] = 0
        
        for p in self.product:
            product_name = p["distri"] + "-" + p["version"] + "-" + p["flavor"] + "-" + p["arch"]
            if product_name in dic_flavor :
                dic_flavor[product_name] = p["id"]

        not_found_flavor = ''
        for k in dic_flavor.keys():
            if dic_flavor[k] == 0:
                not_found_flavor = not_found_flavor + k + " "
        if not_found_flavor != '':
            return "Did not found those Medium Types: " + not_found_flavor, {}
        
        return '', dic_flavor 
