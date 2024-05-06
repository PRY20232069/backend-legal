# To learn more about how to use Nix to configure your environment
# see: https://developers.google.com/idx/guides/customize-idx-env
{ pkgs, ... }: {
  # Which nixpkgs channel to use.
  channel = "stable-23.11"; # or "unstable"

  # Use https://search.nixos.org/packages to find packages
  packages = [
    pkgs.python311
    pkgs.python311Packages.pip
    pkgs.python311Packages.mysqlclient
    pkgs.sudo
    pkgs.pkg-config
    pkgs.mysql80
    pkgs.libmysqlclient
    pkgs.gcc
  ];

  # Sets environment variables in the workspace
  env = { };
  idx = {
    # Search for the extensions you want on https://open-vsx.org/ and use "publisher.id"
    extensions = [
      # "vscodevim.vim"
    ];

    # Enable previews
    previews = {
      enable = true;
      previews = {
        # Previews the swagger page
        # web = {
        #   command = [
        #     "/home/user/backend-legal/myenv/bin/python"
        #     "-m"
        #     "uvicorn"
        #     "main:app"
        #     "--host"
        #     "$HOST"
        #     "--port"
        #     "$PORT"
        #   ];
        #   manager = "web";
        #   env = {
        #     HOST = "0.0.0.0";
        #     PORT = "8000";
        #   };
        # };
      };
    };

    # Workspace lifecycle hooks
    workspace = {
      # Runs when a workspace is first created
      onCreate = {
        # Example: install JS dependencies from NPM
        # npm-install = 'npm install';
      };
      onStart = {
        # Example: start a background task to watch and re-build backend code
        # watch-backend = "npm run watch-backend";
        "main" = "source myenv/bin/activate;pip install -r requirements.txt";
      };
    };
  };
}
