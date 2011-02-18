Summary:	Next generation initrd image generator
Name:		dracut
Version:	008
Release:	%mkrel 2
Group:		System/Base
License:	GPLv2+
URL:		http://apps.sourceforge.net/trac/dracut/wiki
Source0:	http://downloads.sourceforge.net/project/dracut/%{name}-%{version}.tar.bz2
Source3:	50-dracut-mandriva.conf
# (bor) mdv-specific fixes
Patch0:		dracut-004-mdv.patch
# (bor) Restore original Mandriva behaviour of adding bootchart if RPM is installed.
Patch1:		dracut-007-undisable_bootchart.patch
# (bor) compatibility with mkinitrd
Patch15:	dracut-008-mkinitrd.patch
# (bor) Add support for KEYTABLE to dynamically determine whether to install UNICODE or non-UNICODE keymap version.
Patch19:	dracut-008-fix_unicode_keytable.patch
Patch21:	dracut-007-aufs-mount.patch
# (bor) pass flag that dracut was started to systemd (GIT)
Patch22:	dracut-008-plymouth-touch-dev-systemd-plymouth.patch
# (bor) fix i18n parsing in hostonly mode (GIT)
Patch23:	dracut-008-i18n-fixed-config-file-parsing.patch
# (bor) default to UTF-8 for console unless disabled (GIT)
Patch24:	dracut-008-i18n-default-to-vconsole-font.patch
Patch100:	rosa-livecdfix.patch
Requires:	filesystem
Requires:	udev
Requires:	util-linux-ng
Requires:	module-init-tools
Requires:	e2fsprogs
Requires:	cpio
Requires:	coreutils
Requires:	findutils
Requires:	binutils
Requires:	grep
Requires:	mktemp
Requires:	mount
Requires:	bash
Requires:	dash
Requires:	kbd
Requires:	tar
Requires:	gzip
Requires:	bzip2
Requires:	file
Requires:	module-init-tools
Requires:	bridge-utils
Requires:	initscripts
Requires(pre):	plymouth
Requires:	plymouth
Requires:	plymouth(system-theme)
Requires:	bootloader-utils
Requires(post,postun):	update-alternatives
Conflicts:	mkinitrd < 6.0.93-%manbo_mkrel 10
Conflicts:	nash < 6.0.93-%manbo_mkrel 11
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	docbook-dtd45-xml
BuildRequires:	docbook-style-xsl
BuildRequires:	xsltproc

%description
Event driven initrd image generator based around udev.

%prep
%setup -q
%patch0 -p1 -b .mdv.orig
%patch1 -p1 -b .undisable_bootchart.orig
%patch15 -p1 -b .mkinitrd.orig
%patch19 -p1 -b .fix_unicode_keytable.orig
%patch21 -p1 
%patch22 -p1 
%patch23 -p1 
%patch24 -p1 
%patch100 -p1

%build
export CFLAGS="%{optflags}"
%make

%install
rm -rf %{buildroot}
%makeinstall_std sbindir=/sbin sysconfdir=%{_sysconfdir} mandir=%{_mandir}

install -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/dracut.conf.d

# bluca remove patch backup files
find %{buildroot} -name \*.\*.orig -exec rm {} \;

# fix permission of module files
chmod +x %{buildroot}%{_datadir}/dracut/modules.d/*/*.sh

mkdir -p %{buildroot}/boot/dracut
mkdir -p %{buildroot}%{_var}/lib/dracut/overlay

mv %{buildroot}/sbin/lsinitrd %{buildroot}/sbin/lsinitrd-dracut
mv %{buildroot}/sbin/mkinitrd %{buildroot}/sbin/mkinitrd-dracut

cat > README.urpmi << EOF

This ia a mkinitrd replacement.
Consider this software as experimental!

How to use:

dracut -v /boot/initrd-dracut-\$(uname -r).img \$(uname -r)

then run

bootloader-config --action add-kernel /boot/vmlinuz-\$(uname -r) --initrd /boot/initrd-dracut-\$(uname -r).img --kernel-version \$(uname -r) --label dracut

and reboot.

If you want to set dracut as an mkinitrd replacement run
update-alternatives --set mkinitrd /sbin/mkinitrd-dracut
EOF

%clean
rm -rf %{buildroot}

%post
update-alternatives --install /sbin/mkinitrd mkinitrd /sbin/mkinitrd-dracut 90 || :
update-alternatives --install /sbin/lsinitrd lsinitrd /sbin/lsinitrd-dracut 90 || :

%postun
[ ! -e /sbin/mkinitrd-dracut ] && update-alternatives --remove mkinitrd /sbin/mkinitrd-dracut || :
[ ! -e /sbin/lsinitrd-dracut ] && update-alternatives --remove lsinitrd /sbin/lsinitrd-dracut || :

%files
%defattr(-,root,root)
%doc README.generic README.modules README.kernel HACKING TODO AUTHORS 
%doc README.urpmi
%dir /boot/dracut
%dir %{_datadir}/dracut
%dir %{_var}/lib/dracut
%dir %{_var}/lib/dracut/overlay
%config(noreplace) %{_sysconfdir}/dracut.conf
%dir %{_sysconfdir}/dracut.conf.d
%{_sysconfdir}/dracut.conf.d/50-dracut-mandriva.conf
/sbin/dracut
/sbin/dracut-gencmdline
/sbin/dracut-catimages
/sbin/lsinitrd-dracut
/sbin/mkinitrd-dracut
%{_datadir}/dracut/dracut-functions
%{_datadir}/dracut/modules.d
%{_mandir}/man8/dracut*.8*
%{_mandir}/man7/dracut.kernel.7*
%{_mandir}/man5/dracut.conf.5*
