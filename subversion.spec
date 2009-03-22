%define _requires_exceptions devel(libneon

%define apache_version 2.2.0
%define libsvn %mklibname svn 0

%define build_python 1
%{?_without_python: %{expand: %%global build_python 0}}

%define build_ruby 1
%{?_without_ruby: %{expand: %%global build_ruby 0}}

%define build_java 0
%{?_with_java: %{expand: %%global build_java 1}}

%define build_perl 1
%{?_without_perl: %{expand: %%global build_perl 0}}

%define build_test 0
%{?_with_test: %{expand: %%global build_test 1}}

%define with_debug 0
%{?_with_debug: %{expand: %%global with_debug 1}}

%if %mdkversion <= 200700
%define build_java 0
%define build_ruby 0

# play safe work around (misc)
%define py_purelibdir %{py_libdir}
%define py_platlibdir %{py_libdir}
%define py_platsitedir %{py_sitedir}
%endif

Name: subversion
Version: 1.6.0
Release: %mkrel 0.1
Epoch: 2
Summary: A Concurrent Versioning System
License: BSD CC2.0
Group: Development/Other
URL: http://subversion.tigris.org
Source0: http://subversion.tigris.org/tarballs/%name-%version.tar.gz
Source2: %mod_dav_conf
Source3: %mod_authz_conf
Source4: %name.bash-completion
Source5: %name-1.3.0-global-config
Source6: %name-1.3.0-global-servers
Source7: http://svnbook.red-bean.com/nightly/en/svn-book-html-chunk.tar.bz2
Patch0: subversion-1.5.0-underlink.patch
# http://www.rz.uni-karlsruhe.de/~rz41/source/Patches/subversion-1.4.3/hook-scripts-patch
Patch4: subversion-hook-script_pathfix.diff
Patch5: subversion-propchange-email.diff
Patch6: subversion-1.5.5-format_not_a_string_literal_and_no_format_arguments.diff
BuildRequires:	autoconf >= 2.54
BuildRequires:	libtool >= 1.4.2
BuildRequires:	chrpath
BuildRequires:	python >= 2.2
BuildRequires:	texinfo
BuildRequires:	info-install
BuildRequires:	db4-devel
%if %{mdkversion} < 200610
BuildRequires:	neon-devel >= 0.25.0
%else
BuildRequires:	neon-devel
%endif
BuildRequires:	apache-devel >=  %{apache_version}
BuildRequires:	apr-devel >= 1:1.3.0
BuildRequires:	apr-util-devel >= 1.3.0
BuildRequires:	libxslt-proc
BuildRequires:	docbook-style-xsl
BuildRequires:	serf-devel >= 0.3.0
BuildRequires:	sqlite3-devel >= 3.4.0
# Swig is runtime only
BuildRequires:	swig >= 1.3.27
%if %mdkversion >= 1020
BuildRequires:	multiarch-utils >= 1.0.3
%endif
# Obsoletes - kill all non sys build library packages
# Just server and client need some libraries and we need just one
# main ( client ) and one server package, as well bindings and doc packages
Obsoletes: %name-client-tools < 2:1.2.3-4mdk
Obsoletes: %name-repos < 1.2.3-4mdk
Obsoletes: %{_lib}svn_client1_0 < 2:1.2.3-4mdk
Obsoletes: %{_lib}svn_ra_dav1_0 < 2:1.2.3-4mdk
Obsoletes: %{_lib}svn_ra_local1_0 < 2:1.2.3-4mdk
Obsoletes: %{_lib}svn_ra_svn1_0 < 2:1.2.3-4mdk
Obsoletes: %{_lib}svn_delta1_0 < 2:1.2.3-4mdk
Obsoletes: %{_lib}svn_diff1_0 < 2:1.2.3-4mdk
Obsoletes: %{_lib}svn_repos1_0 < 2:1.2.3-4mdk
Obsoletes: %{_lib}svn_subr1_0 < 2:1.2.3-4mdk
Obsoletes: %{_lib}svn_fs_fs1_0 < 2:1.2.3-4mdk
Obsoletes: %{_lib}svn_fs_base1_0 < 2:1.2.3-4mdk
Conflicts: %name-server < 2:1.2.3-4mdk
Conflicts: %{libsvn} < 2:1.3.0-2mdk
Provides: %name-ra-method = %{epoch}:%version-%{release}
Provides: %name-client-tools = %{epoch}:%version-%{release}
Provides: svn = %{epoch}:%{version}
Requires: %{libsvn} = %{epoch}:%{version}
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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

%files -f %name.lang
%defattr(-,root,root)
%_bindir/svn
%_bindir/svnversion
%_bindir/showchange*
%_bindir/search-svnlog*
%_bindir/svn_all_diffs*
%_bindir/svn_load_dirs*
%_bindir/svn-log*
%_bindir/svnlook
%_sysconfdir/bash_completion.d/%name
%_mandir/man1/svn.*
%_mandir/man1/svnlook.*
%_mandir/man1/svnversion.*
%_mandir/man1/svnsync.*
%dir %_datadir/subversion-%{version}
%if %mdkversion <= 910
    # Already included in vim-common on 9.2 and newer.
    %_datadir/vim/syntax/svn.vim
%endif

#--------------------------------------------------------------------------

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

%post doc
%_install_info svn-design.info
%_install_info svn-handbook.info

%postun doc
%_install_info svn-design.info
%_install_info svn-handbook.info

%files doc
%defattr(0644,root,root,755)
%doc svnbook-1.*
%doc doc/user/*.html
%doc doc/user/*.txt

#--------------------------------------------------------------------------

%package -n %libsvn
Summary: Subversion libraries
Group: System/Libraries
Conflicts: subversion < 2:1.3.0-2mdk 

%description -n %libsvn
Subversion common libraries

%if %mdkversion < 200900
%post -n %libsvn -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %libsvn -p /sbin/ldconfig
%endif

%files -n %libsvn
%defattr(-,root,root)
# list all ra libs to make sure we don't miss any
# in a bogus build
%_libdir/libsvn_ra-1.so.*
%_libdir/libsvn_ra_local-1.so.*
%_libdir/libsvn_ra_svn-1.so.*
%_libdir/libsvn_ra_neon-1.so.*
%_libdir/libsvn_ra_serf-*.so.*
%_libdir/libsvn_client*so.*
%_libdir/libsvn_wc-*so.*
%_libdir/libsvn_delta-*so.*
%_libdir/libsvn_subr-*so.*
%_libdir/libsvn_diff-*so.*
%_libdir/libsvn_fs*.so.*
%_libdir/libsvn_repos-*.so.*
%config(noreplace) %_sysconfdir/subversion/*

#--------------------------------------------------------------------------

%package	server
Summary:	Subversion Server
Group:		System/Servers
Requires: %name = %{epoch}:%version-%{release}
Requires(pre):  rpm-helper
Requires(postun): rpm-helper
Requires(post): sed
# soname didn't change between 1.3.x and 1.4.x, but we
# need the right one...
Requires: %{libsvn} = %{epoch}:%{version}
BuildRoot: %{_tmppath}/%name-%version

%description server
This package contains a myriad of tools for subversion server
and repository admins:
  * hot-backup makes a backup of a svn repo without stopping
  * mirror_dir_through_svn.cgi 
  * various hook scripts
  * xslt example 

Note that cvs2svn has moved out of subversion and is a separate
project.  It has not released its own package yet, but you can
find it at http://cvs2svn.tigris.org/

%pre server
%_pre_useradd svn /var/lib/svn /bin/false

%post server
# Libraries for REPOS ( Repository ) and FS ( filesystem backends ) are in
# server now, so we need a ldconfig
%if %mdkversion < 200900
/sbin/ldconfig
%endif
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
%if %mdkversion < 200900
/sbin/ldconfig
%endif

%files server
%defattr(-,root,root)
%doc BUGS CHANGES COMMITTERS COPYING HACKING INSTALL README
%doc notes/repos_upgrade_HOWTO
%_bindir/svnserve
%config(noreplace) %_sysconfdir/xinetd.d/svnserve
%attr(0770,svn,svn) /var/lib/svn
%_mandir/man8/svnserve.8*
%_mandir/man5/svnserve.conf.5*

#--------------------------------------------------------------------------

%package tools
Summary:	Subversion Repo/Server Tools
Group: Development/Other
Requires: %name = %{epoch}:%version-%{release}
Conflicts: %name-server < 1.2.3-4mdk
Obsoletes: %name-repo-tools < 1.2.3-4mdk
# soname didn't change between 1.3.x and 1.4.x, but we
# need the right one...
Requires: %{libsvn} = %{epoch}:%{version}

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
%defattr(-,root,root)
%_bindir/hot-backup*
%_bindir/svnadmin
%_bindir/svnsync
%_bindir/svndumpfilter
%_datadir/%name-%version/repo-tools
%_mandir/man1/svnadmin.1*
%_mandir/man1/svndumpfilter.1*

#--------------------------------------------------------------------------

%if %{build_python}

%package -n	python-svn
Summary:	Python bindings for Subversion
Group: Development/Other
%py_requires -d
Provides: python-subversion = %version-%{release}
Requires: python
# soname didn't change between 1.3.x and 1.4.x, but we
# need the right one...
Requires: %{libsvn} = %{epoch}:%{version}

%description -n python-svn
This package contains the files necessary to use the subversion
library functions within python scripts.

%files -n python-svn
%defattr(0644,root,root,755)
%_libdir/libsvn_swig_py*.so.*
%{py_sitedir}/svn
%{py_platsitedir}/libsvn
%doc tools/examples/*.py subversion/bindings/swig/INSTALL subversion/bindings/swig/NOTES

%endif

#--------------------------------------------------------------------------

%if %{build_ruby}

%package -n	ruby-svn
Summary:	Ruby bindings for Subversion
Group: Development/Ruby
BuildRequires: ruby-devel
Requires: ruby
Requires: %{libsvn} = %{epoch}:%{version}
Provides: ruby-subversion = %{epoch}:%version-%{release}

%description -n	ruby-svn
This package contains the files necessary to use the subversion
library functions within ruby scripts.

%files -n ruby-svn
%defattr(-,root,root)
%ruby_sitearchdir/svn
%exclude %ruby_sitearchdir/*/*/*.la
%ruby_sitelibdir/*/*.rb
%_libdir/libsvn_swig_ruby*.so.*

%endif

#--------------------------------------------------------------------------

%if %{build_java}
%define libsvnjavahl %mklibname svnjavahl 0

%package -n %{libsvnjavahl}
Summary: Svn Java bindings library
Group: System/Libraries

%description -n %{libsvnjavahl}
Svn Java bindings library

%files -n %{libsvnjavahl}
%defattr(0644,root,root,0755)
%_libdir/libsvnjavahl-1.so.*


%package -n svn-javahl
Summary:	Java bindings for Subversion
Group:		Development/Java
Obsoletes:      java-svn < %{epoch}:%{version}-%{release}
Provides:       java-svn = %{epoch}:%{version}-%{release}
Provides:	java-subversion = %{epoch}:%{version}-%{release}
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires: %{libsvn} = %{epoch}:%{version}-%{release}
Requires: %{libsvnjavahl} = %{epoch}:%{version}-%{release}
BuildRequires:  java-devel
BuildRequires:  ant
%if %mdkversion >= 200810
BuildRequires:  java-rpmbuild >= 1.7.3-10
%else
BuildRequires:  jpackage-utils >= 1.7.3-10
%endif
BuildRequires:  junit

%description -n	svn-javahl
This package contains the files necessary to use the subversion
library functions from Java.

%files -n svn-javahl
%defattr(0644,root,root,0755)
%doc subversion/bindings/javahl/README
%{_javadir}/svn-javahl.jar
%{_javadir}/svn-javahl-%{version}.jar

%endif

#--------------------------------------------------------------------------

%if %{build_perl}

%package -n perl-SVN
Summary:	Perl bindings for Subversion
Group:		Development/Perl
BuildRequires: perl-devel
Requires:	%name = %{epoch}:%version-%{release}
Obsoletes:	perl-svn
Provides:	perl-svn = %{epoch}:%version-%{release}
Requires: %{libsvn} = %{epoch}:%{version}

%description -n perl-SVN
This package contains the files necessary to use the subversion
library functions within perl scripts.

%files -n perl-SVN
%defattr(-,root,root)
%doc subversion/bindings/swig/INSTALL subversion/bindings/swig/NOTES
%_libdir/libsvn_swig_perl*.so.*
%{perl_vendorarch}/SVN
%{perl_vendorarch}/auto/SVN
%{perl_sitearch}/*
%_mandir/man3/SVN::*.3*

%endif

#----------------------------------------------------------------

%package devel
Summary: Subversion headers/libraries for development
Group: Development/Other
Provides: libsvn-devel = %{epoch}:%version-%{release}
Obsoletes: libsubversion1_0-devel < 1.2.3-4mdk
Obsoletes: libsubversion1_0-static-devel < 1.2.3-4mdk
%if %{build_java}
Requires: svn-javahl = %{epoch}:%{version}
%endif
%if %{build_perl}
Requires: perl-SVN = %{epoch}:%{version}
Obsoletes: perl-SVN-devel < 2:1.5.2-2
Provides: per-SVN-devel = %{epoch}:%{version}
%endif
%if %{build_perl}
Requires: python-svn = %{epoch}:%{version}
Obsoletes: python-svn-devel < 2:1.5.2-2
Provides: python-svn-devel = %{epoch}:%{version}
%endif
%if %{build_ruby}
Requires: ruby-svn = %{epoch}:%{version}
Obsoletes: ruby-svn-devel < 2:1.5.2-2
Provides: ruby-svn-devel = %{epoch}:%{version}
%endif
Requires: %libsvn = %{epoch}:%version-%release
%if %{mdkversion} < 200610
Requires: neon-devel >= 0.25.0
%else
Requires: neon-devel
%endif

%description devel
This package contains the header files and linker scripts for
subversion libraries.

%files devel
%defattr(-,root,root)
%doc tools/examples/minimal_client.c
%_libdir/libsvn*.la
%_includedir/subversion*/*
%_libdir/libsvn*.so


#----------------------------------------------------------------

%define mod_version  %{apache_version}_%version
%define mod_dav_name mod_dav_svn
%define mod_dav_conf 46_%{mod_dav_name}.conf
%define mod_dav_so %{mod_dav_name}.so
%define mod_authz_name mod_authz_svn
%define mod_authz_conf 47_%{mod_authz_name}.conf
%define mod_authz_so %{mod_authz_name}.so

%package -n	apache-mod_dav_svn
Summary:	Subversion server DSO module for apache
Group:		System/Servers
Requires: %name-tools = %{epoch}:%version-%{release}
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= %{apache_version}
Requires(pre):	apache >= %{apache_version}
Requires(pre):	apache-mod_dav >= %{apache_version}
# soname didn't change between 1.3.x and 1.4.x, but we
# need the right one...
Requires(pre): %{libsvn} = %{epoch}:%{version}
Obsoletes:	apache-mod_authz_svn

%description -n apache-mod_dav_svn
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

%post -n apache-mod_dav_svn
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun -n apache-mod_dav_svn
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
    fi
fi

%files -n apache-mod_dav_svn
%defattr(-,root,root)
%doc subversion/%{mod_authz_name}/INSTALL
%attr(0644,root,root) %config(noreplace) %_sysconfdir/httpd/modules.d/%{mod_dav_conf}
%attr(0644,root,root) %config(noreplace) %_sysconfdir/httpd/modules.d/%{mod_authz_conf}
%attr(0755,root,root) %_libdir/apache-extramodules/%{mod_dav_so}
%attr(0755,root,root) %_libdir/apache-extramodules/%{mod_authz_so}
%attr(0644,root,root) %{_var}/www/icons/subversion.png

%package -n	apache-mod_dontdothat
Summary:	An Apache module that allows you to block specific types of Subversion requests
Group:		System/Servers
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= %{apache_version}
Requires(pre):	apache >= %{apache_version}
Requires(pre):	apache-mod_dav_svn = %{epoch}:%{version}

%description -n apache-mod_dontdothat
mod_dontdothat is an Apache module that allows you to block specific types
of Subversion requests.  Specifically, it's designed to keep users from doing
things that are particularly hard on the server, like checking out the root
of the tree, or the tags or branches directories.  It works by sticking an
input filter in front of all REPORT requests and looking for dangerous types
of requests.  If it finds any, it returns a 403 Forbidden error.

%post -n apache-mod_dontdothat
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun -n apache-mod_dontdothat
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
    fi
fi

%files -n apache-mod_dontdothat
%defattr(-,root,root)
%doc contrib/server-side/mod_dontdothat/README
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/48_mod_dontdothat.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/conf/dontdothat.conf
%attr(0755,root,root) %{_libdir}/apache-extramodules/mod_dontdothat.so

#--------------------------------------------------------------------------

%prep
%setup -q -a 7
%patch0 -p1 -b .underlink
#%patch4 -p0 -b .hook-script_pathfix
# it was removed after 1.3.2 but still referenced in subversion/libsvn_repos/repos.c
#%patch5 -p1 -b .propchange-email
%patch6 -p1 -b .format_not_a_string_literal_and_no_format_arguments

rm -rf neon apr apr-util db4

# fix shellbang lines, #111498
perl -pi -e 's|/usr/bin/env perl|%{_bindir}/perl|g' tools/hook-scripts/*.pl.in

# fix file perms
chmod 644 BUGS CHANGES COMMITTERS COPYING HACKING INSTALL README

# move latest svnbook snapshot as their target version
mv svn-book-html-chunk svnbook-1.6

# lib64 fixes
perl -pi -e "s|\\$serf_prefix/lib\b|\\$serf_prefix/%{_lib}|g" build/ac-macros/serf.m4 configure*

%build
%serverbuild

%if %{build_java}
export JAVADIR=%{_jvmdir}/java
%endif

./configure \
   --prefix=%{_prefix} \
   --sysconfdir=%_sysconfdir \
   --datadir=%_datadir \
   --libdir=%_libdir \
   --localstatedir=/var/lib \
   --mandir=%_mandir \
   --with-apr_memcache=%{_prefix} \
   --with-apxs=%{_sbindir}/apxs \
   --with-apache-libexecdir=%{_libdir}/apache-extramodules \
   --with-apr=%{_bindir}/apr-1-config \
   --with-apr-util=%{_bindir}/apu-1-config \
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
   --enable-shared \
   --with-serf=%{_prefix} \
   --disable-neon-version-check \
   --with-sqlite=%{_prefix}

%{make} all

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
%{_sbindir}/apxs -c -Isubversion/include -Isubversion \
    contrib/server-side/mod_dontdothat/mod_dontdothat.c \
    subversion/libsvn_subr/libsvn_subr-1.la

%install
rm -rf %buildroot

%if %{build_test}
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

%makeinstall_std

%if %{build_python}
%makeinstall_std install-swig-py swig_pydir=%{py_platsitedir}/libsvn swig_pydir_extra=%{py_sitedir}/svn
# Precompile python 
%py_compile %buildroot/%{py_platsitedir}/libsvn
%py_compile %buildroot/%{py_sitedir}/svn

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
%{makeinstall_std} install-javahl

mkdir -p %{buildroot}%{_javadir}
%{__mv} %{buildroot}%{_libdir}/svn-javahl/svn-javahl.jar %{buildroot}%{_javadir}/svn-javahl-%{version}.jar
%{__ln_s} svn-javahl-%{version}.jar %{buildroot}%{_javadir}/svn-javahl.jar

%{_bindir}/chrpath -d %{buildroot}%{_libdir}/libsvnjavahl-1.so

%endif

%if %{build_perl}
# perl bindings
make pure_vendor_install -C subversion/bindings/swig/perl/native DESTDIR=%buildroot
%endif

install -d %buildroot%_sysconfdir/httpd/modules.d
cat %{SOURCE2} > %buildroot%_sysconfdir/httpd/modules.d/%{mod_dav_conf}
cat %{SOURCE3} > %buildroot%_sysconfdir/httpd/modules.d/%{mod_authz_conf}

# install the extra module
install -m0755 contrib/server-side/mod_dontdothat/.libs/mod_dontdothat.so %{buildroot}%{_libdir}/apache-extramodules/

# cleanup
rm -f %{buildroot}%{_libdir}/apache-extramodules/*.*a

cat > %{buildroot}%{_sysconfdir}/httpd/modules.d/48_mod_dontdothat.conf << EOF
<IfDefine HAVE_DONTDOTHAT>
    <IfModule !mod_dontdothat.c>
	LoadModule dontdothat_module    extramodules/mod_dontdothat.so
    </IfModule>
</IfDefine>

<IfModule mod_dontdothat.c>

    <Location /svn>
        DAV svn
        SVNParentPath /var/lib/svn/repositories
        DontDoThatConfigFile %{_sysconfdir}/httpd/conf/dontdothat.conf
    </Location>

</IfModule>
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

# vim syntax hilighting
%if %mdkversion <= 910
    # Already included in vim-common on 9.2 and newer.
    install -d -m 755 %buildroot/%_datadir/vim/syntax
    install -m 644 contrib/client-side/svn.vim %buildroot/%_datadir/vim/syntax
%endif

# various commands
install -m 755 contrib/client-side/search-svnlog.pl %buildroot%_bindir
(cd  %buildroot/%_bindir; ln -sf  search-svnlog.pl search-svnlog)
install -m 755 contrib/client-side/svn_all_diffs.pl %buildroot%_bindir
(cd  %buildroot/%_bindir; ln -sf  svn_all_diffs.pl svn_all_diffs)
install -m 755 contrib/client-side/svn_load_dirs/svn_load_dirs.pl %buildroot%_bindir
(cd  %buildroot/%_bindir; ln -sf  svn_load_dirs.pl svn_load_dirs)
install -m 755 contrib/client-side/svn-log.pl %buildroot%_bindir
(cd  %buildroot/%_bindir; ln -sf  svn-log.pl svn-log)
install -m 755 tools/client-side/showchange.pl %buildroot%_bindir
(cd  %buildroot/%_bindir; ln -sf  showchange.pl showchange)

# bash completion
install -d -m 755 %buildroot%_sysconfdir/bash_completion.d
install -m 644 %SOURCE4 %buildroot%_sysconfdir/bash_completion.d/%name

# Global configs
install -d -m 755 %buildroot%_sysconfdir/subversion
install -m 644 %SOURCE5 %buildroot%_sysconfdir/subversion/config
install -m 644 %SOURCE6 %buildroot%_sysconfdir/subversion/servers

####################
###  repo-tools  ###
####################

# hotbackup tool
install -m 755 tools/backup/hot-backup.py %buildroot%_bindir
(cd %buildroot%_bindir; ln -sf  hot-backup.py hot-backup)

# hook-scripts
install -d -m755 %buildroot%_datadir/%name-%version/repo-tools/hook-scripts
pushd tools/hook-scripts
install -m 644 commit-access-control.cfg.example %buildroot/%_datadir/%name-%version/repo-tools/hook-scripts
install -m 755 commit-access-control.pl %buildroot/%_datadir/%name-%version/repo-tools/hook-scripts
install -m 644 svnperms.conf.example %buildroot/%_datadir/%name-%version/repo-tools/hook-scripts
install -m 755 svnperms.py %buildroot/%_datadir/%name-%version/repo-tools/hook-scripts
install -m 755 mailer/mailer.py %buildroot/%_datadir/%name-%version/repo-tools/hook-scripts
install -m 644 mailer/mailer.conf.example %buildroot/%_datadir/%name-%version/repo-tools/hook-scripts
install -m 644 README %buildroot/%_datadir/%name-%version/repo-tools/hook-scripts
popd

pushd contrib/hook-scripts
install -m 755 commit-email.pl %buildroot/%_datadir/%name-%version/repo-tools/hook-scripts
popd

#xslt
install -d -m755 %buildroot%_datadir/%name-%version/repo-tools/xslt
install -m 644 tools/xslt/svnindex.css %buildroot%_datadir/%name-%version/repo-tools/xslt
install -m 644 tools/xslt/svnindex.xsl %buildroot%_datadir/%name-%version/repo-tools/xslt

#cgi
install -d -m755 %buildroot%_datadir/%name-%version/repo-tools/cgi
install -m 755 contrib/cgi/mirror_dir_through_svn.cgi %buildroot%_datadir/%name-%version/repo-tools/cgi
install -m 644 contrib/cgi/mirror_dir_through_svn.README %buildroot%_datadir/%name-%version/repo-tools/cgi
install -m 755 contrib/cgi/tweak-log.cgi %buildroot%_datadir/%name-%version/repo-tools/cgi

# install a nice icon for web usage
install -d %buildroot/var/www/icons
install -m644 notes/logo/256-colour/subversion_logo_hor-237x32.png %buildroot/var/www/icons/subversion.png

# fix a missing file...
ln -sf libsvn_diff-1.so.0.0.0 %buildroot%_libdir/libsvn_diff.so

%{_bindir}/chrpath -d %{buildroot}%{_bindir}/svn
%{_bindir}/chrpath -d %{buildroot}%{_bindir}/svnlook
%{_bindir}/chrpath -d %{buildroot}%{_bindir}/svnversion
%{_bindir}/chrpath -d %{buildroot}%{_bindir}/svnserve
%{_bindir}/chrpath -d %{buildroot}%{_bindir}/svnadmin
%{_bindir}/chrpath -d %{buildroot}%{_bindir}/svndumpfilter
%{_bindir}/chrpath -d %{buildroot}%{_bindir}/svnsync

# fix the stupid rpath stuff...
find %buildroot%{perl_vendorarch} -type f -name "*.so" | xargs chrpath -d

# handle translations
%find_lang %name

# fix the server parts
install -d %buildroot%_sysconfdir/xinetd.d
cat > svnserve.xinetd << EOF
# default: off
# description: svnserve is the server part of Subversion.
service svnserve
{
    disable		= yes
    port		= 3690
    socket_type		= stream
    protocol		= tcp
    wait		= no
    user		= svn
    server		= %_bindir/svnserve
    server_args		= -i -r /var/lib/svn/repositories
}
EOF
install -m 644 svnserve.xinetd %buildroot%_sysconfdir/xinetd.d/svnserve
install -d %buildroot/var/lib/svn/repositories

# Move perl man
mv %buildroot%_prefix/local/share/man/man3/* %buildroot%_mandir/man3/

# cleanup
find %buildroot -name "perllocal.pod" | xargs rm -f

# fix libtool files perms
chmod 644 %buildroot%_libdir/*.la

%clean
rm -rf %buildroot
