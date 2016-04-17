# はじめに

ここでは、仮想マシンによる plantumlsaas環境の立ち上げ方法について簡単に述べる。
そこで、実行環境は仮想マシン上のubuntu14.04とするようにする。ここでは、そのセットアップ方法についてまとめる。

# インストール

## Vagrant + Virtualboxのインストール

VirtualBoxとVagrantをインストールする。

* https://www.virtualbox.org/wiki/Downloads
* http://downloads.vagrantup.com/

それぞれのサイトから、インストーラを持ってきて、それぞれインストールする。

## Mac OSXにおけるHomebrew Caskを使ったインストール

インストーラを使いたくない人向けにOSXではHomebrew Caskというアプリケーションインストール用のパッケージ管理ソフトがある。virtualboxとvagrantのインストールは以下のコマンドを実行するだけ。

```
$ brew cask install virtualbox vagrant
```

## Vagrantのセットアップ

セットアップは基本的に以下の手順で行う。

* 必要なプラグインのインストール
* 仮想環境の登録
* ハンドル用のディレクトリの作成と初期化


### 必要なプラグインのインストール

スクリプトを扱う上でいくつかのプラグインのインストールが必要なので、インストールする。

```
$ vagrant plugin install dotenv vagrant-host-shell
```

### 仮想環境の登録

仮想環境は、外からダウンロードして登録する。以下のサイトにいろいろな仮想環境（Linuxディストリビューション）がころがっているので、必要な環境を登録しておく。

* http://www.vagrantbox.es/

ここでは、Ubuntu14.04をダウンロードして登録する。

```
$ vagrant box add ubuntu14.04 https://cloud-images.ubuntu.com/vagrant/trusty/current/trusty-server-cloudimg-amd64-vagrant-disk1.box
```

### ハンドル用のディレクトリの作成と初期化

ホームディレクトリにでも、vagrantというディレクトリを作って、初期化する。

```
$ cd plantumlsaas/vm
$ vagrant init ubuntu14.04
```

### .ssh-configの設定

以下を実行する

```
$ vagrant ssh-config --host ubuntu14.04 >> ~/.ssh/config
```


### 仮想マシンの立ち上げと自動セットアップ

次に、仮想マシンを立ち上げる。

```
$ vagrant up
```

上記を実行すると、仮想マシンが作成され、内部に登録されているansibleモジュールの設定に従って、内容が初期化される。

# 仮想マシンのセットアップ、アプリのインストール

以下のコマンドを実行することで、セットアップを再度やりなおすことができる。

```
$ vagrant provision
```

なお同じ作業をansible-playbookを直接叩くことでも実行できる。

```
$ pip install ansible
$ ansible-playbook -i hosts playbook.yml
```

このとき、hostsファイルは自分で作っておく必要がある。

```hosts
[all]
<仮想マシンへのIPアドレス／ホスト名>
```

# Tear-Down

開発が終わり（一段落し）、開発環境を削除したい場合は、以下のコマンドを実行する。

```
$ cd /path/to/plantumlsaas/vm
$ vagrant destroy
```

なお、一旦、破棄した仮想マシンは復帰することが原則できないので、注意すること。
