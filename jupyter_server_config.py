c = get_config()  #noqa

c.ServerApp.jpserver_extensions = {
    "fileglancer": True,
    "jupyterlab": False,
    "jupyterlab_server": False,
    "jupyter_lsp": False,
    "notebook_shim": False,
}

c.Fileglancer.central_url='http://127.0.0.1:8989'
