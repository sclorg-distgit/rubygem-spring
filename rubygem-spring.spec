%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

%global gem_name spring

Name: %{?scl_prefix}rubygem-%{gem_name}
Version: 1.4.0
Release: 4%{?dist}
Summary: Rails application preloader
Group: Development/Languages
License: MIT
URL: http://github.com/rails/spring
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# git clone https://github.com/rails/spring.git && cd spring
# git checkout v1.3.6 && tar czvf rubygem-spring-1.3.6-tests.tar.gz ./test
Source1: rubygem-spring-1.3.6-tests.tar.gz

Requires:      %{?scl_prefix_ruby}ruby(release)
Requires:      %{?scl_prefix_ruby}ruby(rubygems)
# Needed by `spring status`
Requires:      ps
BuildRequires: %{?scl_prefix_ruby}ruby(release)
BuildRequires: %{?scl_prefix_ruby}rubygems-devel
BuildRequires: %{?scl_prefix_ruby}rubygem(minitest)
BuildRequires: %{?scl_prefix_ruby}rubygem(bundler)
BuildRequires: %{?scl_prefix}rubygem(activesupport)
BuildArch:     noarch
Provides:      %{?scl_prefix}rubygem(%{gem_name}) = %{version}
# OkJson is allowed to be bundled:
# https://fedorahosted.org/fpc/ticket/113
Provides:      %{?scl_prefix}bundled(okjson) = 43

%description
Spring is a Rails application preloader. It speeds up development by keeping
your application running in the background so you don't need to boot it every
time you run a test, rake task or migration.

%package doc
Summary: Documentation for %{pkg_name}
Group: Documentation
Requires: %{?scl_prefix}%{pkg_name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{pkg_name}

%prep
%{?scl:scl enable %{scl} - << \EOF}
gem unpack %{SOURCE0}
%{?scl:EOF}

%setup -q -D -T -n  %{gem_name}-%{version}

%{?scl:scl enable %{scl} - << \EOF}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec
%{?scl:EOF}

%build
%{?scl:scl enable %{scl} - << \EOF}
gem build %{gem_name}.gemspec
%gem_install
%{?scl:EOF}

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{_bindir}
cp -pa .%{_bindir}/* \
        %{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

%check
pushd .%{gem_instdir}
tar xf %{SOURCE1}

# Run only unit test now, acceptance tests wants to compile gems extensions
%{?scl:scl enable %{scl} - << \EOF}
ruby -Ilib:test -rspring/watcher -e 'Dir.glob "./test/unit/**/*_test.rb", &method(:require)'
%{?scl:EOF}
popd

%files
%dir %{gem_instdir}
%{_bindir}/spring
%{gem_instdir}/bin
%{gem_libdir}
%exclude %{gem_cache}
%exclude %{gem_instdir}/test/apps/.gitignore
%{gem_spec}
%doc %{gem_instdir}/LICENSE.txt

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md

%changelog
* Thu Mar 03 2016 Pavel Valena <pvalena@redhat.com> - 1.4.0-4
- Fix ps Require

* Thu Mar 03 2016 Pavel Valena <pvalena@redhat.com> - 1.4.0-3
- Update to 1.4.0

* Tue Feb 03 2015 Vít Ondruch <vondruch@redhat.com>
- ps is located on different path in different package on RHEL6.

* Mon Feb 02 2015 Vít Ondruch <vondruch@redhat.com> - 1.1.3-3
- Fix ps binary path.

* Mon Feb 02 2015 Vít Ondruch <vondruch@redhat.com> - 1.1.3-2
- Fix requires.

* Wed Jul 09 2014 Josef Stribny <jstribny@redhat.com> - 1.1.3-1
- Update to 1.1.3

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Mar 20 2014 Josef Stribny <jstribny@redhat.com> - 1.1.2-4
- Use macro for the ps bin path

* Thu Mar 20 2014 Josef Stribny <jstribny@redhat.com> - 1.1.2-3
- Fix ps require

* Tue Mar 18 2014 Josef Stribny <jstribny@redhat.com> - 1.1.2-2
- Add bundled okjson virtual provide
- Add ps dependency
- Exclude .gitignore from tests

* Fri Mar 14 2014 Josef Stribny <jstribny@redhat.com> - 1.1.2-1
- Initial package
