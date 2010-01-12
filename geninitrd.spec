Summary:	Creates an initial ramdisk image for preloading modules
Summary(pl.UTF-8):	Narzędzie do tworzenia inicjalnego ramdysku używanego przy starcie systemu
Name:		geninitrd
Version:	10000.19
# leave rel 1 for ac
Release:	2
License:	GPL
Group:		Applications/System
Source0:	%{name}-%{version}.tar.gz
# Source0-md5:	00b6239fe068b89f7e158523ccc55c8a
Patch0:		%{name}-romfs.patch
Patch1:		%{name}-gzip-compressor.patch
BuildRequires:	xmlto >= 0:0.0.18-1
Requires:	awk
Requires:	busybox-initrd > 1.00-4
Requires:	coreutils
Requires:	cpio
Requires:	fileutils
Requires:	genromfs
Requires:	gzip
Requires:	/usr/bin/ldd
Requires:	mktemp >= 1.5-8
Requires:	module-init-tools >= 3.2.2-6
Requires:	mount
Requires:	pci-database >= 0.4
Requires:	rc-scripts >= 0.2.7
Requires:	tar
%if "%{pld_release}" == "ti"
Requires:	lvm2-initrd
Requires:	mdadm-initrd >= 1.12.0-1
%else
# otherwise LVM subsystem is automatically disabled in geninitrd
Suggests:	lvm2-initrd
# without this softraid installations of PLD fail
Suggests:	mdadm-initrd >= 1.12.0-1
%endif
Obsoletes:	mkinitrd
Conflicts:	grubby < 6.0.24-3
Conflicts:	udev-initrd < 1:104
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
%if "%{pld_release}" == "ti"
%patch0 -p1
%patch1 -p1
%endif

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
