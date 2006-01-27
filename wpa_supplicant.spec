Summary: WPA/WPA2/IEEE 802.1X Supplicant
Name: wpa_supplicant
Version: 0.4.7
Release: 2
License: GPL
Group: System Environment/Base
Source0: http://hostap.epitest.fi/releases/%{name}-%{version}.tar.gz
Source1: %{name}.config
Source2: %{name}.conf
Source3: %{name}.init.d
Source4: %{name}.sysconfig
Source5: madwifi-headers.tar.bz2
Patch0: wpa_supplicant-ctrl-iface-ap-scan.patch
URL: http://hostap.epitest.fi/wpa_supplicant/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: qt-devel

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
%patch0 -p1 -b .ctrl-iface-ap-scan

%build
cp %{SOURCE1} ./.config
tar -xjf %{SOURCE5}
make %{_smp_mflags}
QTDIR=%{_libdir}/qt-3.3 make wpa_gui %{_smp_mflags}

%install
rm -rf %{buildroot}

# init scripts
install -d %{buildroot}/%{_sysconfdir}/init.d
install -d %{buildroot}/%{_sysconfdir}/sysconfig
install -m 0755 %{SOURCE3} %{buildroot}/%{_sysconfdir}/init.d/%{name}
install -m 0644 %{SOURCE4} %{buildroot}/%{_sysconfdir}/sysconfig/%{name}

# config
install -d %{buildroot}/%{_sysconfdir}/%{name}
install -m 0600 %{SOURCE2} %{buildroot}/%{_sysconfdir}/%{name}

# binary
install -d %{buildroot}/%{_sbindir}
install -m 0755 -s wpa_cli %{buildroot}/%{_sbindir}
install -m 0755 -s wpa_supplicant %{buildroot}/%{_sbindir}

# gui
install -d %{buildroot}/%{_bindir}
install -m 0755 -s wpa_gui/wpa_gui %{buildroot}/%{_bindir}

# running
mkdir -p %{buildroot}/%{_localstatedir}/run/%{name}

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
%doc COPYING ChangeLog README README-Windows.txt eap_testing.txt todo.txt wpa_supplicant.conf doc
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_sysconfdir}/init.d/%{name}
%{_sbindir}/wpa_supplicant
%{_sbindir}/wpa_cli
%{_localstatedir}/run/%{name}

%files gui
%defattr(-, root, root)
%{_bindir}/wpa_gui

%changelog
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

