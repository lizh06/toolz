rem extension details at
rem
rem https://marketplace.visualstudio.com/items?itemName=fabiospampinato.vscode-todo-plus

for %%e in (

	ms-vscode.vs-keybindings/0.2.0
	vscode-icons-team.vscode-icons/11.8.0
	vscodevim.vim/1.21.10

	aaron-bond.better-comments/2.1.0
	shardulm94.trailing-spaces/0.3.1
	oderwat.indent-rainbow/7.5.0

	everettjf.filter-line/1.2.10
	ryu1kn.partial-diff/1.4.0

	christian-kohler.path-intellisense/2.4.0

	wayou.vscode-todo-highlight/1.0.4
	rem jgclark.vscode-todo-highlight/2.0.3
	ryanluker.vscode-coverage-gutters/2.6.0
	mechatroner.rainbow-csv/1.7.0
	IBM.output-colorizer/0.1.2

	rem debug
	hediet.debug-visualizer/2.0.6
	hediet.vscode-drawio/1.4.0

	rem markdown
	yzhang.markdown-all-in-one/3.4.0
	shd101wyy.markdown-preview-enhanced/0.5.22
	bierner.markdown-preview-github-styles/0.1.6
	yzane.markdown-pdf/1.4.4

	rem git
	ryu1kn.annotator/0.11.0
	mhutchie.git-graph/1.30.0
	eamodio.gitlens/11.6.1

	rem workspace
	EditorConfig.EditorConfig/0.16.4

	rem python
	ms-python.python/2022.0.1786462952
	ms-python.vscode-pylance/2022.2.1
	ms-python.gather/2021.6.0
	ms-toolsai.jupyter/2022.1.1001775990

	rem golang & rust
	golang.go/0.26.0
	rem ms-vscode.go/0.11.7
	rust-lang.rust/0.6.1

	rem syntax
	wholroyd.jinja/0.0.8
	samuelcolvin.jinjahtml/0.10.6
	rem better jinja
	zxh404.vscode-proto3/0.2.2
	bungcip.better-toml/0.3.2
	redhat.vscode-xml/0.18.1
	redhat.vscode-yaml/1.2.0

	rem browser
	ritwickdey.LiveServer/5.6.1
	auchenberg.vscode-browser-preview/0.5.9
	msjsdiag.debugger-for-edge/1.0.10

) do (
	powershell -noprofile -file %~dp0\vscodeInstall.ps1 \\ms\dist\vscodeext\PROJ\%%e
)
