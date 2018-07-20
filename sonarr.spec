%global user %{name}
%global group %{name}

Name:           sonarr
Version:        2.0.0.5228
Release:        1%{?dist}
Summary:        Automated manager and downloader for TV series
License:        GPLv3
URL:            https://sonarr.tv/
BuildArch:      noarch

Source0:        http://download.sonarr.tv/v2/master/mono/NzbDrone.master.%{version}.mono.tar.gz
Source1:        https://raw.githubusercontent.com/Sonarr/Sonarr/develop/COPYRIGHT.md
Source2:        https://raw.githubusercontent.com/Sonarr/Sonarr/develop/LICENSE.md
Source3:        https://raw.githubusercontent.com/Sonarr/Sonarr/develop/README.md
Source10:       %{name}.service
Source11:       %{name}.xml

BuildRequires:  firewalld-filesystem
BuildRequires:  systemd
BuildRequires:  tar

Requires:       firewalld-filesystem
Requires(post): firewalld-filesystem
Requires:       mono-core
Requires:       libmediainfo
Requires:       sqlite

%description
Sonarr is a PVR for Usenet and BitTorrent users. It can monitor multiple RSS
feeds for new episodes of your favorite shows and will grab, sort and rename
them. It can also be configured to automatically upgrade the quality of files
already downloaded when a better quality format becomes available.

%prep
%autosetup -n NzbDrone
cp %{SOURCE1} %{SOURCE2} %{SOURCE3} .

%install
mkdir -p %{buildroot}%{_datadir}/%{name}
mkdir -p %{buildroot}%{_prefix}/lib/firewalld/services/
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_sharedstatedir}/%{name}

cp -fr * %{buildroot}%{_datadir}/%{name}

install -m 0644 -p %{SOURCE10} %{buildroot}%{_unitdir}/%{name}.service
install -m 0644 -p %{SOURCE11} %{buildroot}%{_prefix}/lib/firewalld/services/%{name}.xml

find %{buildroot} -name "*.mdb" -delete

%pre
getent group %{group} >/dev/null || groupadd -r %{group}
getent passwd %{user} >/dev/null || \
    useradd -r -g %{group} -d %{_sharedstatedir}/%{name} -s /sbin/nologin \
    -c "%{name}" %{user}
exit 0

%post
%systemd_post %{name}.service
%firewalld_reload

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%license COPYRIGHT.md LICENSE.md
%doc README.md
%attr(750,%{user},%{group}) %{_sharedstatedir}/%{name}
%{_datadir}/%{name}
%{_prefix}/lib/firewalld/services/%{name}.xml
%{_unitdir}/%{name}.service

%changelog
* Fri Jul 20 2018 Simone Caronni <negativo17@gmail.com> - 2.0.0.5228-1
- First build.
