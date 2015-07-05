#!/usr/bin/gawk -We
#
# $Id: scan-delta-podcasts.awk,v 0.2 2015/06/30 01:50:14 kc4zvw Exp kc4zvw $

BEGIN {
	RS=""
	FS="\n"
	OFS="|"
}

/^[[:space:]]*#/ {next} 

{
	for (i = 1; i <= 10; i++)
		sub(/[^:]*:[[:space:]]*/, "", $i);

	for (i = 11; i < NF; i++) {
		sub(/^[[:space:]]*/, "", $i);

		$10=$10 " " $i;
		$i="";
	}

	NF=10;
	print
}


END {
	# stuff
}

# End of script
