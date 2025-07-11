#
# Conditional build:
%bcond_without	doc	# API documentation
%bcond_without	tests	# unit tests

%define		module	aiosignal
Summary:	A list of registered asynchronous callbacks
Summary(pl.UTF-8):	Lista zarejestrowanych asynchronicznych wywołań zwrotnych
Name:		python3-%{module}
Version:	1.4.0
Release:	1
License:	Apache v2.0
Group:		Libraries/Python
Source0:	https://files.pythonhosted.org/packages/source/a/aiosignal/%{module}-%{version}.tar.gz
# Source0-md5:	9c692735b1422a94f16bd066ebf1fb7c
URL:		https://pypi.org/project/aiosignal/
BuildRequires:	python3-modules >= 1:3.9
BuildRequires:	python3-setuptools >= 1:51.0
%if %{with tests}
BuildRequires:	python3-coverage >= 7.6
BuildRequires:	python3-frozenlist >= 1.1.0
BuildRequires:	python3-pytest >= 8.3
BuildRequires:	python3-pytest-asyncio >= 1.0.0
BuildRequires:	python3-pytest-cov >= 6.2.1
%if "%{_ver_lt %{py3_ver} 3.13}" == "1"
BuildRequires:	python3-typing_extensions >= 4.2
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-aiohttp_theme
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.9
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A project to manage callbacks in asyncio projects.

Signal is a list of registered asynchronous callbacks.

%description -l pl.UTF-8
Projekt do zarządzania wywołaniami zwrotnymi w projektach asyncio.

Sygnał to lista zarejestrowanych asynchronicznych wywołań zwrotnych.

%package apidocs
Summary:	API documentation for Python %{module} module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona %{module}
Group:		Documentation

%description apidocs
API documentation for Python %{module} module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona %{module}.

%prep
%setup -q -n %{module}-%{version}

%build
%py3_build

%if %{with tests}
# pytest-cov loaded via -p option in pytest.ini
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=pytest_asyncio.plugin \
%{__python3} -m pytest tests
%endif

%if %{with doc}
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.rst CONTRIBUTORS.txt README.rst
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif
