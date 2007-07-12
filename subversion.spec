%define apache_version 2.0.54
%define libsvn %mklibname svn 0

%define build_python 1
%{?_without_python: %{expand: %%global build_python 0}}

%define build_ruby 1
%{?_without_ruby: %{expand: %%global build_ruby 0}}

%define build_java 1
%{?_with_java: %{expand: %%global build_java 1}}
%define gcj_support 1

%define build_perl 1
%{?_without_perl: %{expand: %%global build_perl 0}}

%define build_test 0
%{?_with_test: %{expand: %%global build_test 1}}

%define build_debug 0
%{?_with_debug: %{expand: %%global build_debug 1}}

Name: subversion
Version: 1.4.4
Release: %mkrel 6
Summary: A Concurrent Versioning System
License: BSD CC2.0
Group: Development/Other
URL: http://subversion.tigris.org
Source0: http://subversion.tigris.org/tarballs/%name-%version.tar.bz2
Source1: http://subversion.tigris.org/downloads/%name-%version.tar.bz2.asc
Source2: %mod_dav_conf
Source3: %mod_authz_conf
Source4: %name.bash-completion
Source5: %name-1.3.0-global-config
Source6: %name-1.3.0-global-servers
Source7: http://svnbook.red-bean.com/nightly/en/svn-book-html-chunk.tar.bz2
Patch0: subversion-1.1.3-java.patch
Patch2: subversion-1.3.0-rc6-swig-perl.patch
Patch3: subversion-latest_neon.diff
BuildRequires:	autoconf >= 2.54
BuildRequires:	libtool >= 1.4.2
BuildRequires:	chrpath
BuildRequires:	python >= 2.2
BuildRequires:	texinfo
BuildRequires:	info-install
BuildRequires:	db4-devel
%if %{mdkversion} < 200610
BuildRequires:	neon-devel >= 0.24.7
%else
BuildRequires:	neon-devel >= 0.26
%endif
BuildRequires:	apache-devel >=  %{apache_version}
BuildRequires:	apr-devel >= 1.2.2
BuildRequires:	apr-util-devel >= 1.2.2
BuildRequires:	libxslt-proc
BuildRequires:	docbook-style-xsl
BuildRequires:	swig-devel >= 1.3.27
%if %mdkversion >= 1020
BuildRequires:	multiarch-utils >= 1.0.3
%endif
# Obsoletes - kill all non sys build library packages
# Just server and client need some libraries and we need just one
# main ( client ) and one server package, as well bindings and doc packages
Obsoletes: %name-client-tools < 1.2.3-4mdk
Obsoletes: %name-repos < 1.2.3-4mdk
Obsoletes: %{_lib}svn_client1_0 < 1.2.3-4mdk
Obsoletes: %{_lib}svn_ra_dav1_0 < 1.2.3-4mdk
Obsoletes: %{_lib}svn_ra_local1_0 < 1.2.3-4mdk
Obsoletes: %{_lib}svn_ra_svn1_0 < 1.2.3-4mdk
Obsoletes: %{_lib}svn_delta1_0 < 1.2.3-4mdk
Obsoletes: %{_lib}svn_diff1_0 < 1.2.3-4mdk
Obsoletes: %{_lib}svn_repos1_0 < 1.2.3-4mdk
Obsoletes: %{_lib}svn_subr1_0 < 1.2.3-4mdk
Obsoletes: %{_lib}svn_fs_fs1_0 < 1.2.3-4mdk
Obsoletes: %{_lib}svn_fs_base1_0 < 1.2.3-4mdk
Conflicts: %name-server < 1.2.3-4mdk
Conflicts: %{libsvn} < 1.3.0-2mdk
Provides: %name-ra-method = %version-%{release}
Provides: %name-client-tools = %version-%{release}
# soname didn't change between 1.3.x and 1.4.x, but we
# need the right one...
Requires: %{libsvn} = %{version}
BuildRoot: %{_tmppath}/%name-%version

%description
Subversion is a concurrent version control system which enables one or more
users to collaborate in developing and maintaining a hierarchy of files and
directories while keeping a history of all changes.  Subversion only stores the
differences between versions, instead of every complete file.  Subversion also
keeps a log of who, when, and why changes occured.
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
%_datadir/emacs/site-lisp/psvn.el
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
%doc svnbook-1.3
%doc doc/user/*.html
%doc doc/user/*.txt

#--------------------------------------------------------------------------

%package	-n %libsvn
Summary:	Subversion libraries
Group:		System/Libraries
Conflicts:	subversion < 1.3.0-2mdk 

%description -n %libsvn
Subversion common libraries

%post -n %libsvn -p /sbin/ldconfig
%postun -n %libsvn -p /sbin/ldconfig

%files -n %libsvn
%defattr(-,root,root)
# list all ra libs to make sure we don't miss any
# in a bogus build
%_libdir/libsvn_ra-1.so.*
%_libdir/libsvn_ra_dav-1.so.*
%_libdir/libsvn_ra_local-1.so.*
%_libdir/libsvn_ra_svn-1.so.*
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
Requires: %name = %version-%{release}
Requires(pre):  rpm-helper
Requires(postun): rpm-helper
Requires(post): sed
Requires: xinetd
# soname didn't change between 1.3.x and 1.4.x, but we
# need the right one...
Requires: %{libsvn} = %{version}

%description server
This package contains a myriad of server for subversion server
and repository admins:
  * hot-backup makes a backup of a svn repo without stopping
  * mirror_dir_through_svn.cgi 
  * various hook scripts
  * xslt example 

Note that cvs2svn has moved out of subversion and is a separate
project.  It has not released its own package yet, but you can
find it at http://cvs2svn.tigris.org/

%pre server
%_pre_useradd svn %{_localstatedir}/svn /bin/false

%post server
# Libraries for REPOS ( Repository ) and FS ( filesystem backends ) are in
# server now, so we need a ldconfig
/sbin/ldconfig
# fix svn entries in /etc/services
if ! grep -qE '^svn[[:space:]]+3690/(tcp|udp)[[:space:]]+svnserve' %{_sysconfdir}/services; then
	# cleanup
	sed -i -e '/^svn\(serve\)\?/d;/^# svnserve ports added by subversion-server/d' %{_sysconfdir}/services
	echo "# svnserve ports added by subversion-server" >> /etc/services
	echo -e "svn\t3690/tcp\tsvnserve\t# Subversion svnserve" >> /etc/services
	echo -e "svn\t3690/udp\tsvnserve\t# Subversion svnserve" >> /etc/services
fi

# restarting xinetd service
service xinetd condrestart

%postun server
%_postun_userdel svn
# restarting xinetd service
service xinetd condrestart
/sbin/ldconfig

%files server
%defattr(-,root,root)
%doc BUGS CHANGES COMMITTERS COPYING HACKING INSTALL README
%doc notes/repos_upgrade_HOWTO
%_bindir/svnserve
%_bindir/server-vsn*
%config(noreplace) %_sysconfdir/xinetd.d/svnserve
%attr(0770,svn,svn) %{_localstatedir}/svn
%_mandir/man8/svnserve.8*
%_mandir/man5/svnserve.conf.5*

#--------------------------------------------------------------------------

%package tools
Summary:	Subversion Repo/Server Tools
Group: Development/Other
Requires: %name = %version-%{release}
Conflicts: %name-server < 1.2.3-4mdk
Obsoletes: %name-repo-tools < 1.2.3-4mdk
# soname didn't change between 1.3.x and 1.4.x, but we
# need the right one...
Requires: %{libsvn} = %{version}

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
%_mandir/man1/svnadmin.1*
%_mandir/man1/svndumpfilter.1*
%_datadir/%name-%version/repo-tools

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
Requires: %{libsvn} = %{version}

%description -n python-svn
This package contains the files necessary to use the subversion
library functions within python scripts.

%files -n python-svn
%defattr(0644,root,root,755)
%_libdir/libsvn_swig_py*.so.*
%{py_sitedir}/svn
%{py_platsitedir}/libsvn
%doc tools/examples/*.py subversion/bindings/swig/INSTALL subversion/bindings/swig/NOTES


%package -n	python-svn-devel
Summary:	Python bindings for Subversion, development files
Group: Development/Other
Requires: python-svn = %version-%{release}
Obsoletes: python-svn-static-devel < 1.2.3-4mdk
Provides: python-subversion-devel = %version-%{release}

%description -n python-svn-devel
This package contains the .la files for the python bindings for
subversion.  It's likely nobody will ever need these.

%files -n python-svn-devel
%defattr(-,root,root)
%_libdir/libsvn_swig_py*.so

%endif

#--------------------------------------------------------------------------

%if %{build_ruby}

%package -n	ruby-svn
Summary:	Ruby bindings for Subversion
Group: Development/Ruby
BuildRequires: ruby-devel
Requires: ruby
# soname didn't change between 1.3.x and 1.4.x, but we
# need the right one...
Requires: %{libsvn} = %{version}
Provides: ruby-subversion = %version-%{release}

%description -n	ruby-svn
This package contains the files necessary to use the subversion
library functions within ruby scripts.

%package -n	ruby-svn-devel
Summary:	Ruby bindings for Subversion, development libraries
Group: Development/Ruby
Requires:       ruby-svn = %version-%{release}

%description -n	ruby-svn-devel
This package contains the .la files for the ruby bindings for
subversion.  It's likely nobody will ever need these.

%files -n ruby-svn
%defattr(-,root,root)
%ruby_sitearchdir/svn
%exclude %ruby_sitearchdir/*/*/*.la
%ruby_sitelibdir/*/*.rb
%_libdir/libsvn_swig_ruby*.so.*

%files -n ruby-svn-devel
%defattr(-,root,root)
%ruby_sitearchdir/*/*/*.la
%_libdir/libsvn_swig_ruby*.so

%endif

#--------------------------------------------------------------------------

%if %{build_java}
%package -n svn-javahl
Epoch:          0
Summary:	Java bindings for Subversion
Group:		Development/Java
Obsoletes:      java-svn < %{epoch}:%{version}-%{release}
Provides:       java-svn = %{epoch}:%{version}-%{release}
Provides:	java-subversion = %{epoch}:%{version}-%{release}
Requires:	%{name} = %{version}-%{release}
# soname didn't change between 1.3.x and 1.4.x, but we
# need the right one
Requires:       %{libsvn} = %{version}-%{release}
%if %{gcj_support}
Requires(post): java-gcj-compat
Requires(postun): java-gcj-compat
BuildRequires: java-gcj-compat-devel
%else
BuildRequires:  java-devel
BuildArch:      noarch
%endif
BuildRequires:  ant
BuildRequires:  jpackage-utils
BuildRequires:  junit

%description -n	svn-javahl
This package contains the files necessary to use the subversion
library functions from Java.

%package -n svn-javahl-javadoc
Epoch:          0
Summary:        Javadoc for svn-javahl
Group:          Development/Java
Provides:       %{version}-%{release}

%description -n svn-javahl-javadoc
Javadoc for svn-javahl.

%if %{gcj_support}
%post -n svn-javahl
%{update_gcjdb}

%postun -n svn-javahl
%{clean_gcjdb}
%endif

%files -n svn-javahl
%defattr(0644,root,root,0755)
%doc subversion/bindings/java/README
%{_jnidir}/svn-javahl.jar
%{_jnidir}/svn-javahl-%{version}.jar
%attr(0755,root,root) %{_libdir}/libsvnjavahl-1.so
%if %{gcj_support}
%dir %{_libdir}/gcj/svn-javahl
%attr(-,root,root) %{_libdir}/gcj/svn-javahl/*
%endif

%files -n svn-javahl-javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/svn-javahl-%{version}
%doc %{_javadocdir}/svn-javahl
%endif

#--------------------------------------------------------------------------

%if %{build_perl}

%package -n perl-SVN
Summary:	Perl bindings for Subversion
Group:		Development/Perl
BuildRequires: perl-devel
Requires:	%name = %version-%{release}
Obsoletes:	perl-svn
Provides:	perl-svn = %version-%{release}
# soname didn't change between 1.3.x and 1.4.x, but we
# need the right one...
Requires: %{libsvn} = %{version}

%description -n perl-SVN
This package contains the files necessary to use the subversion
library functions within perl scripts.

%files -n perl-SVN
%defattr(-,root,root)
%doc subversion/bindings/swig/INSTALL subversion/bindings/swig/NOTES
%_libdir/libsvn_swig_perl*.so.*
%{perl_vendorarch}/SVN
%{perl_vendorarch}/auto/SVN
%_mandir/man3/SVN::*.3*

%package -n	perl-SVN-devel
Summary:	Perl bindings for Subversion, development files 
Group:		Development/Other
Requires:	perl-SVN = %version-%{release}
Obsoletes:	perl-svn-devel

%description -n perl-SVN-devel
This package contains the .so files for the perl bindings for
subversion.  It's likely nobody will ever need these.

%files -n perl-SVN-devel
%defattr(-,root,root)
%_libdir/libsvn_swig_perl*.so

%endif

#----------------------------------------------------------------

%package devel
Summary:	Subversion headers/libraries for development
Group:		Development/Other
Provides:	%{_lib}svn-devel = %version-%{release}
Obsoletes:	libsubversion1_0-devel < 1.2.3-4mdk
Obsoletes:	libsubversion1_0-static-devel < 1.2.3-4mdk
Requires: %libsvn = %version-%release

%description devel
This package contains the header files and linker scripts for
subversion libraries.

%files devel
%defattr(-,root,root)
%doc tools/examples/minimal_client.c
%_libdir/libsvn*.la
%_includedir/subversion*/*
%_libdir/libsvn_*.so

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
Epoch:		1
Requires: %name-tools = %version-%{release}
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= %{apache_version}
Requires(pre):	apache >= %{apache_version}
Requires(pre):	apache-mod_dav >= %{apache_version}
# soname didn't change between 1.3.x and 1.4.x, but we
# need the right one...
Requires(pre): %{libsvn} = %{version}
Provides:	apache2-%{mod_dav_name} = %{mod_version}
Obsoletes:	apache2-mod_dav_svn
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

#--------------------------------------------------------------------------

%prep
%setup -q -a 7
%if %{build_java}
%patch0 -p1 -b .java
%endif
%patch2 -p1 -b .perlswig
%patch3 -p0 -b .neon
rm -rf neon apr apr-util db4

%if %{build_java}
%{__perl} -pi -e 's|^LINK_JAVAHL_CXX =(.*)|LINK_JAVAHL_CXX =\1 -avoid-version|;' \
              -e 's|^javahl_javadir =.*|javahl_javadir = %{_jnidir}|;' \
  Makefile.in
%endif

# fix shellbang lines, #111498
perl -pi -e 's|/usr/bin/env perl -w|/usr/bin/perl -w|' tools/hook-scripts/*.pl.in

# fix file perms
chmod 644 BUGS CHANGES COMMITTERS COPYING HACKING INSTALL README

# move latest svnbook snapshot as their target version
mv svn-book-html-chunk svnbook-1.3

%build
%serverbuild
./autogen.sh

# override weird -shrext from ruby (from Fedora)
export svn_cv_ruby_link="%{__cc} -shared"

# both versions could be installed, use the latest one per default
if [ -x %{_bindir}/apr-config ]; then APR=%{_bindir}/apr-config; fi
if [ -x %{_bindir}/apu-config ]; then APU=%{_bindir}/apu-config; fi

if [ -x %{_bindir}/apr-1-config ]; then APR=%{_bindir}/apr-1-config; fi
if [ -x %{_bindir}/apu-1-config ]; then APU=%{_bindir}/apu-1-config; fi

./configure \
   --prefix=%{_prefix} \
   --sysconfdir=%_sysconfdir \
   --datadir=%_datadir \
   --libdir=%_libdir \
   --localstatedir=%{_localstatedir} \
   --mandir=%_mandir \
   --with-apxs=%{_sbindir}/apxs \
   --with-apr=$APR \
   --with-apr-util=$APU \
   --disable-mod-activation \
   --with-swig=%{_prefix} \
   --disable-static \
%if %{build_debug}
   --enable-maintainer-mode \
   --enable-debug \
%endif
%if %{build_java}
   --with-jdk=%{java_home} \
   --with-junit=%{_javadir}/junit.jar \
%endif
   --enable-shared 

# put the apache modules in the correct place
perl -pi -e "s|%_libdir/apache|%_libdir/apache-extramodules|g" Makefile subversion/mod_authz_svn/*la subversion/mod_dav_svn/*la

%{make} all

%if %{build_python}
make swig-py swig_pydir=%{py_platsitedir}/libsvn swig_pydir_extra=%{py_sitedir}/svn
%endif

%if %{build_perl}
make swig-pl
%endif

%if %{build_ruby}
make swig-rb
%endif

%if %{build_java}
%{make} javahl
(cd subversion/bindings/java/javahl/build && %{ant} javadoc)
%endif

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
%endif
%if %{build_ruby}
%makeinstall_std install-swig-rb
%endif
%if %{build_java}
%{makeinstall_std} install-javahl

%{__mv} %{buildroot}%{_jnidir}/svn-javahl.jar %{buildroot}%{_jnidir}/svn-javahl-%{version}.jar
%{__ln_s} svn-javahl-%{version}.jar %{buildroot}%{_jnidir}/svn-javahl.jar

%{__mkdir_p} %{buildroot}%{_javadocdir}/svn-javahl-%{version}
%{__cp} -a subversion/bindings/java/javahl/javadoc/* %{buildroot}%{_javadocdir}/svn-javahl-%{version}
%{__ln_s} svn-javahl-%{version} %{buildroot}%{_javadocdir}/svn-javahl

%{_bindir}/chrpath -d %{buildroot}%{_libdir}/libsvnjavahl-1.so

%if %{gcj_support}
RPM_PACKAGE_NAME=svn-javahl %{_bindir}/aot-compile-rpm
%endif
%endif

%if %{build_perl}
# perl bindings
make pure_vendor_install -C subversion/bindings/swig/perl/native DESTDIR=%buildroot
%endif

install -d %buildroot%_sysconfdir/httpd/modules.d
cat %{SOURCE2} > %buildroot%_sysconfdir/httpd/modules.d/%{mod_dav_conf}
cat %{SOURCE3} > %buildroot%_sysconfdir/httpd/modules.d/%{mod_authz_conf}

######################
###  client-tools  ###
######################

# vim syntax hilighting
%if %mdkversion <= 910
    # Already included in vim-common on 9.2 and newer.
    install -d -m 755 %buildroot/%_datadir/vim/syntax
    install -m 644 contrib/client-side/svn.vim %buildroot/%_datadir/vim/syntax
%endif

# emacs psvn interface
install -d -m 755 %buildroot/%_datadir/emacs/site-lisp
install -m 644 contrib/client-side/psvn/psvn.el %buildroot/%_datadir/emacs/site-lisp

# various commands
install -m 755 contrib/client-side/search-svnlog.pl %buildroot%_bindir
(cd  %buildroot/%_bindir; ln -sf  search-svnlog.pl search-svnlog)
install -m 755 contrib/client-side/svn_all_diffs.pl %buildroot%_bindir
(cd  %buildroot/%_bindir; ln -sf  svn_all_diffs.pl svn_all_diffs)
install -m 755 contrib/client-side/svn_load_dirs.pl %buildroot%_bindir
(cd  %buildroot/%_bindir; ln -sf  svn_load_dirs.pl svn_load_dirs)
install -m 755 contrib/client-side/svn-log.pl %buildroot%_bindir
(cd  %buildroot/%_bindir; ln -sf  svn-log.pl svn-log)
install -m 755 tools/client-side/server-vsn.py %buildroot%_bindir
(cd  %buildroot/%_bindir; ln -sf  server-vsn.py server-vsn)
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
install -m 755 commit-email.pl %buildroot/%_datadir/%name-%version/repo-tools/hook-scripts
install -m 644 svnperms.conf.example %buildroot/%_datadir/%name-%version/repo-tools/hook-scripts
install -m 755 svnperms.py %buildroot/%_datadir/%name-%version/repo-tools/hook-scripts
install -m 755 mailer/mailer.py %buildroot/%_datadir/%name-%version/repo-tools/hook-scripts
install -m 644 mailer/mailer.conf.example %buildroot/%_datadir/%name-%version/repo-tools/hook-scripts
install -m 644 README %buildroot/%_datadir/%name-%version/repo-tools/hook-scripts
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
    server_args		= -i -r %_localstatedir/svn/repositories
}
EOF
install -m 644 svnserve.xinetd %buildroot%_sysconfdir/xinetd.d/svnserve
install -d %buildroot%{_localstatedir}/svn/repositories

# cleanup
find %buildroot -name "perllocal.pod" | xargs rm -f

# fix libtool files perms
chmod 644 %buildroot%_libdir/*.la

%if %{build_java}
%if 0
%check
export CLASSPATH=$(%{_bindir}/build-classpath junit):%{buildroot}%{_jnidir}/svn-javahl.jar:`pwd`/subversion/bindings/java/javahl/src
%{java} -Djava.library.path=%{buildroot}%{_libdir} org.tigris.subversion.javahl.tests.BasicTests
%endif
%endif

%clean
rm -rf %buildroot


