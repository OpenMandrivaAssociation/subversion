# disable the stupid rpmlint shit from hell!!!
%define _build_pkgcheck_set %{nil}
%define _build_pkgcheck_srpm %{nil}

%define apache_version 2.4.0
%define api 1
%define major 0
%define libname %mklibname svn %{api} %{major}
%define devname %mklibname svn -d

# Java requires devel symlinks in non-devel packages due to design
# (System.loadLibrary). Do not add -devel dependencies.
%define _exclude_files_from_autoreq ^%{_libdir}/libsvnjavahl-%{svnjavahl_api}.so$

%bcond_without  python
%bcond_without  ruby
%bcond_without  perl
%bcond_without  gnome_keyring
%bcond_without  kwallet
%bcond_with test
%bcond_with debug

%ifarch %{ix86} x86_64
%bcond_without  java
%endif
%ifarch %arm
%bcond_with  java
%endif

Summary:	A Concurrent Versioning System
Name:		subversion
Epoch:		2
Version:	1.8.5
Release:	3
License:	Apache License
Group:		Development/Tools
Url:		http://subversion.apache.org/
Source0:	http://www.apache.org/dist/subversion/%{name}-%{version}.tar.bz2
Source1:	http://www.apache.org/dist/subversion/%{name}-%{version}.tar.bz2.asc
Source2:	mod_dav_svn.conf
Source3:	subversion.conf
Source5:	%{name}-1.3.0-global-config
Source6:	%{name}-1.3.0-global-servers
Source7:	http://svnbook.red-bean.com/nightly/en/svn-book-html-chunk.tar.bz2
Source8:	svnserve.service
Source9:	svnserve-tmpfiles.conf
Patch0:		subversion-1.8.3-underlink.diff

BuildRequires:	chrpath
BuildRequires:	docbook-style-xsl
BuildRequires:	doxygen
BuildRequires:	libtool
BuildRequires:	texinfo
BuildRequires:	db-devel
BuildRequires:	apache-devel >= %{apache_version}
BuildRequires:	krb5-devel
BuildRequires:	magic-devel
BuildRequires:	pkgconfig(apr-1)
BuildRequires:	pkgconfig(apr-util-1)
BuildRequires:	pkgconfig(libexslt)
BuildRequires:	pkgconfig(neon)
BuildRequires:	pkgconfig(python)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(serf-1)
# Swig is runtime only
BuildRequires:	swig >= 1.3.27
# needs this despite with ruby 0
BuildRequires:	ruby
BuildRequires:	ruby-devel
BuildRequires:	ruby-rdoc

Provides:	%{name}-ra-method = %{EVRD}
Provides:	%{name}-client-tools = %{EVRD}
Provides:	svn = %{EVRD}
# MD because of the sysconfig files moved to this pkg
Conflicts:	%{_lib}svn1 < 2:1.8.5-2

%description
Subversion (SVN) is a concurrent version control system which enables one or
more users to collaborate in developing and maintaining a hierarchy of files
and directories while keeping a history of all changes.  Subversion only stores
the differences between versions, instead of every complete file.  Subversion
also keeps a log of who, when, and why changes occurred.

As such it basically does the same thing CVS does (Concurrent Versioning
System) but has major enhancements compared to CVS and fixes a lot of the
annoyances that CVS users face.

This package contains the client, if you're looking for the server end
of things you want %{name}-server.

%files -f %{name}.lang
# MD moved from lib pkg
%dir %{_sysconfdir}/subversion
%config(noreplace) %{_sysconfdir}/subversion/*
%{_bindir}/svn
%{_bindir}/svnversion
%{_bindir}/showchange*
%{_bindir}/svnlook
%{_mandir}/man1/svn.*
%{_mandir}/man1/svnlook.*
%{_mandir}/man1/svnversion.*
%{_mandir}/man1/svnsync.*
%dir %{_datadir}/subversion-%{version}
%{_sysconfdir}/bash_completion.d/subversion

#--------------------------------------------------------------------------

%package        doc
Summary:	Subversion Documenation
Group:		Documentation
BuildArch:	noarch

%description    doc
This package contains the subversion book and design info files.

%files doc
%doc svnbook-1.*
%doc doc/user/*.html
%doc doc/user/*.txt

#-------------------------------------------------------------------------

%define svnlibs svn_client svn_delta svn_diff svn_fs svn_fs_base svn_fs_fs svn_fs_util svn_repos svn_subr svn_ra svn_ra_local svn_ra_serf svn_ra_svn svn_wc

%package -n	%{libname}
Summary:	Subversion libraries
Group:		System/Libraries
Obsoletes:	%{_lib}svn0 < 2:1.7.13-4
Obsoletes:	%{_lib}svn1 < 2:1.8.5-3
Conflicts:	%{libname} < 2:1.8.5-3

%description -n	%{libname}
Subversion common libraries.

%files -n %{libname}
%{expand:%(for lib in %svnlibs; do cat <<EOF
%{_libdir}/lib$lib-%{api}.so.%{major}*
EOF
done)}

#---------------------------------------------------------------------------

%package -n %{devname}
Summary:	Subversion headers/libraries for development
Group:		Development/C
Provides:	%{name}-devel = %{EVRD}
Requires:	%{libname} = %{EVRD}

%description -n %{devname}
This package contains the header files and linker scripts for
subversion libraries.

%files -n %{devname}
%doc tools/examples/minimal_client.c
%{_includedir}/subversion-1/*
%{expand:%(for lib in %svnlibs; do cat <<EOF
%{_libdir}/lib$lib-%{api}.so
EOF
done)}
# MD should we remove this?
%{_libdir}/libsvn_diff.so

%if %{with java}
%exclude %{_libdir}/libsvnjavahl*
%endif

#----------------------------------------------------------------

%if %{with gnome_keyring}
%define libgnomekeyring %mklibname svn_auth_gnome_keyring %{api} %{major}
%define devgnomekeyring %mklibname svn_auth_gnome_keyring -d

%package -n	%{libgnomekeyring}
Summary:	gnome-keyring support for svn
Group:		System/Libraries
BuildRequires:	pkgconfig(dbus-1) >= 1.2.4.4permissive
BuildRequires:	pkgconfig(gnome-keyring-1)
Requires:	gnome-keyring >= 2.26.1
Obsoletes:	%{_lib}svn-gnome-keyring0 < 2:1.8.5-2

%description -n	%{libgnomekeyring}
Subversion library that allow interaction with the gnome-keyring daemon.

%files -n %{libgnomekeyring}
%{_libdir}/libsvn_auth_gnome_keyring-%{api}.so.%{major}*

%package -n	%{devgnomekeyring}
Summary:	Subversion headers/libraries for development
Group:		Development/GNOME and GTK+
Requires:	%{name}-devel = %{EVRD}
Requires:	%{libgnomekeyring} = %{EVRD}
Conflicts:	%{name}-devel < 2:1.6.17-2
Obsoletes:	%{name}-gnome-keyring-devel < 2:1.8.5-2

%description -n %{devgnomekeyring}
This package contains the header files and linker scripts for the
subversion library using gnome-keyring auth.

%files -n %{devgnomekeyring}
%{_libdir}/libsvn_auth_gnome_keyring-%{api}.so
%endif

#--------------------------------------------------------------------------

%if %{with kwallet}
%define libkwallet %mklibname svn_auth_kwallet %{api} %{major}
%define devkwallet %mklibname svn_auth_kwallet -d

%package -n	%{libkwallet}
Summary:	kwallet support for svn
Group:		System/Libraries
BuildRequires:	kdelibs4-devel
BuildRequires:	pkgconfig(dbus-1)
Requires:	kwallet
Obsoletes:	%{_lib}svn-kwallet0 < 2:1.8.5-2

%description -n	%{libkwallet}
Subversion library that allow interaction with the kwallet daemon.

%files -n	%{libkwallet}
%{_libdir}/libsvn_auth_kwallet-%{api}.so.%{major}*

%package -n 	%{devkwallet}
Summary:	Subversion headers/libraries for development
Group:		Development/KDE and Qt
Requires:	%{name}-devel = %{EVRD}
Requires:	%{libkwallet} = %{EVRD}
Conflicts:	%{name}-devel < 2:1.6.17-2
Obsoletes:	%{name}-kwallet-devel < 2:1.8.5-2

%description -n	%{devkwallet}
This package contains the header files and linker scripts for the
subversion library using kwallet auth.

%files -n %{devkwallet}
%{_libdir}/libsvn_auth_kwallet-%{api}.so
%endif

#--------------------------------------------------------------------------

%package	server
Summary:	Subversion Server
Group:		System/Servers
Requires:	%{name} = %{EVRD}
Requires(pre,preun,postun,post):	rpm-helper
Requires(post):	sed
Requires(post):	systemd

%description server
This package contains the subversion server and configuration files. 

%pre server
%_pre_useradd svn /var/lib/svn /bin/false

%preun server
%_preun_service svnserve

%post server
%tmpfiles_create svnserve
%_post_service svnserve
# fix svn entries in /etc/services
if ! grep -qE '^svn[[:space:]]+3690/(tcp|udp)[[:space:]]+svnserve' %{_sysconfdir}/services; then
        # cleanup
        sed -i -e '/^svn\(serve\)\?/d;/^# svnserve ports added by subversion-server/d' %{_sysconfdir}/services
        echo "# svnserve ports added by subversion-server" >> /etc/services
        echo -e "svn\t3690/tcp\tsvnserve\t# Subversion svnserve" >> /etc/services
        echo -e "svn\t3690/udp\tsvnserve\t# Subversion svnserve" >> /etc/services
fi

%postun server
%_postun_userdel svn

%files server
%doc BUGS CHANGES COMMITTERS LICENSE INSTALL README
%{_bindir}/svnserve
%{_unitdir}/svnserve.service
/var/lib/svn
%{_mandir}/man8/svnserve.8*
%{_mandir}/man5/svnserve.conf.5*
%{_tmpfilesdir}/svnserve.conf

#--------------------------------------------------------------------------

%package	tools
Summary:	Subversion Repo/Server Tools
Group:		Development/Tools
Requires:	%{name} = %{EVRD}

%description tools
This package contains a myriad of tools for subversion server
and repository admins:
  * hot-backup makes a backup of a svn repo without stopping
  * mirror_dir_through_svn.cgi
  * various hook scripts
  * xslt example

Note that cvs2svn has moved out of subversion and is a separate
project.  It has not released its own package yet, but you can
find it at http://cvs2svn.tigris.org/

%files tools
%{_bindir}/hot-backup*
%{_bindir}/svnadmin
%{_bindir}/svnsync
%{_bindir}/svndumpfilter
%{_bindir}/svnrdump
%{_bindir}/svnmucc
%dir %{_libexecdir}/svn-tools
%{_libexecdir}/svn-tools/diff
%{_libexecdir}/svn-tools/diff3
%{_libexecdir}/svn-tools/diff4
%{_libexecdir}/svn-tools/fsfs-access-map
%{_libexecdir}/svn-tools/fsfs-reorg
%{_libexecdir}/svn-tools/fsfs-stats
%{_libexecdir}/svn-tools/svnauthz
%{_libexecdir}/svn-tools/svnauthz-validate
%{_libexecdir}/svn-tools/svn-bench
%{_libexecdir}/svn-tools/svnmucc
%{_libexecdir}/svn-tools/svn-populate-node-origins-index
%{_libexecdir}/svn-tools/svnraisetreeconflict
%{_libexecdir}/svn-tools/svn-rep-sharing-stats
%{_datadir}/%{name}-%{version}/repo-tools
%{_mandir}/man1/svnadmin.1*
%{_mandir}/man1/svndumpfilter.1*
%{_mandir}/man1/svnrdump.1*
%{_mandir}/man1/svnmucc.1*

#--------------------------------------------------------------------------

%if %{with python}
%package -n	python-svn
Summary:	Python bindings for Subversion
Group:		Development/Python
Provides:	python-subversion = %{version}-%{release}
Requires:	python

%description -n	python-svn
This package contains the files necessary to use the subversion
library functions within python scripts.

%files -n	python-svn
%{_libdir}/libsvn_swig_py-%{api}.so.%{major}*
%{py_sitedir}/svn
%{py_platsitedir}/libsvn
%doc tools/examples/*.py subversion/bindings/swig/INSTALL subversion/bindings/swig/NOTES

%package -n	python-svn-devel
Summary:	Subversion headers/libraries for development
Group:		Development/Python
Requires:	%{name}-devel = %{EVRD}
Requires:	python-svn = %{EVRD}
Obsoletes:	python-svn-devel < 2:1.5.2-2
Conflicts:	%{name}-devel < 2:1.6.17-2

%description -n	python-svn-devel
This package contains the header files and linker scripts for
subversion libraries using perl.

%files -n	python-svn-devel
%{_libdir}/libsvn_swig_py-%{api}.so
%endif

#--------------------------------------------------------------------------

%if %{with ruby}
%package -n	ruby-svn
Summary:	Ruby bindings for Subversion
Group:		Development/Ruby
BuildRequires:	ruby-devel
Requires:	ruby
Provides:	ruby-subversion = %{EVRD}

%description -n	ruby-svn
This package contains the files necessary to use the subversion
library functions within ruby scripts.

%files -n	ruby-svn
%{ruby_sitearchdir}/svn
%{ruby_sitelibdir}/*/*.rb
%{_libdir}/libsvn_swig_ruby-%{api}.so.%{major}*

%package -n	ruby-svn-devel
Summary:	Subversion headers/libraries for development
Group:		Development/Ruby
Requires:	ruby-svn = %{EVRD}
Obsoletes:	ruby-svn-devel < 2:1.5.2-2
Conflicts:	%{name}-devel < 2:1.6.17-2

%description -n	ruby-svn-devel
This package contains the header files and linker scripts for
subversion libraries using perl.

%files -n	ruby-svn-devel
%{_libdir}/libsvn_swig_ruby-%{api}.so
%endif

#--------------------------------------------------------------------------

%if %{with java}
# We have the non-major symlink also in this package (due to java design),
# so we only have %%api in package name.
%define libsvnjavahl %mklibname svnjavahl %{api}

%package -n	%{libsvnjavahl}
Summary:	Svn Java bindings library
Group:		System/Libraries

%description -n	%{libsvnjavahl}
Svn Java bindings library

%files -n	%{libsvnjavahl}
%{_libdir}/libsvnjavahl-%{api}.so*

#--------------------------------------------------------------------------

%package -n	svn-javahl
Summary:	Java bindings for Subversion
Group:		Development/Java
Provides:	java-svn = %{EVRD}
Provides:	java-subversion = %{EVRD}
Provides:	subversion-javahl = %{EVRD}
Requires:	%{name} = %{EVRD}
Requires:	%{libsvnjavahl} = %{EVRD}
BuildRequires:	ant
BuildRequires:	java-rpmbuild >= 1.7.3-10
BuildRequires:	junit
BuildRequires:	java-devel

%description -n	svn-javahl
This package contains the files necessary to use the subversion
library functions from Java.

%files -n	svn-javahl
%doc subversion/bindings/javahl/README
%{_javadir}/svn-javahl.jar
%{_javadir}/svn-javahl-%{version}.jar
%endif

#--------------------------------------------------------------------------

%if %{with perl}
%package -n	perl-SVN
Summary:	Perl bindings for Subversion
Group:		Development/Perl
BuildRequires:	perl-devel
Requires:	%{name} = %{EVRD}
Provides:	perl-svn = %{EVRD}

%description -n	perl-SVN
This package contains the files necessary to use the subversion
library functions within perl scripts.

%files -n	perl-SVN
%doc subversion/bindings/swig/INSTALL subversion/bindings/swig/NOTES
%{_libdir}/libsvn_swig_perl-%{api}.so.%{major}*
%{perl_vendorarch}/SVN
%{perl_vendorarch}/auto/SVN
%{perl_sitearch}/*
%{_mandir}/man3/SVN::*.3*

%package -n	perl-svn-devel
Summary:	Subversion headers/libraries for development
Group:		Development/Perl
Requires:	%{name}-devel = %{EVRD}
Requires:	perl-SVN = %{EVRD}
Obsoletes:	perl-SVN-devel < 2:1.5.2-2
Provides:	perl-SVN-devel = %{EVRD}
Conflicts:	%{name}-devel < 2:1.6.17-2

%description -n	perl-svn-devel
This package contains the header files and linker scripts for
subversion libraries using perl.

%files -n	perl-svn-devel
%{_libdir}/libsvn_swig_perl-%{api}.so
%endif

#----------------------------------------------------------------

%package -n	apache-mod_dav_svn
Summary:	Subversion server DSO module for apache
Group:		System/Servers
Requires:	%{name}-tools = %{EVRD}
Requires:	apache-mod_dav >= %{apache_version}

%description -n	apache-mod_dav_svn
This package contains the apache server extension DSO for running
a subversion server.

%files -n    apache-mod_dav_svn
%doc subversion/mod_authz_svn/INSTALL
%config(noreplace) %{_sysconfdir}/httpd/modules.d/10_mod_dav_svn.conf
%config(noreplace) %{_sysconfdir}/httpd/conf.d/subversion.conf
%{_libdir}/apache/mod_dav_svn.so
%{_libdir}/apache/mod_authz_svn.so
%{_libdir}/apache/mod_dontdothat.so

#--------------------------------------------------------------------------

%prep
%setup -q -a 7
%apply_patches

# fix shellbang lines, #111498
perl -pi -e 's|/usr/bin/env perl|%{_bindir}/perl|g' tools/hook-scripts/*.pl.in

# fix file perms
chmod 644 BUGS CHANGES COMMITTERS LICENSE INSTALL README

# move latest svnbook snapshot as their target version
mv svn-book-html-chunk svnbook-1.8

# This PATH order makes the fugly test for libtoolize work...
PATH=/usr/bin:$PATH ./autogen.sh --release

# lib64 fixes
perl -pi -e "s|\\$serf_prefix/lib\b|\\$serf_prefix/%{_lib}|g" build/ac-macros/serf.m4 configure*

%build
%serverbuild

%if %{with java}
export JAVADIR=%{_jvmdir}/java
%endif

%define _disable_ld_no_undefined 1

%if %{with ruby}
# override weird -shrext from ruby
export svn_cv_ruby_link="%{__cc} -shared"
export svn_cv_ruby_sitedir_libsuffix=""
export svn_cv_ruby_sitedir_archsuffix=""
%endif

%configure2_5x \
	--localstatedir=/var/lib \
	--with-apr_memcache=%{_prefix} \
	--with-apxs=%{_bindir}/apxs \
	--with-apache-libexecdir=%{_libdir}/apache/ \
	--with-apr=%{_bindir}/apr-1-config \
	--with-apr-util=%{_bindir}/apu-1-config \
	--disable-mod-activation \
	--with-swig=%{_prefix} \
	--disable-static \
%if %{with debug}
	--enable-maintainer-mode \
	--enable-debug \
%endif
%if %{with java}
	--enable-javahl \
	--with-jdk=%{_jvmdir}/java \
	--with-junit=%{_javadir}/junit.jar \
%endif
%if %{with gnome_keyring}
	--with-gnome-keyring \
%endif
%if %{with kwallet}
	--with-kwallet \
%endif
	--enable-shared \
	--with-gssapi=%{_prefix} \
	--with-libmagic=%{_prefix} \
	--with-serf=%{_prefix} \
	--with-sqlite=%{_prefix}

%if %{with ruby}
# fix weird broken autopoo
perl -pi -e "s|^SWIG_RB_SITE_ARCH_DIR.*|SWIG_RB_SITE_ARCH_DIR=\"%ruby_sitearchdir\"|g" Makefile
perl -pi -e "s|^SWIG_RB_SITE_LIB_DIR.*|SWIG_RB_SITE_LIB_DIR=\"%ruby_sitelibdir\"|g" Makefile
%endif

# fix weird broken autopoo
perl -pi -e "s|^toolsdir.*|toolsdir=%{_libexecdir}/svn-tools|g" Makefile

%{make} all

%if %{with python}
make swig-py swig_pydir=%{py_platsitedir}/libsvn swig_pydir_extra=%{py_sitedir}/svn
%endif

%if %{with perl}
make swig-pl
pushd  subversion/bindings/swig/perl/native
        perl Makefile.PL
popd
%endif

%if %{with ruby}
make swig-rb
%endif

%if %{with java}
make javahl
%endif

%check
%if %{with test}
echo "###########################################################################"
echo "This can take quite some time to finish, so please be patient..."
echo "Don't be too surprised it the tests takes 30 minutes on a dual xeon machine..."
make LC_ALL=C LANG=C LD_LIBRARY_PATH="`pwd`/subversion/bindings/swig/perl/libsvn_swig_perl/.libs:`pwd`/subversion/bindings/swig/python/libsvn_swig_py/.libs:\
`pwd`/subversion/bindings/swig/python/.libs:`pwd`/subversion/libsvn_ra_local/.libs:`pwd`/subversion/svnadmin/.libs:\
`pwd`/subversion/tests/libsvn_ra_local/.libs:`pwd`/subversion/tests/libsvn_fs/.libs:`pwd`/subversion/tests/libsvn_wc/.libs:\
`pwd`/subversion/tests/libsvn_fs_base/.libs:`pwd`/subversion/tests/libsvn_diff/.libs:`pwd`/subversion/tests/libsvn_subr/.libs:\
`pwd`/subversion/tests/libsvn_delta/.libs:`pwd`/subversion/tests/libsvn_repos/.libs:`pwd`/subversion/tests/.libs:\
`pwd`/subversion/svnserve/.libs:`pwd`/subversion/libsvn_fs/.libs:`pwd`/subversion/libsvn_ra/.libs:`pwd`/subversion/libsvn_wc/.libs:\
`pwd`/subversion/mod_dav_svn/.libs:`pwd`/subversion/mod_authz_svn/.libs:`pwd`/subversion/svnlook/.libs:`pwd`/subversion/svndumpfilter/.libs:\
`pwd`/subversion/libsvn_client/.libs:`pwd`/subversion/libsvn_fs_base/bdb/.libs:`pwd`/subversion/libsvn_fs_base/util/.libs:\
`pwd`/subversion/libsvn_fs_base/.libs:`pwd`/subversion/libsvn_diff/.libs:`pwd`/subversion/libsvn_subr/.libs:`pwd`/subversion/svnversion/.libs:\
`pwd`/subversion/libsvn_ra_dav/.libs:`pwd`/subversion/libsvn_ra_svn/.libs:`pwd`/subversion/libsvn_delta/.libs:`pwd`/subversion/libsvn_fs_fs/.libs:\
`pwd`/subversion/libsvn_repos/.libs:`pwd`/subversion/clients/cmdline/.libs:$LD_LIBRARY_PATH" check
%endif

%install
%makeinstall_std

%if %{with python}
%makeinstall_std install-swig-py swig_pydir=%{py_platsitedir}/libsvn swig_pydir_extra=%{py_sitedir}/svn
# Precompile python
%py_compile %{buildroot}/%{py_platsitedir}/libsvn
%py_compile %{buildroot}/%{py_sitedir}/svn
%endif

%if %{with perl}
%makeinstall_std install-swig-pl-lib
pushd subversion/bindings/swig/perl/native/
        perl Makefile.PL
        %makeinstall_std
popd
%endif

%if %{with ruby}
%makeinstall_std install-swig-rb
%endif
%if %{with java}
%makeinstall_std install-javahl

mkdir -p %{buildroot}%{_javadir}
mv %{buildroot}%{_libdir}/svn-javahl/svn-javahl.jar %{buildroot}%{_javadir}/svn-javahl-%{version}.jar
ln -s svn-javahl-%{version}.jar %{buildroot}%{_javadir}/svn-javahl.jar

%{_bindir}/chrpath -d %{buildroot}%{_libdir}/libsvnjavahl-1.so
%endif

%if %{with perl}
# perl bindings
make pure_vendor_install -C subversion/bindings/swig/perl/native DESTDIR=%{buildroot}
%endif

install -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/httpd/modules.d/10_mod_dav_svn.conf
install -D -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/httpd/conf.d/subversion.conf

install -D -p -m 0644 %{SOURCE9} %{buildroot}%{_tmpfilesdir}/svnserve.conf

# install the extra module
%makeinstall_std install-tools

# cleanup
#rm -f %{buildroot}%{_libdir}/*.*a

######################
###  client-tools  ###
######################

# various commands
# contrib was removed in subversion-1.7.x :
#  -- http://subversion.apache.org/docs/release-notes/1.7.html
#  -- (shlomif)
# install -m 755 contrib/client-side/search-svnlog.pl %%{buildroot}%%{_bindir}
# (cd  %%{buildroot}/%%{_bindir}; ln -sf  search-svnlog.pl search-svnlog)
# install -m 755 contrib/client-side/svn_all_diffs.pl %%{buildroot}%%{_bindir}
# (cd  %%{buildroot}/%%{_bindir}; ln -sf  svn_all_diffs.pl svn_all_diffs)
# install -m 755 contrib/client-side/svn_load_dirs/svn_load_dirs.pl %%{buildroot}%%{_bindir}
# (cd  %%{buildroot}/%%{_bindir}; ln -sf  svn_load_dirs.pl svn_load_dirs)
# install -m 755 contrib/client-side/svn-log.pl %%{buildroot}%%{_bindir}
# (cd  %%{buildroot}/%%{_bindir}; ln -sf  svn-log.pl svn-log)

install -m 755 tools/client-side/showchange.pl %{buildroot}%{_bindir}
(cd  %{buildroot}/%{_bindir}; ln -sf  showchange.pl showchange)

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
popd

pushd tools/hook-scripts
install -m 755 commit-email.rb %{buildroot}/%{_datadir}/%{name}-%{version}/repo-tools/hook-scripts
popd

#xslt
install -d -m755 %{buildroot}%{_datadir}/%{name}-%{version}/repo-tools/xslt
install -m 644 tools/xslt/svnindex.css %{buildroot}%{_datadir}/%{name}-%{version}/repo-tools/xslt
install -m 644 tools/xslt/svnindex.xsl %{buildroot}%{_datadir}/%{name}-%{version}/repo-tools/xslt

#cgi
# contrib was removed in subversion-1.7.x :
# install -d -m755 %%{buildroot}%%{_datadir}/%%{name}-%%{version}/repo-tools/cgi
# install -m 755 contrib/cgi/mirror_dir_through_svn.cgi %%{buildroot}%%{_datadir}/%%{name}-%%{version}/repo-tools/cgi
# install -m 644 contrib/cgi/mirror_dir_through_svn.README %%{buildroot}%%{_datadir}/%%{name}-%%{version}/repo-tools/cgi
# install -m 755 contrib/cgi/tweak-log.cgi %%{buildroot}%%{_datadir}/%%{name}-%%{version}/repo-tools/cgi

# fix a missing file...
ln -sf libsvn_diff-1.so.0.0.0 %{buildroot}%{_libdir}/libsvn_diff.so

%{_bindir}/chrpath -d %{buildroot}%{_bindir}/svn
%{_bindir}/chrpath -d %{buildroot}%{_bindir}/svnlook
%{_bindir}/chrpath -d %{buildroot}%{_bindir}/svnversion
%{_bindir}/chrpath -d %{buildroot}%{_bindir}/svnserve
%{_bindir}/chrpath -d %{buildroot}%{_bindir}/svnadmin
%{_bindir}/chrpath -d %{buildroot}%{_bindir}/svndumpfilter
%{_bindir}/chrpath -d %{buildroot}%{_bindir}/svnsync
%{_bindir}/chrpath -d %{buildroot}%{_bindir}/svnrdump

# fix the stupid rpath stuff...
myf() { find %{buildroot}%{perl_vendorarch} -type f -name "*.so"; }
# Fix the readonly permissions of the perl files.
myf | xargs chmod u+w
myf | xargs chrpath -d

# handle translations
%find_lang %{name}

# fix the server parts
mkdir -p %{buildroot}%{_unitdir}
install -p -m644 %{SOURCE8} %{buildroot}%{_unitdir}/svnserve.service
install -d %{buildroot}/var/lib/svn/repositories

# Move perl man
chmod u+w %{buildroot}%_prefix/local/share/man/man3/*
mv -f %{buildroot}%_prefix/local/share/man/man3/* %{buildroot}%{_mandir}/man3/

# cleanup
find %{buildroot} -name "perllocal.pod" | xargs rm -f

