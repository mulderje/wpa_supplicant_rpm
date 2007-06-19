#!/bin/bash
#
# wpa_supplicant 
#
# chkconfig:   - 12 88
# description: wpa_supplicant is a WPA Supplicant for Linux, BSD and \
#     Windows with support for WPA and WPA2 (IEEE 802.11i / RSN). Supplicant \
#     is the IEEE 802.1X/WPA component that is used in the client stations. \
#     It implements key negotiation with a WPA Authenticator and it controls \
#     the roaming and IEEE 802.11 authentication/association of the wlan driver.
# processname: wpa_supplicant
# config:      /etc/wpa_supplicant/wpa_supplicant.conf
#

# Source function library.
. /etc/rc.d/init.d/functions

# Source networking configuration.
. /etc/sysconfig/network

# Check that networking is up.
[ "$NETWORKING" = "no" ] && exit 0

exec="/usr/sbin/wpa_supplicant"
prog=$(basename $exec)
conf="/etc/wpa_supplicant/wpa_supplicant.conf"
lockfile=/var/lock/subsys/$prog

[ -e /etc/sysconfig/$prog ] && . /etc/sysconfig/$prog
[ "$INTERFACES" != "" ] || exit 0
[ "$DRIVERS" != "" ] || exit 0

start() {
 	echo -n $"Starting $prog: $conf, $INTERFACES, $DRIVERS"
	daemon $prog -c $conf $INTERFACES $DRIVERS -B
	retval=$?
	echo
	[ $retval -eq 0 ] && touch $lockfile
	return $retval
}

stop() {
	echo -n $"Stopping $prog: "
	killproc $prog
	retval=$?
	echo
	[ $retval -eq 0 ] && rm -f $lockfile
	return $retval
}

restart() {
	stop
	start
}

reload() {
	restart
}

force_reload() {
	restart
}

fdr_status() {
	status $prog
}


case "$1" in
	start|stop|restart|reload)
  		$1
		;;
	force-reload)
		force_reload
		;;
	status)
		fdr_status
		;;
	condrestart|try-restart)
		[ -f $lockfile ] || restart
		;;
	*)
		echo $"Usage: $0 {start|stop|status|restart|try-restart|reload|force-reload}"
		exit 1
esac

