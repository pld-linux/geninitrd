Summary:	Creates an initial ramdisk image for preloading modules
Summary(pl):	Narz�dzie do tworzenia inicjalnego ramdysku u�ywanego przy starcie systemu
Name:		geninitrd
Version:	3865
Release:	3
License:	GPL
Group:		Applications/System
Source0:	ftp://ftp.pld-linux.org/people/arekm/software/%{name}-%{version}.tar.gz
# Source0-md5:	4c8d2cf6a17f69703a237d750b45d788
Patch0:		%{name}-drop-min-max-kernel.patch
Patch1:		%{name}-typos.patch
PreReq:		rc-scripts >= 0.2.7
Requires:	awk
Requires:	busybox-initrd >= 1.00-0.pre5.0
Requires:	fileutils
Requires:	genromfs
Requires:	gzip
Requires:	mktemp >= 1.5-8
Requires:	mount
Requires:	pci-database >= 0.4
Requires:	sh-utils
Requires:	tar
Obsoletes:	mkinitrd
Conflicts:	mdadm-initrd < 1.4.0-3
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Mkinitrd creates filesystem images for use as initial ramdisk (initrd)
images. These ramdisk images are often used to preload the block
device modules (SCSI or RAID) needed to access the root filesystem.

In other words, generic kernels can be built without drivers for any
SCSI adapters which load the SCSI driver as a module. Since the kernel
needs to read those modules, but in this case it isn't able to address
the SCSI adapter, an initial ramdisk is used. The initial ramdisk is
loaded by the operating system loader (normally LILO) and is available
to the kernel as soon as the ramdisk is loaded. The ramdisk image
loads the proper SCSI adapter and allows the kernel to mount the root
filesystem. The geninitrd program creates such a ramdisk using
information found in the /etc/modules.conf file.

%description -l pl
Mkinitrd s�u�y do tworzenia obrazu systemu plikowego u�ywanego jako
inicjalny ramdysk (initrd), z kt�rego przy starcie systemu s� �adowane
modu�y kernela z obs�ug� urz�dze� kt�rych obs�uga nie jest
wkompilowana w kernel. Zazwyczaj modu�ami �adowanymi z inicjalnego
systemu plikowego s� sterowniki SCSI, IDE czy te� RAID po to �eby w
dalszej cz�ci inicjacji systemu by� mo�liwy dost�p do g��wnego
systemu plikowego (root fs).

Dzi�ki initrd jest mo�liwe u�ywanie dystrybucyjnego kernela w kt�rym
wkompilowana jest minimalna ilo�� obs�ugi r�nych urz�dze�, a reszta
kodu obs�ugi sterownik�w SCSI, IDE czy RAID jest doczytywana w trakcie
startu z initrd. Skrypt geninitrd generuje obraz ramdysku na podstawie
bie��cych informacji zawartych w /etc/modules.conf.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

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
%config(noreplace) /etc/sysconfig/geninitrd
%{_mandir}/man8/*
