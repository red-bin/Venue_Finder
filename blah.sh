mkdir yelp
for url in `cat hosts.txt | sort | uniq` ; do 
    business=`echo $url | awk -F'/' '{ print $NF}'`
    bdir="/tmp/yelp/${business}" 
    echo "Processing ${business}..."
    mkdir ${bdir} 2>/dev/null && rm -rf ${bdir} && mkdir ${bdir}
    pushd $bdir
    wget $url
    popd
    sleep 1.5
done
