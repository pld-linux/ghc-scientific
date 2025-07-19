#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	scientific
Summary:	Numbers represented using scientific notation
Summary(pl.UTF-8):	Liczby reprezentowane przy użyciu notacji naukowej
Name:		ghc-%{pkgname}
Version:	0.3.6.2
Release:	2
License:	BSD
Group:		Development/Languages
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	f4f40eec14dd8c9308d8dd478212e4b7
URL:		http://hackage.haskell.org/package/scientific
BuildRequires:	ghc >= 7.0.1
BuildRequires:	ghc-base >= 4.3
BuildRequires:	ghc-binary >= 0.4.1
BuildRequires:	ghc-bytestring >= 0.10.4
BuildRequires:	ghc-containers >= 0.1
BuildRequires:	ghc-deepseq >= 1.3
BuildRequires:	ghc-hashable >= 1.1.2
BuildRequires:	ghc-integer-logarithms >= 1
BuildRequires:	ghc-primitive >= 0.1
BuildRequires:	ghc-text >= 0.8
%if %{with prof}
BuildRequires:	ghc-prof >= 6.12.3
BuildRequires:	ghc-base-prof >= 4.3
BuildRequires:	ghc-binary-prof >= 0.4.1
BuildRequires:	ghc-bytestring-prof >= 0.10.4
BuildRequires:	ghc-containers-prof >= 0.1
BuildRequires:	ghc-deepseq-prof >= 1.3
BuildRequires:	ghc-hashable-prof >= 1.1.2
BuildRequires:	ghc-integer-logarithms-prof >= 1
BuildRequires:	ghc-primitive-prof >= 0.1
BuildRequires:	ghc-text-prof >= 0.8
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
Requires(post,postun):	/usr/bin/ghc-pkg
%requires_eq	ghc
Requires:	ghc-base >= 4.3
Requires:	ghc-binary >= 0.4.1
Requires:	ghc-bytestring >= 0.10.4
Requires:	ghc-containers >= 0.1
Requires:	ghc-deepseq >= 1.3
Requires:	ghc-hashable >= 1.1.2
Requires:	ghc-integer-logarithms >= 1
Requires:	ghc-primitive >= 0.1
Requires:	ghc-text >= 0.8
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
Arbitrary-precision floating-point numbers represented using
scientific notation regular expressions.

%description -l pl.UTF-8
Liczby zmiennoprzecinkowe o dowolnej precyzji, reprezentowane przy
użyciu wyrażeń regularnych notacji naukowej.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-base-prof >= 4.3
Requires:	ghc-binary-prof >= 0.4.1
Requires:	ghc-bytestring-prof >= 0.10.4
Requires:	ghc-containers-prof >= 0.1
Requires:	ghc-deepseq-prof >= 1.3
Requires:	ghc-hashable-prof >= 1.1.2
Requires:	ghc-integer-logarithms-prof >= 1
Requires:	ghc-primitive-prof >= 0.1
Requires:	ghc-text-prof >= 0.8

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
%doc LICENSE changelog
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%attr(755,root,root) %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSscientific-%{version}-*.so
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSscientific-%{version}-*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSscientific-%{version}-*_p.a
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/ByteString
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/ByteString/Builder
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Text
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Text/Lazy
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Text/Lazy/Builder
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/GHC
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/GHC/Integer
#{_libdir}/%{ghcdir}/%{pkgname}-%{version}/{*,*/*,*/*/*,*/*/*/*}.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.dyn_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*/*.dyn_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*/*/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*/*/*.dyn_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*/*/*/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*/*/*/*.dyn_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*/*/*/*/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*/*/*/*/*.dyn_hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSscientific-%{version}-*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*/*/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*/*/*/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*/*/*/*/*.p_hi
%endif

%files doc
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
