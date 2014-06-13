%define	major 1
%define	libname %mklibname sctp %{major}
%define devname %mklibname sctp -d

Summary:	User-space access to Linux Kernel SCTP
Name:		lksctp-tools
Version:	1.0.16
Release:	2
# src/apps/bindx_test.C is GPLv2, I've asked upstream for clarification
License:	GPLv2 and GPLv2+ and LGPLv2 and MIT
Group:		System/Libraries
Url:		http://lksctp.sourceforge.net
Source0:	http://downloads.sourceforge.net/lksctp/%{name}-%{version}.tar.gz
Patch0:		lksctp-tools-1.0.16-libdir.patch
BuildRequires:	libtool

%track
prog %{name} = {
	url = http://sourceforge.net/projects/lksctp/
	regex = lksctp-tools-(__VER__)\.tar\.gz
	version = %{version}
}

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

%package -n	%{devname}
Summary:	Development files for lksctp-tools
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	sctp-devel = %{version}-%{release}

%description -n	%{devname}
Development files for lksctp-tools which include man pages, header files,
static libraries, symlinks to dynamic libraries and some tutorial source code.

%prep
%setup -q
%apply_patches
autoreconf -fi

%build

CFLAGS="%optflags -fuse-ld=bfd" %configure \
    --disable-static

# remove rpath from libtool
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make

%install
rm -f doc/rfc2960.txt doc/states.txt

%makeinstall_std INSTALL="install -p"

# cleanups
rm -rf %{buildroot}%{_datadir}/doc/lksctp-tools

%files
%{_bindir}/*

%files -n %{libname}
%{_libdir}/libsctp.so.%{major}*
%dir %{_libdir}/lksctp-tools/
%{_libdir}/lksctp-tools/libwithsctp.so.%{major}*

%files -n %{devname}
%doc AUTHORS ChangeLog COPYING* README
%doc doc/*.txt
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/lksctp-tools/*.so
%{_datadir}/lksctp-tools/
%{_mandir}/man3/*
%{_mandir}/man7/*

