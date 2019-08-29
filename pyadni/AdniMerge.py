import mechanize
import http.cookiejar
import subprocess
import pandas as pd
import re
import os
import sys

DEBUG = True
ADNI_LOGIN_URL = "https://ida.loni.usc.edu/login.jsp?project=ADNI&page=HOME"
ADNI_BASE_DL_URL = "https://utilities.loni.usc.edu/download/study?type=GET_FILES"
ADNIMERGE_FILE_ID = "311"

class AdniMerge(object):
        
    def __init__(self, csv_data_folder = "./data/"):
        self.csv_data_folder = os.getcwd() + '/' + csv_data_folder
        self.tables, self.empty = self.get_tables()
        
        if(self.empty):
            print("[INFO]: You don't have data")
        
    def get_tables(self):
        """ Return (tables, empty) """
        tables = []
        
        if(not(os.path.isdir(self.csv_data_folder))):
            print("[ERROR]: Please, update tables!")
            return (tables, True)
        
        for root, dirs, files in os.walk(self.csv_data_folder):
            for file in files:
                if file.endswith('.csv'):
                    tables.append(file)
                    
        if len(tables) == 0:
            if DEBUG:
                print("[ERROR]: Please, update tables!")
            return (tables, True)
        
        return (tables, False)
        
    def update_from_file(self, tar_path, r_script_path = "./rdata2csv.r", output_path = "./data/"):
        
        if(not(os.path.isfile(tar_path))):
            print("[ERROR]: tar.gz file does not exists!")
            return False

        base = os.getcwd() + '/'
        cmd = "Rscript --vanilla %s --%s --%s" % (base + r_script_path, tar_path, base + output_path)
        print(cmd)
        proc = subprocess.Popen(cmd,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                shell=True,
                                universal_newlines=True)
        std_out, std_err = proc.communicate()   
        
        if proc.returncode == 0:
            print("[INFO]: Update Complete!")
            return True
        
        elif proc.returncode == 1:
            print("[ERROR]: While updating")
            return False
    
        return False
    
    def update_from_adni(self, user_email, user_password, r_script_path = "./rdata2csv.r", output_path = "./data/"):              
        browser = mechanize.Browser()
        cj = http.cookiejar.LWPCookieJar()
        browser.set_handle_robots(False)
        browser.set_handle_equiv(True)
        browser.set_handle_referer(True)
        browser.set_handle_redirect(True)
        browser.set_cookiejar(cj)
        browser.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
        
        # User Agent
        k = ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36')
        
        # Add User Agent In Header
        browser.addheaders = [('User-agent', k)]
        
        browser.open(ADNI_LOGIN_URL)
        
        # Now Login Page Is Ready
        try:
            browser._factory.is_html = True
        except:
            print("[ERROR]: While downloading, verify your connection")
            return False
        
        # Select Form By Index
        browser.select_form(nr=0)
        browser.form['userEmail'] = user_email
        browser.form['userPassword'] = user_password
        browser.submit()
        
        try:
            x = browser.find_link("Study Data")
            browser.follow_link(x)

            html = browser.response().read().decode()

            # Find authKey and userId so mechanize can download files
            authKey = re.findall('authKey\=(.+?)"', html)[0]
            userId = re.findall('userId\=(.+?)"', html)[0]
        except:
            print("[ERROR]: While downloading, verify your credentials")
            return False
        
        url_download = ADNI_BASE_DL_URL
        url_download += "&userId=" + userId
        url_download += "&authKey=" + authKey
        url_download += "&fileId=" + ADNIMERGE_FILE_ID
        
        filename = 'ADNIMERGE.tar.gz'
        
        if DEBUG:
            print("[INFO]: Downloading ADNIMERGE.tar.gz (~70mb)")
            
        try:
            browser.retrieve(url_download, 'ADNIMERGE.tar.gz')[0]
        except:
            print("[ERROR]: While downloading, verify your connection")
            return False
        
        if(not (self.update_from_file(filename))):
            print("[ERROR]: While extracting... Deleting temporary files")
            os.remove(filename)
            return False
        
        os.remove(filename)
        
        if DEBUG:
            print("[INFO]: Your database is update!")
            
        return True
    
    def get_table_names(self):
        tables, result = self.get_tables()
        tables_dict = {}
        
        for table_name in tables:
            table_name = table_name.replace('.csv', '')
            table_path = ('%s%s.csv') % (self.csv_data_folder, table_name)
            tables_dict[table_name] = table_path
        
        return dict(sorted(tables_dict.items()))
        
    def get_table(self, table_name):
        table_path = ('%s/%s.csv') % (self.csv_data_folder, table_name)
        return pd.read_csv(table_path)
