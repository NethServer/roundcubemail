%define rcm_version 1.4.11
Name:           roundcubemail
Version: 1.4.11.2
Release: 1%{?dist}
Summary:        Simple, modern & fast web-based email client.
License:        AGPLv3+
Group:          Networking/WWW
URL:            https://roundcube.net/
Source0:        https://github.com/roundcube/roundcubemail/releases/download/%{rcm_version}/%{name}-%{rcm_version}-complete.tar.gz
Source1: roundcubemail.httpd
Source2: roundcubemail.logrotate
Source3: https://github.com/alexandregz/twofactor_gauthenticator/archive/master.zip
Requires:       httpd
Requires:	    php
Requires: php-curl
Requires: php-date
Requires: php-dom
Requires: php-fileinfo
Requires: php-filter
Requires: php-gd
Requires: php-hash
Requires: php-iconv
Requires: php-intl
Requires: php-json
Requires: php-ldap
Requires: php-mbstring
Requires: php-openssl
Requires: php-pcre
Requires: php-pdo
Requires: php-pspell
Requires: php-session
Requires: php-simplexml
Requires: php-sockets
Requires: php-spl
Requires: php-xml

BuildArch:      noarch

%description
RoundCube Webmail is a browser-based multilingual IMAP client
with an application-like user interface. It provides full
functionality you expect from an e-mail client, including MIME
support, address book, folder manipulation, message searching
and spell checking. RoundCube Webmail is written in PHP and 
requires a database: MySQL, PostgreSQL and SQLite are known to
work. The user interface is fully skinnable using XHTML and
CSS 2.

%prep
mkdir %{name}-%{rcm_version}
cd %{name}-%{rcm_version}
tar xzvf %{SOURCE0}

%build
# Nothing to do!!

%install

# create /etc/roundcubemail for first installation
mkdir -p %{buildroot}/etc/%{name}


# Temp directory
mkdir -p %{buildroot}/usr/share/%{name}/temp

# Logs
mkdir -p %{buildroot}/var/log/%{name}

install -d -m 755 %{buildroot}%{_datadir}/%{name}
cp -r %{name}-%{rcm_version}/%{name}-%{rcm_version}/* %{buildroot}%{_datadir}/%{name}

# Link to config file
ln -s /etc/roundcubemail/config.inc.php     %{buildroot}%{_datadir}/%{name}/config/config.inc.php

# Apache with mod_php or php-fpm
install -Dpm 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/httpd/conf.d/%{name}.conf

# Log rotate
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d
cp -pr %SOURCE2 %{buildroot}%{_sysconfdir}/logrotate.d/roundcubemail

# GPG keys
mkdir -p %{buildroot}/usr/share/roundcubemail/enigma

# Plugins directory 2FA
mkdir -p %{buildroot}/usr/share/%{name}/plugins/twofactor_gauthenticator/
unzip %{SOURCE3}
cp -a twofactor_gauthenticator-master/* %{buildroot}/usr/share/%{name}/plugins/twofactor_gauthenticator/

%files
%{_datadir}/%{name}
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/roundcubemail
%dir %attr(0750,apache,apache) %{_datadir}/%{name}/temp
%dir %attr(0750,apache,apache) %{_datadir}/%{name}/enigma
%dir %attr(0750,apache,apache) /var/log/%{name}
%dir %attr(0755,root,root) %{_datadir}/%{name}/plugins/twofactor_gauthenticator
%dir %attr(0755,root,root) /etc/%{name}

%post

%postun

%clean

%changelog
* Wed Nov 03 2021 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.4.11.2-1
- Roundcubemail: Log folder not created - NethServer/dev#6591

* Tue Jul 06 2021 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.4.11.1-1
- Roundcubemail 1.4.11 - NethServer/dev#6541

* Sun Apr 25 2021 stephane de Labrusse <stephdl@de-labrusse.fr> 1.4.11
- Upstream upgrade to 1.4.11

* Wed Oct 7 2020 stephane de Labrusse <stephdl@de-labrusse.fr> 1.4.9
- Upstream upgrade

* Tue Aug 18 2020 stephane de Labrusse <stephdl@de-labrusse.fr> 1.4.8
- Upstream upgrade
- 2FA bundled : https://github.com/alexandregz/twofactor_gauthenticator

* Tue Aug 04 2020 stephane de Labrusse <stephdl@de-labrusse.fr> 1.4.7
- Upstream upgrade

* Wed Apr 29 2020 stephane de Labrusse <stephdl@de-labrusse.fr> 1.4.4
- Upstream upgrade

* Mon Apr 06 2020 stephane de labrusse <stephdl@de-labrusse.fr> 1.4.3-el7
- first release
