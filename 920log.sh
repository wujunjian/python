#!/bin/bash

key=920
outdir=/data/appdatas/cloud/logs/$key/

mkdir -p $outdir

lasthour=`date -d"1 hour ago" +'%H'`
lastday=`date -d"1 hour ago" +'%Y%m%d'`
lastdayhour=`date -d"1 hour ago" +'%Y-%m-%d/%H'`

file="/data/appdatas/cloud/logs/$lastdayhour/*.gz.done"

#echo $file
outfile=$outdir`hostname`_$lastday$lasthour
zcat $file | grep cno=$key > $outfile
rm -rf $outfile.gz
gzip $outfile


#ftp

# func_ftp host user password cmd1 [cmd2]
func_ftp()
{
    test $# -lt 4 && return 1

    /usr/bin/ftp -inv << END
        open $1 $FTPPORT
        user $2 $3
	passive
        binary
        $4
        $5
        bye
END
    return $?
}

FTPPORT=21
# func_lftp host user password cmd[s]
func_lftp()
{

    test $# -ne 4 && return 1

    ftmp=`/bin/mktemp`
    /bin/cat > $ftmp << END
        debug 4
        open -p $FTPPORT ftp://$1
        user $2 "$3"
        set net:timeout 10
        set net:max-retries 6
        set net:reconnect-interval-base 5
        set net:reconnect-interval-multiplier 1
        $4
        bye
END
    /usr/bin/lftp -f $ftmp
    /bin/rm -f $ftmp

    return $?
}

func_lftp 221.228.204.76 qmon 05astIRT "put $outfile.gz"

rm -rf $outfile.gz

