#
# Conditional build:
%bcond_without	apidocs		# gtk-doc API documentation
%bcond_without	static_libs	# static library
%bcond_without	vala		# Vala API

Summary:	HTTP web service mocking library
Summary(pl.UTF-8):	Biblioteka do tworzenia atrap usług HTTP
Name:		uhttpmock1
Version:	0.9.0
Release:	1
License:	LGPL v2.1+
Group:		Libraries
#Source0Download: https://gitlab.freedesktop.org/pwithnall/uhttpmock/tags
Source0:	https://gitlab.freedesktop.org/pwithnall/uhttpmock/-/archive/%{version}/uhttpmock-%{version}.tar.bz2
# Source0-md5:	ad0e688655dc98d7e17fa0ef732bf4d7
URL:		https://gitlab.freedesktop.org/pwithnall/uhttpmock
BuildRequires:	glib2-devel >= 1:2.38
BuildRequires:	gobject-introspection-devel >= 0.10
BuildRequires:	gtk-doc >= 1.14
BuildRequires:	libsoup3-devel >= 3.1.2
BuildRequires:	meson
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	vala
Requires:	glib2 >= 1:2.38
Requires:	libsoup3 >= 3.1.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
uhttpmock is a project for mocking web service APIs which use HTTP or
HTTPS. It provides a library, libuhttpmock, which implements recording
and playback of HTTP request-response traces.

%description -l pl.UTF-8
uhttpmock to projekt do tworzenia atrap API serwisów WWW,
wykorzystujących HTTP lub HTTPS. Udostępnia bibliotekę implementującą
zapisywanie i odtwarzanie śladów HTTP żądanie-odpowiedź.

%package devel
Summary:	Header files for uhttpmock library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki uhttpmock
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.38
Requires:	libsoup3-devel >= 3.1.2

%description devel
Header files for uhttpmock library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki uhttpmock.

%package static
Summary:	Static uhttpmock library
Summary(pl.UTF-8):	Statyczna biblioteka uhttpmock
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static uhttpmock library.

%description static -l pl.UTF-8
Statyczna biblioteka uhttpmock.

%package -n vala-libuhttpmock1
Summary:	Vala API for uhttpmock library
Summary(pl.UTF-8):	API języka Vala do biblioteki uhttpmock
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	vala
Requires:	vala-libsoup3 >= 3.1.2
BuildArch:	noarch

%description -n vala-libuhttpmock1
Vala API for uhttpmock library.

%description -n vala-libuhttpmock1 -l pl.UTF-8
API języka Vala do biblioteki uhttpmock.

%package apidocs
Summary:	API documentation for uhttpmock library
Summary(pl.UTF-8):	Dokumentacja API biblioteki uhttpmock
Group:		Documentation
Requires:	gtk-doc-common
BuildArch:	noarch

%description apidocs
API documentation for uhttpmock library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki uhttpmock.

%prep
%setup -q -n uhttpmock-%{version}

%build
%meson build

%ninja_build -C build \
	%{!?with_static_libs:--default-library=shared} \
	%{!?with_apidocs:-Dgtk_doc=false}

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README
%attr(755,root,root) %{_libdir}/libuhttpmock-1.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libuhttpmock-1.0.so.1
%{_libdir}/girepository-1.0/Uhm-1.0.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libuhttpmock-1.0.so
%{_includedir}/libuhttpmock-1.0
%{_datadir}/gir-1.0/Uhm-1.0.gir
%{_pkgconfigdir}/libuhttpmock-1.0.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libuhttpmock-1.0.a
%endif

%if %{with vala}
%files -n vala-libuhttpmock1
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/libuhttpmock-1.0.deps
%{_datadir}/vala/vapi/libuhttpmock-1.0.vapi
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libuhttpmock-1.0
%endif
