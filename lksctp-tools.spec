%define	major 1
%define	libname %mklibname sctp %{major}
%define develname %mklibname sctp -d

Summary:	User-space access to Linux Kernel SCTP
Name:		lksctp-tools
Version:	1.0.11
Release:	3
# src/apps/bindx_test.C is GPLv2, I've asked upstream for clarification
License:	GPLv2 and GPLv2+ and LGPLv2 and MIT
Group:		System/Libraries
URL:		http://lksctp.sourceforge.net
Source0:	 http://downloads.sourceforge.net/lksctp/%{name}-%{version}.tar.gz
Patch0:		lksctp-tools-1.0.6-libdir.patch
Patch1:		lksctp-tools-1.0.11-SCTP_SENDER_DRY_EVENT.diff
BuildRequires:	autoconf automake libtool
Requires:	%{libname} = %{version}-%{release}

%description
This is the lksctp-tools package for Linux Kernel SCTP (Stream Control
Transmission Protocol) Reference Implementation.

This package is intended to supplement the Linux Kernel SCTP Reference
Implementation now available in the Linux kernel source tree in
versions 2.5.36 and following.  For more information on LKSCTP see the
package documentation README file, section titled "LKSCTP - Linux
Kernel SCTP."

This package contains the command-line tools.

%package -n	%{libname}
Summary:	Shared User-space access to Linux Kernel SCTP library
Group:		System/Libraries

%description -n	%{libname}
This is the lksctp-tools package for Linux Kernel SCTP (Stream Control
Transmission Protocol) Reference Implementation.

This package is intended to supplement the Linux Kernel SCTP Reference
Implementation now available in the Linux kernel source tree in
versions 2.5.36 and following.  For more information on LKSCTP see the
package documentation README file, section titled "LKSCTP - Linux
Kernel SCTP."

This package contains the shared library.

%package -n	%{develname}
Summary:	Development files for lksctp-tools
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	sctp-devel = %{version}-%{release}

%description -n	%{develname}
Development files for lksctp-tools which include man pages, header files,
static libraries, symlinks to dynamic libraries and some tutorial source code.

%package	doc
Summary:	Documents pertaining to SCTP
Group:		System/Libraries

%description	doc
Documents pertaining to LKSCTP & SCTP in general (IETF RFC's & Internet
Drafts).

%prep

%setup -q
%patch0 -p1
%patch1 -p0

%build
autoreconf -fi

%configure \
    --disable-static

# remove rpath from libtool
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make

%install

rm -f doc/rfc2960.txt doc/states.txt

%makeinstall_std INSTALL="install -p"

# cleanups
find %{buildroot}%{_libdir}/ -name "*.*a"  | xargs rm -f
rm -rf %{buildroot}%{_datadir}/doc/lksctp-tools

%files
%{_bindir}/*

%files -n %{libname}
%doc AUTHORS ChangeLog COPYING* README
%{_libdir}/lib*.so.%{major}*
%dir %{_libdir}/lksctp-tools/
%{_libdir}/lksctp-tools/libwithsctp.so.*

%files -n %{develname}
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/lksctp-tools/*.so
%{_datadir}/lksctp-tools/
%{_mandir}/man3/*
%{_mandir}/man7/*

%files doc
%doc doc/*.txt

%changelog
* Thu Mar 15 2012 Oden Eriksson <oeriksson@mandriva.com> 1.0.11-0
- initial Mandriva package (fedora import)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Oct 05 2010 Parag Nemade <paragn AT fedoraproject.org> - 1.0.11-2
- Merge-review cleanup (#226100)

* Tue Dec  1 2009 Jan Safranek <jsafrane@redhat.com> 1.0.11-1
- Update to 1.0.11
- Remove rpath from compiled binaries
- Remove static libraries

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Apr 14 2009 Zdenek Prikryl <zprikryl@redhat.com> 1.0.10-1
- added release tag to Requires of devel and doc packages (#492531)
- Update to 1.0.10

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Aug 06 2008 Zdenek Prikryl <zprikryl@redhat.com> 1.0.9-1
- Update to 1.0.9

* Wed Jul 16 2008 Zdenek Prikryl <zprikryl@redhat.com> 1.0.8-1
- Update to 1.0.8

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.7-3
- Autorebuild for GCC 4.3

* Wed Aug 29 2007 Karsten Hopp <karsten@redhat.com> 1.0.7-2
- rebuild for buildid

* Wed Aug 08 2007 Karsten Hopp <karsten@redhat.com> 1.0.7-1
- update to 1.0.7
- update license tag

* Wed Feb 21 2007 Karsten Hopp <karsten@redhat.com> 1.0.6-3
- add post/postun requirements
- review fixes

* Tue Sep 19 2006 Karsten Hopp <karsten@redhat.de> 1.0.6-2
- fix fileconflict (#205225)

* Tue Jul 25 2006 Karsten Hopp <karsten@redhat.de> 1.0.6-1
- update to 1.0.6

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.0.5-1.fc5.2.1
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.0.5-1.fc5.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.0.5-1.fc5.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan 24 2006 Warren Togami <wtogami@redhat.com> 1.0.5-1
- 1.0.5

* Fri Nov 11 2005 Matthias Saou <http://freshrpms.net/> 1.0.4-1
- Update to 1.0.4.
- Update syntax patch.
- Execute bootstrap if no configure script is found.
- Don't own entire man? directories.
- Own data and lib lksctp-tools directories.
- Move devel libs in _libdir/lksctp-tools/ to devel package.
- Exclude .la files.
- Minor spec file cleanups.

* Wed Mar 02 2005 Karsten Hopp <karsten@redhat.de> 1.0.2-5
- build with gcc-4

* Mon Feb 07 2005 Karsten Hopp <karsten@redhat.de> 1.0.2-4
- initialize variable before use
- fix subscript out of range bug (#147286)

* Mon Jan 24 2005 Karsten Hopp <karsten@redhat.de> 1.0.2-3
- build for FC

* Mon Jan 24 2005 Karsten Hopp <karsten@redhat.de> 1.0.2-2.40E.1
- initial RH version based on sourceforge rpm

* Thu Dec 30 2004 Sridhar Samudrala <sri@us.ibm.com> 1.0.2-1
- 1.0.2 Release

* Tue May 11 2004 Sridhar Samudrala <sri@us.ibm.com> 1.0.1-1
- 1.0.1 Release

* Thu Feb 26 2004 Sridhar Samudrala <sri@us.ibm.com> 1.0.0-1
- 1.0.0 Release

* Fri Feb  6 2004 Francois-Xavier Kowalski <francois-xavier.kowalski@hp.com> 0.9.0-1
- package only .txt doc files

* Wed Feb  4 2004 Francois-Xavier Kowalski <francois-xavier.kowalski@hp.com> 0.7.5-1
- badly placed & undelivered files
- simplified delivery list

* Tue Jan 27 2004 Francois-Xavier Kowalski <francois-xavier.kowalski@hp.com> 0.7.5-1
- Integrate comment from project team

* Sat Jan 10 2004 Francois-Xavier Kowalski <francois-xavier.kowalski@hp.com> 2.6.0_test7_0.7.4-1
- Creation
