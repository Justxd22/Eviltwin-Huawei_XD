#!/system/bin/sh

OLDSUB='192.168.43'
NEWSUB='200.200.200'
INTRF='wlan0'
LOCTBL=97

export PATH=/system/bin

ip route del ${OLDSUB}.0/24 dev ${INTRF} table $LOCTBL
ip route add ${NEWSUB}.0/24 dev ${INTRF} table $LOCTBL

ip address add ${NEWSUB}.1/24 dev ${INTRF}

#set -- $(busybox printf '%s' "$*" | busybox sed 's/'"${OLDSUB}"'/'"${NEWSUB}"'/g')
unset OLDSUB NEWSUB INTRF LOCTBL

echo $* > /data/misc/wifi/logs
exec dnsmasq.bin -d --no-resolv --no-poll --dhcp-range=192.168.42.2,192.168.42.254,1h --dhcp-range=200.200.200.2,200.200.200.254,8h --dhcp-range=192.168.44.2,192.168.44.254,1h --dhcp-range=192.168.45.2,192.168.45.254,1h --dhcp-range=192.168.46.2,192.168.46.254,1h --dhcp-range=192.168.47.2,192.168.47.254,1h --dhcp-range=192.168.48.2,192.168.48.254,1h --dhcp-range=192.168.49.2,192.168.49.254,1h --dhcp-option=3,200.200.200.1 --dhcp-option=6,200.200.200.1  --server=8.8.8.8 --log-queries  --log-dhcp --address=/#/200.200.200.1

RLS="$(ip rule | grep -vE 'unreachable|local')"
echo "$RLS"
for t in $(echo "$RLS" | busybox awk '{print $NF}' | busybox uniq); do ip r s table $t; done
