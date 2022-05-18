%global user %{name}
%global group %{name}

Name:           sonarr
Version:        3.0.8.1507
Release:        1%{?dist}
Summary:        Automated manager and downloader for TV series
License:        GPLv3
URL:            https://sonarr.tv/
BuildArch:      noarch

Source0:        https://download.sonarr.tv/v3/main/%{version}/Sonarr.main.%{version}.linux.tar.gz
Source1:        https://raw.githubusercontent.com/Sonarr/Sonarr/phantom-develop/COPYRIGHT.md
Source2:        https://raw.githubusercontent.com/Sonarr/Sonarr/phantom-develop/LICENSE.md
Source3:        https://raw.githubusercontent.com/Sonarr/Sonarr/phantom-develop/README.md
Source10:       %{name}.service
Source11:       %{name}.xml

BuildRequires:  firewalld-filesystem
BuildRequires:  systemd
BuildRequires:  tar

Requires:       firewalld-filesystem
Requires(post): firewalld-filesystem
Requires:       mono-core
Requires:       libmediainfo
Requires(pre):  shadow-utils
Requires:       sqlite

%description
Sonarr is a PVR for Usenet and BitTorrent users. It can monitor multiple RSS
feeds for new episodes of your favorite shows and will grab, sort and rename
them. It can also be configured to automatically upgrade the quality of files
already downloaded when a better quality format becomes available.

%prep
%autosetup -n Sonarr
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
* Tue May 18 2022 Jacob K <j8kap@hotmail.com> - 3.0.8.1507-1
- Update to 3.0.8.1507.

* Mon Mar 07 2022 Simone Caronni <negativo17@gmail.com> - 3.0.7.1477-1
- Update to 3.0.7.1477.

* Sun Jun 20 2021 Jacob K <j8kap@hotmail.com> - 3.0.6.1342-1
- Update to 3.0.6.1342.

* Sun Jun 20 2021 Simone Caronni <negativo17@gmail.com> - 3.0.6.1266-1
- Update to 3.0.6.1266.

* Mon Apr 19 2021 Simone Caronni <negativo17@gmail.com> - 3.0.6.1196-1
- Update to 3.0.6.1196 from main branch.

* Sun Mar 07 2021 Simone Caronni <negativo17@gmail.com> - 3.0.4.1139-1
- Update to 3.0.4.1139.

* Thu Feb 11 2021 Simone Caronni <negativo17@gmail.com> - 3.0.4.1126-1
- Update to 3.0.4.1126.

* Tue Feb 02 2021 Simone Caronni <negativo17@gmail.com> - 3.0.4.1096-1
- Update to 3.0.4.1096.

* Thu Jan 21 2021 Simone Caronni <negativo17@gmail.com> - 3.0.4.1080-1
- Update to 3.0.4.1080.

* Thu Jan  7 2021 Simone Caronni <negativo17@gmail.com> - 3.0.4.1059-1
- Update to 3.0.4.1059.

* Sat Dec 26 2020 Simone Caronni <negativo17@gmail.com> - 3.0.4.1039-1
- Update to 3.0.4.1039.

* Tue Dec 08 2020 Simone Caronni <negativo17@gmail.com> - 3.0.4.1024-1
- Update to 3.0.4.1024.

* Sat Nov 21 2020 Simone Caronni <negativo17@gmail.com> - 3.0.4.1017-1
- Update to 3.0.4.1017.

* Tue Nov 17 2020 Simone Caronni <negativo17@gmail.com> - 3.0.4.1009-1
- Update to 3.0.4.1009.

* Thu Nov 05 2020 Simone Caronni <negativo17@gmail.com> - 3.0.4.993-1
- Update to 3.0.4.993.

* Thu Oct 29 2020 Simone Caronni <negativo17@gmail.com> - 3.0.4.991-1
- Update to 3.0.4.991.

* Fri Oct 16 2020 Simone Caronni <negativo17@gmail.com> - 3.0.4.982-1
- Update to 3.0.4.982.

* Tue Oct 06 2020 Simone Caronni <negativo17@gmail.com> - 3.0.3.955-1
- Update to 3.0.3.955.

* Tue Aug 25 2020 Simone Caronni <negativo17@gmail.com> - 3.0.3.911-1
- Update to 3.0.3.911.

* Sun Aug 16 2020 Simone Caronni <negativo17@gmail.com> - 3.0.3.907-1
- Update to 3.0.3.907.

* Tue Jul 14 2020 Simone Caronni <negativo17@gmail.com> - 3.0.3.899-1
- Update to 3.0.3.899.

* Sun Jun 28 2020 Simone Caronni <negativo17@gmail.com> - 3.0.3.896-1
- Update to 3.0.3.896.

* Wed Apr 01 2020 Simone Caronni <negativo17@gmail.com> - 2.0.0.5344-1
- Update to 2.0.0.5344.

* Sun Sep 08 2019 Simone Caronni <negativo17@gmail.com> - 2.0.0.5338-1
- Update to 2.0.0.5338.

* Mon Apr 01 2019 Simone Caronni <negativo17@gmail.com> - 2.0.0.5322-1
- Update to 2.0.0.5322.

* Thu Jan 24 2019 Simone Caronni <negativo17@gmail.com> - 2.0.0.5301-1
- Update to 2.0.0.5301.

* Wed Oct 10 2018 Simone Caronni <negativo17@gmail.com> - 2.0.0.5252-1
- Update to 2.0.0.5252.

* Fri Jul 20 2018 Simone Caronni <negativo17@gmail.com> - 2.0.0.5228-1
- First build.
