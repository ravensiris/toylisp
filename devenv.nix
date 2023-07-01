{ pkgs, ... }:

{
  packages = [ 
	pkgs.nodePackages_latest.pyright
  ];

  languages.python = {
	enable = true;
	package = pkgs.python311Full;
	poetry.enable = true;
  };
}
