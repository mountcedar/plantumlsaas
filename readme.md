# はじめに

このプロジェクトは、PlantUMLをSaaS経由で利用するためのウェブサービスを開発するプロジェクトです。
基本的に、環境の運用は仮想マシン上で行い、このプロジェクトは仮想環境を立ち上げるソースコード、
スクリプト一式を提供します。

仮想マシンの使い方は、以下をごらんください。

* [仮想マシンのセットアップ](vm/readme.md)

## 起動したSaaSサービスの使い方

仮想マシンを起動すると、以下のAPIからPlantUMLの機能を呼び出すことができます。

```
http://<your host/your domain>/services/uml/get?<plantuml expression>
```

上記を用いることで、markdownなどからplantumlのサービスにアクセスすることができます。
```
![uml example](http://www.wandercode.jp/services/uml/get?
  hoge->geho: hello world
  )
```

![uml example](http://www.wandercode.jp/services/uml/get?
  hoge->geho: hello world
  )
