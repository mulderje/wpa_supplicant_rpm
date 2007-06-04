Summary: WPA/WPA2/IEEE 802.1X Supplicant
Name: wpa_supplicant
Epoch: 1
Version: 0.5.7
Release: 3%{?dist}
License: GPL
Group: System Environment/Base
Source0: http://hostap.epitest.fi/releases/%{name}-%{version}.tar.gz
Source1: %{name}.config
Source2: %{name}.conf
Source3: %{name}.init.d
Source4: %{name}.sysconfig
Source5: madwifi-headers-r1475.tar.bz2
Patch0: wpa_supplicant-assoc-timeout.patch
Patch1: wpa_supplicant-driver-wext-debug.patch
Patch2: wpa_supplicant-wep-key-fix.patch
# http://hostap.epitest.fi/bugz/show_bug.cgi?id=192
Patch3: wpa_supplicant-fix-deprecated-dbus-function.patch
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

%build
cp %{SOURCE1} ./.config
tar -xjf %{SOURCE5}
make %{_smp_mflags}
QTDIR=%{_libdir}/qt-3.3 make wpa_gui %{_smp_mflags}

%install
rm -rf %{buildroot}

# init scripts
install -d %{buildroot}/%{_sysconfdir}/rc.d/init.d
install -d %{buildroot}/%{_sysconfdir}/sysconfig
install -m 0755 %{SOURCE3} %{buildroot}/%{_sysconfdir}/rc.d/init.d/%{name}
install -m 0644 %{SOURCE4} %{buildroot}/%{_sysconfdir}/sysconfig/%{name}

# config
install -d %{buildroot}/%{_sysconfdir}/%{name}
install -m 0600 %{SOURCE2} %{buildroot}/%{_sysconfdir}/%{name}

# binary
install -d %{buildroot}/%{_sbindir}
install -m 0755 -s wpa_passphrase %{buildroot}/%{_sbindir}
install -m 0755 -s wpa_cli %{buildroot}/%{_sbindir}
install -m 0755 -s wpa_supplicant %{buildroot}/%{_sbindir}
mkdir -p %{buildroot}/%{_sysconfdir}/dbus-1/system.d/
install -m 0644 dbus-wpa_supplicant.conf %{buildroot}/%{_sysconfdir}/dbus-1/system.d/wpa_supplicant.conf

# gui
install -d %{buildroot}/%{_bindir}
install -m 0755 -s wpa_gui/wpa_gui %{buildroot}/%{_bindir}

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
%doc COPYING ChangeLog README README-Windows.txt eap_testing.txt todo.txt wpa_supplicant.conf examples
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_sysconfdir}/rc.d/init.d/%{name}
%{_sysconfdir}/dbus-1/system.d/%{name}.conf
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

