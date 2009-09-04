# The following should match PROGRAM, VERSION and RELEASE in the
# Makefile accompanying this program (and the .tgz defined in Source
# below.

%define name    libwulf
%define version 1.0.2
%define release %mkrel 5

%define lib_version     1.0.2
%define lib_major       1
%define lib_name_orig   %mklibname wulf
%define lib_name        %{lib_name_orig}%{lib_major}

Summary: The core library of the wulfstat family of xmlsysd clients

Name: %name
Version: %version
Release: %release
Group: Monitoring
License: GPL
Source: http://www.phy.duke.edu/~rgb/wulfware/%{name}-%{version}.tgz
Requires: libxml2
BuildRequires: libxml2-devel
BuildRoot:      %{_tmppath}/%{name}-%{version}-root
URL:	http://www.phy.duke.edu/~rgb/wulfware/

%description 
libwulf is the core common library required by wulfstat and wulflogger,
two xmlsysd clients that poll and display various statistics from a
cluster in a user-controllable loop.  libwulf contains routines that
open and parse a wulfhosts (cluster/lan descriptor) file, establish
xmlsysd connections in a threaded subtask to all hosts in the wulfhosts
file, and in parallel with this initialize and update selected
statistics.  libwulf functions form an API adequate to support many
kinds of toplevel log and gui applications reasonably efficiently.

%package -n     %{lib_name}-devel
Summary:        Development tools for programs which will use the libwulf library
Group:          Development/C
Requires:       %{lib_name} = %{version}
Obsoletes:      %{name}-devel
Provides:       %{name}-devel = %{version}-%{release}

%description -n %{lib_name}-devel
This package contains the header files for developing programs
which uses the libwulf library.

%package -n     %{lib_name}
Summary:        A library of functions for the wulfware applications
Group:          System/Libraries
Obsoletes:      %{name}
Provides:       %{name} = %{version}-%{release}

%description -n %{lib_name}
This package contains the .so libraries for wulfware applications.

%package -n     %{lib_name}-static-devel
Summary:        Static libraries for programs which will use the libwulf library
Group:          Development/C
Requires:       %{lib_name}-devel = %{version}
Provides:       %{name}-static-devel = %{version}-%{release}

%description -n %{lib_name}-static-devel
This package contains the static libraries for developing
programs which uses the libwulf library.


%prep
%setup -q -n %{name}

%build
make clean
make

%install
make PREFIX=%{buildroot}/usr install
%ifarch x86_64
mv  %{buildroot}/usr/lib  %{buildroot}%{_libdir}
%endif
ln -snf %{name}.so.%{lib_version} %{buildroot}%{_libdir}/%{name}.so

%clean
rm -rf $RPM_BUILD_ROOT
rm -rf %{builddir}

%files -n %{lib_name}-devel
%defattr(-,root,root,-)
%doc COPYING README CHANGELOG
%{_includedir}/*
%{_libdir}/*.so
%{_mandir}/man3/*


%files -n %{lib_name}
%defattr(-,root,root,-)
#%doc Readme
%{_libdir}/*.so.*


%files -n %{lib_name}-static-devel
%defattr(-,root,root,-)
%doc COPYING README CHANGELOG
%{_libdir}/*.a


%if %mdkversion < 200900
%post -n %{lib_name} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{lib_name} -p /sbin/ldconfig 
%endif


