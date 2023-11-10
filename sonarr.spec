# mock configuration:
# - Requires network for running yarn/dotnet build

%global commit0 de23182d593e2284972103d505e66dd8d812dfdb
%global date 20231110
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
#global tag %{version}

%global debug_package %{nil}
%define _build_id_links none

%global user %{name}
%global group %{name}

%global dotnet 6.0

%ifarch x86_64
%global rid x64
%endif

%ifarch aarch64
%global rid arm64
%endif

%ifarch armv7hl
%global rid arm
%endif

%if 0%{?fedora} >= 36
%global __requires_exclude ^liblttng-ust\\.so\\.0.*$
%endif

Name:           sonarr
Version:        4.0.0.0
Release:        10%{!?tag:.%{date}git%{shortcommit0}}%{?dist}
Summary:        Automated manager and downloader for TV series
License:        GPLv3
URL:            https://sonarr.tv/

BuildArch:      x86_64 aarch64 armv7hl

%if 0%{?tag:1}
Source0:        https://github.com/Sonarr/Sonarr/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
%else
Source0:        https://github.com/Sonarr/Sonarr/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
%endif

Source10:       %{name}.service
Source11:       %{name}.xml

BuildRequires:  dotnet-sdk-%{dotnet}
BuildRequires:  firewalld-filesystem
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  nodejs
BuildRequires:  systemd
BuildRequires:  tar
BuildRequires:  yarnpkg

Requires:       firewalld-filesystem
Requires(post): firewalld-filesystem
Requires:       libmediainfo
Requires:       sqlite
Requires(pre):  shadow-utils

%if 0%{?rhel} >= 8 || 0%{?fedora}
Requires:       (%{name}-selinux if selinux-policy)
%endif

Obsoletes:      %{name} < 4.0.0

%description
Sonarr is a PVR for Usenet and BitTorrent users. It can monitor multiple RSS
feeds for new episodes of your favorite shows and will grab, sort and rename
them. It can also be configured to automatically upgrade the quality of files
already downloaded when a better quality format becomes available.

%prep
%if 0%{?tag:1}
%autosetup -p1
%else
%autosetup -p1 -n Sonarr-%{commit0}
%endif

# Remove test coverage and Windows specific stuff from project file
pushd src
dotnet sln Sonarr.sln remove \
  NzbDrone.Api.Test \
  NzbDrone.Automation.Test \
  NzbDrone.Common.Test \
  NzbDrone.Core.Test \
  NzbDrone.Host.Test \
  NzbDrone.Integration.Test \
  NzbDrone.Libraries.Test \
  NzbDrone.Mono.Test \
  NzbDrone.Test.Common \
  NzbDrone.Test.Dummy \
  NzbDrone.Update.Test \
  NzbDrone.Windows.Test \
  NzbDrone.Windows \
  ServiceHelpers/ServiceInstall \
  ServiceHelpers/ServiceUninstall
popd

%build
export DOTNET_CLI_TELEMETRY_OPTOUT=1
dotnet msbuild -restore src/Sonarr.sln \
    -p:RuntimeIdentifiers=linux-%{rid} \
    -p:Configuration=Release \
    -p:Platform=Posix \
    -v:normal

# Use a huge timeout for aarch64 builds
yarn install --frozen-lockfile --network-timeout 1000000
yarn run build --mode production

%install
mkdir -p %{buildroot}%{_libdir}/%{name}
mkdir -p %{buildroot}%{_sharedstatedir}/%{name}

cp -a _output/net%{dotnet}/* _output/UI %{buildroot}%{_libdir}/%{name}/

install -D -m 0644 -p %{SOURCE10} %{buildroot}%{_unitdir}/%{name}.service
install -D -m 0644 -p %{SOURCE11} %{buildroot}%{_prefix}/lib/firewalld/services/%{name}.xml

find %{buildroot} -name "*.pdb" -delete
find %{buildroot} -name "ffprobe" -exec chmod 0755 {} \;

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
%license COPYRIGHT.md LICENSE.md SECURITY.md
%doc README.md
%attr(750,%{user},%{group}) %{_sharedstatedir}/%{name}
%{_libdir}/%{name}
%{_prefix}/lib/firewalld/services/%{name}.xml
%{_unitdir}/%{name}.service

%changelog
* Fri Nov 10 2023 Simone Caronni <negativo17@gmail.com> - 4.0.0.0-10.20231110gitde23182
- Update to latest snapshot.

* Mon Oct 30 2023 Simone Caronni <negativo17@gmail.com> - 4.0.0.0-9.20231030git165e3db
- Update to latest snapshot.

* Tue Oct 17 2023 Simone Caronni <negativo17@gmail.com> - 4.0.0.0-8.20231017gita131c88
- Update to latest snapshot.

* Tue Oct 03 2023 Simone Caronni <negativo17@gmail.com> - 4.0.0.0-7.20230930gitb4ef873
- Update to latest snapshot.

* Mon Sep 11 2023 Simone Caronni <negativo17@gmail.com> - 4.0.0.0-6.20230911git0abb4ce
- Update to latest snapshot.
- Change build to more closely match upstream.

* Mon Sep 04 2023 Simone Caronni <negativo17@gmail.com> - 4.0.0.0-5.20230902gitfaecdc8
- Update to latest snapshot.

* Sun Aug 27 2023 Simone Caronni <negativo17@gmail.com> - 4.0.0.0-4.20230823git5a7f42a
- Update to latest snapshot.

* Sun Aug 20 2023 Simone Caronni <negativo17@gmail.com> - 4.0.0.0-3.20230820git866fbc7
- Update to latest snapshot.

* Tue Aug 08 2023 Simone Caronni <negativo17@gmail.com> - 4.0.0.0-2.20230808git65323d5
- Update to latest snapshot.

* Thu Jul 20 2023 Simone Caronni <negativo17@gmail.com> - 4.0.0.0-1.20230720gitdee8820
- Update to 4.x snapshot, switch to .NET.
- Trim changelog.

* Tue Apr 11 2023 Simone Caronni <negativo17@gmail.com> - 3.0.10.1567-1
- Update to 3.0.10.1567.

* Mon Mar 20 2023 Simone Caronni <negativo17@gmail.com> - 3.0.10.1566-1
- Update to 3.0.10.1566.

* Mon Aug 15 2022 Simone Caronni <negativo17@gmail.com> - 3.0.9.1549-1
- Update to 3.0.9.1549.

* Wed May 18 2022 Simone Caronni <negativo17@gmail.com> - 3.0.8.1507-1
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
