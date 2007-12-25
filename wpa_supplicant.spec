Summary: WPA/WPA2/IEEE 802.1X Supplicant
Name: wpa_supplicant
Epoch: 1
Version: 0.5.7
Release: 21%{?dist}
License: BSD
Group: System Environment/Base
Source0: http://hostap.epitest.fi/releases/%{name}-%{version}.tar.gz
Source1: %{name}.config
Source2: %{name}.conf
Source3: %{name}.init.d
Source4: %{name}.sysconfig
Source5: madwifi-headers-r1475.tar.bz2
Source6: fi.epitest.hostap.WPASupplicant.service
Source7: %{name}.logrotate
Patch0: wpa_supplicant-assoc-timeout.patch
Patch1: wpa_supplicant-driver-wext-debug.patch
Patch2: wpa_supplicant-wep-key-fix.patch
# http://hostap.epitest.fi/bugz/show_bug.cgi?id=192
Patch3: wpa_supplicant-fix-deprecated-dbus-function.patch     #Upstream
Patch4: wpa_supplicant-0.5.7-debug-file.patch                 #Upstream
Patch5: wpa_supplicant-0.5.7-qmake-location.patch
Patch6: wpa_supplicant-0.5.7-flush-debug-output.patch         #Upstream
Patch7: wpa_supplicant-0.5.7-sigusr1-changes-debuglevel.patch #Dropped
Patch8: wpa_supplicant-0.5.7-always-scan.patch
Patch9: wpa_supplicant-0.5.7-dbus-iface-segfault-fix.patch    #Upstream
Patch10: wpa_supplicant-0.5.7-dbus-blobs.patch
Patch11: wpa_supplicant-0.5.7-dbus-permissions-fix.patch
Patch12: wpa_supplicant-0.5.7-ignore-dup-ca-cert-addition.patch
Patch13: wpa_supplicant-0.5.7-fix-dynamic-wep-with-mac80211.patch #Upstream
Patch14: wpa_supplicant-0.5.7-use-IW_ENCODE_TEMP.patch
Patch15: wpa_supplicant-0.5.7-fix-signal-leaks.patch              #Upstream
Patch16: wpa_supplicant-0.5.9-adhoc-frequency.patch
URL: http://w1.fi/wpa_supplicant/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: qt-devel
BuildRequires: openssl-devel
BuildRequires: readline-devel
BuildRequires: dbus-devel

PreReq: chkconfig

%description
wpa_supplicant is a WPA Supplicant for Linux, BSD and Windows with support 
for WPA and WPA2 (IEEE 802.11i / RSN). Supplicant is the IEEE 802.1X/WPA 
component that is used in the client stations. It implements key negotiation 
with a WPA Authenticator and it controls the roaming and IEEE 802.11 
authentication/association of the wlan driver.

%package gui
Summary: Graphical User Interface for %{name}
Group: Application/System

%description gui
Graphical User Interface for wpa_supplicant written using QT3

%prep
%setup -q
%patch0 -p1 -b .assoc-timeout
%patch1 -p1 -b .driver-wext-debug
%patch2 -p1 -b .wep-key-fix
%patch3 -p0 -b .fix-deprecated-dbus-functions
%patch4 -p1 -b .debug-file
%patch5 -p1 -b .qmake-location
%patch6 -p1 -b .flush-debug-output
%patch7 -p1 -b .sigusr1-changes-debuglevel
%patch8 -p1 -b .always-scan
%patch9 -p1 -b .dbus-iface-segfault-fix
%patch10 -p2 -b .dbus-blobs
%patch11 -p1 -b .dbus-permissions-fix
%patch12 -p1 -b .ignore-dup-ca-cert-addition
%patch13 -p1 -b .fix-dynamic-wep-with-mac80211
%patch14 -p1 -b .use-IW_ENCODE_TEMP
%patch15 -p1 -b .signal-leak-fixes
%patch16 -p2 -b .adhoc-freq

%build
cp %{SOURCE1} ./.config
tar -xjf %{SOURCE5}
CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS ;
CXXFLAGS="${CXXFLAGS:-%optflags}" ; export CXXFLAGS ;
make %{_smp_mflags}
QTDIR=%{_libdir}/qt-3.3 make wpa_gui %{_smp_mflags}

%install
rm -rf %{buildroot}

# init scripts
install -d %{buildroot}/%{_sysconfdir}/rc.d/init.d
install -d %{buildroot}/%{_sysconfdir}/sysconfig
install -m 0755 %{SOURCE3} %{buildroot}/%{_sysconfdir}/rc.d/init.d/%{name}
install -m 0644 %{SOURCE4} %{buildroot}/%{_sysconfdir}/sysconfig/%{name}
install -d %{buildroot}/%{_sysconfdir}/logrotate.d
install -m 0644 %{SOURCE7} %{buildroot}/%{_sysconfdir}/logrotate.d/%{name}

# config
install -d %{buildroot}/%{_sysconfdir}/%{name}
install -m 0600 %{SOURCE2} %{buildroot}/%{_sysconfdir}/%{name}

# binary
install -d %{buildroot}/%{_sbindir}
install -m 0755 wpa_passphrase %{buildroot}/%{_sbindir}
install -m 0755 wpa_cli %{buildroot}/%{_sbindir}
install -m 0755 wpa_supplicant %{buildroot}/%{_sbindir}
install -d %{buildroot}/%{_sysconfdir}/dbus-1/system.d/
install -m 0644 dbus-wpa_supplicant.conf %{buildroot}/%{_sysconfdir}/dbus-1/system.d/wpa_supplicant.conf
install -d %{buildroot}/%{_datadir}/dbus-1/system-services/
install -m 0644 %{SOURCE6} %{buildroot}/%{_datadir}/dbus-1/system-services

# gui
install -d %{buildroot}/%{_bindir}
install -m 0755 wpa_gui/wpa_gui %{buildroot}/%{_bindir}

# running
mkdir -p %{buildroot}/%{_localstatedir}/run/%{name}

# man pages
install -d %{buildroot}%{_mandir}/man{5,8}
install -m 0644 doc/docbook/*.8 %{buildroot}%{_mandir}/man8
install -m 0644 doc/docbook/*.5 %{buildroot}%{_mandir}/man5

# some cleanup in docs
rm -f  doc/.cvsignore
rm -rf doc/docbook


%clean
rm -rf %{buildroot}

%post
if [ $1 = 1 ]; then
	chkconfig --add %{name}
fi

%preun
if [ $1 = 0 ]; then
	service %{name} stop > /dev/null 2>&1
	/sbin/chkconfig --del %{name}
fi


%files
%defattr(-, root, root)
%doc COPYING ChangeLog README eap_testing.txt todo.txt wpa_supplicant.conf examples
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%{_sysconfdir}/rc.d/init.d/%{name}
%{_sysconfdir}/dbus-1/system.d/%{name}.conf
%{_datadir}/dbus-1/system-services/fi.epitest.hostap.WPASupplicant.service
%{_sbindir}/wpa_passphrase
%{_sbindir}/wpa_supplicant
%{_sbindir}/wpa_cli
%dir %{_localstatedir}/run/%{name}
%dir %{_sysconfdir}/%{name}
%{_mandir}/man8/*
%{_mandir}/man5/*

%files gui
%defattr(-, root, root)
%{_bindir}/wpa_gui

%changelog
* Tue Dec 25 2007 Dan Williams <dcbw@redhat.com> - 0.5.7-21
- Backport 'frequency' option for Ad-Hoc network configs

* Mon Dec 24 2007 Dan Williams <dcbw@redhat.com> - 0.5.7-20
- Fix LSB initscript header to ensure 'messagebus' is started first (rh #244029)

* Thu Dec  6 2007 Dan Williams <dcbw@redhat.com> - 0.5.7-19
- Fix two leaks when signalling state and scan results (rh #408141)

* Mon Dec  3 2007 Dan Williams <dcbw@redhat.com> - 0.5.7-18
- Add logrotate config file (rh #404181)
- Add new LSB initscript header to initscript with correct deps (rh #244029)
- Move other runtime arguments to /etc/sysconfig/wpa_supplicant

* Thu Nov 15 2007 Dan Williams <dcbw@redhat.com> - 0.5.7-17
- Start after messagebus service (rh #385191)
- Fix initscript 'condrestart' command (rh #217281)

* Tue Nov 13 2007 Dan Williams <dcbw@redhat.com> - 0.5.7-16
- Add IW_ENCODE_TEMP patch for airo driver and Dynamic WEP
- Fix error in wpa_supplicant-0.5.7-ignore-dup-ca-cert-addition.patch that
    caused the last error to not be printed
- Fix wpa_supplicant-0.5.7-ignore-dup-ca-cert-addition.patch to ignore
    duplicate cert additions for all certs and keys
- Change license to BSD due to linkage against OpenSSL since there is no
    OpenSSL exception in the GPLv2 license text that upstream ships

* Sun Oct 28 2007 Dan Williams <dcbw@redhat.com> - 0.5.7-15
- Fix Dynamic WEP associations with mac80211-based drivers

* Sun Oct 28 2007 Dan Williams <dcbw@redhat.com> - 0.5.7-14
- Don't error an association on duplicate CA cert additions

* Wed Oct 24 2007 Dan Williams <dcbw@redhat.com> - 0.5.7-13
- Correctly set the length of blobs added via the D-Bus interface

* Wed Oct 24 2007 Dan Williams <dcbw@redhat.com> - 0.5.7-12
- Fix conversion of byte arrays to strings by ensuring the buffer is NULL
    terminated after conversion

* Sat Oct 20 2007 Dan Williams <dcbw@redhat.com> - 0.5.7-11
- Add BLOB support to the D-Bus interface
- Fix D-Bus interface permissions so that only root can use the wpa_supplicant
    D-Bus interface

* Tue Oct  9 2007 Dan Williams <dcbw@redhat.com> - 0.5.7-10
- Don't segfault with dbus control interface enabled and invalid network
    interface (rh #310531)

* Tue Sep 25 2007 Dan Williams <dcbw@redhat.com> - 0.5.7-9
- Always allow explicit wireless scans triggered from a control interface

* Thu Sep 20 2007 Dan Williams <dcbw@redhat.com> - 0.5.7-8
- Change system bus activation file name to work around D-Bus bug that fails
    to launch services unless their .service file is named the same as the
    service itself

* Fri Aug 24 2007 Dan Williams <dcbw@redhat.com> - 0.5.7-7
- Make SIGUSR1 change debug level on-the-fly; useful in combination with
    the -f switch to log output to /var/log/wpa_supplicant.log
- Stop stripping binaries on install so we get debuginfo packages
- Remove service start requirement for interfaces & devices from sysconfig file,
    since wpa_supplicant's D-Bus interface is now turned on

* Fri Aug 17 2007 Dan Williams <dcbw@redhat.com> - 0.5.7-6
- Fix compilation with RPM_OPT_FLAGS (rh #249951)
- Make debug output to logfile a runtime option

* Fri Aug 17 2007 Christopher Aillon <caillon@redhat.com> - 0.5.7-5
- Update the license tag

* Tue Jun 19 2007 Dan Williams <dcbw@redhat.com> - 0.5.7-4
- Fix initscripts to use -Dwext by default, be more verbose on startup
    (rh #244511)

* Mon Jun  4 2007 Dan Williams <dcbw@redhat.com> - 0.5.7-3
- Fix buffer overflow by removing syslog patch (#rh242455)

* Mon Apr  9 2007 Dan Williams <dcbw@redhat.com> - 0.5.7-2
- Add patch to send output to syslog

* Thu Mar 15 2007 Dan Williams <dcbw@redhat.com> - 0.5.7-1
- Update to 0.5.7 stable release

* Mon Oct 27 2006 Dan Williams <dcbw@redhat.com> - 0.4.9-1
- Update to 0.4.9 for WE-21 fixes, remove upstreamed patches
- Don't package doc/ because they aren't actually wpa_supplicant user documentation,
    and becuase it pulls in perl

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.4.8-10.1
- rebuild

* Thu Apr 27 2006 Dan Williams <dcbw@redhat.com> - 0.4.8-10
- Add fix for madwifi and WEP (wpa_supplicant/hostap bud #140) (#rh190075#)
- Fix up madwifi-ng private ioctl()s for r1331 and later
- Update madwifi headers to r1475

* Tue Apr 25 2006 Dan Williams <dcbw@redhat.com> - 0.4.8-9
- Enable Wired driver, PKCS12, and Smartcard options (#rh189805#)

* Tue Apr 11 2006 Dan Williams <dcbw@redhat.com> - 0.4.8-8
- Fix control interface key obfuscation a bit

* Sun Apr  2 2006 Dan Williams <dcbw@redhat.com> - 0.4.8-7
- Work around older & incorrect drivers that return null-terminated SSIDs

* Mon Mar 27 2006 Dan Williams <dcbw@redhat.com> - 0.4.8-6
- Add patch to make orinoco happy with WEP keys
- Enable Prism54-specific driver
- Disable ipw-specific driver; ipw2x00 should be using WEXT instead

* Fri Mar  3 2006 Dan Williams <dcbw@redhat.com> - 0.4.8-5
- Increase association timeout, mainly for drivers that don't
	fully support WPA ioctls yet

* Fri Mar  3 2006 Dan Williams <dcbw@redhat.com> - 0.4.8-4
- Add additional BuildRequires #rh181914#
- Add prereq on chkconfig #rh182905# #rh182906#
- Own /var/run/wpa_supplicant and /etc/wpa_supplicant #rh183696#

* Wed Mar  1 2006 Dan Williams <dcbw@redhat.com> - 0.4.8-3
- Install wpa_passphrase too #rh183480#

* Mon Feb 27 2006 Dan Williams <dcbw@redhat.com> - 0.4.8-2
- Don't expose private data on the control interface unless requested

* Fri Feb 24 2006 Dan Williams <dcbw@redhat.com> - 0.4.8-1
- Downgrade to 0.4.8 stable release rather than a dev release

* Sun Feb 12 2006 Dan Williams <dcbw@redhat.com> - 0.5.1-3
- Documentation cleanup (Terje Rosten <terje.rosten@ntnu.no>)

* Sun Feb 12 2006 Dan Williams <dcbw@redhat.com> - 0.5.1-2
- Move initscript to /etc/rc.d/init.d

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.5.1-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.5.1-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Sun Feb  5 2006 Dan Williams <dcbw@redhat.com> 0.5.1-1
- Update to 0.5.1
- Add WE auth fallback to actually work with older drivers

* Thu Jan 26 2006 Dan Williams <dcbw@redhat.com> 0.4.7-2
- Bring package into Fedora Core
- Add ap_scan control interface patch
- Enable madwifi-ng driver

* Sun Jan 15 2006 Douglas E. Warner <silfreed@silfreed.net> 0.4.7-1
- upgrade to 0.4.7
- added package w/ wpa_gui in it

* Mon Nov 14 2005 Douglas E. Warner <silfreed@silfreed.net> 0.4.6-1
- upgrade to 0.4.6
- adding ctrl interface changes recommended 
  by Hugo Paredes <hugo.paredes@e-know.org>

* Sun Oct  9 2005 Douglas E. Warner <silfreed@silfreed.net> 0.4.5-1
- upgrade to 0.4.5
- updated config file wpa_supplicant is built with
  especially, the ipw2100 driver changed to just ipw
  and enabled a bunch more EAP
- disabled dist tag

* Thu Jun 30 2005 Douglas E. Warner <silfreed@silfreed.net> 0.4.2-3
- fix typo in init script

* Thu Jun 30 2005 Douglas E. Warner <silfreed@silfreed.net> 0.4.2-2
- fixing init script using fedora-extras' template
- removing chkconfig default startup

* Tue Jun 21 2005 Douglas E. Warner <silfreed@silfreed.net> 0.4.2-1
- upgrade to 0.4.2
- new sample conf file that will use any unrestricted AP
- make sysconfig config entry
- new BuildRoot for Fedora Extras
- adding dist tag to Release

* Fri May 06 2005 Douglas E. Warner <silfreed@silfreed.net> 0.3.8-1
- upgrade to 0.3.8

* Thu Feb 10 2005 Douglas E. Warner <silfreed@silfreed.net> 0.3.6-2
- compile ipw driver in

* Wed Feb 09 2005 Douglas E. Warner <silfreed@silfreed.net> 0.3.6-1
- upgrade to 0.3.6

* Thu Dec 23 2004 Douglas E. Warner <silfreed@silfreed.net> 0.2.5-4
- fixing init script

* Mon Dec 20 2004 Douglas E. Warner <silfreed@silfreed.net> 0.2.5-3
- fixing init script
- adding post/preun items to add/remove via chkconfig

* Mon Dec 20 2004 Douglas E. Warner <silfreed@silfreed.net> 0.2.5-2
- adding sysV scripts

* Mon Dec 20 2004 Douglas E. Warner <silfreed@silfreed.net> 0.2.5-1
- Initial RPM release.

