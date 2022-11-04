import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from concurrent.futures import ThreadPoolExecutor



class Upmsp:
    def __init__(self) -> None:
        self.districtCodes = []
        self.schoolCodes = []
        self.schoolData = []
    
    def getDistrictCodes(self):
        response = requests.get('https://upmsp.edu.in/SchoolInformationSearchUPB.aspx')
        soup = BeautifulSoup(response.content, 'lxml')
        districtCodes = [i['value'] for i in soup.find('option', string='Select District').find_next_siblings('option')]
        self.districtCodes = districtCodes
        print(f'{len(districtCodes)} Districts found.')

    def getSchoolCodes(self, districtCode):
        try:
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
            }

            data = f'ctl00%24ScriptManagerUPMSP=ctl00%24cphBody%24UpdatePanel1%7Cctl00%24cphBody%24ddl_districtCode&__EVENTTARGET=ctl00%24cphBody%24ddl_districtCode&__EVENTARGUMENT=&__LASTFOCUS=&__VIEWSTATE=VPo%2FcwnyYqUtd9tCZ5gjsVlav8J6QO6N98evqYG2cVaR7OVtJNJ8kLiKMWm80X6KgoDZp7HAEIF8DMSW8cIfXZF8XBnQdlIkBcYd68gYnzq4kr1ETl%2Bi2AYPYEXQmQttSbOz6dXk7sC%2FLwsXqkDotSjC%2FT5vHGJgLsVkyk884fHVXUZ2SyXGk%2FgvhhYW5agDnfG3tyTwrtfMcF1kWZ18qg%3D%3D&__VIEWSTATEGENERATOR=AA1900B4&__VIEWSTATEENCRYPTED=&__EVENTVALIDATION=yTSetXpHMJaZ6Su7BPchIVPTDC%2B9s5Ul3cz7Z%2Fwncz8DcVrR%2FRAbFEcuMTW5svDAM0i10nnfm%2Bviz1GdYwdD4XyY3n66jbKspyD6PHePnSZ6R4zmcw2oCzJZbo0%2Fgw9Z8THzonF2VOvUBCew7TPy65Q2iWJYeOjegXEx4KkI%2FaKR%2BdErgl0xPg4XA%2B1u4jX5lpqUygFmqKKJO7Lq4FH1sgzfhCAdmZ%2FYLjHJ9QCu5biJqe3Px09Xrs52dNyvWbzh%2BvoWjjkkE7oi8AyheLUXqwRhPFGh4AYfkms7y5sSop%2Fpz4cPa50q6ibFjqQiVHwDi0fTF1%2Bk0SU649cvqCkzlByt2VsNr3nxB1mo5Twrx7I9aj6DJJ0NWcFhKyf6LudVQF2W6IHoQ7XT7SA33rAfr9IGFpLkIGBNbW%2BP%2FxrR%2BERbdqmi%2F65%2BPUnvykMYiw30fHLHh2mOka4vcz2pnhIYcP981Z4KOu%2Bi4TMBLc29I4c2vvqG%2F0PTvZYMkDFsCzB9GY4JD63c4%2BZpUyPHsYXkWGvKJTddpEr7n03db781ag5QICgJ5WZYxgs5RJtC3zHpPfDrvK%2F33hB%2F1qId8bZdWSTRXeBSbRktoNUnW33EXm60tWZrKBlBsUW02DTp2a1cPXtcrmrEW0YdLDqfSINqJWRybKajH%2BSlZtecquZb8dn7UVCSEBQYth0OyoWve%2FzkNBp%2FZ2JG7iCaeEqC6v4IVxxJO0NJ4pG6Zjqy528GURorKMeObsqlJsYcImuKLemtVn3g%2Fzffg7Ql%2FaRxl2LXj0zgcXEUBY%2BtyKMFJYUvi075zMUa6d2QJfyNhpw%2BBFTCIIulEmCuOZxflHEMF9JmjepwuWxxx6J5IfDHttVykj%2FkM72pY%2B1t3dpNxK1pbYApPjSTGSSDILQ6BCV7kASHhp7BSSjEmlSvKClDvrHaM49tjs9eVY38jTRCPxW%2BZIWqu%2FzwkNZ4YofRNRF3VvlcRejmKfpbCIfIshZubjbu2dMXWbvVRLLqmk9TLNQGlr0%2FibNAsinShVT80e0%2FcmdTfoBpaIrmiyMAWqs%2BgvQPAz%2FhM4zOLGXy5NMPHUhb5%2FAVGo3TYXltTdohWfpZJUIR1as4YniqyRoNrvEFoMTT9%2FbtLbxn5tLbRnHZ7ZCozX67Y7gpwBvIjKYMM3OeSy4OfI9mb9fL5KfRBR95ypJwcGvdgFK0Qa4Wq4jAwkhWfq78Y7CSiPX3v2ZB%2FdJrCQlwM57WYEFU0JfTB3ilMb7s0l0uKVkp6T4C6g0hgXKElEW8rhJg16EfJYA3c3xkLwtDAy%2FJ7sAqdA%2BFPqjOIUR9PxpRWHxzvBdTgIa7palR6BHUh2VMysUB06cTqPEz6XK8zvARtNA1RcUfY0hMp5dqSNsnwkZ1NaQOTj%2BZBu2oCEdNaw3aln4l5qv4FyPgk8ONF1Sp0Reg3ufmnWHzaHXrpm%2BS2YO36jZV41EZagqhc%2FpEkZRy8U7G%2FggnR%2BDuHt2nOhr1CRqw6ThKJjHma1NotJ3eTO9xAvsJb3XWqHBHB0NmYokrb1%2BCwGNbtt2TcAmhFSaL2GYU3O7twre2i1MB4d79hStzPQj%2FKSvZGNbMcFkLP%2FwELiUB8nwg1VpQQCQbtx4Wq2iTzgFIViVMOvzmMoi2mleX0LX78p5sWD8Lex0GoljvTQjoy1jj0vF6RiEnJcMnwTKKIId7CJ9yHQrOSjwsNT9ZMOjLCxg%2F6o7EeRLsEURS9d%2FjXhFAKLtVcp73unBN%2BJeoXOZy9xYYvD%2F7GYYFVafeVpp3M7KCF31C%2FVEzFB0HBvj%2F6KlKsr0dRK7Ce2CehwPVnTeed63IUzz1w4STbXyajMFA6VqrLvRaWJP0HLdsbKUsPC9EgXb45Vib1deUz1Mr1S%2FcmCJk%2BG2aKSGO08PdCUtHFkXqPkS%2F8ogx&ctl00%24cphBody%24ddl_districtCode={districtCode}&ctl00%24cphBody%24ddl_Tehsil=&ctl00%24cphBody%24ddl_Block=&ctl00%24cphBody%24ddl_SchoolType=&ctl00%24cphBody%24ddl_vc_SchoolName=&__ASYNCPOST=true&'
            response = requests.post('https://upmsp.edu.in/SchoolInformationSearchUPB.aspx', data=data, headers=headers)
            soup = BeautifulSoup(response.content, 'lxml')
            schoolCodes = [i['value'] for i in soup.find('select', {'id':'ctl00_cphBody_ddl_vc_SchoolName'}).find('option', string='Select School').find_next_siblings('option')]
            self.schoolCodes.extend(schoolCodes)
            print(f'{len(schoolCodes)} Schools in District code : {districtCode} found.')
        except Exception as e:
            print(e)

    def getSchoolData(self, schoolCode):
        try:
            params = {
                'Code': f'{schoolCode}',
            }

            response = requests.get('https://upmsp.edu.in/SchoolWebSite/SchoolInformation.aspx', params=params)
            soup = BeautifulSoup(response.content, 'lxml')
            dfs = pd.read_html(soup.prettify())
            schoolData = list(dfs[3].set_index([0]).fillna('').to_dict().values())[0]
            schoolData['विद्यालय का नाम (हिन्दी में)'] = ' '.join(re.findall('[\u0900-\u097F]+', schoolData['विद्यालय का नाम (हिन्दी में)']))
            self.schoolData.append(schoolData)
            print(f'Got school data for School code : {schoolCode}')
        except Exception as e:
            print(e)

    def writeXl(self):
        df = pd.DataFrame.from_dict(self.schoolData)
        df.to_excel('upmsp_output.xlsx')

    def main(self):
        self.getDistrictCodes()

        with ThreadPoolExecutor(max_workers=200) as executor:
            executor.map(self.getSchoolCodes, self.districtCodes)

        with ThreadPoolExecutor(max_workers=500) as executor:
            executor.map(self.getSchoolData, self.schoolCodes)

        self.writeXl()


if __name__ == '__main__':
    obj = Upmsp()
    obj.main()
