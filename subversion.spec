# disable the stupid rpmlint shit from hell!!!
%define _build_pkgcheck_set %{nil}
%define _build_pkgcheck_srpm %{nil}

%define _disable_ld_no_undefined 1

%define apache_version 2.4.0
%define libsvn %mklibname svn 0
%define libsvngnomekeyring %mklibname svn-gnome-keyring 0
%define libsvnkwallet %mklibname svn-kwallet 0

# Java requires devel symlinks in non-devel packages due to design
# (System.loadLibrary). Do not add -devel dependencies.
%if %{_use_internal_dependency_generator}
%define __noautoreqfiles '%{_libdir}/libsvnjavahl-%{svnjavahl_api}\\.so$'
%define __noautoreq 'devel\\(libneon(.*)\\)'
%else
%define _exclude_files_from_autoreq ^%{_libdir}/libsvnjavahl-%{svnjavahl_api}.so$
%define _requires_exceptions devel(libneon
%endif

%define build_python 1
%{?_without_python: %{expand: %%global build_python 0}}

%define build_ruby 1
%{?_without_ruby: %{expand: %%global build_ruby 0}}

%define build_java 1
%{?_with_java: %{expand: %%global build_java 1}}

%define build_perl 1
%{?_without_perl: %{expand: %%global build_perl 0}}

%define build_gnome_keyring 1
%{?_without_gnome_keyring: %{expand: %%global build_gnome_keyring 0}}

%define build_kwallet 1
%{?_without_kwallet: %{expand: %%global build_kwallet 0}}

%define build_test 0
%{?_with_test: %{expand: %%global build_test 1}}

%define with_debug 0
%{?_with_debug: %{expand: %%global with_debug 1}}

%if %{build_java}
# We have the non-major symlink also in this package (due to java design),
# so we only have %api in package name.
%define svnjavahl_api 1
%define libsvnjavahl %mklibname svnjavahl %{svnjavahl_api}
%endif

%ifarch %mips %arm
%define build_java 0
%endif

Summary:	A Concurrent Versioning System
Name:		subversion
Version:	1.7.5
Release:	3
Epoch:		2
License:	BSD CC2.0
Group:		Development/Other
URL:		http://subversion.apache.org/
Source0:	http://www.apache.org/dist/subversion/%{name}-%{version}.tar.bz2
Source1:	http://www.apache.org/dist/subversion/%{name}-%{version}.tar.bz2.asc
Source2:	svnserve.service
Source3:	svnserve.sysconf
Source5:	%{name}-1.3.0-global-config
Source6:	%{name}-1.3.0-global-servers
Source7:	http://svnbook.red-bean.com/nightly/en/svn-book-html-chunk.tar.bz2
Patch0:		subversion-1.7.0-rc3-no_tests.diff
Patch1:		svn-ruby-1.9-fixes.patch
Patch2:		svn-update-ruby-tests.patch
Patch3:		subversion-1.7.5-kdewallet.cpp-g++-fix.patch
BuildRequires:	autoconf automake libtool
BuildRequires:	chrpath
BuildRequires:	python
BuildRequires:	texinfo
BuildRequires:	info-install
BuildRequires:	db-devel
BuildRequires:	pkgconfig(neon)
BuildRequires:	apache-devel >= %{apache_version}
BuildRequires:	pkgconfig(apr-1)
BuildRequires:	pkgconfig(apr-util-1)
BuildRequires:	libxslt-proc
BuildRequires:	docbook-style-xsl
BuildRequires:	doxygen
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	krb5-devel
BuildRequires:	magic-devel
# Swig is runtime only
BuildRequires:	swig >= 1.3.27
# needs this despite build_ruby 0
BuildRequires:	ruby
BuildRequires:	ruby-devel
BuildRequires:	ruby-rdoc
Provides:	%{name}-ra-method = %{EVRD}
Provides:	%{name}-client-tools = %{EVRD}
Provides:	svn = %{EVRD}
Requires:	%{libsvn} >= %{EVRD}

%description
Subversion (SVN) is a concurrent version control system which enables one or
more users to collaborate in developing and maintaining a hierarchy of files
and directories while keeping a history of all changes.  Subversion only stores
the differences between versions, instead of every complete file.  Subversion
also keeps a log of who, when, and why changes occured.

As such it basically does the same thing CVS does (Concurrent Versioning
System) but has major enhancements compared to CVS and fixes a lot of the
annoyances that CVS users face.

This package contains the client, if you're looking for the server end
of things you want %{name}-repos.

%package	doc
Summary:	Subversion Documenation
Group:		Development/Other

%description	doc
Subversion is a concurrent version control system which enables
one or more users to collaborate in developing and maintaining a
hierarchy of files and directories while keeping a history of all
changes. Subversion only stores the differences between versions,
instead of every complete file. Subversion also keeps a log of
who, when, and why changes occured.

As such it basically does the same thing CVS does (Concurrent
Versioning System) but has major enhancements compared to CVS and
fixes a lot of the annoyances that CVS users face.

This package contains the subversion book and design info files.

%package -n	%{libsvn}
Summary:	Subversion libraries
Group:		System/Libraries

%description -n	%{libsvn}
Subversion common libraries

%if %{build_gnome_keyring}
%package -n	%{libsvngnomekeyring}
Summary:	gnome-keyring support for svn
Group:		System/Libraries
BuildRequires:	pkgconfig(gnome-keyring-1)
BuildRequires:	pkgconfig(dbus-1)
Requires:	gnome-keyring >= 2.26.1

%description -n	%{libsvngnomekeyring}
Subversion libraries that allow interaction with the gnome-keyring daemon
%endif

%if %{build_kwallet}
%package -n	%{libsvnkwallet}
Summary:	kwallet support for svn
Group:		System/Libraries
BuildRequires:	kdelibs4-devel
BuildRequires:	pkgconfig(dbus-1)
Requires:	kwallet

%description -n	%{libsvnkwallet}
Subversion libraries that allow interaction with the kwallet daemon.
%endif

%package	server
Summary:	Subversion Server
Group:		System/Servers
Requires:	%{name} >= %{EVRD}
# soname didn't change between 1.3.x and 1.4.x, but we
# need the right one...
Requires:	%{libsvn} >= %{EVRD}

%description	server
This package contains a myriad of tools for subversion server
and repository admins:
  * hot-backup makes a backup of a svn repo without stopping
  * mirror_dir_through_svn.cgi 
  * various hook scripts
  * xslt example 

Note that cvs2svn has moved out of subversion and is a separate
project.  It has not released its own package yet, but you can
find it at http://cvs2svn.tigris.org/

%package	tools
Summary:	Subversion Repo/Server Tools
Group:		Development/Other
Requires:	%{name} >= %{EVRD}
# soname didn't change between 1.3.x and 1.4.x, but we
# need the right one...
Requires:	%{libsvn} >= %{epoch}:%{version}

%description	tools
This package contains a myriad of tools for subversion server
and repository admins:
  * hot-backup makes a backup of a svn repo without stopping
  * mirror_dir_through_svn.cgi 
  * various hook scripts
  * xslt example 

Note that cvs2svn has moved out of subversion and is a separate
project.  It has not released its own package yet, but you can
find it at http://cvs2svn.tigris.org/


%if %{build_python}
%package -n	python-svn
Summary:	Python bindings for Subversion
Group:		Development/Python
%py_requires -d
Provides:	python-subversion = %{version}-%{release}
Requires:	python
# soname didn't change between 1.3.x and 1.4.x, but we
# need the right one...
Requires:	%{libsvn} >= %{EVRD}

%description -n	python-svn
This package contains the files necessary to use the subversion
library functions within python scripts.
%endif

%if %{build_ruby}
%package -n	ruby-svn
Summary:	Ruby bindings for Subversion
Group:		Development/Ruby
Requires:	ruby
Requires:	%{libsvn} >= %{EVRD}
Provides:	ruby-subversion = %{EVRD}

%description -n	ruby-svn
This package contains the files necessary to use the subversion
library functions within ruby scripts.
%endif

%if %{build_java}
%package -n	%{libsvnjavahl}
Summary:	Svn Java bindings library
Group:		System/Libraries
Conflicts:	subversion-devel < 2:1.6.0-3
Obsoletes:	%{_lib}svnjavahl0 < 2:1.6.0-3

%description -n	%{libsvnjavahl}
Svn Java bindings library

%package -n	svn-javahl
Summary:	Java bindings for Subversion
Group:		Development/Java
Obsoletes:	java-svn < %{EVRD}
Provides:	java-svn = %{EVRD}
Provides:	java-subversion = %{EVRD}
Requires:	%{name} >= %{EVRD}
Requires:	%{libsvn} >= %{EVRD}
Requires:	%{libsvnjavahl} >= %{EVRD}
BuildRequires:	java-devel
BuildRequires:	ant
BuildRequires:	jpackage-utils >= 1.7.3-10
BuildRequires:	junit

%description -n	svn-javahl
This package contains the files necessary to use the subversion
library functions from Java.
%endif

%if %{build_perl}
%package -n	perl-SVN
Summary:	Perl bindings for Subversion
Group:		Development/Perl
BuildRequires:	perl-devel
Requires:	%{name} >= %{EVRD}
Obsoletes:	perl-svn < %{EVRD}
Provides:	perl-svn = %{EVRD}
Requires:	%{libsvn} >= %{EVRD}

%description -n	perl-SVN
This package contains the files necessary to use the subversion
library functions within perl scripts.
%endif

%package	devel
Summary:	Subversion headers/libraries for development
Group:		Development/C
Provides:	libsvn-devel = %{EVRD}
%if %{build_perl}
Requires:	perl-SVN >= %{EVRD}
Obsoletes:	perl-SVN-devel < 2:1.5.2-2
Provides:	per-SVN-devel = %{EVRD}
%endif
%if %{build_perl}
Requires:	python-svn >= %{EVRD}
Obsoletes:	python-svn-devel < 2:1.5.2-2
Provides:	python-svn-devel = %{EVRD}
%endif
%if %{build_ruby}
Requires:	ruby-svn >= %{EVRD}
Obsoletes:	ruby-svn-devel < 2:1.5.2-2
Provides:	ruby-svn-devel = %{EVRD}
%endif
Requires:	%{libsvn} >= %{EVRD}
Requires:	neon-devel
%if %{build_gnome_keyring}
Requires:	%{libsvngnomekeyring} >= %{EVRD}
%endif
%if %{build_kwallet}
Requires:	%{libsvnkwallet} >= %{EVRD}
%endif

%description devel
This package contains the header files and linker scripts for
subversion libraries.

%package -n	apache-mod_dav_svn
Summary:	Subversion server DSO module for apache
Group:		System/Servers
Requires:	%{name}-tools >= %{EVRD}
Requires:	apache >= %{apache_version}
Requires:	apache-mod_dav >= %{apache_version}
# soname didn't change between 1.3.x and 1.4.x, but we
# need the right one...
Requires(pre):	%{libsvn} >= %{EVRD}
Obsoletes:	apache-mod_authz_svn

%description -n	apache-mod_dav_svn
Subversion is a concurrent version control system which enables
one or more users to collaborate in developing and maintaining a
hierarchy of files and directories while keeping a history of all
changes. Subversion only stores the differences between versions,
instead of every complete file. Subversion also keeps a log of
who, when, and why changes occured.

As such it basically does the same thing CVS does (Concurrent
Versioning System) but has major enhancements compared to CVS and
fixes a lot of the annoyances that CVS users face.

This package contains the apache server extension DSO for running
a subversion server.

%package -n	apache-mod_dontdothat
Summary:	An Apache module that allows you to block specific types of Subversion requests
Group:		System/Servers
Requires:	apache >= %{apache_version}
Requires:	apache-mod_dav_svn = %{EVRD}

%description -n apache-mod_dontdothat
mod_dontdothat is an Apache module that allows you to block specific types
of Subversion requests.  Specifically, it's designed to keep users from doing
things that are particularly hard on the server, like checking out the root
of the tree, or the tags or branches directories.  It works by sticking an
input filter in front of all REPORT requests and looking for dangerous types
of requests.  If it finds any, it returns a 403 Forbidden error.

%prep
%setup -q -a7

# don't build the tests as we're not running make test since many many years...
%patch0 -p0

%patch1 -p0 -b .ruby19_1~
%patch2 -p0 -b .ruby19_2~

%patch3 -p1 -b .gcc47

# fix shellbang lines, #111498
perl -pi -e 's|/usr/bin/env perl|%{_bindir}/perl|g' tools/hook-scripts/*.pl.in

# fix file perms
chmod 644 BUGS CHANGES COMMITTERS INSTALL README

# move latest svnbook snapshot as their target version
mv svn-book-html-chunk svnbook-1.7

# lib64 fixes
perl -pi -e "s|/lib\b|/%{_lib}|g" \
    build/ac-macros/serf.m4 \
    build/ac-macros/apr_memcache.m4 \
    build/ac-macros/berkeley-db.m4 \
    build/ac-macros/sasl.m4 \
    build/ac-macros/sqlite.m4 \
    build/ac-macros/zlib.m4 \
    configure*

./autogen.sh --release

cp %{SOURCE2} .
cp %{SOURCE3} .

%build
%serverbuild

%if %{build_java}
export JAVADIR=%{_jvmdir}/java
export JAVA_HOME=%{_jvmdir}/java
%endif

%configure2_5x \
    --localstatedir=/var/lib \
    --with-apr_memcache=%{_prefix} \
    --with-apxs=%{_bindir}/apxs \
    --with-apache-libexecdir=%{_libdir}/apache \
    --with-apr=%{_bindir}/apr-1-config \
    --with-apr-util=%{_bindir}/apu-1-config \
    --with-editor=vim \
    --disable-mod-activation \
    --with-swig=%{_prefix} \
    --disable-static \
%if %{with_debug}
    --enable-maintainer-mode \
    --enable-debug \
%endif
%if %{build_java}
    --enable-javahl \
    --with-jdk=%{_jvmdir}/java \
    --with-junit=%{_javadir}/junit.jar \
%endif
%if %{build_gnome_keyring}
    --with-gnome-keyring \
%endif
%if %build_kwallet
    --with-kwallet \
%endif
    --enable-shared \
    --with-gssapi=%{_prefix} \
    --with-libmagic=%{_prefix} \
    --disable-neon-version-check \
    --with-sqlite=%{_prefix}

%make all

%if %{build_python}
make swig-py swig_pydir=%{py_platsitedir}/libsvn swig_pydir_extra=%{py_sitedir}/svn
%endif

%if %{build_perl}
make swig-pl
pushd  subversion/bindings/swig/perl/native
	perl Makefile.PL
popd
%endif

%if %{build_ruby}
make swig-rb
%endif

%if %{build_java}
make javahl
%endif

%check
%if %{build_test}
make check
%endif

%install
%makeinstall_std

%if %{build_python}
%makeinstall_std install-swig-py swig_pydir=%{py_platsitedir}/libsvn swig_pydir_extra=%{py_sitedir}/svn
# Precompile python
%py_compile %{buildroot}/%{py_platsitedir}/libsvn
%py_compile %{buildroot}/%{py_sitedir}/svn
%endif

%if %{build_perl}
%makeinstall_std install-swig-pl-lib
pushd subversion/bindings/swig/perl/native/
perl Makefile.PL
%makeinstall_std
popd
%endif

%if %{build_ruby}
%makeinstall_std install-swig-rb
%endif
%if %{build_java}
%makeinstall_std install-javahl

%__mkdir_p %{buildroot}%{_javadir}
%__mv %{buildroot}%{_libdir}/svn-javahl/svn-javahl.jar %{buildroot}%{_javadir}/svn-javahl-%{version}.jar
%__ln_s svn-javahl-%{version}.jar %{buildroot}%{_javadir}/svn-javahl.jar

%{_bindir}/chrpath -d %{buildroot}%{_libdir}/libsvnjavahl-1.so
%endif

%if %{build_perl}
# perl bindings
make pure_vendor_install -C subversion/bindings/swig/perl/native DESTDIR=%{buildroot}
%endif

install -d %{buildroot}%{_sysconfdir}/httpd/modules.d
echo "LoadModule dav_svn_module %{_libdir}/apache/mod_dav_svn.so" > %{buildroot}%{_sysconfdir}/httpd/modules.d/146_mod_dav_svn.conf
echo "LoadModule authz_svn_module %{_libdir}/apache/mod_authz_svn.so" > %{buildroot}%{_sysconfdir}/httpd/modules.d/147_mod_authz_svn.conf

cat > %{buildroot}%{_sysconfdir}/httpd/modules.d/148_mod_dontdothat.conf << EOF
LoadModule dontdothat_module %{_libdir}/apache/mod_dontdothat.so

<Location /svn>
    DAV svn
    SVNParentPath /var/lib/svn/repositories
    DontDoThatConfigFile %{_sysconfdir}/httpd/conf/dontdothat.conf
</Location>
EOF

install -d %{buildroot}%{_sysconfdir}/httpd/conf
cat > %{buildroot}%{_sysconfdir}/httpd/conf/dontdothat.conf << EOF
[recursive-actions]
/*/trunk = allow
/ = deny
/* = deny
/*/tags = deny
/*/branches = deny
/*/* = deny
/*/*/tags = deny
/*/*/branches = deny
EOF

######################
###  client-tools  ###
######################
install -d -m 755 %{buildroot}%{_sysconfdir}/bash_completion.d
install -m 644 tools/client-side/bash_completion \
    %{buildroot}%{_sysconfdir}/bash_completion.d/subversion

# Global configs
install -d -m 755 %{buildroot}%{_sysconfdir}/subversion
install -m 644 %{SOURCE5} %{buildroot}%{_sysconfdir}/subversion/config
install -m 644 %{SOURCE6} %{buildroot}%{_sysconfdir}/subversion/servers

####################
###  repo-tools  ###
####################
# hotbackup tool
install -m 755 tools/backup/hot-backup.py %{buildroot}%{_bindir}
(cd %{buildroot}%{_bindir}; ln -sf  hot-backup.py hot-backup)

# hook-scripts
install -d -m755 %{buildroot}%{_datadir}/%{name}-%{version}/repo-tools/hook-scripts
pushd tools/hook-scripts
install -m 644 commit-access-control.cfg.example %{buildroot}/%{_datadir}/%{name}-%{version}/repo-tools/hook-scripts
install -m 755 commit-access-control.pl %{buildroot}/%{_datadir}/%{name}-%{version}/repo-tools/hook-scripts
install -m 644 svnperms.conf.example %{buildroot}/%{_datadir}/%{name}-%{version}/repo-tools/hook-scripts
install -m 755 svnperms.py %{buildroot}/%{_datadir}/%{name}-%{version}/repo-tools/hook-scripts
install -m 755 mailer/mailer.py %{buildroot}/%{_datadir}/%{name}-%{version}/repo-tools/hook-scripts
install -m 644 mailer/mailer.conf.example %{buildroot}/%{_datadir}/%{name}-%{version}/repo-tools/hook-scripts
install -m 755 commit-email.rb %{buildroot}/%{_datadir}/%{name}-%{version}/repo-tools/hook-scripts
install -m 755 log-police.py %{buildroot}/%{_datadir}/%{name}-%{version}/repo-tools/hook-scripts
install -m 755 svn2feed.py %{buildroot}/%{_datadir}/%{name}-%{version}/repo-tools/hook-scripts
install -m 755 validate-extensions.py %{buildroot}/%{_datadir}/%{name}-%{version}/repo-tools/hook-scripts
install -m 755 verify-po.py %{buildroot}/%{_datadir}/%{name}-%{version}/repo-tools/hook-scripts
popd

#xslt
install -d -m755 %{buildroot}%{_datadir}/%{name}-%{version}/repo-tools/xslt
install -m 644 tools/xslt/svnindex.css %{buildroot}%{_datadir}/%{name}-%{version}/repo-tools/xslt
install -m 644 tools/xslt/svnindex.xsl %{buildroot}%{_datadir}/%{name}-%{version}/repo-tools/xslt

# fix a missing file...
ln -sf libsvn_diff-1.so.0.0.0 %{buildroot}%{_libdir}/libsvn_diff.so

%{_bindir}/chrpath -d %{buildroot}%{_bindir}/svn
%{_bindir}/chrpath -d %{buildroot}%{_bindir}/svnlook
%{_bindir}/chrpath -d %{buildroot}%{_bindir}/svnversion
%{_bindir}/chrpath -d %{buildroot}%{_bindir}/svnserve
%{_bindir}/chrpath -d %{buildroot}%{_bindir}/svnadmin
%{_bindir}/chrpath -d %{buildroot}%{_bindir}/svndumpfilter
%{_bindir}/chrpath -d %{buildroot}%{_bindir}/svnsync

# fix the stupid rpath stuff...
find %{buildroot}%{perl_vendorarch} -type f -name "*.so" | xargs chrpath -d

# handle translations
%find_lang %{name}

# Install svnserve bits
install -d %{buildroot}/var/run/svnserve
install -d %{buildroot}/var/lib/svn/repositories
install -d %{buildroot}/lib/systemd/system
install -d %{buildroot}%{_sysconfdir}/sysconfig

install -m0644 svnserve.service %{buildroot}/lib/systemd/system/svnserve.service
install -m0644 svnserve.sysconf %{buildroot}%{_sysconfdir}/sysconfig/svnserve

# Move perl man
mv %{buildroot}%{_prefix}/local/share/man/man3/* %{buildroot}%{_mandir}/man3/

# cleanup
find %{buildroot} -name "perllocal.pod" | xargs rm -f

%pre server
%_pre_useradd svn /var/lib/svn /bin/false

%post server
# Libraries for REPOS ( Repository ) and FS ( filesystem backends ) are in
# server now, so we need a ldconfig
# fix svn entries in /etc/services
if ! grep -qE '^svn[[:space:]]+3690/(tcp|udp)[[:space:]]+svnserve' %{_sysconfdir}/services; then
	# cleanup
	sed -i -e '/^svn\(serve\)\?/d;/^# svnserve ports added by subversion-server/d' %{_sysconfdir}/services
	echo "# svnserve ports added by subversion-server" >> /etc/services
	echo -e "svn\t3690/tcp\tsvnserve\t# Subversion svnserve" >> /etc/services
	echo -e "svn\t3690/udp\tsvnserve\t# Subversion svnserve" >> /etc/services
fi
if [ $1 -eq 1 ] ; then 
    # Initial installation 
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

%postun server
%_postun_userdel svn
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /bin/systemctl try-restart svnserve.service >/dev/null 2>&1 || :
fi

%preun server
if [ $1 = 0 ]; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable svnserve.service > /dev/null 2>&1 || :
    /bin/systemctl stop svnserve.service > /dev/null 2>&1 || :
fi

%post -n apache-mod_dav_svn
/bin/systemctl daemon-reload >/dev/null 2>&1 || :

%postun -n apache-mod_dav_svn
if [ "$1" = "0" ]; then
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

%post -n apache-mod_dontdothat
/bin/systemctl daemon-reload >/dev/null 2>&1 || :

%postun -n apache-mod_dontdothat
if [ "$1" = "0" ]; then
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

%files -f %{name}.lang
%{_sysconfdir}/bash_completion.d/subversion
%{_bindir}/svn
%{_bindir}/svnversion
%{_bindir}/svnlook
%{_mandir}/man1/svn.*
%{_mandir}/man1/svnlook.*
%{_mandir}/man1/svnversion.*
%{_mandir}/man1/svnsync.*
%dir %{_datadir}/subversion-%{version}

%files doc
%doc svnbook-1.*
%doc doc/user/*.html
%doc doc/user/*.txt

%if %{build_gnome_keyring}
%files -n %{libsvngnomekeyring}
# list all ra libs to make sure we don't miss any
# in a bogus build
%{_libdir}/libsvn_auth_gnome_keyring-1.so.0*
%endif

%if %{build_kwallet}
%files -n %{libsvnkwallet}
# list all ra libs to make sure we don't miss any
# in a bogus build
%{_libdir}/libsvn_auth_kwallet-1.so.0*
%endif

%files -n %{libsvn}
%config(noreplace) %{_sysconfdir}/subversion/*
# list all ra libs to make sure we don't miss any
# in a bogus build
%{_libdir}/libsvn_ra-1.so.*
%{_libdir}/libsvn_ra_local-1.so.*
%{_libdir}/libsvn_ra_svn-1.so.*
%{_libdir}/libsvn_ra_neon-1.so.*
%{_libdir}/libsvn_client*so.*
%{_libdir}/libsvn_wc-*so.*
%{_libdir}/libsvn_delta-*so.*
%{_libdir}/libsvn_subr-*so.*
%{_libdir}/libsvn_diff-*so.*
%{_libdir}/libsvn_fs*.so.*
%{_libdir}/libsvn_repos-*.so.*

%files server
%doc BUGS CHANGES COMMITTERS INSTALL
%config(noreplace) %{_sysconfdir}/sysconfig/svnserve
%{_bindir}/svnserve
/lib/systemd/system/svnserve.service
/var/run/svnserve
/var/lib/svn
%{_mandir}/man8/svnserve.8*
%{_mandir}/man5/svnserve.conf.5*

%files tools
%{_bindir}/hot-backup*
%{_bindir}/svnadmin
%{_bindir}/svnsync
%{_bindir}/svndumpfilter
%{_bindir}/svnrdump
%{_datadir}/%{name}-%{version}/repo-tools
%{_mandir}/man1/svnadmin.1*
%{_mandir}/man1/svndumpfilter.1*
%{_mandir}/man1/svnrdump.1*

%if %{build_ruby}
%files -n ruby-svn
%{ruby_sitearchdir}/svn
%{ruby_sitelibdir}/*/*.rb
%{_libdir}/libsvn_swig_ruby*.so.*
%endif

%if %{build_python}
%files -n python-svn
%doc tools/examples/*.py subversion/bindings/swig/INSTALL subversion/bindings/swig/NOTES
%{_libdir}/libsvn_swig_py*.so.*
%{py_sitedir}/svn
%{py_platsitedir}/libsvn
%endif

%if %{build_java}
%files -n %{libsvnjavahl}
%{_libdir}/libsvnjavahl-%{svnjavahl_api}.*

%files -n svn-javahl
%doc subversion/bindings/javahl/README
%{_javadir}/svn-javahl.jar
%{_javadir}/svn-javahl-%{version}.jar
%endif

%if %{build_perl}
%files -n perl-SVN
%doc subversion/bindings/swig/INSTALL subversion/bindings/swig/NOTES
%{_libdir}/libsvn_swig_perl*.so.*
%{perl_vendorarch}/SVN
%{perl_vendorarch}/auto/SVN
%{perl_sitearch}/*
%{_mandir}/man3/SVN::*.3*
%endif

%files devel
%doc tools/examples/minimal_client.c
%{_includedir}/subversion*/*
%{_libdir}/libsvn*.so
%if %{build_java}
%exclude %{_libdir}/libsvnjavahl*
%endif

%files -n apache-mod_dav_svn
%doc subversion/mod_authz_svn/INSTALL
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/146_mod_dav_svn.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/147_mod_authz_svn.conf
%attr(0755,root,root) %{_libdir}/apache/mod_dav_svn.so
%attr(0755,root,root) %{_libdir}/apache/mod_authz_svn.so

%files -n apache-mod_dontdothat
%doc tools/server-side/mod_dontdothat/README
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/148_mod_dontdothat.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/conf/dontdothat.conf
%attr(0755,root,root) %{_libdir}/apache/mod_dontdothat.so


%changelog
* Mon May 21 2012 Bernhard Rosenkraenzer <bero@bero.eu> 2:1.7.5-1
+ Revision: 799743
- Update to 1.7.5
- Drop now-obsolete apache241 patch

* Sun Mar 11 2012 Oden Eriksson <oeriksson@mandriva.com> 2:1.7.4-3
+ Revision: 784194
- the mod_dontdothat modules is already built and installed correctly
- delete what's not needed anymore

* Fri Mar 09 2012 Oden Eriksson <oeriksson@mandriva.com> 2:1.7.4-2
+ Revision: 783673
- fix build with java
- use java-1.6.0-devel for java since java-1.7.0-devel don't work yet
- re-enable java, gnome, kde to see if it works

* Fri Mar 09 2012 Oden Eriksson <oeriksson@mandriva.com> 2:1.7.4-1
+ Revision: 783662
- 1.7.4
- simplify the apache config
- fix build with apache 2.4
- new svn-book
- drop xinetd and use the systemd config from fedora
- various fixes
- use 201200
- spooky
- 1.7.3
- new svn-book
- mod_dontdothat is back

* Sat Feb 11 2012 Oden Eriksson <oeriksson@mandriva.com> 2:1.7.2-5
+ Revision: 772840
- rebuild

* Sat Feb 04 2012 Nicolas Lécureuil <nlecureuil@mandriva.com> 2:1.7.2-4
+ Revision: 771181
- Rebuild against new ruby

  + Bernhard Rosenkraenzer <bero@bero.eu>
    - Allow building with ruby 1.9

* Mon Jan 23 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 2:1.7.2-3
+ Revision: 766977
- rebuild against perl 5.14.2

* Sun Jan 22 2012 Oden Eriksson <oeriksson@mandriva.com> 2:1.7.2-2
+ Revision: 765970
- rebuilt for perl-5.14.2

* Mon Jan 09 2012 Bernhard Rosenkraenzer <bero@bero.eu> 2:1.7.2-1
+ Revision: 759210
- If EDITOR, VISUAL and SVN_EDITOR are all unset, try vim
  instead of erroring out
- Update to 1.7.2

* Fri Dec 16 2011 Nicolas Lécureuil <nlecureuil@mandriva.com> 2:1.7.1-4
+ Revision: 743087
- Rebuild because of *AGAIN* a BS failure
- Rebuild to fix deps

* Tue Nov 29 2011 Oden Eriksson <oeriksson@mandriva.com> 2:1.7.1-2
+ Revision: 735463
- delete all libtool .la files

* Tue Nov 29 2011 Oden Eriksson <oeriksson@mandriva.com> 2:1.7.1-1
+ Revision: 735409
- spec file massage
- drop redundant cruft
- 1.7.1
- new svn-book

* Sat Oct 15 2011 Oden Eriksson <oeriksson@mandriva.com> 2:1.7.0-2
+ Revision: 704770
- enabled the ruby support again (thanks peroyvind), now waiting for java...

* Thu Oct 13 2011 Oden Eriksson <oeriksson@mandriva.com> 2:1.7.0-1
+ Revision: 704603
- another try... this is getting boring...
- disable ruby for now because of broken ruby (r698552)
- more guesswork (br: ruby, ruby-rdoc)
- whoops! :-)
- hmmm..., guessing "BuildRequires: automake" is missing
- 1.7.0
- new svn-book-html-chunk
- added backport/update spec file macros
- disable the java crap for now
- 1.7.0-rc4
- cleanups
- don't build the tests as we're not running make test since many many years...
- fix build
- 1.7.0-rc3
- drop redundant and useless patches
- fix deps, file lists, etc.
- fix build
- rebuilt against new serf libs

  + Tomasz Pawel Gajc <tpg@mandriva.org>
    - rebuild

  + Paulo Andrade <pcpa@mandriva.com.br>
    - subversion 1.6.17 needs serf-0.7.2

  + Per Øyvind Karlsen <peroyvind@mandriva.org>
    - rebuild against new serf

* Thu Jun 02 2011 Oden Eriksson <oeriksson@mandriva.com> 2:1.6.17-1
+ Revision: 682484
- 1.6.17 (fixes CVE-2011-1752, CVE-2011-1783, CVE-2011-1921)
- new svn-book-html (S7)

* Sat May 14 2011 Oden Eriksson <oeriksson@mandriva.com> 2:1.6.16-4
+ Revision: 674433
- rebuild

* Wed Mar 30 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 2:1.6.16-3
+ Revision: 649257
- rebuild against new berkeley db 5.1.25

* Sun Mar 20 2011 Oden Eriksson <oeriksson@mandriva.com> 2:1.6.16-2
+ Revision: 647157
- link against bdb-5.x, heh...

* Sat Mar 05 2011 Funda Wang <fwang@mandriva.org> 2:1.6.16-1
+ Revision: 642186
- update to new version 1.6.16

* Sat Jan 08 2011 Oden Eriksson <oeriksson@mandriva.com> 2:1.6.15-1mdv2011.0
+ Revision: 629796
- 1.6.15
- new svn-book

* Fri Jan 07 2011 Funda Wang <fwang@mandriva.org> 2:1.6.13-4mdv2011.0
+ Revision: 629448
- rebuild

* Wed Dec 01 2010 Paulo Andrade <pcpa@mandriva.com.br> 2:1.6.13-3mdv2011.0
+ Revision: 604628
- Rebuild with apr with workaround to gcc type based strict aliasing issue

* Fri Oct 29 2010 Ahmad Samir <ahmadsamir@mandriva.org> 2:1.6.13-2mdv2011.0
+ Revision: 590266
- don't exclude ruby .la files, delete them as they're not packaged at all

  + Michael Scherer <misc@mandriva.org>
    - rebuild for python 2.7

* Sat Oct 02 2010 Funda Wang <fwang@mandriva.org> 2:1.6.13-1mdv2011.0
+ Revision: 582457
- readd missing files
- new version 1.6.13

* Sat Sep 18 2010 Funda Wang <fwang@mandriva.org> 2:1.6.12-5mdv2011.0
+ Revision: 579440
- rebuild
- add missing requires

* Sun Aug 01 2010 Funda Wang <fwang@mandriva.org> 2:1.6.12-3mdv2011.0
+ Revision: 564342
- rebuild for perl 5.12.1

* Wed Jul 21 2010 Thierry Vignaud <tv@mandriva.org> 2:1.6.12-2mdv2011.0
+ Revision: 556480
- rebuild for new perl

* Tue Jul 20 2010 Oden Eriksson <oeriksson@mandriva.com> 2:1.6.12-1mdv2011.0
+ Revision: 555138
- 1.6.12

  + Funda Wang <fwang@mandriva.org>
    - update url

* Sun Apr 25 2010 Götz Waschk <waschk@mandriva.org> 2:1.6.11-2mdv2010.1
+ Revision: 538786
- add kwallet support (bug #55709)

  + Funda Wang <fwang@mandriva.org>
    - more under link fixes
    - use standard ldflags

* Sun Apr 18 2010 Funda Wang <fwang@mandriva.org> 2:1.6.11-1mdv2010.1
+ Revision: 536089
- add back conf files
- new version  1.6.11

* Tue Apr 06 2010 Eugeni Dodonov <eugeni@mandriva.com> 2:1.6.9-3mdv2010.1
+ Revision: 532369
- Rebuild for openssl 1.0.0.

* Fri Feb 26 2010 Oden Eriksson <oeriksson@mandriva.com> 2:1.6.9-2mdv2010.1
+ Revision: 511642
- rebuilt against openssl-0.9.8m

* Fri Jan 22 2010 Funda Wang <fwang@mandriva.org> 2:1.6.9-1mdv2010.1
+ Revision: 494793
- add back svn conf
- new version 1.6.9

* Wed Jan 06 2010 Götz Waschk <waschk@mandriva.org> 2:1.6.6-3mdv2010.1
+ Revision: 486601
- add gnome-keyring support (bug #51197)

* Fri Jan 01 2010 Oden Eriksson <oeriksson@mandriva.com> 2:1.6.6-2mdv2010.1
+ Revision: 484732
- rebuilt against bdb 4.8

* Thu Oct 22 2009 Oden Eriksson <oeriksson@mandriva.com> 2:1.6.6-1mdv2010.0
+ Revision: 458906
- 1.6.6

* Mon Sep 28 2009 Olivier Blin <blino@mandriva.org> 2:1.6.5-4mdv2010.0
+ Revision: 450367
- do not build java on mips & arm (from Arnaud Patard)

* Sun Sep 20 2009 Guillaume Rousse <guillomovitch@mandriva.org> 2:1.6.5-3mdv2010.0
+ Revision: 446061
- install upstream bash completion
- don't enforce a specific security model on repository in package, let msec handle it (fix #31750)

* Sat Aug 22 2009 Oden Eriksson <oeriksson@mandriva.com> 2:1.6.5-1mdv2010.0
+ Revision: 419684
- 1.6.5

* Fri Aug 07 2009 Oden Eriksson <oeriksson@mandriva.com> 2:1.6.4-1mdv2010.0
+ Revision: 411314
- 1.6.4

* Fri Jul 17 2009 Oden Eriksson <oeriksson@mandriva.com> 2:1.6.3-2mdv2010.0
+ Revision: 396791
- rebuild

* Mon Jun 22 2009 Oden Eriksson <oeriksson@mandriva.com> 2:1.6.3-1mdv2010.0
+ Revision: 388089
- 1.6.3

* Sat Jun 06 2009 Oden Eriksson <oeriksson@mandriva.com> 2:1.6.2-3mdv2010.0
+ Revision: 383268
- rebuilt against new apr/apr-util libs

* Sun May 17 2009 Guillaume Rousse <guillomovitch@mandriva.org> 2:1.6.2-2mdv2010.0
+ Revision: 376707
- keep bash completion in its own package

* Tue May 12 2009 Oden Eriksson <oeriksson@mandriva.com> 2:1.6.2-1mdv2010.0
+ Revision: 374919
- 1.6.2

* Fri Apr 10 2009 Oden Eriksson <oeriksson@mandriva.com> 2:1.6.1-1mdv2009.1
+ Revision: 365783
- 1.6.1
- new svn-book

* Mon Mar 30 2009 Anssi Hannula <anssi@mandriva.org> 2:1.6.0-4mdv2009.1
+ Revision: 362445
- add missing obsoletes (Charles A Edwards)

* Sun Mar 29 2009 Anssi Hannula <anssi@mandriva.org> 2:1.6.0-3mdv2009.1
+ Revision: 362121
- provide .so symlink in java library package due to java design
  (reported by Mika Laitio)

* Sun Mar 22 2009 Oden Eriksson <oeriksson@mandriva.com> 2:1.6.0-2mdv2009.1
+ Revision: 360399
- re-enable java support

* Sun Mar 22 2009 Oden Eriksson <oeriksson@mandriva.com> 2:1.6.0-1mdv2009.1
+ Revision: 360262
- whoops!, bump release
- fix install of commit-email.pl
- fix build
- 1.6.0
- rediffed one last hunk in P6 (they forgot about it upstream)
- fix deps

* Thu Dec 25 2008 Funda Wang <fwang@mandriva.org> 2:1.5.5-2mdv2009.1
+ Revision: 318906
- rebuild for new python

* Tue Dec 23 2008 Oden Eriksson <oeriksson@mandriva.com> 2:1.5.5-1mdv2009.1
+ Revision: 318028
- 1.5.5
- new svn-book
- fix build with -Werror=format-security (P6)

* Mon Dec 15 2008 Oden Eriksson <oeriksson@mandriva.com> 2:1.5.4-3mdv2009.1
+ Revision: 314523
- rebuilt against db4.7

* Sun Nov 23 2008 Oden Eriksson <oeriksson@mandriva.com> 2:1.5.4-2mdv2009.1
+ Revision: 305990
- fix backporting

* Fri Oct 24 2008 Oden Eriksson <oeriksson@mandriva.com> 2:1.5.4-1mdv2009.1
+ Revision: 297000
- 1.5.4

  + Guillaume Rousse <guillomovitch@mandriva.org>
    - don't deal with xinetd in server post-installation (bug #44766)

* Fri Oct 10 2008 Oden Eriksson <oeriksson@mandriva.com> 2:1.5.3-1mdv2009.1
+ Revision: 291599
- -1.5.3

* Sat Sep 06 2008 Guillaume Rousse <guillomovitch@mandriva.org> 2:1.5.2-3mdv2009.0
+ Revision: 281840
- server package doesn't requires xinetd (bug #28947)
  fix server package description

* Tue Sep 02 2008 Helio Chissini de Castro <helio@mandriva.com> 2:1.5.2-2mdv2009.0
+ Revision: 279061
- Added svn as provides for main package
- Removed all separated devel packages and concentrated in one only package

* Sun Aug 31 2008 Oden Eriksson <oeriksson@mandriva.com> 2:1.5.2-1mdv2009.0
+ Revision: 277787
- 1.5.2
- new svn-book

* Tue Aug 26 2008 Oden Eriksson <oeriksson@mandriva.com> 2:1.5.1-3mdv2009.0
+ Revision: 276139
- stop doing stupid neon version checks
- rebuild

* Wed Aug 06 2008 Oden Eriksson <oeriksson@mandriva.com> 2:1.5.1-2mdv2009.0
+ Revision: 264265
- new S7
- enable serf support

* Tue Aug 05 2008 Oden Eriksson <oeriksson@mandriva.com> 2:1.5.1-1mdv2009.0
+ Revision: 264068
- 1.5.0/1.5.1
- 1.5.1

* Thu Jul 17 2008 Oden Eriksson <oeriksson@mandriva.com> 2:1.5.0-4mdv2009.0
+ Revision: 237779
- fix deps and rebuild against neon-devel (duh!)

* Thu Jun 26 2008 Helio Chissini de Castro <helio@mandriva.com> 2:1.5.0-3mdv2009.0
+ Revision: 229346
- Fix the epoch issue. Two different epochs are set in different subpackages and install got confused

  + Oden Eriksson <oeriksson@mandriva.com>
    - rebuild
    - fix the libsvnjavahl naming
    - fix deps (neon-devel 0.25.0+)

* Thu Jun 26 2008 Oden Eriksson <oeriksson@mandriva.com> 1.5.0-1mdv2009.0
+ Revision: 229318
- fix group
- hard code %%{_localstatedir} to /var/lib
- re-added the apache conf (don't use mdvsys sync or fix it!!!)
- new svnbook-1.5
- fix build
- can't use noarch for a sub package only
- make the _requires_exceptions catch devel(libneon (will match 64bit too)
- try to fix the javahl build
- rebuild

  + Helio Chissini de Castro <helio@mandriva.com>
    - New upstream version 1.5.0
    - Removed old no more valid patches
    - Changed bindings infrastructure
    - Added unlink patch for some applications

  + Thierry Vignaud <tv@mandriva.org>
    - add spacing in description
    - add SVN in description as requested for easier searches in rpmdrake
    - rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers
    - adapt to %%_localstatedir now being /var instead of /var/lib (#22312)

* Mon Jan 14 2008 Oden Eriksson <oeriksson@mandriva.com> 1.4.6-5mdv2008.1
+ Revision: 151900
- rebuild for perl-5.10.0

  + Pixel <pixel@mandriva.com>
    - rebuild for perl-5.10.0

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Wed Dec 26 2007 Oden Eriksson <oeriksson@mandriva.com> 1.4.6-3mdv2008.1
+ Revision: 138135
- the exclusion of devel(libneon) has to work on x86_64 also...

* Wed Dec 26 2007 Oden Eriksson <oeriksson@mandriva.com> 1.4.6-2mdv2008.1
+ Revision: 138011
- avoid pulling latest devel(libneon) for now

* Sun Dec 23 2007 Oden Eriksson <oeriksson@mandriva.com> 1.4.6-1mdv2008.1
+ Revision: 137279
- fix deps, it will not build against latest neon
- some sources got lost somehow...
- 1.4.6
- rebuilt against latest build deps
- rediffed P3
- new svn-book (S7)
- make it backportable again...

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

  + Anssi Hannula <anssi@mandriva.org>
    - buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)

* Tue Oct 02 2007 Funda Wang <fwang@mandriva.org> 1.4.5-5mdv2008.0
+ Revision: 94731
- fix provides

* Sun Sep 16 2007 Oden Eriksson <oeriksson@mandriva.com> 1.4.5-4mdv2008.0
+ Revision: 88400
- plan c
- plan b
- make it backportable

* Sun Sep 16 2007 David Walluck <walluck@mandriva.org> 1.4.5-3mdv2008.0
+ Revision: 88364
- pass -module in addition to -avoid-version when build java native library

* Sat Sep 15 2007 Anssi Hannula <anssi@mandriva.org> 1.4.5-2mdv2008.0
+ Revision: 87192
- rebuild to filter out autorequires on GCJ AOT objects
- remove unnecessary Requires(post) on java-gcj-compat

* Wed Aug 29 2007 Helio Chissini de Castro <helio@mandriva.com> 1.4.5-1mdv2008.0
+ Revision: 74496
- New upstream minor version

* Sat Aug 25 2007 Oden Eriksson <oeriksson@mandriva.com> 1.4.4-7mdv2008.0
+ Revision: 71388
- also install propchange-email.pl (duh!)
- build against latest system neon libs (0.26.4)
- fix shellbang (again?)
- added P4 to include the path to the hook-scripts
- added P5. propchange-email.pl was removed after 1.3.2 but still referenced in subversion/libsvn_repos/repos.c
- added the apache-mod_dontdothat sub package
- update the svn-book
- added latest neon in the subversion-latest_neon.diff patch (but don't build against it just yet)
- update the svn-book

* Fri Jun 22 2007 Andreas Hasenack <andreas@mandriva.com> 1.4.4-6mdv2008.0
+ Revision: 43248
- using serverbuild macro

* Tue Jun 12 2007 Andreas Hasenack <andreas@mandriva.com> 1.4.4-5mdv2008.0
+ Revision: 38111
- updated to version 1.4.4

* Sat May 26 2007 David Walluck <walluck@mandriva.org> 1.4.3-5mdv2008.0
+ Revision: 31317
- proper java support (svn-javahl, svn-javahl-javadoc)
- ruby-svn-devel requires ruby-svn
- fix java-svn summary
- remove rpath from binaries
- really fix broken Requires() syntax

* Sat May 26 2007 David Walluck <walluck@mandriva.org> 1.4.3-4mdv2008.0
+ Revision: 31269
- enable java support
- fix broken Requires() syntax
- replace BuildPreReq with BuildRequires

* Sun Apr 22 2007 Pascal Terjan <pterjan@mandriva.org> 1.4.3-3mdv2008.0
+ Revision: 16960
- Use Development/Ruby group for ruby-svn
- Use ruby macros (and put it a the right place on x86_64)


* Sun Mar 11 2007 Oden Eriksson <oeriksson@mandriva.com> 1.4.3-2mdv2007.1
+ Revision: 141377
- rebuild

* Thu Jan 25 2007 Oden Eriksson <oeriksson@mandriva.com> 1.4.3-1mdv2007.1
+ Revision: 113351
- 1.4.3 (Minor bugfixes)
- rediffed P3

* Tue Jan 23 2007 Oden Eriksson <oeriksson@mandriva.com> 1.4.2-4mdv2007.1
+ Revision: 112686
- rebuild
- make it find neon 0.26.3

  + Götz Waschk <waschk@mandriva.org>
    - use find-lang

* Fri Jan 12 2007 Guillaume Rousse <guillomovitch@mandriva.org> 1.4.2-3mdv2007.1
+ Revision: 107906
- bump release
- fix bash completion
- update bash completion

* Tue Nov 28 2006 Michael Scherer <misc@mandriva.org> 1.4.2-2mdv2007.1
+ Revision: 87812
- Bump release for new python rebuild

* Wed Nov 08 2006 Helio Chissini de Castro <helio@mandriva.com> 1.4.2-1mdv2007.0
+ Revision: 78135
- missing man entry.
- New upstream version
- Fix on neon test patch. Again, we have a new version than max tested on svn
  configs. subversion tests up to 26.1, we have 26.2.

* Wed Oct 18 2006 Andreas Hasenack <andreas@mandriva.com> 1.4.0-2mdv2007.1
+ Revision: 65966
- bumped release
- added specific requirement for libsvn, since the soname
  didn't change from 1.3.x to 1.4.x

* Tue Oct 17 2006 Andreas Hasenack <andreas@mandriva.com> 1.4.0-1mdv2007.1
+ Revision: 65749
- adjust autoconf requirement
- restore 1.4 (merge back)
- bump release
- rollback to pre-1.4.0 state
- fix /etc/services handling (#26202)

  + Helio Chissini de Castro <helio@mandriva.com>
    - Change requires on subversion dav module
    - New stable upstream version

* Fri Jul 14 2006 Andreas Hasenack <andreas@mandriva.com> 1.3.2-4mdv2007.0
+ Revision: 41082
- own %%{_datadir}/subversion-%%{version} directory (#12658)
- improve /etc/services handling (#21442)

* Fri Jul 14 2006 Andreas Hasenack <andreas@mandriva.com> 1.3.2-3mdv2007.0
+ Revision: 41077
- some files are arch dependant, move them to the right place
 (#22251)
- updated neon patch
- make sure we build all repository access libraries

  + Oden Eriksson <oeriksson@mandriva.com>
    - make it backportable
    - make it use the latest apr and apr-util per default

* Fri Jun 02 2006 Andreas Hasenack <andreas@mandriva.com> 1.3.2-1mdv2007.0
+ Revision: 31844
- updated to version 1.3.2
- added signature file
- renamed mdv to packages because mdv is too generic and it's hosting only packages anyway
- protect default repository directory (#22287)
- fix for #21793

  + Helio Chissini de Castro <helio@mandriva.com>
    - Raise release number to recompile.
    - Fixed permission of documentation dir. Thanks to Andreas
    - Fixed compilation against neon 0.26 and old swig
    - Missing source
    - New upstream version
    - Fixed patch to compile against neon 0.25 or 0.26
    - Close documentation bug http://qa.mandriva.com/show_bug.cgi?id=20317
    - Adopted _sysconfdir/subversion strategy to make password cache disabled by
      default. Requested by Andreas Hasenack
    - Small spec cleanup
    - Added svnbook release 1.1 ( Creative Commons license )
    - Changed path to java compilation ( still disabled buy default )
    - Fix java switch option
    - Fixed python bindings. Fix http://qa.mandriva.com/show_bug.cgi?id=20744
      Thanks to Andreas and Bogdano
    - Fixed perl bindings install agains new perl 5.8.8. Thanks to Rafael.
    - Fixed devel lib requires
    - Disabled java compilation, since -compat packages for make gcj usefull are in
      contrib. Thanks to spturtle.
    - Add missing requires in devel package. Thanks to Oden

  + Oden Eriksson <oeriksson@mandriva.com>
    - built against new neon (0.25.1+, 0.26.0 in cooker contrib)

* Mon Jan 02 2006 Helio Chissini de Castro <helio@mandriva.com> 1.3.0-8mdk
+ Revision: 1358
- Fixed spec for final release
- Updated for final release 1.3.0

* Wed Dec 21 2005 Helio Chissini de Castro <helio@mandriva.com> 1.3.0-7mdk
+ Revision: 1328
- Updated for rc7.
- Remove enable-dso, which leads to a segfault in ix86 archs. Related to bugs:
  http://qa.mandriva.com/show_bug.cgi?id=13725 and
  http://qa.mandriva.com/show_bug.cgi?id=19886
- Release candidate 6 ( on hold until svn devels decide that this is ready for
  production )
- Small type fix by Olivier Thauvin ( java and ruby switches )
- Small patch to fix perl compilation

  + Pixel <pixel@mandriva.com>
    - increase release number
    - the vc-svn.el bundled in subversion says: "This file no longer lives here, it lives in FSF Emacs."
      better remove it

  + Laurent Montel <lmontel@mandriva.com>
    - Minor typo in patch

* Tue Dec 06 2005 Laurent Montel <lmontel@mandriva.com> 1.3.0-5mdk
+ Revision: 1250
- Fix svn-config+multiarch (patch from Gb thanks)

  + Helio Chissini de Castro <helio@mandriva.com>
    - Subversion now requires swig >= .27
    - Oden patch to match build_perl switch

* Mon Nov 28 2005 Helio Chissini de Castro <helio@mandriva.com> 1.3.0-3mdk
+ Revision: 1205
- On behalf of Guillaume Rousse <guillomovitch@mandriva.org>
- install bash-completion from eponym project
- don't flag bash completion as config
- %%mkrel
- spec cleanup
- use standard version for apache module
- fix doc and libtool file perms

* Tue Nov 22 2005 Helio Chissini de Castro <helio@mandriva.com> 1.3.0-2mdk
+ Revision: 1191
- Latest hour rc4 tarball fix for faulty libtool
- Fix for empty changelog (none)
- New upstream release candidate ( rc3 )
- Moved common libraries for a libsvn package.
- Added conflicts against old package
- Swig not play nice with nprocs on compilations
- Release candidate 2 for next version
- Fixed swig .27 bindings compilation proble ( libapr related )
- Removed pt_BR potfile patch ( fixed upstream )
- Added debug option
- Added patch to fix segfault on i18n pt_BR translation
- Fix perl-SVN name to follow policy
- Again trying to make java build on all archs. Add explicit patch on flags was needed since gcc for x86_64 files installations place differs from x86.
- Redistribute libraries for right place.
- Added conflicts for server package and obsoletes for libsvn_fs*
  http://qa.mandriva.com/show_bug.cgi?id=18846
- Renabled java package ( hope is right this time )
- Disable java until solve problems of jni.h install.
- Fix jvm_home placement. gcj still uses lib instead of lib64 on x86_64
- Added missing obsoletes and provides ( thanks to Michael Scherer )
- Reenabled Java package as default
- Fix obsoletes for lib64 on x86_64 archs
- Update release to fix changelog
- Fix conditional java build
- New layout finished. All useless splitted libs are obsoleted in favor of one
  client and one server package. Tools package remains same.
- Bindings for Java reenabled using the native gcc compiler
- Build for python, ruby and perl changed. Python is now in site-packages.
- All apache related stuff goes to package apache-mod_dav_svn.

* Sat Aug 27 2005 Andreas Hasenack <andreas@mandriva.com> 1.2.1-4mdk
+ Revision: 749
- rebuild and recover changelog which was mistakenly erased in
  the previous package

* Sat Aug 27 2005 Andreas Hasenack <andreas@mandriva.com> 1.2.1-3mdk
+ Revision: 743
- Compile with -fPIC to fix python binding, see #17246
  (fix by Couriousous <couriousous@mandriva.org>)
- fix build on x86_64 (by Thierry Vignaud <tvignaud@mandriva.com>)
- reverting Helio's changes: the new layout is not ready yet and
  we need a subversion package with important fixes. Helio, you can
  reapply this later with svn merge.

  + Helio Chissini de Castro <helio@mandriva.com>
    -  work in progress for new packahe layout

* Thu Jul 07 2005 Helio Chissini de Castro <helio@mandriva.com> 1.2.1-1mdk
+ Revision: 316
- New upstream release 1.2.1
- Still old spec layout and packages. Postergating for next release
- Subversion package updated in subversion repository :-)
- Still depends on libneon 0.24.7
- Fixed hierarchy on subversion

* Tue Jun 07 2005 Helio Chissini de Castro <helio@mandriva.com> 1.2.0-6mdk
- Fix build
- Removed invalid patches
- Removed reconstruction of auto*tools

* Tue Jun 07 2005 Oden Eriksson <oeriksson@mandriva.com> 1.2.0-5mdk
- fix deps

* Fri Jun 03 2005 Oden Eriksson <oeriksson@mandriva.com> 1.2.0-4mdk
- rename the apache sub packages (apache2/apache)
- the conf.d directory is renamed to modules.d
- use new rpm-4.4.x pre,post magic

* Tue May 31 2005 Oden Eriksson <oeriksson@mandriva.com> 1.2.0-3mdk
- added the ruby bindings on request by Andre Nathan
- build it against neon 0.25

* Sat May 28 2005 Oden Eriksson <oeriksson@mandriva.com> 1.2.0-2mdk
- fix deps again...

* Fri May 27 2005 Oden Eriksson <oeriksson@mandriva.com> 1.2.0-1mdk
- 1.2.0
- fix deps
- make the tests work. works on x86_64 too, nice.

* Sun May 22 2005 Oden Eriksson <oeriksson@mandriva.com> 1.1.4-2mdk
- added P4 from fedora (x86_64 fixes)
- disable running the tests on x86_64 for now, many tests fails
- fix deps
- rework the --with[out] magic

* Wed Apr 06 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 1.1.4-1mdk
- 1.1.4
- drop the swig patch (P2) as it seems implemented upstream

* Sun Mar 20 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 1.1.3-13mdk
- use the %%mkrel macro

* Fri Mar 18 2005 Michael Scherer <misc@mandrake.org> 1.1.3-12mdk
- enhance summary

* Wed Mar 02 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 1.1.3-11mdk
- fix svn-config, reported by willem boschman
- nuke *.pyc files

* Mon Feb 28 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 1.1.3-10mdk
- fix %%post and %%postun to prevent double restarts
- fix deps and conditional %%multiarch

* Fri Feb 18 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 1.1.3-9mdk
- spec file cleanups, remove the ADVX-build stuff

* Tue Feb 08 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 1.1.3-8mdk
- rebuilt against new apr and for apache 2.0.53
- update description

* Mon Feb 07 2005 Buchan Milne <bgmilne@linux-mandrake.com> 1.1.3-7mdk
- rebuild for ldap2.2_7

* Fri Feb 04 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 1.1.3-6mdk
- rebuilt against new openldap libs

* Wed Feb 02 2005 Michael Scherer <misc@mandrake.org> 1.1.3-5mdk
- fix swig compil ( patch from trunk )

* Fri Jan 21 2005 Michael Scherer <misc@mandrake.org> 1.1.3-4mdk
- reenable python and perl binding, with some voodoo
- add a switch to remove test
- remove the rpath rpmlint warning

* Mon Jan 17 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 1.1.3-3mdk
- added P0,P1 plus some other stuff from fedora
- fix deps

* Mon Jan 17 2005 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 1.1.3-2mdk
- Fix directory ownership

* Sat Jan 15 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 1.1.3-1mdk
- 1.1.3
- make --with debug work
- added two more build switches, --with swig and --with test, the swig
  bindings is disabled until this is fixed either in swig or in 
  subversion
- added the server sub package, someone asked for it?
- misc spec file fixes

* Tue Dec 28 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 1.1.2-1mdk
- lib64 fixes

* Wed Dec 08 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 1.1.1-4mdk
- make it build on amd64

* Sat Dec 04 2004 Michael Scherer <misc@mandrake.org> 1.1.1-3mdk
- Rebuild for new python
- fix chrpath stuff

* Wed Nov 24 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 1.1.1-2mdk
- nuke redundant provides

* Thu Nov 18 2004 Ben Reser <ben@reser.org> 1.1.1-1mdk
- 1.1.1

* Fri Oct 08 2004 Ben Reser <ben@reser.org> 1.1.0-1mdk
- 1.1.0
- Fix bindings build for changes in 1.1.0
- Add libsvn_fs_base and libsvn_fs_fs packages to allow users
  using the fsfs backend to avoid the bdb dependency.

* Thu Sep 23 2004 Ben Reser <ben@reser.org> 1.0.8-1mdk
- 1.0.8 (security fix for CAN-2004-0749)

* Sun Sep 19 2004 Ben Reser <ben@reser.org> 1.0.7-1mdk
- 1.0.7 
- Built against Berkely DB 4.2.  Users using previous
  packages should dump their repos before installing.

* Wed Jul 21 2004 Ben Reser <ben@reser.org> 1.0.6-1mdk
- 1.0.6 (includes a minor security fix)
- libneon >= 0.24.7 is now needed.

* Fri Jun 11 2004 Ben Reser <ben@reser.org> 1.0.5-1mdk
- 1.0.5 (security fix for CAN-2004-0413)

* Thu May 20 2004 Ben Reser <ben@reser.org> 1.0.3-1mdk
- 1.0.3 (security fix for CAN-2004-0397)

* Wed Apr 28 2004 Ben Reser <ben@reser.org> 1.0.2-1mdk
- 1.0.2

* Sat Mar 13 2004 Ben Reser <ben@reser.org> 1.0.1-1mdk
- 1.0.1
- Remove the editor config that makes it default to nano.
- cvs2svn is no longer part of subversion and has split off 
  onto its own project at http://cvs2svn.tigris.org/
  I'll package it as soon as it releases something.  Due to
  the fast amount of development it is better to check it out
  of the svn repository now.
- Remove obsolete auth_provider examples.
- Fixup python sh'bang lines on some scripts.

