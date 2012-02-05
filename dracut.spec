Summary:	Next generation initrd image generator
Name:		dracut
Version:	014
Release:	2
Group:		System/Base
License:	GPLv2+
URL:		https://dracut.wiki.kernel.org/
Source0:	http://www.kernel.org/pub/linux/utils/boot/dracut/%{name}-%{version}.tar.bz2
Source3:	50-dracut-mandriva.conf
Patch1: 0001-dracut-export-host_fs_types-host_devs.patch
Patch2: 0002-module-setup.sh-use-host_fs_types-host_devs.patch
Patch3: 0003-95iscsi-iscsiroot-unset-used-variables-before-starti.patch
Patch4: 0004-99base-dracut-lib.sh-killproc-prefix-local-variables.patch
Patch5: 0005-dracut.spec-remove-unnecessary-dependencies.patch
Patch6: 0006-TEST-12-RAID-DEG-mkdir-run.patch
Patch7: 0007-99base-dracut-lib.sh-added-inst_mount_hook-add_mount.patch
Patch8: 0008-dracut-add-add-fstab-and-mount-option.patch
Patch9: 0009-mkinitrd-dracut.sh-s-read_args-read_arg-g.patch
Patch10: 0010-Fix-live-update-script-769970.patch
Patch11: 0011-Makefile-set-bindir-to-prefix-bin-rather-than-sbin.patch
Patch12: 0012-Makefile-dash-does-not-like-expansion.patch
Patch13: 0013-mkinitrd-Mention-the-nocompress-option-in-help-outpu.patch
Patch14: 0014-Fix-Unicode-keytable.patch
Patch15: 0015-Handle-compressed-kmods.patch
Patch16: 0016-Only-install-files-from-etc-ld.so.conf.d-directory.patch
Patch17: 0017-plymouth-Include-kms-modules-even-if-they-are-not-cu.patch
Patch18: 0018-kernel-modules-Find-and-ulitmately-dereference-any-s.patch
Patch19: 0019-btrfs-Ensure-crc32c-module-is-installed.patch
Patch20: 0020-resume-Fix-failure-when-invalid-device-passed-via-re.patch
Patch21: 0021-dmsquash-Ensure-the-loop-kernel-module-is-included-a.patch
Patch22: 0022-init-Fix-bogus-message-about-invalid-root-device.patch
Patch23: 0023-udev-Attempt-to-install-any-programs-used-by-udev-ru.patch
Patch24: 0024-98usrmount-mount-usr.sh-Don-t-pass-mount-options-to-.patch
Patch25: 0025-TEST-10-RAID-fixed-TESTDIR-handling.patch
Patch26: 0026-Allow-to-add-mount-points-even-not-in-hostonly-mode.patch
Patch27: 0027-Check-module-dependencies-of-mount-points.patch
Patch28: 0028-Fix-get_maj_min-to-follow-symlink.patch
Patch29: 0029-Pass-device-name-instead-of-major-minor-in-for_each_.patch
Patch30: 0030-nfs-fix-regex-patterns-in-check.patch
Patch31: 0031-lvm-pass-the-correct-rd.lvm.lv-parameter.patch
Patch32: 0032-Create-a-symlink-for-the-live-image-s-base-loop-devi.patch
Patch33: 0033-interpret-off-as-false-in-getargbool.patch
Patch34: 0034-minor-cleanups-in-parsing-for-dmsquash-live-and-live.patch
Patch35: 0035-fstab-sys-mount-it-in-initramfs-instead-of-newroot-i.patch
Patch36: 0036-typo-fix.patch
Patch37: 0037-mktemp-was-long-obsoleted-by-coreutils.patch
Patch38: 0038-dmsquash-live-really-changed-dev-live-baseloop-to-ru.patch
Patch39: 0039-90kernel-modules-module-setup.sh-install-modules.ord.patch
Patch40: 0040-Handle-upper-case-MAC-addresses-in-ifname-option.patch
Patch41: 0041-server-id-in-ip-is-not-optional.patch
Patch42: 0042-ip-server-id-should-be-server-IP.patch
Patch43: 0043-remove-extra-semicolons-in-dracut.8.xml.patch
Patch44: 0044-deal-common-part-of-etc-passwd-in-99base.patch
Patch45: 0045-Add-job-control-support-to-emergency-shell.patch
Patch46: 0046-change-root-home-dir-to-root.patch
Patch47: 0047-Add-ssh-client-module-code.patch
Patch48: 0048-ctty-add-help-line-in-usage.patch
Patch49: 0049-plymouth-add-xz-support-for-kernel-modules.patch
Patch50: 0050-add-xz-compression-for-kernel-modules.patch
Patch51: 0051-lsinitrd-add-s-option-to-sort-the-initrd-output-by-f.patch
Patch52: 0052-dracut-unset-GREP_OPTIONS.patch
Patch53: 0053-lsinitrd-use-xz-with-single-stream-if-available.patch
Patch54: 0054-plymouth-kernel-cleanup-not-needed-parts-for-shutdow.patch
Patch55: 0055-network-dhclient-script-set-FQDN.patch
Patch56: 0056-AUTHORS-updated-and-fixed-.mailmap.patch
Patch57: 0057-dracut-dracut.8.xml-added-more-documentation-about-L.patch
Patch58: 0058-98usrmount-mount-usr.sh-do-not-mount-usr-read-only.patch
Patch59: 0059-40network-also-look-in-drivers-s390-net-for-network-.patch
Patch60: 0060-fix-rpm-build-error-after-adding-ssh-client-module.patch
Patch61: 0061-iscsi-multipath-also-search-in-drivers-s390-scsi.patch
Patch62: 0062-dracut-_get_fs_type-also-handle-dev-block-maj-min.patch
Patch63: 0063-dracut-functions-get_maj_min-major-and-minor-was-swa.patch
Patch64: 0064-90crypt-module-setup.sh-prepend-luks-to-hostonly-cmd.patch
Patch65: 0065-99base-init-remove-tmpfs-on-dev.patch
Patch66: 0066-netroot-actually-run-netroot-hooks.patch
Patch67: 0067-let-some-modules-to-respect-mount_needs.patch
Patch68: 0068-95ssh-client-module-setup.sh-spell-corrections.patch
Patch69: 0069-95ssh-client-module-setup.sh-do-not-install-ssh-clie.patch
Patch70: 0070-add-usrmove-module.patch
Patch71: 0071-dracut.spec-add-compat-symlinks-to-sbin.patch
Patch72: 0072-usrmove-install-missing-binaries-and-set-x-only-for-.patch
Patch73: 0073-30usrmove-usrmove-convert.sh-rename-duplicate-librar.patch
Patch74: 0074-dracut.spec-create-compat-symlink-instead-of-ghost.patch
Patch75: 0075-fix-kernel-modules-search-for-s390.patch
Patch76: 0076-fix-kernel-modules-search-for-s390.patch
Patch77: 0077-30usrmove-usrmove-convert.sh-do-not-force-selinux-au.patch
Patch78: 0078-dracut-functions-install-nosegneg-libs-additionally-.patch
Patch79: 0079-renamed-usrmove-to-convertfs.patch
Patch80: 0080-30convertfs-convertfs.sh-fix-check-for-var-run-and-v.patch
# (bor) mdv-specific fixes
Patch1000: dracut-011-mdv.patch
# (bor) Restore original Mandriva behaviour of adding bootchart if RPM is installed.
Patch1001: dracut-007-undisable_bootchart.patch
# (bor) compatibility with mkinitrd
Patch1002: dracut-010-mkinitrd.patch
# (bor) Add support for KEYTABLE to dynamically determine whether to install UNICODE or non-UNICODE keymap version.
Patch1003: dracut-007-aufs-mount.patch
# (anssi) handle gzip compressed KMS kernel modules
Patch1004: dracut-011-rosa-livecdfix.patch
Patch1005: dracut-013-ld.so.conf.workaround.patch
Requires(pre):	filesystem
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
BuildRequires:	docbook-dtd45-xml
BuildRequires:	docbook-style-xsl
BuildRequires:	xsltproc
BuildRequires:	dash
BuildRequires:	bash
Obsoletes:	dracut < 013

%description
Dracut contains tools to create a bootable initramfs for 2.6 Linux kernels.
Unlike existing implementations, dracut does hard-code as little as possible
into the initramfs. Dracut contains various modules which are driven by the
event-based udev. Having root on MD, DM, LVM2, LUKS is supported as well as
NFS, iSCSI, NBD, FCoE with the dracut-network package.

%prep
%setup -q
%apply_patches

%build
export CFLAGS="%{optflags}"
%make

%install
rm -rf %{buildroot}

%makeinstall_std sbindir=/sbin sysconfdir=%{_sysconfdir} mandir=%{_mandir}

install -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/dracut.conf.d

# bluca remove patch backup files
find %{buildroot} -type f -name '*.orig' -exec rm {} \;
find %{buildroot} -type f -name '*~' -exec rm {} \;

# fix permission of module files
chmod +x %{buildroot}%{_prefix}/lib/dracut/modules.d/*/*.sh

mkdir -p %{buildroot}/boot/dracut
mkdir -p %{buildroot}%{_var}/lib/dracut/overlay
install -m 755 -d %{buildroot}%{_datadir}/dracut

install -d %{buildroot}%{_sbindir}
mv %{buildroot}%{_bindir}/* %{buildroot}%{_sbindir}/

mv %{buildroot}%{_sbindir}/lsinitrd %{buildroot}%{_sbindir}/lsinitrd-dracut
mv %{buildroot}%{_sbindir}/mkinitrd %{buildroot}%{_sbindir}/mkinitrd-dracut

cat > README.urpmi << EOF
dracut is the default mkinitrd replacement in mandriva

If you relly want to use old mkinitrd instead of dracut run
update-alternatives --set mkinitrd /sbin/mkinitrd-mkinitrd
EOF

# rpmlint madness
chmod 755 %{buildroot}%{_prefix}/lib/dracut/modules.d/99aufs-mount/install

%post
update-alternatives --install /sbin/mkinitrd mkinitrd %{_sbindir}/mkinitrd-dracut 110 || :
update-alternatives --install /sbin/lsinitrd lsinitrd %{_sbindir}/lsinitrd-dracut 110 || :

%postun
[ ! -e /sbin/mkinitrd-dracut ] && update-alternatives --remove mkinitrd %{_sbindir}/mkinitrd-dracut || :
[ ! -e /sbin/lsinitrd-dracut ] && update-alternatives --remove lsinitrd %{_sbindir}/lsinitrd-dracut || :

%files
%doc README.generic README.modules README.kernel HACKING TODO AUTHORS
%doc README.urpmi
%dir /boot/dracut
%dir %{_datadir}/dracut
%dir %{_var}/lib/dracut
%dir %{_var}/lib/dracut/overlay
%config(noreplace) %{_sysconfdir}/dracut.conf
%dir %{_sysconfdir}/dracut.conf.d
%{_sysconfdir}/dracut.conf.d/50-dracut-mandriva.conf
%{_sbindir}/dracut
%{_sbindir}/dracut-gencmdline
%{_sbindir}/dracut-catimages
%{_sbindir}/lsinitrd-dracut
%{_sbindir}/mkinitrd-dracut
%{_prefix}/lib/dracut/dracut-functions
%{_prefix}/lib/dracut/modules.d
%{_prefix}/lib/dracut/dracut-logger
%{_mandir}/man8/dracut*.8*
%{_mandir}/man7/dracut.kernel.7*
%{_mandir}/man7/dracut.cmdline.7*
%{_mandir}/man5/dracut.conf.5*
