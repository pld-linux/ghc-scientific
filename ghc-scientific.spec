#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	scientific
Summary:	Numbers represented using scientific notation
Name:		ghc-%{pkgname}
Version:	0.3.4.6
Release:	1
License:	BSD
Group:		Development/Languages
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	beaffa29a79f0717729c9dc48820c149
URL:		http://hackage.haskell.org/package/scientific
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-base >= 3
BuildRequires:	ghc-base <= 5
BuildRequires:	ghc-bytestring >= 0.9
%if %{with prof}
BuildRequires:	ghc-prof >= 6.12.3
BuildRequires:	ghc-base-prof >= 3
BuildRequires:	ghc-base-prof <= 5
BuildRequires:	ghc-bytestring-prof >= 0.9
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
Requires(post,postun):	/usr/bin/ghc-pkg
%requires_eq	ghc
Requires:	ghc-base >= 3
Requires:	ghc-base <= 5
Requires:	ghc-bytestring >= 0.9
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
Arbitrary-precision floating-point numbers represented using
scientific notation regular expressions.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-base-prof >= 3
Requires:	ghc-base-prof <= 5
Requires:	ghc-bytestring-prof >= 0.9

%description prof
Profiling %{pkgname} library for GHC. Should be installed when GHC's
profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%package doc
Summary:	HTML documentation for ghc %{pkgname} package
Summary(pl.UTF-8):	Dokumentacja w formacie HTML dla pakietu ghc %{pkgname}
Group:		Documentation

%description doc
HTML documentation for ghc %{pkgname} package.

%description doc -l pl.UTF-8
Dokumentacja w formacie HTML dla pakietu ghc %{pkgname}.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.hs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build
runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/html %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc LICENSE
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/HSscientific-%{version}.o
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSscientific-%{version}.a
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/ByteString
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/ByteString/Builder
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Text
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Text/Lazy
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Text/Lazy/Builder
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/GHC
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/GHC/Integer
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/GHC/Integer/Logarithms
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Math
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Math/NumberTheory
#{_libdir}/%{ghcdir}/%{pkgname}-%{version}/{*,*/*,*/*/*,*/*/*/*}.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*/*/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*/*/*/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*/*/*/*/*.hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSscientific-%{version}_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*/*/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*/*/*/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*/*/*/*/*.p_hi
%endif

%files doc
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
