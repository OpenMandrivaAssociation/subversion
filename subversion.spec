# disable the stupid rpmlint shit from hell!!!
%define _build_pkgcheck_set %{nil}
%define _build_pkgcheck_srpm %{nil}

%define _disable_ld_no_undefined 1

%define _requires_exceptions devel(libneon

%define apache_version 2.4.0
%define libsvn %mklibname svn 0
%define libsvngnomekeyring %mklibname svn-gnome-keyring 0
%define libsvnkwallet %mklibname svn-kwallet 0

# Java requires devel symlinks in non-devel packages due to design
# (System.loadLibrary). Do not add -devel dependencies.
%define _exclude_files_from_autoreq ^%{_libdir}/libsvnjavahl-%{svnjavahl_api}.so$

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
Version:	1.7.4
Release:	2
Epoch: 2
License:	BSD CC2.0
Group:		Development/Other
URL:		http://subversion.apache.org/
Source0:	http://www.apache.org/dist/subversion/%{name}-%{version}.tar.bz2
Source1:	http://www.apache.org/dist/subversion/%{name}-%{version}.tar.bz2.asc
Source2:	svnserve.service
Source3:	svnserve.sysconf
Source5:	%name-1.3.0-global-config
Source6:	%name-1.3.0-global-servers
Source7:	http://svnbook.red-bean.com/nightly/en/svn-book-html-chunk.tar.bz2
Patch0:		subversion-1.7.0-rc3-no_tests.diff
Patch1:		svn-ruby-1.9-fixes.patch
Patch2:		svn-update-ruby-tests.patch
Patch3:		subversion-1.7.4-apache241.diff
BuildRequires:	autoconf automake libtool
BuildRequires:	chrpath
BuildRequires:	python >= 2.2
BuildRequires:	texinfo
BuildRequires:	info-install
BuildRequires:	db-devel
BuildRequires:	neon-devel
BuildRequires:	apache-devel >=  %{apache_version}
BuildRequires:	apr-devel >= 1:1.4.6
BuildRequires:	apr-util-devel >= 1.4.1
BuildRequires:	libxslt-proc
BuildRequires:	docbook-style-xsl
BuildRequires:	sqlite3-devel >= 3.6.18
BuildRequires:	krb5-devel
%if %mdvver < 201200
BuildRequires:	file-devel
%else
BuildRequires:	magic-devel
%endif
# Swig is runtime only
BuildRequires:	swig >= 1.3.27
# needs this despite build_ruby 0
BuildRequires:	ruby
BuildRequires:	ruby-devel
BuildRequires:	ruby-rdoc
Provides:	%name-ra-method = %{epoch}:%version-%{release}
Provides:	%name-client-tools = %{epoch}:%version-%{release}
Provides:	svn = %{epoch}:%{version}
Requires:	%{libsvn} >= %{epoch}:%{version}

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
of things you want %name-repos. 

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

%package -n	%libsvn
Summary:	Subversion libraries
Group:		System/Libraries

%description -n	%libsvn
Subversion common libraries

%if %{build_gnome_keyring}
%package -n	%libsvngnomekeyring
Summary:	gnome-keyring support for svn
Group:		System/Libraries
%if %mdvver < 201010
BuildRequires:	gnome-keyring-devel >= 2.26.1
%else
BuildRequires:	libgnome-keyring-devel
%endif
BuildRequires:	dbus-devel >= 1.2.4.4permissive
Requires:	gnome-keyring >= 2.26.1

%description -n	%libsvngnomekeyring
Subversion libraries that allow interaction with the gnome-keyring daemon
%endif

%if %{build_kwallet}
%package -n	%libsvnkwallet
Summary:	kwallet support for svn
Group:		System/Libraries
BuildRequires:	kdelibs4-devel
BuildRequires:	dbus-devel >= 1.2.4.4permissive
Requires:	kwallet

%description -n	%libsvnkwallet
Subversion libraries that allow interaction with the kwallet daemon.
%endif

%package	server
Summary:	Subversion Server
Group:		System/Servers
Requires:	%name >= %{epoch}:%version-%{release}
# soname didn't change between 1.3.x and 1.4.x, but we
# need the right one...
Requires:	%{libsvn} >= %{epoch}:%{version}

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
Requires:	%name >= %{epoch}:%version-%{release}
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
Provides:	python-subversion = %version-%{release}
Requires:	python
# soname didn't change between 1.3.x and 1.4.x, but we
# need the right one...
Requires:	%{libsvn} >= %{epoch}:%{version}

%description -n	python-svn
This package contains the files necessary to use the subversion
library functions within python scripts.
%endif

%if %{build_ruby}
%package -n	ruby-svn
Summary:	Ruby bindings for Subversion
Group:		Development/Ruby
Requires:	ruby
Requires:	%{libsvn} >= %{epoch}:%{version}
Provides:	ruby-subversion = %{epoch}:%version-%{release}

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
Obsoletes:	java-svn < %{epoch}:%{version}-%{release}
Provides:       java-svn = %{epoch}:%{version}-%{release}
Provides:	java-subversion = %{epoch}:%{version}-%{release}
Requires:	%{name} >= %{epoch}:%{version}-%{release}
Requires:	%{libsvn} >= %{epoch}:%{version}-%{release}
Requires:	%{libsvnjavahl} >= %{epoch}:%{version}-%{release}
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
Requires:	%name >= %{epoch}:%version-%{release}
Obsoletes:	perl-svn
Provides:	perl-svn = %{epoch}:%version-%{release}
Requires:	%{libsvn} >= %{epoch}:%{version}

%description -n	perl-SVN
This package contains the files necessary to use the subversion
library functions within perl scripts.
%endif

%package	devel
Summary:	Subversion headers/libraries for development
Group:		Development/C
Provides:	libsvn-devel = %{epoch}:%version-%{release}
%if %{build_perl}
Requires:	perl-SVN >= %{epoch}:%{version}
Obsoletes:	perl-SVN-devel < 2:1.5.2-2
Provides:	per-SVN-devel = %{epoch}:%{version}
%endif
%if %{build_perl}
Requires:	python-svn >= %{epoch}:%{version}
Obsoletes:	python-svn-devel < 2:1.5.2-2
Provides:	python-svn-devel = %{epoch}:%{version}
%endif
%if %{build_ruby}
Requires:	ruby-svn >= %{epoch}:%{version}
Obsoletes:	ruby-svn-devel < 2:1.5.2-2
Provides:	ruby-svn-devel = %{epoch}:%{version}
%endif
Requires:	%libsvn >= %{epoch}:%version-%release
Requires:	neon-devel
%if %{build_gnome_keyring}
Requires:	%libsvngnomekeyring >= %{epoch}:%version-%release
%endif
%if %{build_kwallet}
Requires:	%libsvnkwallet >= %{epoch}:%version-%release
%endif

%description devel
This package contains the header files and linker scripts for
subversion libraries.

%package -n	apache-mod_dav_svn
Summary:	Subversion server DSO module for apache
Group:		System/Servers
Requires:	%name-tools >= %{epoch}:%version-%{release}
Requires:	apache >= %{apache_version}
Requires:	apache-mod_dav >= %{apache_version}
# soname didn't change between 1.3.x and 1.4.x, but we
# need the right one...
Requires(pre):	%{libsvn} >= %{epoch}:%{version}
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
Requires:	apache-mod_dav_svn = %{epoch}:%{version}

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
%patch3 -p0 -b .apache241

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
    --with-jdk=%{java_home} \
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

# compile the extra module as well...
%{_bindir}/apxs -c -Isubversion/include -Isubversion \
    tools/server-side/mod_dontdothat/mod_dontdothat.c \
    subversion/libsvn_subr/libsvn_subr-1.la

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

mkdir -p %{buildroot}%{_javadir}
%{__mv} %{buildroot}%{_libdir}/svn-javahl/svn-javahl.jar %{buildroot}%{_javadir}/svn-javahl-%{version}.jar
%{__ln_s} svn-javahl-%{version}.jar %{buildroot}%{_javadir}/svn-javahl.jar

%{_bindir}/chrpath -d %{buildroot}%{_libdir}/libsvnjavahl-1.so
%endif

%if %{build_perl}
# perl bindings
make pure_vendor_install -C subversion/bindings/swig/perl/native DESTDIR=%{buildroot}
%endif

install -d %{buildroot}%{_sysconfdir}/httpd/modules.d
echo "LoadModule dav_svn_module %{_libdir}/apache/mod_dav_svn.so" > %{buildroot}%{_sysconfdir}/httpd/modules.d/146_mod_dav_svn.conf
echo "LoadModule authz_svn_module %{_libdir}/apache/mod_authz_svn.so" > %{buildroot}%{_sysconfdir}/httpd/modules.d/147_mod_authz_svn.conf

# install the extra module
install -m0755 tools/server-side/mod_dontdothat/.libs/mod_dontdothat.so %{buildroot}%{_libdir}/apache/

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
%find_lang %name

# Install svnserve bits
install -d %{buildroot}/var/run/svnserve
install -d %{buildroot}/var/lib/svn/repositories
install -d %{buildroot}/lib/systemd/system
install -d %{buildroot}%{_sysconfdir}/sysconfig

install -m0644 svnserve.service %{buildroot}/lib/systemd/system/svnserve.service
install -m0644 svnserve.sysconf %{buildroot}%{_sysconfdir}/sysconfig/svnserve

# Move perl man
mv %{buildroot}%_prefix/local/share/man/man3/* %{buildroot}%{_mandir}/man3/

# cleanup
find %{buildroot} -name "perllocal.pod" | xargs rm -f

# delete all libtool .la files
find %{buildroot} -name "*.la" | xargs rm -f

%post doc
%_install_info svn-design.info
%_install_info svn-handbook.info

%postun doc
%_install_info svn-design.info
%_install_info svn-handbook.info

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
%files -n %libsvngnomekeyring
# list all ra libs to make sure we don't miss any
# in a bogus build
%{_libdir}/libsvn_auth_gnome_keyring-1.so.0*
%endif

%if %{build_kwallet}
%files -n %libsvnkwallet
# list all ra libs to make sure we don't miss any
# in a bogus build
%{_libdir}/libsvn_auth_kwallet-1.so.0*
%endif

%files -n %libsvn
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
