Name:           roundcubemail
Version:        1.4.3
Release:        2%{?dist}
Summary:        Simple, modern & fast web-based email client.
License:        AGPLv3+
Group:          Networking/WWW
URL:            https://roundcube.net/
Source0:        https://github.com/roundcube/roundcubemail/releases/download/%{version}/%{name}-%{version}-complete.tar.gz 
Source1: roundcubemail.httpd
Source2: roundcubemail.logrotate
Source3: roundcubemail.template-custom-70USER_PREFERENCES
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
mkdir %{name}-%{version}
cd %{name}-%{version}
tar xzvf %{SOURCE0}

%build
# Nothing to do!!

%install

# Temp directory
mkdir -p %{buildroot}/usr/share/%{name}/temp

# Logs
mkdir -p %{buildroot}/usr/share/%{name}/logs

install -d -m 755 %{buildroot}%{_datadir}/%{name}
cp -r %{name}-%{version}/%{name}-%{version}/* %{buildroot}%{_datadir}/%{name}

# Link to config file
ln -s /etc/roundcubemail/config.inc.php     %{buildroot}%{_datadir}/%{name}/config/config.inc.php

# Apache with mod_php or php-fpm
install -Dpm 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/httpd/conf.d/%{name}.conf

# Log rotate
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d
cp -pr %SOURCE2 %{buildroot}%{_sysconfdir}/logrotate.d/roundcubemail

# GPG keys
mkdir -p %{buildroot}/usr/share/roundcubemail/enigma

# custom-template
mkdir -p %{buildroot}%{_sysconfdir}/e-smith/templates-custom/etc/roundcubemail/config.inc.php
cp -pr %SOURCE3 %{buildroot}%{_sysconfdir}/e-smith/templates-custom/etc/roundcubemail/config.inc.php/70USER_PREFERENCES



%files
%{_datadir}/%{name}
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/roundcubemail
%dir %attr(0750,apache,apache) %{_datadir}/%{name}/temp
%dir %attr(0750,apache,apache) %{_datadir}/%{name}/enigma
%dir %attr(0750,apache,apache) %{_datadir}/%{name}/logs
%{_sysconfdir}/e-smith/templates-custom/etc/roundcubemail/config.inc.php/70USER_PREFERENCES
%post
%postun

%changelog
* Mon Apr 06 2020 stephane de labrusse <stephdl@de-labrusse.fr> 1.4.3-el7
- first release
