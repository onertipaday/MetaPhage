# Coded by Gioele Lazzari (gioele.lazza@studenti.univr.it)
software = "db_manager.py"
version = "0.1.0"

import sys, os, argparse, logging, subprocess



parser = argparse.ArgumentParser(
    description = 'This script is designed to manage all the databases used '
                  'in the MetaPhage nextflow pipeline. This script is intended to be '
                  'placed in MetaPhage/bin.',
    formatter_class = argparse.RawTextHelpFormatter)

options = parser.add_argument_group("Options")

options.add_argument('-v', '--version', action='version', version= software + " v" + version)
# what follow are ALL the parameters passed by nextflow
options.add_argument('-p', '--mod_phix', dest='mod_phix', metavar='STRING', default=None)
options.add_argument('-p1', '--file_phix_alone', dest='file_phix_alone', metavar='PATH', default=None)
options.add_argument('-k', '--mod_kraken2', dest='mod_kraken2', metavar='STRING', default=None)
options.add_argument('-k1', '--file_kraken2_db', dest='file_kraken2_db', metavar='PATH', default=None)



def error(msg):
    sys.stderr.write("ERROR: {}\n".format(msg))
    sys.stderr.flush()
    sys.exit(1)



def manage(projectDir, 
           mod_phix, file_phix_alone,
           mod_kraken2, file_kraken2_db):

    # create a subfolder for containg all the variables
    varDir = projectDir + "bin/groovy_vars/"
    if not os.path.exists(varDir):
        os.makedirs(varDir)
    
    def makeChannel(asset, content):
        # this file is the one actually opened in the process
        f = open(varDir + asset, "w")
        f.write(content)
        f.close()
        # this file in the working dir is just to temporize the process
        f = open(asset, "w")
        f.write(content)
        f.close()


    #################################
    # phix ##########################
    #################################
    rel_path = "db/phix/"
    mod_folder = projectDir + rel_path

    if mod_phix == "custom":
        if file_phix_alone == "-":
            error('With --mod_phix custom you have to specify also --file_phix_alone')
        else:
            makeChannel("file_phix_alone", file_phix_alone)

    elif mod_phix == "phiX174":
        if not os.path.exists(mod_folder + "phiX174.fasta"):
            url = "https://www.ebi.ac.uk/ena/browser/api/fasta/AF176027.1?download=true"
            loggin.info(mod_folder + "phiX174.fasta" + ' absent, downloading it from ' + url + ". Please wait...")
            output = os.popen('wget -O ' + mod_folder + "phiX174.fasta" + ' ' + url) 
        else:
            logging.info(mod_folder + "phiX174.fasta" + ' already present')
        makeChannel("file_phix_alone", "db/phix/phiX174.fasta")

    elif mod_phix == "WA11":
        if not os.path.exists(mod_folder + "WA11.fasta"):
            url = "https://www.ebi.ac.uk/ena/browser/api/fasta/DQ079895.1?download=true"
            loggin.info(mod_folder + "WA11.fasta" + ' absent, downloading it from ' + url + ". Please wait...")
            output = os.popen('wget -O ' + mod_folder + "WA11.fasta" + ' ' + url) 
        else:
            loggin.info(mod_folder + "WA11.fasta" + ' already present')
        makeChannel("file_phix_alone", "db/phix/WA11.fasta")

    
    #################################
    # kraken2 #######################
    #################################
    if mod_kraken2 == "custom":
        if file_kraken2_db == "-":
            error('With --mod_kraken2 custom you have to specify also --file_kraken2_db')
        else:
            makeChannel("file_kraken2_db", file_kraken2_db)
    
    elif mod_kraken2 == "miniBAV":
        rel_path = "db/kraken2/miniBAV/"
        mod_folder = projectDir + rel_path
        if not os.path.exists(mod_folder + "hash.k2d") or not os.path.exists(mod_folder + "opts.k2d") or not os.path.exists(mod_folder + "taxo.k2d"):
            url = "ftp://ftp.ccb.jhu.edu/pub/data/kraken2_dbs/old/minikraken2_v1_8GB_201904.tgz"
            loggin.info(mod_folder + "*" + ' absent, downloading it from ' + url + ". Please wait...")
            output = os.popen('wget -O ' + mod_folder + "archive.tgz" + ' ' + url) 
            logging.info("Decompressing...")
            output = os.popen('tar zxvf %s --directory %s' % (mod_folder + "archive.tgz", mod_folder))
            output = os.popen('mv %s %s' % (mod_folder + "minikraken2_v1_8GB/*", mod_folder))
            output = os.popen('rm -rf %s' % (mod_folder + "minikraken2_v1_8GB"))
            output = os.popen('rm %s' % (mod_folder + "archive.tgz"))
            logging.info("OK")
        else:
            logging.info(mod_folder + "*" + ' already present')
        makeChannel("file_kraken2_db", rel_path)
    
    elif mod_kraken2 == "miniBAVH":
        rel_path = "db/kraken2/miniBAVH/"
        mod_folder = projectDir + rel_path
        if not os.path.exists(mod_folder + "hash.k2d") or not os.path.exists(mod_folder + "opts.k2d") or not os.path.exists(mod_folder + "taxo.k2d"):
            url = "ftp://ftp.ccb.jhu.edu/pub/data/kraken2_dbs/old/minikraken2_v2_8GB_201904.tgz"
            loggin.info(mod_folder + "*" + ' absent, downloading it from ' + url + ". Please wait...")
            output = os.popen('wget -O ' + mod_folder + "archive.tgz" + ' ' + url) 
            logging.info("Decompressing...")
            output = os.popen('tar zxvf %s --directory %s' % (mod_folder + "archive.tgz", mod_folder))
            output = os.popen('mv %s %s' % (mod_folder + "minikraken2_v2_8GB/*", mod_folder))
            output = os.popen('rm -rf %s' % (mod_folder + "minikraken2_v2_8GB"))
            output = os.popen('rm %s' % (mod_folder + "archive.tgz"))
            logging.info("OK")
        else:
            logging.info(mod_folder + "*" + ' already present')
        makeChannel("file_kraken2_db", rel_path)




if __name__ == "__main__":

    parameters = parser.parse_args()

    # create the .log file
    logging.basicConfig(filename ="./db_manager.log", filemode='w', level = logging.INFO, # level sets the threshold
                        format = '%(asctime)s %(levelname)s: %(message)s',
                        datefmt = '%H:%M:%S') 
    logging.info('Processing of databases is started.\n')

    # understand project directory
    projectDir = os.path.realpath(__file__).replace("bin/db_manager.py", "")
    logging.info("projectDir: " + projectDir + "\n")

    # core function
    manage(projectDir, 
           parameters.mod_phix, parameters.file_phix_alone,
           parameters.mod_kraken2, parameters.file_kraken2_db)

    
