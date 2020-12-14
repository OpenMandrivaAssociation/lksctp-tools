%define major 1
%define libname %mklibname sctp %{major}
%define devname %mklibname sctp -d


Summary:	User-space access to Linux Kernel SCTP
Name:		lksctp-tools
Version:	1.0.18
Release:	1
# src/apps/bindx_test.C is GPLv2, I've asked upstream for clarification
License:	GPLv2 and GPLv2+ and LGPLv2 and MIT
Group:		System/Libraries
Url:		http://lksctp.sourceforge.net
Source0:	https://github.com/sctp/lksctp-tools/archive/%{name}-%{version}.tar.gz
Patch0:		lksctp-tools-1.0.16-libdir.patch
Patch1:		lksctp-tools-1.0.18-withsctp-use-PACKAGE_VERSION-in-withsctp.h.patch
Patch2:		lksctp-tools-1.0.18-configure.ac-add-CURRENT-REVISION-and-AGE-for-libsct.patch
Patch3:		lksctp-tools-1.0.18-build-fix-netinet-sctp.h-not-to-be-installed.patch
Patch4:		lksctp-tools-1.0.18-build-remove-v4.12-secondary-defines-in-favor-of-HAV.patch
Patch5:		lksctp-tools-1.0.18-build-fix-probing-for-HAVE_SCTP_SENDV.patch
Patch6:		lksctp-tools-1.0.18-build-0b0dce7a36fb-actually-belongs-to-v4.19.patch
Patch7:		lksctp-tools-symver.patch
BuildRequires:	libtool

%description
This is the lksctp-tools package for Linux Kernel SCTP (Stream Control
Transmission Protocol) Reference Implementation.

This package is intended to supplement the Linux Kernel SCTP Reference
Implementation now available in the Linux kernel source tree in
versions 2.5.36 and following.  For more information on LKSCTP see the
package documentation README file, section titled "LKSCTP - Linux
Kernel SCTP."

This package contains the command-line tools.

%package -n %{libname}
Summary:	Shared User-space access to Linux Kernel SCTP library
Group:		System/Libraries

%description -n %{libname}
This is the lksctp-tools package for Linux Kernel SCTP (Stream Control
Transmission Protocol) Reference Implementation.

This package is intended to supplement the Linux Kernel SCTP Reference
Implementation now available in the Linux kernel source tree in
versions 2.5.36 and following.  For more information on LKSCTP see the
package documentation README file, section titled "LKSCTP - Linux
Kernel SCTP."

This package contains the shared library.

%package -n %{devname}
Summary:	Development files for lksctp-tools
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	sctp-devel = %{version}-%{release}

%description -n %{devname}
Development files for lksctp-tools which include man pages, header files,
static libraries, symlinks to dynamic libraries and some tutorial source code.

%prep
%autosetup -p1
[ ! -x ./configure ] && sh bootstrap

%build
%configure \
    --disable-static

# remove rpath from libtool
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make_build

%install
rm -f doc/rfc2960.txt doc/states.txt

%make_install INSTALL="install -p"

%files
%{_bindir}/*

%files -n %{libname}
%{_libdir}/libsctp.so.%{major}*
%dir %{_libdir}/lksctp-tools/
%{_libdir}/lksctp-tools/libwithsctp.so.%{major}*

%files -n %{devname}
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/lksctp-tools/*.so
%{_datadir}/lksctp-tools/
%{_mandir}/man3/*
%{_mandir}/man7/*
%{_libdir}/pkgconfig/*.pc
