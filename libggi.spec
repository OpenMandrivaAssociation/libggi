%define major	2
%define libname	%mklibname ggi %{major}
%define devname	%mklibname ggi -d

Summary:	A fast, simple, small and flexible user-space graphics library
Name:		libggi
Version:	2.2.2
Release:	20
License:	GPLv2
Group:		System/Libraries
Url:		http://www.ggi-project.org/
Source0:	http://www.ggi-project.org/ftp/ggi/v2.2/%{name}-%{version}.src.tar.bz2
Patch0:		libggi-2.0.1-no-lcd823-ppc.patch
Patch3:		libggi-2.0.3-xpath.patch
Patch4:		libggi_wformat.patch

Buildrequires:	aalib-devel
Buildrequires:	libgii-devel >= 1.0.2-2
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	pkgconfig(directfb)
BuildRequires:	pkgconfig(xext)
BuildConflicts:	svgalib-devel

%description
LibGGI is a fast, simple, small and flexible user-space graphics
library developed by the GGI Project <http://www.ggi-project.org/>.
It attempts to abstract the many different graphics output systems
existing under Unix (and in the future, other platforms). The support
for all of these different types of displays and hardware are provided
by dynamically-loaded mini-libraries.

LibGGI can transparently (to the LibGGI-using application) display
graphics on an X window, fbcon (Linux framebuffer driver), or the 
glide library, through their respective graphics drivers, or targets. 
There are also some other targets which display through another 
target, such as multi to display simultaneously on multiple displays 
at once, and tile to tile your display to different monitors.

LibGGI supports acceleration of graphics primitives where possible.

LibGGI is a very generic piece of software, that will run on about
every platform that has remotely heard of POSIX (ports to other systems
such as Win32 are underway) and on many display subsystems.

%package -n	%{libname}
Summary:	Main library for %{name}
Group:		System/Libraries
Requires:	%{name}

%description -n	%{libname}
This package contains the library needed to run programs dynamically
linked with %{name}.

%package -n	%{devname}
Summary:	Headers for developing programs that will use %{name}
Group:		Development/Other
Requires:	%{libname} = %{version}-%{release} libgii-devel
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{_lib}ggi-static-devel < 2.2.2-18

%description -n	%{devname}
This package contains the headers that programmers will need to develop
applications which will use %{name}.

%prep
%setup -q
%apply_patches
perl -pi -e "s|/lib\b|/%{_lib}|g" * m4/*

%build
# workaround configure failure
export echo=echo
%configure2_5x \
	--disable-static \
	--with-gii=%{_prefix} \
	--disable-debug

%make 

%install
# workaround failure
export echo=echo
%makeinstall_std

%files
%doc FAQ NEWS README doc/env.txt doc/targets.txt
%dir %{_sysconfdir}/ggi/
%dir %{_sysconfdir}/ggi/targets
%config(noreplace) %{_sysconfdir}/ggi/libggi.conf
%config(noreplace) %{_sysconfdir}/ggi/targets/fbdev.conf
%{_bindir}/*
%dir %{_libdir}/ggi/
%dir %{_libdir}/ggi/default/
%dir %{_libdir}/ggi/default/fbdev
%dir %{_libdir}/ggi/display
%dir %{_libdir}/ggi/helper
%{_libdir}/ggi/*/*.so
%{_libdir}/ggi/default/fbdev/*.so
%{_mandir}/man1/*

%files -n %{libname}
%{_libdir}/libggi.so.%{major}*

%files -n %{devname}
%doc ChangeLog doc/*.txt
%{_includedir}/ggi/*
%{_libdir}/*.so
%{_mandir}/man3/*
%{_mandir}/man7/*

