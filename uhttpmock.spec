#
# Conditional build:
%bcond_without	apidocs		# gtk-doc API documentation
%bcond_without	static_libs	# static library
%bcond_without	vala		# Vala API

Summary:	HTTP web service mocking library
Summary(pl.UTF-8):	Biblioteka do tworzenia atrap usług HTTP
Name:		uhttpmock
Version:	0.5.3
Release:	1
License:	LGPL v2.1+
Group:		Libraries
#Source0Download: https://gitlab.com/uhttpmock/uhttpmock/tags
Source0:	https://gitlab.com/uhttpmock/uhttpmock/repository/archive.tar.bz2?ref=%{version}&fake_out=/%{name}-%{version}.tar.bz2
# Source0-md5:	2ce00dc72d5f21ae5db779a2dc76cebd
URL:		https://gitlab.com/groups/uhttpmock
BuildRequires:	autoconf >= 2.65
BuildRequires:	automake >= 1:1.9
BuildRequires:	glib2-devel >= 1:2.36
BuildRequires:	gobject-introspection-devel >= 0.10
BuildRequires:	gtk-doc >= 1.14
BuildRequires:	libsoup-devel >= 2.48
BuildRequires:	libtool >= 2:2
BuildRequires:	pkgconfig
BuildRequires:	vala
Requires:	glib2 >= 1:2.36
Requires:	libsoup >= 2.48
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
Requires:	glib2-devel >= 1:2.36
Requires:	libsoup-devel >= 2.48

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

%package -n vala-libuhttpmock
Summary:	Vala API for uhttpmock library
Summary(pl.UTF-8):	API języka Vala do biblioteki uhttpmock
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	vala
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description -n vala-libuhttpmock
Vala API for uhttpmock library.

%description -n vala-libuhttpmock -l pl.UTF-8
API języka Vala do biblioteki uhttpmock.

%package apidocs
Summary:	API documentation for uhttpmock library
Summary(pl.UTF-8):	Dokumentacja API biblioteki uhttpmock
Group:		Documentation
Requires:	gtk-doc-common
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
API documentation for uhttpmock library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki uhttpmock.

%prep
%setup -q -n %{name}-%{version}-a7f61360d387e2b8fcbdee33f7be17fae2ab9e55

%build
%{__gtkdocize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{?with_apidocs:--enable-gtk-doc} \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static} \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libuhttpmock-0.0.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README
%attr(755,root,root) %{_libdir}/libuhttpmock-0.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libuhttpmock-0.0.so.0
%{_libdir}/girepository-1.0/Uhm-0.0.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libuhttpmock-0.0.so
%{_includedir}/libuhttpmock-0.0
%{_datadir}/gir-1.0/Uhm-0.0.gir
%{_pkgconfigdir}/libuhttpmock-0.0.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libuhttpmock-0.0.a
%endif

%if %{with vala}
%files -n vala-libuhttpmock
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/libuhttpmock-0.0.deps
%{_datadir}/vala/vapi/libuhttpmock-0.0.vapi
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libuhttpmock-0.0
%endif
