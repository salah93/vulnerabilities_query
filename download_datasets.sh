wget -O zipfiles/2018.zip https://nvd.nist.gov/feeds/json/cve/1.0/nvdcve-1.0-2018.json.zip
wget -O zipfiles/2017.zip https://nvd.nist.gov/feeds/json/cve/1.0/nvdcve-1.0-2017.json.zip
wget -O zipfiles/2016.zip https://nvd.nist.gov/feeds/json/cve/1.0/nvdcve-1.0-2016.json.zip
wget -O zipfiles/2015.zip https://nvd.nist.gov/feeds/json/cve/1.0/nvdcve-1.0-2015.json.zip
wget -O zipfiles/2014.zip https://nvd.nist.gov/feeds/json/cve/1.0/nvdcve-1.0-2014.json.zip
wget -O zipfiles/2013.zip https://nvd.nist.gov/feeds/json/cve/1.0/nvdcve-1.0-2013.json.zip
wget -O zipfiles/2012.zip https://nvd.nist.gov/feeds/json/cve/1.0/nvdcve-1.0-2012.json.zip
wget -O zipfiles/2011.zip https://nvd.nist.gov/feeds/json/cve/1.0/nvdcve-1.0-2011.json.zip
wget -O zipfiles/2010.zip https://nvd.nist.gov/feeds/json/cve/1.0/nvdcve-1.0-2010.json.zip
wget -O zipfiles/2009.zip https://nvd.nist.gov/feeds/json/cve/1.0/nvdcve-1.0-2009.json.zip
wget -O zipfiles/2008.zip https://nvd.nist.gov/feeds/json/cve/1.0/nvdcve-1.0-2008.json.zip
wget -O zipfiles/2007.zip https://nvd.nist.gov/feeds/json/cve/1.0/nvdcve-1.0-2007.json.zip
wget -O zipfiles/2006.zip https://nvd.nist.gov/feeds/json/cve/1.0/nvdcve-1.0-2006.json.zip
wget -O zipfiles/2005.zip https://nvd.nist.gov/feeds/json/cve/1.0/nvdcve-1.0-2005.json.zip
wget -O zipfiles/2004.zip https://nvd.nist.gov/feeds/json/cve/1.0/nvdcve-1.0-2004.json.zip
wget -O zipfiles/2003.zip https://nvd.nist.gov/feeds/json/cve/1.0/nvdcve-1.0-2003.json.zip
wget -O zipfiles/2002.zip https://nvd.nist.gov/feeds/json/cve/1.0/nvdcve-1.0-2002.json.zip

for f in `ls zipfiles/*zip`
do
    unzip -d datasets/ $f
done
