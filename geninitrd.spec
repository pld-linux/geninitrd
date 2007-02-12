Summary:	Creates an initial ramdisk image for preloading modules
Summary(pl.UTF-8):   Narzędzie do tworzenia inicjalnego ramdysku używanego przy starcie systemu
Name:		geninitrd
Version:	6711
Release:	0.1
License:	GPL
Group:		Applications/System
#Source0:	ftp://ftp.pld-linux.org/people/arekm/software/%{name}-%{version}.tar.gz
Source0:	%{name}-%{version}.tar.gz
# Source0-md5:	0825a468854a9c1b71197c86aa9b640f
Patch0:	%{name}-fixes.patch
BuildRequires:	xmlto >= 0:0.0.18-1
Requires:	awk
Requires:	busybox-initrd >= 1.00-0.rc3.2
Requires:	fileutils
Requires:	genromfs
Requires:	gzip
# without this softraid installations of PLD fail
Requires:	mdadm-initrd >= 1.12.0-1
Requires:	mktemp >= 1.5-8
Requires:	mount
Requires:	pci-database >= 0.4
Requires:	rc-scripts >= 0.2.7
Requires:	sh-utils
Requires:	tar
Obsoletes:	mkinitrd
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
%patch0 -p1

%build
rm -f geninitrd.8
%{__make} geninitrd.8

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	BUILDROOT=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog
%attr(755,root,root) /sbin/geninitrd
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/geninitrd
%{_mandir}/man8/*
