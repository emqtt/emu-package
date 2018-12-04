%define debug_package %{nil}
%define _user %{_name}
%define _group %{_name}
%define _conf_dir %{_sysconfdir}/%{_name}
%define _log_dir %{_var}/log/%{_name}
%define _lib_home /usr/lib/%{_name}
%define _var_home %{_sharedstatedir}/%{_name}
%define _dist %(bash -c "echo %{dist} | cut -d'.' -f2")
%define _build_name_fmt %{_arch}/%{_name}%{?_ostype}-v%{_version}-%{_release}.%{_dist}.%{_arch}.rpm

Name: %{_name}
Version: %{_version}
Release: %{_release}%{?dist}
Summary: emqx
Group: System Environment/Daemons
License: Apache License Version 2.0
URL: https://www.emqx.io
BuildRoot: %{_tmppath}/%{_name}-%{_version}-root
Provides: %{_name}

%description
EMQX, a distributed, massively scalable, highly extensible MQTT message broker written in Erlang/OTP.

%prep

%build

%install
mkdir -p %{buildroot}%{_lib_home}
mkdir -p %{buildroot}%{_log_dir}
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_conf_dir}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_var_home}
mkdir -p %{buildroot}%{_initddir}

cp -R %{_reldir}/lib %{buildroot}%{_lib_home}/
cp -R %{_reldir}/erts-* %{buildroot}%{_lib_home}/
cp -R %{_reldir}/releases %{buildroot}%{_lib_home}/
cp -R %{_reldir}/bin %{buildroot}%{_lib_home}/
cp -R %{_reldir}/etc/* %{buildroot}%{_conf_dir}/
cp -R %{_reldir}/data/* %{buildroot}%{_var_home}/
install -m755 %{_service_src} %{buildroot}%{_service_dst}

%pre
if [ $1 = 1 ]; then
  # Initial installation
  /usr/bin/getent group %{_group} >/dev/null || /usr/sbin/groupadd -r %{_group}
  if ! /usr/bin/getent passwd %{_user} >/dev/null ; then
      /usr/sbin/useradd -r -g %{_group} -m -d %{_sharedstatedir}/%{_name} -c "%{_name}" %{_user}
  fi
fi

%post
if [ $1 = 1 ]; then
    ln -s %{_lib_home}/bin/emqx %{_bindir}/emqx
    ln -s %{_lib_home}/bin/emqx_ctl %{_bindir}/emqx_ctl
fi
%{_post_addition}

%preun
%{_preun_addition}
# Only on uninstall, not upgrades
if [ $1 = 0 ]; then
    if [ -e %{_initddir}/%{_name} ] ; then
        /sbin/service %{_name} stop > /dev/null 2>&1
        /sbin/chkconfig --del %{_name}
    else
        systemctl disable %{_name}.service
    fi
    rm -f %{_bindir}/emqx
    rm -f %{_bindir}/emqx_ctl
fi
exit 0

%files
%defattr(-,root,root)
%{_service_dst}
%{_lib_home}
%attr(0700,%{_user},%{_group}) %dir %{_var_home}
%attr(0700,%{_user},%{_group}) %config(noreplace) %{_var_home}/*
%attr(0755,%{_user},%{_group}) %dir %{_log_dir}
%attr(0755,%{_user},%{_group}) %config(noreplace) %{_conf_dir}/*

%clean
rm -rf %{buildroot}

%changelog

