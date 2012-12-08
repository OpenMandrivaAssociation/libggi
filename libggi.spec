%define major 2
%define libname %mklibname ggi %{major}
%define develname %mklibname ggi -d

Summary:	A fast, simple, small and flexible user-space graphics library
Name:		libggi
Version:	2.2.2
Release:	19
License:	GPL
Group:		System/Libraries
URL:		http://www.ggi-project.org/
Source:		http://www.ggi-project.org/ftp/ggi/v2.2/%{name}-%{version}.src.tar.bz2
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

%package -n	%{develname}
Summary:	Headers for developing programs that will use %{name}
Group:		Development/Other
Requires:	%{libname} = %{version}-%{release} libgii-devel
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{_lib}ggi2-devel < 2.2.2-18
Obsoletes:	%{_lib}ggi2-static-devel < 2.2.2-18
Obsoletes:	%{_lib}ggi-static-devel < 2.2.2-18

%description -n	%{develname}
This package contains the headers that programmers will need to develop
applications which will use %{name}.

%prep
%setup -q
%apply_patches

perl -pi -e "s|/lib\b|/%{_lib}|g" * m4/*

# regenerate configure script
#./autogen.sh < borked

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
%{_mandir}/man3/*
%{_mandir}/man7/*

%files -n %{libname}
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%doc ChangeLog doc/*.txt
%{_includedir}/ggi/*
%{_libdir}/*.so


%changelog
* Mon Jan 02 2012 Matthew Dawkins <mattydaw@mandriva.org> 2.2.2-17mdv2012.0
+ Revision: 748670
- cleaned up spec
- disabled static build
- removed pre 2009 scriptlets

  + Andrey Bondrov <abondrov@mandriva.org>
    - Rebuild for .la files issue

* Fri Apr 29 2011 Oden Eriksson <oeriksson@mandriva.com> 2.2.2-16
+ Revision: 660252
- mass rebuild

* Sun Nov 28 2010 Oden Eriksson <oeriksson@mandriva.com> 2.2.2-15mdv2011.0
+ Revision: 602547
- rebuild

* Tue Mar 16 2010 Oden Eriksson <oeriksson@mandriva.com> 2.2.2-14mdv2010.1
+ Revision: 520795
- rebuilt for 2010.1

* Sun Sep 27 2009 Olivier Blin <blino@mandriva.org> 2.2.2-13mdv2010.0
+ Revision: 449878
- fix format errors (from Arnaud Patard)
- drop old patches
- rediff xpath patch (from Arnaud Patard)

* Fri Nov 07 2008 Olivier Blin <blino@mandriva.org> 2.2.2-12mdv2009.1
+ Revision: 300425
- rebuild with new xcb
- rebuild for new libx11

* Sat Jul 12 2008 Funda Wang <fwang@mandriva.org> 2.2.2-10mdv2009.0
+ Revision: 234123
- new devel package policy

* Tue Jul 08 2008 Oden Eriksson <oeriksson@mandriva.com> 2.2.2-9mdv2009.0
+ Revision: 232805
- fix build (bundled autopoo is too borked)

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Sun Jan 13 2008 Thierry Vignaud <tv@mandriva.org> 2.2.2-7mdv2008.1
+ Revision: 150565
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Fri Jun 15 2007 Christiaan Welvaart <spturtle@mandriva.org> 2.2.2-6mdv2008.0
+ Revision: 40003
- removed versioned autoconf and automake build deps - not needed
- drop old patches from specfile

* Wed Jun 13 2007 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 2.2.2-5mdv2008.0
+ Revision: 38612
- Rebuild with libslang2.


* Fri Mar 16 2007 Olivier Blin <oblin@mandriva.com> 2.2.2-4mdv2007.1
+ Revision: 144668
- move changelog and devel docs in devel package
- drop INSTALL files
- do not include 8 years old changelog (but keep recent one)

* Sun Feb 18 2007 Anssi Hannula <anssi@mandriva.org> 2.2.2-2mdv2007.1
+ Revision: 122602
- workaround build failure with echo=echo
- update filelist
- fix build
- rebuild for new libgii

  + Tomasz Pawel Gajc <tpg@mandriva.org>
    - new version
    - bunzip patches
    - spec file clean
    - Import libggi

* Tue Sep 19 2006 Gwenole Beauchesne <gbeauchesne@mandriva.com> 2.1.1-3mdv2007.0
- Rebuild

* Wed Jun 07 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 2.1.1-2mdv2007.0
- fix build against glibc 2.4 (P5)
- fix buildrequires

* Fri Aug 19 2005 Per Øyvind Karlsen <pkarlsen@mandriva.com> 2.1.1-1mdk
- 2.1.1
- %%mkrel
- update gcc4 patch (P1)

* Thu Aug 18 2005 Gwenole Beauchesne <gbeauchesne@mandriva.com> 2.1.0-3mdk
- gcc4, lib64 & libtool fixes

* Sat Dec 25 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 2.1.0-2mdk
- use automake1.9 & autoconf2.5

* Tue Dec 21 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 2.1.0-1mdk
- 2.1.0

* Fri Jun 18 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 2.0.5-1mdk
- 2.0.5
- enable directfb support (since directfb is now in main)
- buildconfligts on svgalib-devel so we don't accidentally build with
  svgalib support if svgalib-devel is installed (--disable-svga actually seems
  to enable it, that's why I use buildconflicts in stead)
- drop P2
- require libgii >= 0.8.5

