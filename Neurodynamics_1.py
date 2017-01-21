import os, shutil, glob, re, fnmatch
from subprocess import call
import pandas as pd
import collections
from collections import defaultdict

class HBNL:
    
    def neuro_transfer(self, src, trg):
        """Given a full path, moves new neuropsych folders to correct folder in /raw_data/neuropsych/site_name
        src = full path of where new neuropsych folders are
        trg = neuropsych site directory"""
        
        self.src = src
        self.trg = trg
        for roots, subFolders, files in os.walk(src):
            for file in files:
                subFolder = os.path.join(trg, file[:8])
                if not os.path.isdir(subFolder):
                    os.makedirs(subFolder)
                    print('making new dir...' + subFolder)
                shutil.copy(os.path.join(roots, file), subFolder)
                print ('copying ' + file  + ' to '+ subFolder)
        return True

    def sync_error(self, ev2_path, dat_path):
        """Provide file pathway of event file and dat file and function will return corrected event file.
           If ev2 file is missing an entire event then program will stop"""
        
        self.ev2_path = ev2_path
        self.dat_path = dat_path

        #read event file as df and assign column names  
        df = pd.read_csv(ev2_path, header=None, delim_whitespace=True)
        df.columns = ['trial','type','stim1', 'stim2', 'stim3', 'latency']

        #create 2 df's and sort non_zero df to compare to dat file
        non_zero_ev2= df.loc[df['type'] > 0]
        zero_ev2= df.loc[df['type'] < 0.9] 
        non_zero_ev2.sort('trial', ascending=True, inplace=True) 

        #read dat file as df & assign column names
        lst = []
        with open(dat_path, 'r') as f:
            for line in f.readlines()[21:]:
                lst.append(line.split())
                df_dat = pd.DataFrame(lst)
                df_dat.columns=['trial','resp','type', 'correct', 'latency', 'stim']

        #if ev2 is totally missing an event then exit function 
        if len(non_zero_ev2) != len(df_dat):
            print('ev2 file is', len(non_zero_ev2), 'lines long', '\n', 
                  'dat file is', len(df_dat), 'lines long', '\n',
                  'dat file is', len(df_dat) - len(non_zero_ev2), 'line longer than event file')
            sys.exit()
            
        #replace type/stim codes column in ev2 file with stim codes column in dat file     
        non_zero_ev2['type'] = df_dat['type'].values
        
        #add 0's and overwrite ev2 file
        frames = [zero_ev2, non_zero_ev2]
        new_ev2_df = pd.concat(frames)
        new_ev2_df.to_csv(ev2_path ,sep = " ", index=False, header=False)

        return True   
    

    def xml_to_df(self, path):
        """Given a full path to neuropsych sub folders, returns data frame of first 6 lines of xml file"""
        
        self.path=path
        xml = [os.path.join(root,name) for root,dirs,files in os.walk(path) for name in files if name.endswith(".xml")]

        ids_lst=[]
        dob_lst = []
        gen_lst=[]
        test_lst =[]
        ses_lst=[]
        han_lst=[]
        for i in xml:
            with open(i) as f:
                for line in f:
                    if line.startswith('  <Sub'):
                        ids_lst.extend(re.findall(r'<SubjectID>(.*?)</SubjectID>', line))
                    if line.startswith('  <DOB'):
                        dob_lst.extend(re.findall(r'<DOB>(.*?)</DOB>', line))
                    if line.startswith('  <Gen'):
                        gen_lst.extend(re.findall(r'<Gender>(.*?)</Gender>', line))
                    if line.startswith('  <Test'):
                        test_lst.extend(re.findall(r'<TestDate>(.*?)</TestDate>', line))
                    if line.startswith('  <Sess'):
                        ses_lst.extend(re.findall(r'<SessionCode>(.*?)</SessionCode>', line))
                    if line.startswith('  <Hand'):
                        han_lst.extend(re.findall(r'<Hand>(.*?)</Hand>', line))

        data_set = pd.DataFrame(ids_lst, columns=["Subject ID"])
        data_set['Test_Date'] = test_lst
        data_set['DOB'] = dob_lst
        data_set['Gender'] = gen_lst
        data_set['Handedness'] = han_lst
        data_set['Run Letter'] = ses_lst

        data_set['Test_Date'] =pd.to_datetime(data_set.Test_Date)
        table = data_set.sort_values('Test_Date', ascending=True)
        print("sorting by test date...")
        return table
    
    #can be broken down into 3-4 smaller methods 
    def cnt_to_h1(self, dir_stem, exp_names, src):
        """Search a ns folder for cnt files of tasks used for peak picking, copies cnts to folders named after tasks, converts to avg.h1
        dir_stem = full path of where you want .avg.h1 files
        exp_names = list of experiment names
        src = full path of ns folder"""
        
        self.dir_stem = dir_stem
        self.exp_names = exp_names
        self.src = src
        
        #create directories based on experiment names
        for exp in exp_names:
            new_dirs = os.path.join(dir_stem, exp)
            if not os.path.exists(new_dirs):
                os.makedirs(new_dirs)
                print("creating " + new_dirs)
            else:
                print(new_dirs + " already there")
                
        #copy cnt file to appropriate directory
        for roots, dirs, files in os.walk(src):
            for name in files:
                if name.endswith("orig.cnt"):
                    pass
                elif name.startswith(exp_names[0]) and name.endswith(".cnt"):
                    shutil.copy(os.path.abspath(roots + '/' + name), os.path.join(dir_stem, exp_names[0]))
                elif name.startswith(exp_names[1]) and name.endswith(".cnt"):
                    shutil.copy(os.path.abspath(roots + '/' + name), os.path.join(dir_stem, exp_names[1]))
                elif name.startswith(exp_names[2]) and name.endswith(".cnt"):
                    shutil.copy(os.path.abspath(roots + '/' + name), os.path.join(dir_stem, exp_names[2]))

        #create cnt.h1 
        for path, subdirs, files in os.walk(dir_stem):
            for name in files:
                if name.endswith(".cnt"):
                    subprocess.call("create_cnthdf1_from_cntneuroX.sh {}".format(name), shell=True, cwd=path)
                    print("creating new file for... " + name)
                    
        #create avg.h1
        for path, subdirs, files in os.walk(dir_stem):
            for name in files:    
                if name.startswith("ant") and name.endswith("_cnt.h1"):
                    os.chdir(os.path.join(path))
                    call("create_avghdf1_from_cnthdf1X -lpfilter 8 -hpfilter 0.03 -thresh 75 -baseline_times -125 0 *_cnt.h1", shell=True)
                    print("creating avg.h1 for " + name)
                elif name.startswith(("aod", "vp3")) and name.endswith("_cnt.h1"):
                    os.chdir(os.path.join(path))
                    call("create_avghdf1_from_cnthdf1X -lpfilter 16 -hpfilter 0.03 -thresh 75 -baseline_times -125 0 *_cnt.h1", shell=True)
                    print("creating avg.h1 for " +name)
                    
        #remove unecessary files 
        for path, subdirs, files in os.walk(dir_stem):
            for name in files:
                if name.endswith((".cnt", "_cnt.h1")):
                    os.remove(os.path.join(path + '/' + name))
                    print("removing... " + name)
        return True
    

    def ext_count(self, filepath):
        """counts number of different file extetnsions for each experiment and returns the missing experiments for a given
            file extension"""
        
        self.filepath = filepath 

        #can probably turn into dictionary...
        dat_names = ['vp3', 'cpt', 'ern', 'ant', 'aod', 'ans', 'stp', 'gng']
        cnt_names = ['eeo', 'eec', 'vp3', 'cpt', 'ern', 'ant', 'aod', 'ans', 'stp', 'gng']
        ps_names = ['vp3', 'cpt', 'ern', 'ant', 'aod', 'anr', 'stp', 'gng']
        avg_dict = {'vp3': '3',
                    'gng': '2',
                    'ern': '4',
                    'stp': '2',
                    'ant': '4',
                    'cpt': '6',
                    'aod': '2',
                    'anr': '2'}
        avg_od = collections.OrderedDict(sorted(avg_dict.items()))

        #count of each type of file extension 
        avg_lst = []
        cnt_lst = []
        cnt_rr = []
        dat_lst = []
        ps_lst = []
        for root, dirs, files in os.walk(filepath):
            for name in files:
                if name.endswith("avg"):
                    avg_lst.append(name.split("_")[0])
                if name.endswith("_32.cnt"):
                    cnt_lst.append(name.split("_")[0])
                if name.endswith("dat"):
                    dat_lst.append(name.split("_")[0])
                if name.endswith("ps"):
                    ps_lst.append(name.split("_")[0])
                if name.endswith("_rr.cnt"):
                    cnt_rr.append(name.split("_")[0])
                
                    
        print("File extension Count:", '\n',
             len(avg_lst), '.avg files', '\n',
             len(cnt_lst), '.cnt files', '\n',
             len(dat_lst), '.dat files', '\n',
             len(ps_lst), '.ps files', '\n',
             len(cnt_rr), 're-runs', '(',str(cnt_rr).strip("[]"),')')
        
        print ('Missing dat files =', ','.join(set(dat_names).difference(dat_lst)))
        print ('Missing cnt files =', ','.join(set(cnt_names).difference(cnt_lst)))
        print ('Missing ps files =', ','.join(set(ps_names).difference(ps_lst)))

        #count frequency of each task with .avg extension 
        fq= defaultdict(int)
        for w in avg_lst:
            fq[w] += 1

        fq_od = collections.OrderedDict(sorted(fq.items()))

         
        for key in avg_od:
            if key not in fq_od:
                print('Missing avg files = ', key)
                #print(key,avg_dict[key])
        return True
                
                
    def tracker_by_site(self, filepath, neuro_or_erp):
        """given a file that contains ALL tracker files for neuro or ERP in a certain month -- will
        separate text files based on site number"""
        
        self.filepath = filepath
        self.neuro_or_erp = neuro_or_erp

        with open(filepath,'r') as f:
            entries = map(str.strip,f.readlines())

        entries = sorted([entry.split() for entry in entries], key = lambda k: k[1])

        for entry in entries:
            ID = entry[1][0]
            with open(neuro_or_erp.format(ID),'a') as f:
                f.write(' '.join(entry) + '\n')
        return True

hbnl = HBNL()