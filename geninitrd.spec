# TODO:
# - BUG: you can't set in /etc/mdadm.conf:
#  DEVICE partitions containers
#  (which is default BTW if none set). Generation of initrd will fail
#
Summary:	Creates an initial ramdisk image for preloading modules
Summary(pl.UTF-8):	Narzędzie do tworzenia inicjalnego ramdysku używanego przy starcie systemu
Name:		geninitrd
Version:	12639
Release:	3
License:	GPL
Group:		Applications/System
Source0:	%{name}-%{version}.tar.gz
# Source0-md5:	bd47ea3ca6dbeea39af6bc5eb1d12e5a
# svn diff http://svn.pld-linux.org/svn/geninitrd/trunk -r 12652:HEAD > geninitrd-svn.patch
Patch0:		%{name}-svn.patch
URL:		http://svn.pld-linux.org/trac/svn/wiki/packages/geninitrd
BuildRequires:	xmlto >= 0:0.0.18-1
Requires:	/usr/bin/ldd
Requires:	awk
Requires:	busybox-initrd >= 1.1.0
Requires:	coreutils
Requires:	cpio
Requires:	fileutils
Requires:	glibc-misc
Requires:	gzip
Requires:	mktemp >= 1.5-8
Requires:	mount
Requires:	pci-database >= 0.4
Requires:	rc-scripts >= 0.2.7
Requires:	tar
Requires:	virtual(module-tools)
# otherwise LVM subsystem is not enabled in geninitrd
Suggests:	lvm2-initrd
# without this softraid installations of PLD fail
Suggests:	mdadm-initrd >= 1.12.0-1
Suggests:	genromfs
Suggests:	pciutils
# suggest for blkid
%if "%{pld_release}" != "ac"
Suggests:	util-linux-initrd
%endif
Obsoletes:	mkinitrd
%if "%{pld_release}" == "ac"
Conflicts:	grubby < 5.0.4-3.1
%else
Conflicts:	grubby < 6.0.24-3
%endif
Conflicts:	kmod < 7-2
Conflicts:	module-init-tools < 3.2.2-6
Conflicts:	pciutils < 2.2.9
Conflicts:	udev-initrd < 1:168
Conflicts:	xz < 4.999.9
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Geninitrd creates filesystem images for use as initial ramdisk
(initrd) images. These ramdisk images are often used to preload the
block device modules (SCSI or RAID) needed to access the root
filesystem.

In other words, generic kernels can be built without drivers for any
SCSI adapters which load the SCSI driver as a module. Since the kernel
needs to read those modules, but in this case it isn't able to address
the SCSI adapter, an initial ramdisk is used. The initial ramdisk is
loaded by the operating system loader (normally LILO) and is available
to the kernel as soon as the ramdisk is loaded. The ramdisk image
loads the proper SCSI adapter and allows the kernel to mount the root
filesystem. The geninitrd program creates such a ramdisk using
information found in the /etc/modules.conf file.

%description -l pl.UTF-8
Geninitrd służy do tworzenia obrazu systemu plikowego używanego jako
inicjalny ramdysk (initrd), z którego przy starcie systemu są ładowane
moduły kernela z obsługą urządzeń których obsługa nie jest
wkompilowana w kernel. Zazwyczaj modułami ładowanymi z inicjalnego
systemu plikowego są sterowniki SCSI, IDE czy też RAID po to żeby w
dalszej części inicjacji systemu był możliwy dostęp do głównego
systemu plikowego (root fs).

Dzięki initrd jest możliwe używanie dystrybucyjnego kernela w którym
wkompilowana jest minimalna ilość obsługi różnych urządzeń, a reszta
kodu obsługi sterowników SCSI, IDE czy RAID jest doczytywana w trakcie
startu z initrd. Skrypt geninitrd generuje obraz ramdysku na podstawie
bieżących informacji zawartych w /etc/modules.conf.

%prep
%setup -q
%patch0 -p0

%build
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/geninitrd
%attr(755,root,root) /sbin/geninitrd
%{_mandir}/man8/geninitrd.8*

%dir /lib/geninitrd
/lib/geninitrd/functions
/lib/geninitrd/mod-*.sh
%attr(755,root,root) /lib/geninitrd/extract-ikconfig

%dir /lib/geninitrd/udev-rules
/lib/geninitrd/udev-rules/*.rules
