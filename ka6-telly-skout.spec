#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	25.08.2
%define		qtver		6.8
%define		kaname		telly-skout
Summary:	TV guide based on Kirigami
Name:		ka6-%{kaname}
Version:	25.08.2
Release:	1
License:	GPL v2+
Group:		X11/Applications
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	a29ee2810c3c655785d24a7577d48550
URL:		https://kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6Gui-devel >= 5.11.1
BuildRequires:	Qt6Widgets-devel
BuildRequires:	cmake >= 3.20
BuildRequires:	gettext-tools
BuildRequires:	kf6-extra-cmake-modules >= 6.4.0
BuildRequires:	python3
BuildRequires:	kf6-kcoreaddons-devel >= 6.4.0
BuildRequires:	kf6-kconfig-devel >= 6.4.0
BuildRequires:	gettext-tools
BuildRequires:	kf6-ki18n-devel >= 6.4.0
BuildRequires:	kf6-kirigami-addons-devel
BuildRequires:	kf6-qqc2-desktop-style-devel >= 6.4.0
BuildRequires:	ninja
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	shared-mime-info
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires(post,postun):	desktop-file-utils
%requires_eq_to Qt6Core Qt6Core-devel
Obsoletes:	ka5-%{kaname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A convergent TV guide based on Kirigami.

%prep
%setup -q -n %{kaname}-%{version}

%build
%cmake \
	-B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON
%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kaname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database_post

%postun
%update_desktop_database_postun

%files -f %{kaname}.lang
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/telly-skout
%{_desktopdir}/org.kde.telly-skout.desktop
%{_iconsdir}/hicolor/scalable/apps/org.kde.telly-skout.svg
%{_datadir}/metainfo/org.kde.telly-skout.appdata.xml
