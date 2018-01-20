# global pre_release rc1

Name:           clementine
Version:        master
Release:        1
Summary:        A music player and library organizer

Group:          Applications/Multimedia
License:        GPLv3+ and GPLv2+
URL:            https://github.com/clementine-player/Clementine
Source0:        https://github.com/clementine-player/Clementine/archive/master.tar.gz

BuildRequires:  boost-devel
BuildRequires:  cmake
BuildRequires:  cryptopp-devel
BuildRequires:  desktop-file-utils
BuildRequires:  fftw-devel
BuildRequires:  gettext
BuildConflicts: gmock-devel >= 1.6
%if 0%{?fedora} && 0%{?fedora} < 20
BuildRequires:  gmock-devel
%endif
BuildRequires:  gstreamer1-devel
BuildRequires:  gstreamer1-plugins-base-devel
BuildRequires:  gtest-devel
BuildRequires:  libcdio-devel
BuildRequires:  libchromaprint-devel
BuildRequires:  libechonest-devel
%ifnarch s390 s390x
BuildRequires:  libgpod-devel
BuildRequires:  libimobiledevice-devel
%endif
BuildRequires:  liblastfm-devel
BuildRequires:  libmtp-devel
BuildRequires:  libmygpo-qt-devel
BuildRequires:  libnotify-devel
BuildRequires:  libplist-devel
BuildRequires:  libprojectM-devel >= 2.0.1-7
BuildRequires:  libqxt-devel
BuildRequires:  libxml2-devel
BuildRequires:  protobuf-devel
BuildRequires:  pkgconfig(qca2)
BuildRequires:  qt4-devel
BuildRequires:  qjson-devel
BuildRequires:  qtiocompressor-devel
BuildRequires:  qtsinglecoreapplication-devel
BuildRequires:  qtsingleapplication-devel >= 2.6.1-2
BuildRequires:  sha2-devel
BuildRequires:  sparsehash-devel
BuildRequires:  sqlite-devel
BuildRequires:  taglib-devel >= 1.8
BuildRequires:  libudisks2-devel
# %%check
BuildRequires:  dbus-x11
BuildRequires:  xorg-x11-server-Xvfb
BuildRequires:  xorg-x11-xauth

Requires:       gstreamer1-plugins-good
Requires:       hicolor-icon-theme
Requires:       qca-ossl%{?_isa}

%description
Clementine is a multi-platform music player. It is inspired by Amarok 1.4,
focusing on a fast and easy-to-use interface for searching and playing your
music.

%prep
%setup -qn %{name}-%{version}

# Remove most 3rdparty libraries
mv 3rdparty/{gmock,qocoa,qsqlite,sha2,libmygpo-qt,vreen}/ .
rm -fr 3rdparty/*
mv {gmock,qocoa,qsqlite,sha2,libmygpo-qt,vreen}/ 3rdparty/

# Can't run all the unit tests
#   songloader requires internet connection
for test in songloader; do
    sed -i -e "/${test}_test/d" tests/CMakeLists.txt
done


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake} \
  -DBUILD_WERROR:BOOL=OFF \
  -DCMAKE_BUILD_TYPE:STRING=Release \
  -DUSE_SYSTEM_QTSINGLEAPPLICATION=1 \
  -DUSE_SYSTEM_PROJECTM=1 \
  -DUSE_SYSTEM_QXT=1 \
  ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install DESTDIR=%{buildroot} -C %{_target_platform}


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/clementine.desktop
pushd %{_target_platform}
# Run a fake X session since some tests check for X, tests still fail sometimes
xvfb-run -a dbus-launch --exit-with-session make test ||:
popd


%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
  touch --no-create %{_datadir}/icons/hicolor &>/dev/null
  gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
  update-desktop-database &> /dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
update-desktop-database &> /dev/null || :

%files
%doc Changelog COPYING
%{_bindir}/clementine
%{_bindir}/clementine-tagreader
%{_datadir}/appdata/clementine.appdata.xml
%{_datadir}/applications/clementine.desktop
%{_datadir}/icons/hicolor/*/apps/clementine.*
%{_datadir}/kde4/services/clementine-feed.protocol
%{_datadir}/kde4/services/clementine-itms.protocol
%{_datadir}/kde4/services/clementine-itpc.protocol
%{_datadir}/kde4/services/clementine-zune.protocol
