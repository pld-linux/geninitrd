Summary:	Creates an initial ramdisk image for preloading modules
Summary(pl):	Narzêdzie do tworzenia inicjalnego ramdysku u¿ywanego przy starcie systemu
Name:		geninitrd
Version:	2.26
Release:	2
License:	GPL
Group:		Applications/System
Source0:	ftp://ftp.pld.org.pl/software/geninitrd/%{name}-%{version}.tar.gz
# Source0-md5: fed147fc76cfb22a6cf81b3a164e4b7c
Requires:	awk
Requires:	sh-utils
Requires:	fileutils
Requires:	mount
Requires:	bsp >= 0.3.0
Requires:	gzip
Requires:	tar
Requires:	genromfs
Prereq:		rc-scripts >= 0.2.7
Requires:	mktemp >= 1.5-8
Obsoletes:	mkinitrd
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
Mkinitrd s³u¿y do tworzenia obrazu systemu plikowego u¿ywanego jako
inicjalny ramdysk (initrd), z którego przy starcie systemu s± ³adowane
modu³y kernela z obs³ug± urz±dzeñ których obs³uga nie jest
wkompilowana w kernel. Zazwyczaj modu³ami ³adowanymi z inicjalnego
systemu plikowego s± sterowniki SCSI, IDE czy te¿ RAID po to ¿eby w
dalszej czê¶ci inicjacji systemu by³ mo¿liwy dostêp do g³ównego
systemu plikowego (root fs).

Dziêki initrd jest mo¿liwe u¿ywanie dystrybucyjnego kernela w którym
wkompilowana jest minimalna ilo¶æ obs³ugi ró¿nych urz±dzeñ, a reszta
kodu obs³ugi sterowników SCSI, IDE czy RAID jest doczytywana w trakcie
startu z initrd. Skrypt geninitrd generuje obraz ramdysku na podstawie
bie¿±cych informacji zawartych w /etc/modules.conf.

%prep
%setup -q

%build

%install
rm -rf $RPM_BUILD_ROOT

%{__make} BUILDROOT=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) /sbin/geninitrd
%config(noreplace) /etc/sysconfig/geninitrd
%{_mandir}/man8/*
