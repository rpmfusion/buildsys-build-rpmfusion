%define repo rpmfusion

Name:           buildsys-build-%{repo}
Epoch:          10
Version:        11
Release:        0.31
Summary:        Tools and files used by the %{repo} buildsys 

Group:          Development/Tools
License:        MIT
URL:            http://rpmfusion.org
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source2:        %{name}-list-kernels.sh
Source5:        %{name}-README
Source11:       %{name}-kerneldevpkgs-current

# provide this to avoid a error when generating akmods packages
Provides:       buildsys-build-rpmfusion-kerneldevpkgs-akmod-%{_target_cpu}

# rpmlint will complain this should be a noarch package; but for
#  proper builddeps deps it needs to be a non-noarch package
ExclusiveArch:  i586 i686 x86_64 ppc ppc64

# unneeded
%define debug_package %{nil}

%description
This package contains tools and lists of recent kernels that get used when
building kmod-packages.

%package        kerneldevpkgs-current
Summary:        Meta-package to get all current kernel-devel packages into the buildroot
Group:          Development/Tools
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       %{name}-kerneldevpkgs-%{_target_cpu} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       %{name}-kerneldevpkgs-current-%{_target_cpu} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       %{name}-kerneldevpkgs-newest-%{_target_cpu} = %{?epoch:%{epoch}:}%{version}-%{release}

Requires:       %{_bindir}/kmodtool
BuildRequires:  %{_bindir}/kmodtool

# we use our own magic here to safe ourself to cut'n'paste the BR
%{expand:%(bash %{SOURCE2} --current --requires --prefix %{_sourcedir}/%{name}- 2>/dev/null)}

%description kerneldevpkgs-current
This is a meta-package used by the buildsystem to track the kernel-devel
packages for all current up-to-date kernels into the buildroot to build
kmods against them.

%files kerneldevpkgs-current
%defattr(-,root,root,-)
%doc .tmp/current/README

%prep
# for debugging purposes output the stuff we use during the rpm generation
bash %{SOURCE2} --current --requires --prefix %{_sourcedir}/%{name}-
sleep 2


%build
echo nothing to build


%install
rm -rf $RPM_BUILD_ROOT .tmp/
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/%{name} $RPM_BUILD_ROOT/%{_bindir} .tmp/newest .tmp/current

# install the stuff we need
install -p -m 0755 %{SOURCE2}  $RPM_BUILD_ROOT/%{_bindir}/%{name}-kerneldevpkgs
install -p -m 0644 %{SOURCE5}  .tmp/current/README
ln -s kerneldevpkgs-current $RPM_BUILD_ROOT/%{_datadir}/%{name}/kerneldevpkgs-newest
install -p -m 0644 %{SOURCE11} $RPM_BUILD_ROOT/%{_datadir}/%{name}/kerneldevpkgs-current


# adjust default-path
sed -i 's|^default_prefix=.*|default_prefix=%{_datadir}/%{name}/|'  \
 $RPM_BUILD_ROOT/%{_bindir}/%{name}-kerneldevpkgs


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_datadir}/%{name}/



%changelog
* Thu Feb 04 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10:11-0.31
- rebuild for kernel 2.6.30.10-105.2.13.fc11

* Fri Jan 22 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10:11-0.30
- rebuild for kernel 2.6.30.10-105.2.4.fc11

* Sat Dec 26 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10:11-0.29
- rebuild for kernel 2.6.30.10-105.fc11

* Sun Dec 06 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10:11-0.28
- rebuild for kernel 2.6.30.9-102.fc11

* Sun Nov 22 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10:11-0.27
- rebuild for kernel 2.6.30.9-99.fc11

* Thu Nov 05 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10:11-0.26
- rebuild for kernel 2.6.30.9-96.fc11

* Tue Oct 20 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10:11-0.25
- rebuild for kernel 2.6.30.9-90.fc11

* Wed Sep 30 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10:11-0.24
- rebuild for kernel 2.6.30.8-64.fc11

* Wed Sep 30 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10:11-0.23
- rebuild for kernel 2.6.30.8

* Tue Sep 01 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10:11-0.22
- rebuild for kernel 2.6.30.5-43.fc11

* Wed Aug 26 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10:11-0.21
- rebuild for kernel 2.6.29.6-217.2.16.fc11

* Sun Aug 23 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10:11-0.20
- rebuild for kernel 2.6.30.5-32.fc11

* Thu Aug 20 2009 Xavier Lamien <laxathom@fedoraproject.org> - 10:11-0.19
- rebuild for kernel 2.6.29.6-217.2.8.fc11

* Sat Aug 15 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10:11-0.16
- rebuild for kernel 2.6.29.6-217.2.7.fc11

* Fri Aug 14 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10:11-0.15
- rebuild for kernel 2.6.29.6-217.2.6.fc11

* Fri Jul 31 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10:11-0.14
- rebuild for kernel 2.6.29.6-217.2.3.fc11

* Tue Jul 14 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10:11-0.13
- rebuild for kernel 2.6.29.6-213.fc11

* Sun Jun 21 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10:11-0.12
- rebuild for kernel 2.6.29.5-191.fc11

* Mon Apr 06 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10:11-0.10
- use isa to make sure we get the right kernel 

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10:11-0.9
- rebuild for new F11 features

* Sun Feb 15 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10:11-0.8
- adjust for Fedora new kenrels scheme
- use a different way to generate lists

* Sun Jan 11 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10:11-0.7
- rebuild, and just use the latest as default

* Sun Jan 11 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10:11-0.6
- rebuild for kernel 2.6.29-0.25.rc0.git14.fc11

* Sun Jan 04 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10:11-0.5
- rebuild for kernel 2.6.29-0.9.rc0.git4.fc11

* Sun Dec 28 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10:11-0.4
- rebuild for kernel 2.6.28-3.fc11

* Sun Dec 27 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10:11-0.3
- just track in the latest kernel

* Sun Dec 21 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10:11-0.2
- rebuild for kernel 2.6.28-0.140.rc9.git1.fc11

* Sun Dec 14 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10:11-0.1
- rebuild for kernel 2.6.28-0.127.rc8.git1.fc11

* Wed Nov 19 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10:10-0.11
- rebuild for kernel 2.6.27.5-117.fc10

* Tue Nov 18 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10:10-0.10
- rebuild for kernel 2.6.27.5-113.fc10

* Fri Nov 14 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10:10-0.9
- rebuild for kernel 2.6.27.5-109.fc10

* Sun Nov 09 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10:10-0.8
- rebuild for kernel 2.6.27.4-79.fc10

* Fri Nov 07 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10:10-0.7
- rebuilt

* Sun Nov 02 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10:10-0.6
- rebuild for kernel 2.6.27.4-68.fc10

* Sun Oct 26 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10:10-0.5
- rebuild for kernel 2.6.27.4-47.rc3.fc10

* Sun Oct 19 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 10:10-0.4
- rebuild for kernel 2.6.27.3-27.rc1.fc10

* Thu Oct 02 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 10:10-0.3
- install filterfile for ppc64

* Thu Oct 02 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 10:10-0.2
- don't use the --buildrequires stuff, doesn't work in plague/mock
- provide compatible symlink for "newest"

* Thu Oct 02 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 10:10-0.1
- adjust things for rawhide
-- no xen kernels anymore, so no need for the whole newest and current handling
-- just require kernels unversioned if buildsys-build-rpmfusion-kerneldevpkgs
   contains lines with "default"

* Sun May 04 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 9:9.0-3
- adjust output for new kernel scheme

* Sun May 04 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 9:9.0-2
- add epoch to provides/requires

* Sun May 04 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 9:9.0-1
- Build for F9 kernel

* Mon Mar 31 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 2-2
- Update to latest kernels 2.6.24.4-64.fc8 2.6.21.7-3.fc8xen

* Sat Jan 26 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 9:1-2
- s/akmods/akmod/

* Wed Jan 09 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 9:1-3
- Build for rawhide
- disable kerneldevpkgs-newest and kerneldevpkgs-current packages, as we
  don't maintain them for rawhide
- add epoch for new versioning scheme

* Thu Dec 20 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 22-1
- Update to latest kernels 2.6.21-2952.fc8xen 2.6.23.9-85.fc8

* Thu Dec 20 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 22-1
- Update to latest kernels 2.6.21-2952.fc8xen 2.6.23.9-85.fc8

* Mon Dec 03 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 21-1
- Update to latest kernels 2.6.23.8-63.fc8 2.6.21-2952.fc8xen

* Sat Nov 10 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 20-1
- Update to latest kernels 2.6.23.1-49.fc8 2.6.21-2950.fc8xen

* Tue Oct 29 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 19-1
- Update to latest kernels 2.6.23.1-41.fc8 2.6.21-2950.fc8xen

* Tue Oct 28 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 18-1
- Update to latest kernels 2.6.23.1-41.fc8 2.6.21-2950.fc8xen

* Sun Oct 28 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 17-3
- don't include file with know variants and instead properly fix the script

* Sun Oct 28 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 17-2
- include file with know variants as it is needed in buildsys

* Sun Oct 28 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 17-1
- split buildsys stuff out into a seperate package
- rename to buildsys-build-rpmfusion
- add proper obsoletes
- give subpackages and files more sane names and places

* Sat Oct 27 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 16-2
- Update to latest kernels 2.6.23.1-35.fc8 2.6.21-2950.fc8xen

* Sat Oct 27 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 16-1
- Update to latest kernels 2.6.23.1-35.fc8 2.6.21-2949.fc8xen

* Thu Oct 18 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 15-1
- rebuilt for latest kernels

* Thu Oct 18 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 14-1
- rebuilt for latest kernels

* Thu Oct 18 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 13-1
- rebuilt for latest kernels

* Thu Oct 18 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 12-1
- rebuilt for latest kernels

* Fri Oct 12 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 11-1
- rebuilt for latest kernels

* Thu Oct 11 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 10-1
- rebuilt for latest kernels

* Wed Oct 10 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 9-2
- fix typo

* Wed Oct 10 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 9-1
- rebuilt for latest kernels

* Sun Oct 07 2007 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 8-1
- update for 2.6.23-0.224.rc9.git6.fc8

* Sun Oct 07 2007 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 7-1
- update for 2.6.23-0.222.rc9.git1.fc8

* Wed Oct 03 2007 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 6-1
- update for 2.6.23-0.217.rc9.git1.fc8 and 2.6.21-2947.fc8xen

* Wed Oct 03 2007 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5-1
- disable --all-but-latest stuff -- does not work as expected
- rename up2date list of kernels from "latest" to "current" as latest 
  and newest are to similar in wording; asjust script as well
- kmodtool: don't provide kernel-modules, not needed anymore with
  the new stayle and hurts

* Sun Sep 09 2007 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 4-2
- fix typos in spec file and list-kernels script
- interdependencies between the two buildsys-build packages needs to be
  arch specific as well

* Sun Sep 09 2007 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 4-1
- s/latests/latest/
- update kernel lists for rawhide and test2 kernels
- make kmod-helpers-livna-list-kernels print BuildRequires for all kernels
  as well; this is not needed and will slow build a bit as it will track 
  all the kernel-devel packages in, but that way we make sure they are really
  available in the buildsys

* Fri Sep 07 2007 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 3-4
- implement proper arch deps 

* Fri Sep 07 2007 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 3-3
- proper list of todays rawhide-kernels

* Fri Sep 07 2007 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 3-2
- fix typo in kmod-helpers-livna-latests-kernels

* Fri Sep 07 2007 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 3-1
- adjust for devel

* Sat Sep 01 2007 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2-1
- initial package
